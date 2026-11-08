// Wallet signature discovery checkpoint. Local SQLite only: no RPC or background work.
// Three independent facts: SIGNATURE_DISCOVERED, RPC_CAPTURED, READER_FINISHED.
// Reader completion is NOT proof that all CPI/transfer semantics or history are known.

const initialized = new WeakSet();
const clip = (x, n = 180) => String(x || '').slice(0, n);

export function initWalletSignatureCoverage(db) {
  if (initialized.has(db)) return;
  db.exec(`CREATE TABLE IF NOT EXISTS wallet_sig_jobs (
    wallet TEXT NOT NULL, sig TEXT NOT NULL, block_time_ms INTEGER,
    state TEXT NOT NULL DEFAULT 'DISCOVERED', quiet INTEGER NOT NULL DEFAULT 0, first_seen_ms INTEGER NOT NULL,
    updated_ms INTEGER NOT NULL, error_kind TEXT,
    PRIMARY KEY (wallet, sig)
  );
  CREATE INDEX IF NOT EXISTS wallet_sig_jobs_pending ON wallet_sig_jobs(wallet, state, block_time_ms);
  CREATE TABLE IF NOT EXISTS wallet_sig_windows (
    wallet TEXT PRIMARY KEY, checked_at_ms INTEGER NOT NULL,
    previous_anchor TEXT, newest_sig TEXT, oldest_seen_sig TEXT,
    signatures_found INTEGER NOT NULL, anchor_reached INTEGER NOT NULL,
    observation TEXT NOT NULL, first_sample INTEGER NOT NULL
  );`);
  initialized.add(db);
}

/**
 * Persist every signature returned by a completed wallet poll AND advance the old
 * wallet.last_sig cursor in one SQLite transaction. If a crash occurs after this
 * transaction but before in-memory enqueue, outstanding rows survive restart.
 *
 * "anchor reached" describes only the requested incremental window. First
 * sampling 25 signatures cannot establish that the wallet's whole past is read.
 */
export function checkpointWalletPage(db, { wallet, rows, priorAnchor = null, first = false,
  reached = false, observedAt = Date.now() }) {
  if (!wallet || !Array.isArray(rows)) throw new TypeError('wallet and rows required');
  if (rows.some(r => !r?.signature || typeof r.signature !== 'string')) throw new Error('invalid signature page');
  initWalletSignatureCoverage(db);
  const newest = rows[0]?.signature ?? null;
  const oldest = rows.at(-1)?.signature ?? null;
  const observation = first ? 'INITIAL_SAMPLE_ONLY'
    : reached ? 'INCREMENTAL_ANCHOR_REACHED' : 'WINDOW_TRUNCATED_OR_ANCHOR_LOST';
  const own = !db.isTransaction;
  if (own) db.exec('BEGIN');
  try {
    const insert = db.prepare(`INSERT INTO wallet_sig_jobs
      (wallet, sig, block_time_ms, state, quiet, first_seen_ms, updated_ms)
      VALUES (?, ?, ?, ?, ?, ?, ?)
      ON CONFLICT(wallet,sig) DO UPDATE SET
      block_time_ms=COALESCE(excluded.block_time_ms,wallet_sig_jobs.block_time_ms),
      updated_ms=excluded.updated_ms`);
    let discovered = 0;
    for (const row of rows) {
      insert.run(wallet, row.signature, Number.isFinite(row.blockTime) ? row.blockTime * 1000 : null,
        row.err ? 'CHAIN_FAILED' : 'DISCOVERED', first ? 1 : 0, observedAt, observedAt);
      discovered++;
    }
    db.prepare(`INSERT INTO wallet_sig_windows
      (wallet,checked_at_ms,previous_anchor,newest_sig,oldest_seen_sig,signatures_found,anchor_reached,observation,first_sample)
      VALUES (?,?,?,?,?,?,?,?,?)
      ON CONFLICT(wallet) DO UPDATE SET checked_at_ms=excluded.checked_at_ms,
      previous_anchor=excluded.previous_anchor,newest_sig=excluded.newest_sig,
      oldest_seen_sig=excluded.oldest_seen_sig,signatures_found=excluded.signatures_found,
      anchor_reached=excluded.anchor_reached,observation=excluded.observation,
      first_sample=excluded.first_sample`)
      .run(wallet, observedAt, priorAnchor, newest, oldest, rows.length, reached ? 1 : 0, observation, first ? 1 : 0);
    const updated = db.prepare(`UPDATE wallets SET last_poll=?, last_sig=COALESCE(?,last_sig),
      backfilled=1 WHERE address=?`).run(observedAt, newest, wallet);
    if (updated.changes !== 1) throw new Error('wallet cursor update missing: no durable checkpoint');
    if (own) db.exec('COMMIT');
    return { wallet, observation, discovered, newest, oldest, anchorReached: Boolean(reached) && !first };
  } catch (e) {
    if (own && db.isTransaction) db.exec('ROLLBACK');
    throw e;
  }
}

/** Jobs are replayable after a restart; no network request is initiated here. */
export function pendingWalletSignatures(db, wallet, limit = 120) {
  initWalletSignatureCoverage(db);
  return db.prepare(`SELECT sig, block_time_ms AS t, quiet, state
    FROM wallet_sig_jobs WHERE wallet=? AND state IN ('DISCOVERED','RPC_CAPTURED')
    ORDER BY updated_ms DESC, block_time_ms DESC LIMIT ?`)
    .all(wallet, Math.max(1, Math.min(120, Number(limit) || 120)));
}

function updateJob(db, wallet, sig, state, errorKind = null, at = Date.now()) {
  initWalletSignatureCoverage(db);
  db.prepare(`INSERT INTO wallet_sig_jobs(wallet,sig,block_time_ms,state,first_seen_ms,updated_ms,error_kind)
    VALUES (?,?,NULL,?,?,?,?)
    ON CONFLICT(wallet,sig) DO UPDATE SET
      state=excluded.state,updated_ms=excluded.updated_ms,error_kind=excluded.error_kind`)
    .run(wallet, sig, state, at, at, errorKind);
}

export const markWalletRpcCaptured = (db, wallet, sig) => updateJob(db,wallet,sig,'RPC_CAPTURED');
export const markWalletReaderFinished = (db, wallet, sig) => updateJob(db,wallet,sig,'READER_FINISHED');
export const markWalletReaderFailed = (db, wallet, sig, limited = false) =>
  updateJob(db,wallet,sig,'NEEDS_MANUAL_REPLAY',limited ? 'RPC_RATE_LIMIT' : 'READER_FAILED');

export function walletSignatureCoverage(db, wallet) {
  initWalletSignatureCoverage(db);
  const window = db.prepare('SELECT * FROM wallet_sig_windows WHERE wallet=?').get(wallet) || null;
  const states = db.prepare(`SELECT state, COUNT(*) count FROM wallet_sig_jobs
    WHERE wallet=? GROUP BY state`).all(wallet);
  return { wallet, window, states, conclusion: window?.observation || 'NO_SCAN_WINDOW_RECORDED',
    historyComplete: false, note: 'Incremental anchor and processed reader events never prove complete wallet history' };
}
