// Read-only economic evidence journal. Preserve the ENTIRE jsonParsed RPC transaction;
// extracted instruction rows are indexes into that source, never asserted economic control.
import { createHash } from 'node:crypto';

const TOKEN = new Set(['TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA', 'TokenzQdBNbLqP5VYzRBRT44hA3hGMSiYqt6vHu4x5Xm']);
const SYSTEM = '11111111111111111111111111111111';
let initialized = new WeakSet();
export function initEvidence(db) {
  if (initialized.has(db)) return;
  db.exec(`CREATE TABLE IF NOT EXISTS econ_transactions (
    sig TEXT PRIMARY KEY, slot INTEGER, block_time INTEGER, status TEXT NOT NULL,
    rpc_json TEXT NOT NULL, sha256 TEXT NOT NULL, observed_at INTEGER NOT NULL,
    coverage TEXT NOT NULL DEFAULT 'RPC_JSONPARSED_NOT_COMPLETE_WALLET_HISTORY');
  CREATE TABLE IF NOT EXISTS econ_instructions (
    sig TEXT NOT NULL, outer_i INTEGER NOT NULL, inner_i INTEGER NOT NULL,
    kind TEXT NOT NULL, program TEXT, mint TEXT, from_account TEXT, to_account TEXT,
    from_owner TEXT, to_owner TEXT, amount_raw TEXT, raw_json TEXT NOT NULL,
    PRIMARY KEY (sig, outer_i, inner_i));
  CREATE INDEX IF NOT EXISTS econ_edges_from ON econ_instructions(from_owner, mint);
  CREATE INDEX IF NOT EXISTS econ_edges_to ON econ_instructions(to_owner, mint);
  CREATE TABLE IF NOT EXISTS econ_wallet_processing (
    sig TEXT NOT NULL, wallet TEXT NOT NULL, state TEXT NOT NULL,
    attempts INTEGER NOT NULL DEFAULT 0, updated_at INTEGER NOT NULL,
    last_error TEXT,
    PRIMARY KEY (sig, wallet)
  );`);
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
const keyOf = k => typeof k === 'string' ? k : (k?.pubkey ?? null);
function tokenOwners(tx, keys) {
  const out = new Map();
  for (const b of [...(tx.meta?.preTokenBalances || []), ...(tx.meta?.postTokenBalances || [])]) {
    const a = keys[b.accountIndex];
    if (!a) continue;
    const old = out.get(a);
    if (old && (old.owner !== (b.owner ?? null) || old.mint !== (b.mint ?? null))) out.set(a, { owner: null, mint: null, conflict: true });
    else if (!old) out.set(a, { owner: b.owner ?? null, mint: b.mint ?? null });
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
    rows.push({ outer_i: oi, inner_i: ii, program, kind,
      mint: kind === 'TOKEN_TRANSFER' ? (info.mint ?? src?.mint ?? dst?.mint ?? null) : null,
      from_account: from, to_account: to,
      from_owner: kind === 'SOL_TRANSFER' ? from : src?.owner ?? null,
      to_owner: kind === 'SOL_TRANSFER' ? to : dst?.owner ?? null,
      amount_raw: kind === 'SOL_TRANSFER' ? String(info.lamports ?? '')
        : kind === 'TOKEN_TRANSFER' ? String(info.tokenAmount?.amount ?? info.amount ?? '') : null,
      raw_json: JSON.stringify(ix), owner_conflict: Boolean(src?.conflict || dst?.conflict) });
  };
  for (let i = 0; i < outer.length; i++) {
    visit(outer[i], i, -1);
    (inner.get(i) || []).forEach((ix, j) => visit(ix, i, j));
  }
  // Keep orphaned innerInstructions as well; malformed RPC data must not be silently discarded.
  for (const [i, batch] of inner) if (i < 0 || i >= outer.length) batch.forEach((ix, j) => visit(ix, i, j));
  return rows;
}
export function persistEvidence(db, sig, tx, observedAt = Date.now()) {
  if (typeof sig !== 'string' || !sig) throw new Error('signature required');
  initEvidence(db);
  const raw = JSON.stringify(tx), hash = createHash('sha256').update(raw).digest('hex');
  const existing = db.prepare('SELECT sha256 FROM econ_transactions WHERE sig = ?').get(sig);
  if (existing?.sha256 === hash) return { sig, duplicate: true, hash };
  const decoded = decodeEvidence(tx);
  const own = !db.isTransaction;
  if (own) db.exec('BEGIN');
  try {
    db.prepare(`INSERT INTO econ_transactions (sig, slot, block_time, status, rpc_json, sha256, observed_at)
      VALUES (?, ?, ?, ?, ?, ?, ?) ON CONFLICT(sig) DO UPDATE SET
      slot=excluded.slot, block_time=excluded.block_time, status=excluded.status,
      rpc_json=excluded.rpc_json, sha256=excluded.sha256, observed_at=excluded.observed_at`)
      .run(sig, tx.slot ?? null, tx.blockTime ?? null, tx.meta.err ? 'FAILED' : 'RPC_OBSERVED', raw, hash, observedAt);
    db.prepare('DELETE FROM econ_instructions WHERE sig = ?').run(sig);
    const ins = db.prepare(`INSERT INTO econ_instructions
      (sig,outer_i,inner_i,kind,program,mint,from_account,to_account,from_owner,to_owner,amount_raw,raw_json)
      VALUES (?,?,?,?,?,?,?,?,?,?,?,?)`);
    for (const r of decoded) ins.run(sig,r.outer_i,r.inner_i,r.kind,r.program,r.mint,r.from_account,r.to_account,r.from_owner,r.to_owner,r.amount_raw,r.raw_json);
    if (own) db.exec('COMMIT');
  } catch (e) { if (own && db.isTransaction) db.exec('ROLLBACK'); throw e; }
  return { sig, duplicate: false, hash, instructions: decoded.length };
}
export function transactionEvidence(db, sig) {
  initEvidence(db);
  const tx = db.prepare('SELECT * FROM econ_transactions WHERE sig = ?').get(sig);
  if (!tx) return null;
  const instructions = db.prepare('SELECT * FROM econ_instructions WHERE sig = ? ORDER BY outer_i, inner_i').all(sig);
  return { ...tx, rpc: JSON.parse(tx.rpc_json), instructions };
}
export function recipientCandidates(db, sender, mint = null, limit = 100) {
  initEvidence(db);
  const rows = db.prepare(`SELECT i.sig, i.outer_i, i.inner_i, i.from_owner, i.to_owner, i.mint,
     i.from_account, i.to_account, i.amount_raw, t.block_time, t.slot
     FROM econ_instructions i JOIN econ_transactions t ON t.sig=i.sig
     WHERE t.status='RPC_OBSERVED' AND i.kind='TOKEN_TRANSFER' AND i.from_owner=?
       AND i.to_owner IS NOT NULL AND i.to_owner!=i.from_owner
       AND (? IS NULL OR i.mint=?) ORDER BY t.block_time DESC, t.slot DESC LIMIT ?`)
    .all(sender, mint, mint, Math.max(1, Math.min(500, limit)));
  return { sender, mint, coverage: 'ONLY_CAPTURED_RPC_TX_AND_RESOLVED_TOKEN_ACCOUNT_OWNERS',
    interpretation: 'OBSERVED_INSTRUCTION_TRANSFER; receiving wallet is a candidate, not controlled identity or a proven later sale', rows };
}
export function crossMintCandidates(db, address, maxHours = 24, limit = 40) {
  initEvidence(db);
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
  initEvidence(db);
  const rows = db.prepare(`SELECT w.sig, MIN(w.t) first_trade_at, COUNT(*) summary_rows
    FROM wallet_trades w LEFT JOIN econ_transactions e ON e.sig=w.sig
    WHERE w.wallet=? AND e.sig IS NULL AND w.sig NOT LIKE 'slot:%'
    GROUP BY w.sig ORDER BY first_trade_at DESC LIMIT ?`)
    .all(wallet, Math.max(1, Math.min(500, limit)));
  return { wallet, rows, coverage: 'KNOWN_WALLET_TRADES_MISSING_RPC_CAPTURE_ONLY',
    next: 'Fetch each listed transaction independently or replay archived jsonParsed RPC; empty rows do not prove complete wallet history' };
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
