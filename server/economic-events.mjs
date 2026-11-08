// Read-only economic evidence journal. Preserve the ENTIRE jsonParsed RPC transaction;
// extracted instruction rows are indexes into that source, never asserted economic control.
import { createHash } from 'node:crypto';

const TOKEN = new Set(['TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA', 'TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb']);
const SYSTEM = '11111111111111111111111111111111';
let initialized = new WeakSet();
export function initEvidence(db) {
  if (initialized.has(db)) return;
  db.exec(`CREATE TABLE IF NOT EXISTS econ_transactions (
    sig TEXT PRIMARY KEY, slot INTEGER, block_time INTEGER, status TEXT NOT NULL,
    rpc_json TEXT NOT NULL, sha256 TEXT NOT NULL, observed_at INTEGER NOT NULL,
    coverage TEXT NOT NULL DEFAULT 'RPC_JSONPARSED_NOT_COMPLETE_WALLET_HISTORY',
    capture_source TEXT NOT NULL DEFAULT 'UNKNOWN', commitment TEXT);
  CREATE TABLE IF NOT EXISTS econ_instructions (
    sig TEXT NOT NULL, outer_i INTEGER NOT NULL, inner_i INTEGER NOT NULL,
    kind TEXT NOT NULL, program TEXT, mint TEXT, from_account TEXT, to_account TEXT,
    from_owner TEXT, to_owner TEXT, amount_raw TEXT, owner_conflict INTEGER NOT NULL DEFAULT 0, raw_json TEXT NOT NULL,
    PRIMARY KEY (sig, outer_i, inner_i));
  CREATE INDEX IF NOT EXISTS econ_edges_from ON econ_instructions(from_owner, mint);
  CREATE INDEX IF NOT EXISTS econ_edges_to ON econ_instructions(to_owner, mint);`);
  for (const [table, column, ddl] of [
    ['econ_transactions','capture_source',"ALTER TABLE econ_transactions ADD COLUMN capture_source TEXT NOT NULL DEFAULT 'UNKNOWN'"],
    ['econ_transactions','commitment',"ALTER TABLE econ_transactions ADD COLUMN commitment TEXT"],
    ['econ_instructions','owner_conflict',"ALTER TABLE econ_instructions ADD COLUMN owner_conflict INTEGER NOT NULL DEFAULT 0"],
  ]) {
    if (!db.prepare('PRAGMA table_info(' + table + ')').all().some(r => r.name === column)) db.exec(ddl);
  }
  initialized.add(db);
}
// GET endpoints must never implicitly migrate or initialize the database.
function evidenceAvailable(db) {
  const rows = db.prepare("SELECT name FROM sqlite_master WHERE type='table' AND name IN ('econ_transactions','econ_instructions')").all();
  return rows.length === 2
    && db.prepare('PRAGMA table_info(econ_instructions)').all().some(r => r.name === 'owner_conflict');
}
const keyOf = k => typeof k === 'string' ? k : (k?.pubkey ?? null);
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
  const keys = (tx.transaction.message.accountKeys || []).map(keyOf);
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
    const kind = token && ['transfer', 'transferChecked'].includes(parsed?.type) ? 'TOKEN_TRANSFER'
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
    db.prepare(`INSERT INTO econ_transactions (sig, slot, block_time, status, rpc_json, sha256, observed_at, capture_source, commitment)
      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?) ON CONFLICT(sig) DO UPDATE SET
      slot=excluded.slot, block_time=excluded.block_time, status=excluded.status,
      rpc_json=excluded.rpc_json, sha256=excluded.sha256, observed_at=excluded.observed_at,
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
     i.from_account, i.to_account, i.amount_raw, t.block_time, t.slot
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
    x.sig funding_sig, x.outer_i, x.inner_i, x.amount_raw funding_lamports
    FROM wallet_trades a JOIN econ_instructions x ON x.from_owner=a.wallet AND x.kind='SOL_TRANSFER'
    JOIN econ_transactions t ON t.sig=x.sig AND t.status='RPC_OBSERVED'
    JOIN wallet_trades b ON b.wallet=x.to_owner AND b.side='buy' AND b.mint!=a.mint
    WHERE a.wallet=? AND a.side='sell' AND a.t<=t.block_time*1000
      AND b.t>=t.block_time*1000 AND b.t-a.t<=? AND x.to_owner IS NOT NULL
      AND x.to_owner!=a.wallet ORDER BY b.t DESC LIMIT ?`)
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
export function recipientOutcomes(db, sender, mint = null, limit = 20, maxHours = 24) {
  const direct = recipientCandidates(db, sender, mint, Math.min(30, Math.max(1, limit)));
  if (!evidenceAvailable(db)) return { ...direct, observation: 'LOCAL_INDEX_UNAVAILABLE', rows: [] };
  const windowMs = Math.max(1, Math.min(168, Number(maxHours) || 24)) * 3600_000;
  const sells = db.prepare(`SELECT sig, wallet, mint, side, sol, t FROM wallet_trades
    WHERE wallet=? AND mint=? AND side='sell' AND t>=? AND t<=?
    ORDER BY t ASC LIMIT 5`);
  const rows = direct.rows.map(r => {
    const transferAt = Number.isFinite(r.block_time) ? r.block_time * 1000 : null;
    if (transferAt === null || !r.mint) return { ...r, followupStatus: 'TRANSFER_TIME_OR_MINT_UNKNOWN',
      observedSells: [], crossMintCandidates: [] };
    const observedSells = sells.all(r.to_owner, r.mint, transferAt, transferAt + windowMs);
    const cross = crossMintCandidates(db, r.to_owner, Math.ceil(windowMs / 3600_000), 25).rows
      .filter(x => x.sold_mint === r.mint && x.sold_at >= transferAt && x.sold_at <= transferAt + windowMs);
    return { ...r, followupStatus: 'LOCAL_OBSERVATIONS_ONLY', observedSells, crossMintCandidates: cross };
  });
  return { ...direct, windowMs, observation: 'READ_ONLY_CAPTURED_EVIDENCE_AND_WALLET_TRADE_SUMMARIES',
    interpretation: 'Follow-up sells and cross-Mint paths are candidates, NOT transferred-inventory provenance or common control',
    rows };
}
