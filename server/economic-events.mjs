// Read-only economic evidence journal. Preserve the ENTIRE jsonParsed RPC transaction;
// extracted instruction rows are indexes into that source, never asserted economic control.
import { createHash } from 'node:crypto';

const TOKEN = new Set(['TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA', 'TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb']);
const SYSTEM = '11111111111111111111111111111111';
let initialized = new WeakSet();
export function initEvidence(db) {
  if (initialized.has(db)) return;
  db.exec(`CREATE TABLE IF NOT EXISTS econ_transactions (
    sig TEXT PRIMARY KEY, slot INTEGER, block_time INTEGER, block_tx_index INTEGER,
    status TEXT NOT NULL DEFAULT 'RPC_OBSERVED',
    rpc_json TEXT NOT NULL, sha256 TEXT NOT NULL, observed_at INTEGER NOT NULL,
    coverage TEXT NOT NULL DEFAULT 'RPC_JSONPARSED_NOT_COMPLETE_WALLET_HISTORY',
    capture_source TEXT NOT NULL DEFAULT 'UNKNOWN', commitment TEXT);
  CREATE TABLE IF NOT EXISTS econ_instructions (
    sig TEXT NOT NULL, outer_i INTEGER NOT NULL, inner_i INTEGER NOT NULL,
    kind TEXT NOT NULL, program TEXT, mint TEXT, from_account TEXT, to_account TEXT,
    from_owner TEXT, to_owner TEXT, amount_raw TEXT, owner_conflict INTEGER NOT NULL DEFAULT 0, raw_json TEXT NOT NULL,
    PRIMARY KEY (sig, outer_i, inner_i));
  CREATE INDEX IF NOT EXISTS econ_edges_from ON econ_instructions(from_owner, mint);
  CREATE INDEX IF NOT EXISTS econ_edges_to ON econ_instructions(to_owner, mint);
  CREATE TABLE IF NOT EXISTS econ_wallet_processing (
    sig TEXT NOT NULL, wallet TEXT NOT NULL, state TEXT NOT NULL,
    attempts INTEGER NOT NULL DEFAULT 0, updated_at INTEGER NOT NULL,
    last_error TEXT,
    PRIMARY KEY (sig, wallet)
  );`);
  for (const [table, column, ddl] of [
    ['econ_transactions','capture_source',"ALTER TABLE econ_transactions ADD COLUMN capture_source TEXT NOT NULL DEFAULT 'UNKNOWN'"],
    ['econ_transactions','commitment',"ALTER TABLE econ_transactions ADD COLUMN commitment TEXT"],
    ['econ_transactions','block_tx_index',"ALTER TABLE econ_transactions ADD COLUMN block_tx_index INTEGER"],
    ['econ_transactions','status',"ALTER TABLE econ_transactions ADD COLUMN status TEXT NOT NULL DEFAULT 'RPC_OBSERVED'"],
    ['econ_instructions','owner_conflict',"ALTER TABLE econ_instructions ADD COLUMN owner_conflict INTEGER NOT NULL DEFAULT 0"],
  ]) {
    if (!db.prepare('PRAGMA table_info(' + table + ')').all().some(r => r.name === column)) db.exec(ddl);
  }
  initialized.add(db);
}
// Transaction capture, wallet reader completion, and history coverage are distinct facts.
// A wallet is complete here only when this wallet reader has run its tx hooks and
// written its legacy swap summaries; this is NOT full protocol/CPI decoding.
export function walletProcessing(db, sig, wallet) {
  initEvidence(db);
  return db.prepare('SELECT state, attempts, updated_at, last_error FROM econ_wallet_processing WHERE sig=? AND wallet=?').get(sig, wallet) || null;
}
export function setWalletProcessing(db, sig, wallet, state, error = null) {
  if (!['CAPTURED', 'COMPLETE', 'RETRY_REQUIRED'].includes(state)) throw new Error('invalid wallet processing state');
  if (!sig || !wallet) throw new Error('signature and wallet required');
  initEvidence(db);
  const t = Date.now(), message = error ? String(error.message ?? error).slice(0, 400) : null;
  if (state === 'CAPTURED') {
    db.prepare(`INSERT INTO econ_wallet_processing(sig,wallet,state,attempts,updated_at,last_error)
      VALUES (?,?,'CAPTURED',1,?,NULL)
      ON CONFLICT(sig,wallet) DO UPDATE SET state='CAPTURED',
      attempts=attempts+1, updated_at=excluded.updated_at, last_error=NULL`).run(sig,wallet,t);
  } else {
    const changed = db.prepare('UPDATE econ_wallet_processing SET state=?, updated_at=?, last_error=? WHERE sig=? AND wallet=?')
      .run(state,t,message,sig,wallet);
    if (!changed.changes) throw new Error('wallet processing capture state absent');
  }
  return walletProcessing(db,sig,wallet);
}
// GET endpoints must never implicitly migrate or initialize the database.
function evidenceAvailable(db) {
  const rows = db.prepare("SELECT name FROM sqlite_master WHERE type='table' AND name IN ('econ_transactions','econ_instructions')").all();
  return rows.length === 2
    && db.prepare('PRAGMA table_info(econ_instructions)').all().some(r => r.name === 'owner_conflict');
}
const keyOf = k => typeof k === 'string' ? k : (k?.pubkey ?? null);
// jsonParsed message.accountKeys contains static transaction keys; versioned transactions can
// add lookup-table addresses in meta.loadedAddresses. Token-balance accountIndex and compiled
// instruction programIdIndex resolve against the combined list in writable-then-readonly order.
function fullAccountKeys(tx) {
  const accountKeys = tx.transaction?.message?.accountKeys || [];
  // jsonParsed getTransaction responses already materialize lookup-table accounts in
  // message.accountKeys and label them source=lookupTable. Do not append meta.loadedAddresses
  // to that representation or accountIndex resolution would shift/duplicate addresses.
  if (accountKeys.some(k => k && typeof k === 'object' && k.source === 'lookupTable')) {
    return accountKeys.map(keyOf);
  }
  // Raw/full JSON responses keep static message.accountKeys and expose loadedAddresses
  // separately. Support that representation too, without claiming fields that are absent.
  const staticKeys = accountKeys.map(keyOf);
  const writable = (tx.meta?.loadedAddresses?.writable || []).map(keyOf);
  const readonly = (tx.meta?.loadedAddresses?.readonly || []).map(keyOf);
  return [...staticKeys, ...writable, ...readonly];
}
function tokenOwners(tx, keys) {
  const out = new Map();
  for (const b of [...(tx.meta?.preTokenBalances || []), ...(tx.meta?.postTokenBalances || [])]) {
    const account = keys[b.accountIndex];
    if (!account) continue;
    const owner = b.owner ?? null, mint = b.mint ?? null, old = out.get(account);
    if (!old) { out.set(account, { owner, mint, conflict: false }); continue; }
    if (old.conflict) continue;
    const conflict = Boolean((old.owner && owner && old.owner !== owner) || (old.mint && mint && old.mint !== mint));
    out.set(account, conflict ? { owner: null, mint: null, conflict: true }
      : { owner: old.owner ?? owner, mint: old.mint ?? mint, conflict: false });
  }
  return out;
}

export function decodeEvidence(tx) {
  if (!tx?.transaction?.message || !tx.meta) throw new Error('Missing transaction/message/meta; cannot claim complete RPC capture');
  const keys = fullAccountKeys(tx);
  const owners = tokenOwners(tx, keys);
  const outer = tx.transaction.message.instructions || [];
  const inner = new Map();
  for (const set of tx.meta.innerInstructions || []) inner.set(set.index, set.instructions || []);
  const rows = [];
  const visit = (ix, oi, ii) => {
    const program = ix.programId ?? (Number.isInteger(ix.programIdIndex) ? keys[ix.programIdIndex] : null);
    const parsed = ix.parsed && typeof ix.parsed === 'object' ? ix.parsed : null;
    const info = parsed?.info || {};
    const token = TOKEN.has(program) || ix.program === 'spl-token' || ix.program === 'spl-token-2022';
    const system = program === SYSTEM || ix.program === 'system';
    const kind = token && ['transfer', 'transferChecked', 'transferCheckedWithFee'].includes(parsed?.type) ? 'TOKEN_TRANSFER'
      : system && parsed?.type === 'transfer' ? 'SOL_TRANSFER' : 'OTHER';
    const from = kind === 'OTHER' ? null : (info.source ?? null);
    const to = kind === 'OTHER' ? null : (info.destination ?? null);
    const src = kind === 'TOKEN_TRANSFER' ? owners.get(from) : null;
    const dst = kind === 'TOKEN_TRANSFER' ? owners.get(to) : null;
    const mintConflict = kind === 'TOKEN_TRANSFER' && Boolean(
      (info.mint && src?.mint && info.mint !== src.mint) ||
      (info.mint && dst?.mint && info.mint !== dst.mint) ||
      (src?.mint && dst?.mint && src.mint !== dst.mint));
    const ownerConflict = Boolean(src?.conflict || dst?.conflict || mintConflict);
    rows.push({ outer_i: oi, inner_i: ii, program, kind,
      mint: kind === 'TOKEN_TRANSFER' ? (mintConflict ? null : info.mint ?? src?.mint ?? dst?.mint ?? null) : null,
      from_account: from, to_account: to,
      from_owner: kind === 'SOL_TRANSFER' ? from : ownerConflict ? null : src?.owner ?? null,
      to_owner: kind === 'SOL_TRANSFER' ? to : ownerConflict ? null : dst?.owner ?? null,
      amount_raw: kind === 'SOL_TRANSFER' ? String(info.lamports ?? '')
        : kind === 'TOKEN_TRANSFER' ? String(info.tokenAmount?.amount ?? info.amount ?? '') : null,
      raw_json: JSON.stringify(ix), owner_conflict: ownerConflict });
  };
  for (let i = 0; i < outer.length; i++) {
    visit(outer[i], i, -1);
    (inner.get(i) || []).forEach((ix, j) => visit(ix, i, j));
  }
  // Keep orphaned innerInstructions as well; malformed RPC data must not be silently discarded.
  for (const [i, batch] of inner) if (i < 0 || i >= outer.length) batch.forEach((ix, j) => visit(ix, i, j));
  return rows;
}
export function persistEvidence(db, sig, tx, observedAt = Date.now(), provenance = {}) {
  if (typeof sig !== 'string' || !sig) throw new Error('signature required');
  if (tx?.transaction?.signatures?.[0] !== sig) throw new Error('RPC signature mismatch or missing');
  const captureSource = ['WALLET_RPC','OFFLINE_ARCHIVE'].includes(provenance.captureSource) ? provenance.captureSource : 'UNKNOWN';
  const commitment = ['processed','confirmed','finalized'].includes(provenance.commitment) ? provenance.commitment : null;
  initEvidence(db);
  const raw = JSON.stringify(tx), hash = createHash('sha256').update(raw).digest('hex');
  const existing = db.prepare('SELECT sha256 FROM econ_transactions WHERE sig = ?').get(sig);
  if (existing?.sha256 === hash) return { sig, duplicate: true, hash };
  const decoded = decodeEvidence(tx);
  const own = !db.isTransaction;
  if (own) db.exec('BEGIN');
  try {
    db.prepare(`INSERT INTO econ_transactions (sig, slot, block_time, block_tx_index, status, rpc_json, sha256, observed_at, capture_source, commitment)
      VALUES (?, ?, ?, NULL, ?, ?, ?, ?, ?, ?) ON CONFLICT(sig) DO UPDATE SET
      slot=excluded.slot, block_time=excluded.block_time,
      block_tx_index=CASE WHEN econ_transactions.slot IS NOT excluded.slot THEN NULL ELSE econ_transactions.block_tx_index END,
      status=excluded.status, rpc_json=excluded.rpc_json, sha256=excluded.sha256, observed_at=excluded.observed_at,
      capture_source=excluded.capture_source, commitment=excluded.commitment`)
      .run(sig, tx.slot ?? null, tx.blockTime ?? null, tx.meta.err ? 'FAILED' : 'RPC_OBSERVED', raw, hash, observedAt, captureSource, commitment);
    db.prepare('DELETE FROM econ_instructions WHERE sig = ?').run(sig);
    const ins = db.prepare(`INSERT INTO econ_instructions
      (sig,outer_i,inner_i,kind,program,mint,from_account,to_account,from_owner,to_owner,amount_raw,owner_conflict,raw_json)
      VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)`);
    for (const r of decoded) ins.run(sig,r.outer_i,r.inner_i,r.kind,r.program,r.mint,r.from_account,r.to_account,r.from_owner,r.to_owner,r.amount_raw,r.owner_conflict ? 1 : 0,r.raw_json);
    if (own) db.exec('COMMIT');
  } catch (e) { if (own && db.isTransaction) db.exec('ROLLBACK'); throw e; }
  return { sig, duplicate: false, hash, instructions: decoded.length };
}
export function recordBlockTransactionOrder(db, block, slot = null) {
  initEvidence(db);
  const txs = Array.isArray(block?.transactions) ? block.transactions : [];
  const blockSlot = Number.isInteger(slot) ? slot : (Number.isInteger(block?.slot) ? block.slot : null);
  if (blockSlot === null || !Number.isInteger(blockSlot) || blockSlot < 0) throw new Error('block slot required');
  const seen = new Set(), rows = [];
  for (let index = 0; index < txs.length; index++) {
    const sig = txs[index]?.transaction?.signatures?.[0];
    if (typeof sig !== 'string' || !sig) continue;
    if (seen.has(sig)) throw new Error('duplicate transaction signature in block');
    seen.add(sig);
    rows.push({ sig, index });
  }
  const update = db.prepare('UPDATE econ_transactions SET block_tx_index=? WHERE sig=? AND slot=?');
  const own = !db.isTransaction;
  if (own) db.exec('BEGIN');
  try {
    let matched = 0;
    for (const row of rows) matched += Number(update.run(row.index, row.sig, blockSlot).changes || 0);
    if (own) db.exec('COMMIT');
    return { slot: blockSlot, transactionCount: txs.length, indexedTransactions: rows.length, matched };
  } catch (e) {
    if (own && db.isTransaction) db.exec('ROLLBACK');
    throw e;
  }
}

export function transactionEvidence(db, sig) {
  if (!evidenceAvailable(db)) return null;
  const tx = db.prepare('SELECT * FROM econ_transactions WHERE sig = ?').get(sig);
  if (!tx) return null;
  const instructions = db.prepare('SELECT * FROM econ_instructions WHERE sig = ? ORDER BY outer_i, inner_i').all(sig);
  return { ...tx, rpc: JSON.parse(tx.rpc_json), instructions };
}
export function recipientCandidates(db, sender, mint = null, limit = 100) {
  if (!evidenceAvailable(db)) return { sender, mint, coverage: 'EVIDENCE_NOT_INITIALIZED',
    interpretation: 'Local evidence index unavailable, not a claim of no transfers', rows: [] };
  const rows = db.prepare(`SELECT i.sig, i.outer_i, i.inner_i, i.from_owner, i.to_owner, i.mint,
     i.from_account, i.to_account, i.amount_raw, t.block_time, t.slot,
     t.sha256 AS archive_sha256, t.capture_source AS capture_source,
     t.block_tx_index AS block_tx_index,
     t.observed_at AS capture_observed_at_ms, t.commitment AS commitment
     FROM econ_instructions i JOIN econ_transactions t ON t.sig=i.sig
     WHERE t.status='RPC_OBSERVED' AND i.kind='TOKEN_TRANSFER' AND i.owner_conflict=0 AND i.from_owner=?
       AND i.to_owner IS NOT NULL AND i.to_owner!=i.from_owner
       AND (? IS NULL OR i.mint=?) ORDER BY t.block_time DESC, t.slot DESC LIMIT ?`)
    .all(sender, mint, mint, Math.max(1, Math.min(500, limit)));
  return { sender, mint, coverage: 'ONLY_CAPTURED_RPC_TX_AND_RESOLVED_TOKEN_ACCOUNT_OWNERS',
    interpretation: 'OBSERVED_INSTRUCTION_TRANSFER; receiving wallet is a candidate, not controlled identity or a proven later sale', rows };
}
export function crossMintCandidates(db, address, maxHours = 24, limit = 40) {
  if (!evidenceAvailable(db)) return { address, coverage: 'EVIDENCE_NOT_INITIALIZED',
    interpretation: 'Local evidence index unavailable, not a claim of no funding', rows: [] };
  // Use the existing wallet ledger as a hypothesis source. It is not an execution-level asset ledger.
  const window = Math.max(1, Math.min(168, maxHours)) * 3600_000;
  const rows = db.prepare(`SELECT a.wallet seller, a.mint sold_mint, a.sig sell_sig, a.t sold_at, a.sol sell_sol,
    b.wallet buyer, b.mint bought_mint, b.sig buy_sig, b.t bought_at,
    x.sig funding_sig, x.outer_i, x.inner_i, x.amount_raw funding_lamports,
    ta.slot sell_slot, t.slot funding_slot, tb.slot buy_slot
    FROM wallet_trades a
    JOIN econ_transactions ta ON ta.sig=a.sig AND ta.status='RPC_OBSERVED'
    JOIN econ_instructions x ON x.from_owner=a.wallet AND x.kind='SOL_TRANSFER'
    JOIN econ_transactions t ON t.sig=x.sig AND t.status='RPC_OBSERVED'
    JOIN wallet_trades b ON b.wallet=x.to_owner AND b.side='buy' AND b.mint!=a.mint
    JOIN econ_transactions tb ON tb.sig=b.sig AND tb.status='RPC_OBSERVED'
    WHERE a.wallet=? AND a.side='sell'
      AND ta.slot<t.slot AND t.slot<tb.slot
      AND a.t<=t.block_time*1000
      AND b.t>=t.block_time*1000 AND b.t-a.t<=? AND x.to_owner IS NOT NULL
      AND x.to_owner!=a.wallet ORDER BY tb.slot DESC LIMIT ?`)
    .all(address,window,Math.max(1,Math.min(100,limit)));
  return { address, windowMs: window, coverage: 'WALLET_TRADES_AND_CAPTURED_SYSTEM_TRANSFERS_ONLY',
    interpretation: 'TEMPORAL_FUNDING_PATH_CANDIDATE_NOT_LAMPORT_PROVENANCE_OR_COMMON_CONTROL', rows };
}
// Report pre-upgrade or dropped-feed signatures that have wallet trades but no full RPC capture.
// This is a gap index, not an RPC call or proof that history can be retrieved.
export function missingEvidence(db, wallet, limit = 100) {
  if (!evidenceAvailable(db)) {
    // No evidence tables yet: every locally summarized signature is a known evidence gap.
    // Query the existing wallet table without creating or modifying SQLite objects.
    const rows = db.prepare(`SELECT sig, MIN(t) first_trade_at, COUNT(*) summary_rows
      FROM wallet_trades WHERE wallet=? AND sig NOT LIKE 'slot:%'
      GROUP BY sig ORDER BY first_trade_at DESC LIMIT ?`)
      .all(wallet, Math.max(1, Math.min(500, limit)));
    return { wallet, coverage: 'EVIDENCE_NOT_INITIALIZED_ALL_KNOWN_WALLET_TRADES_UNCAPTURED',
      next: 'Capture or replay archived RPC; this is not a complete wallet history', rows };
  }
  const rows = db.prepare(`SELECT w.sig, MIN(w.t) first_trade_at, COUNT(*) summary_rows
    FROM wallet_trades w LEFT JOIN econ_transactions e ON e.sig=w.sig
    WHERE w.wallet=? AND e.sig IS NULL AND w.sig NOT LIKE 'slot:%'
    GROUP BY w.sig ORDER BY first_trade_at DESC LIMIT ?`)
    .all(wallet, Math.max(1, Math.min(500, limit)));
  return { wallet, rows, coverage: 'KNOWN_WALLET_TRADES_MISSING_RPC_CAPTURE_ONLY',
    next: 'Fetch each listed transaction independently or replay archived jsonParsed RPC; empty rows do not prove complete wallet history' };
}

/** Bounded local-only investigation of recipients; no RPC, enrollment, signing or AI. */
function ownerTokenBalanceDeltaRaw(tx, owner, mint) {
  if (!tx?.meta || typeof owner !== 'string' || typeof mint !== 'string') return null;
  const keys = fullAccountKeys(tx);
  const pre = new Map(), post = new Map();
  for (const row of tx.meta.preTokenBalances || []) {
    if (row?.mint !== mint || row?.owner !== owner) continue;
    const account = keys[row.accountIndex], amount = row.uiTokenAmount?.amount;
    if (!account || !/^\d+$/.test(String(amount ?? ''))) continue;
    pre.set(account, (pre.get(account) || 0n) + BigInt(amount));
  }
  for (const row of tx.meta.postTokenBalances || []) {
    if (row?.mint !== mint || row?.owner !== owner) continue;
    const account = keys[row.accountIndex], amount = row.uiTokenAmount?.amount;
    if (!account || !/^\d+$/.test(String(amount ?? ''))) continue;
    post.set(account, (post.get(account) || 0n) + BigInt(amount));
  }
  if (!pre.size && !post.size) return null;
  const accounts = new Set([...pre.keys(), ...post.keys()]);
  let delta = 0n;
  for (const account of accounts) delta += (post.get(account) || 0n) - (pre.get(account) || 0n);
  return delta.toString();
}

export function recipientOutcomes(db, sender, mint = null, limit = 20, maxHours = 24) {
  const direct = recipientCandidates(db, sender, mint, Math.min(30, Math.max(1, limit)));
  if (!evidenceAvailable(db)) return { ...direct, observation: 'LOCAL_INDEX_UNAVAILABLE', rows: [] };
  const windowMs = Math.max(1, Math.min(168, Number(maxHours) || 24)) * 3600_000;
  // blockTime is only second-resolution and cannot establish transaction order. Use the
  // captured transaction slot as the minimum ordering fact; same-slot follow-ups remain UNKNOWN
  // because getTransaction does not expose a block transaction index.
  const sells = db.prepare(`SELECT w.sig, w.wallet, w.mint, w.side, w.sol, w.t,
      e.slot AS sell_slot, e.block_time AS sell_block_time, e.block_tx_index AS sell_block_tx_index
    FROM wallet_trades w JOIN econ_transactions e ON e.sig=w.sig
    WHERE w.wallet=? AND w.mint=? AND w.side='sell' AND e.status='RPC_OBSERVED'
      AND e.block_time IS NOT NULL AND e.block_time>=? AND e.block_time<=?
      AND (e.slot>? OR (e.slot=? AND e.block_tx_index IS NOT NULL)) AND w.sig!=?
    ORDER BY e.slot ASC, e.block_tx_index ASC LIMIT 6`);
  const rows = direct.rows.map(r => {
    const transferAt = Number.isFinite(r.block_time) ? r.block_time * 1000 : null;
    if (transferAt === null || !r.mint) return { ...r, followupStatus: 'TRANSFER_TIME_OR_MINT_UNKNOWN',
      sellObservation: 'TRANSFER_TIME_OR_MINT_UNKNOWN', observedSells: [], crossMintCandidates: [] };
    // econ_transactions.block_time is in seconds; wallet ledger/output windows are milliseconds.
    const sellRows = sells.all(r.to_owner, r.mint, r.block_time, r.block_time + windowMs / 1000, r.slot, r.slot, r.sig).filter(sell =>
      sell.sell_slot > r.slot || (sell.sell_slot === r.slot && r.block_tx_index !== null && sell.sell_block_tx_index !== null && sell.sell_block_tx_index > r.block_tx_index));
    const observedSellsTruncated = sellRows.length > 5;
    const observedSells = sellRows.slice(0, 5).map(sell => {
      const evidence = transactionEvidence(db, sell.sig);
      const sellDeltaRaw = evidence ? ownerTokenBalanceDeltaRaw(evidence.rpc, r.to_owner, r.mint) : null;
      const transferAmountRaw = /^\d+$/.test(String(r.amount_raw ?? '')) ? String(r.amount_raw) : null;
      // Token-2022 TransferCheckedWithFee amount is gross; the fee is withheld
      // separately on the destination token account. Preserve that distinction.
      const transferInstruction = db.prepare('SELECT raw_json, program, kind FROM econ_instructions WHERE sig=? AND outer_i=? AND inner_i=? LIMIT 1').get(r.sig, r.outer_i, r.inner_i);
      let transferFeeRaw = null;
      let transferNetAmountRaw = transferAmountRaw;
      try {
        const parsedTransfer = transferInstruction?.raw_json ? JSON.parse(transferInstruction.raw_json) : null;
        const info = parsedTransfer?.parsed?.info;
        const fee = info?.feeAmount ?? info?.fee ?? null;
        if (parsedTransfer?.parsed?.type === 'transferCheckedWithFee' && /^\d+$/.test(String(fee ?? ''))) {
          transferFeeRaw = String(fee);
          const gross = BigInt(transferAmountRaw ?? '0');
          const feeBig = BigInt(transferFeeRaw);
          transferNetAmountRaw = feeBig <= gross ? (gross - feeBig).toString() : null;
        }
      } catch {}
      const sameMintDirections = evidence
        ? evidence.instructions.filter(ix => ix.kind === 'TOKEN_TRANSFER' && ix.mint === r.mint
          && ix.owner_conflict === 0
          && (ix.from_owner === r.to_owner || ix.to_owner === r.to_owner))
        : [];
      const hasMixedSameMintFlow = sameMintDirections.some(ix => ix.from_owner === r.to_owner)
        && sameMintDirections.some(ix => ix.to_owner === r.to_owner);
      let inventoryLink = 'PROVENANCE_UNKNOWN';
      if (hasMixedSameMintFlow) {
        // Net owner balance can hide simultaneous inbound/outbound inventory in one transaction.
        // Do not call a net-compatible delta provenance evidence.
        inventoryLink = 'INTRA_TRANSACTION_NET_DELTA_AMBIGUOUS';
      } else if (sellDeltaRaw !== null && transferAmountRaw !== null && BigInt(sellDeltaRaw) < 0n) {
        const soldRaw = -BigInt(sellDeltaRaw);
        const receivedRaw = BigInt(transferNetAmountRaw ?? transferAmountRaw);
        if (transferFeeRaw !== null) {
          inventoryLink = soldRaw > receivedRaw
            ? 'CANNOT_BE_FULLY_SOURCED_FROM_THIS_SINGLE_TRANSFER'
            : 'TOKEN_2022_TRANSFER_FEE_PRESENT_PROVENANCE_UNPROVEN';
        } else {
          inventoryLink = soldRaw > receivedRaw
            ? 'CANNOT_BE_FULLY_SOURCED_FROM_THIS_SINGLE_TRANSFER'
            : 'AMOUNT_COMPATIBLE_BUT_PROVENANCE_UNPROVEN';
        }
      }
      const priorInbound = db.prepare(`SELECT 1 FROM econ_instructions
        WHERE kind='TOKEN_TRANSFER' AND owner_conflict=0 AND to_owner=? AND mint=?
          AND sig IN (SELECT sig FROM econ_transactions WHERE status='RPC_OBSERVED' AND block_time IS NOT NULL AND block_time < ?)
        LIMIT 1`).get(r.to_owner, r.mint, Math.floor(transferAt / 1000));
      if (priorInbound && inventoryLink !== 'CANNOT_BE_FULLY_SOURCED_FROM_THIS_SINGLE_TRANSFER')
        inventoryLink = 'PRIOR_CAPTURED_INBOUND_ACTIVITY_EXISTS';
      return { ...sell, sellDeltaRaw, transferFeeRaw, transferNetAmountRaw, inventoryLink };
    });
    const cross = crossMintCandidates(db, r.to_owner, Math.ceil(windowMs / 3600_000), 25).rows
      .filter(x => x.sold_mint === r.mint && x.sold_at >= transferAt && x.sold_at <= transferAt + windowMs);
    return { ...r, followupStatus: 'LOCAL_OBSERVATIONS_ONLY',
      sellObservation: observedSells.length ? 'LOCAL_SELL_SUMMARY_OBSERVED' : 'NOT_OBSERVED_IN_CAPTURED_WINDOW',
      observedSellsTruncated,
      inventoryProvenance: observedSells.map(x => x.inventoryLink),
      observedSells, crossMintCandidates: cross };
  });
  return { ...direct, windowMs, observation: 'READ_ONLY_CAPTURED_EVIDENCE_AND_WALLET_TRADE_SUMMARIES',
    interpretation: 'Follow-up sells and cross-Mint paths are candidates, NOT transferred-inventory provenance or common control',
    rows };
}

// Known local RPC captures that failed wallet-reader consumption can be retried
// with NO new RPC call. Bounded to prevent permanent parser failures looping.
export function retryableWalletProcessing(db, { beforeMs = Date.now() - 60_000, limit = 10, maxAttempts = 5 } = {}) {
  initEvidence(db);
  return db.prepare(`SELECT p.sig, p.wallet, p.attempts, t.block_time
    FROM econ_wallet_processing p
    JOIN econ_transactions t ON t.sig=p.sig
    JOIN wallets w ON w.address=p.wallet AND w.watching=1
    WHERE p.state='RETRY_REQUIRED' AND p.attempts < ? AND p.updated_at <= ?
    ORDER BY p.updated_at ASC LIMIT ?`)
    .all(Math.max(1, Math.min(20, maxAttempts)),
      beforeMs, Math.max(1, Math.min(100, limit)));
}
