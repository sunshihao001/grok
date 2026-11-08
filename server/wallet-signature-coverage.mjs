// Durable signature *discovery* for the existing Blix wallet reader.
// Do not duplicate econ_wallet_processing: that is the sole captured/retry/complete state.
import { initEvidence } from './economic-events.mjs';

const initialized = new WeakSet();
export function initWalletSignatureCoverage(db) {
  if (initialized.has(db)) return;
  db.exec(`CREATE TABLE IF NOT EXISTS wallet_sig_jobs (
    wallet TEXT NOT NULL, sig TEXT NOT NULL, block_time_ms INTEGER,
    state TEXT NOT NULL DEFAULT 'DISCOVERED', quiet INTEGER NOT NULL DEFAULT 0,
    discovered_at_ms INTEGER NOT NULL, updated_ms INTEGER NOT NULL,
    PRIMARY KEY(wallet,sig)
  );
  CREATE INDEX IF NOT EXISTS wallet_sig_jobs_pending ON wallet_sig_jobs(wallet,state,block_time_ms);
  CREATE TABLE IF NOT EXISTS wallet_sig_windows (
    wallet TEXT PRIMARY KEY, checked_at_ms INTEGER NOT NULL,
    previous_anchor TEXT, newest_sig TEXT, oldest_seen_sig TEXT,
    signatures_found INTEGER NOT NULL, anchor_reached INTEGER NOT NULL,
    observation TEXT NOT NULL, first_sample INTEGER NOT NULL,
    gaps_seen INTEGER NOT NULL DEFAULT 0, last_gap_at_ms INTEGER,
    ever_initial_sample INTEGER NOT NULL DEFAULT 0
  );`);
  initialized.add(db);
}

/**
 * Atomic discovery+watermark. A crash after commit but before enqueue leaves
 * jobs available for recovery; a failed insert must NOT advance last_sig.
 * An initial 25-signature sample is always partial lifetime history.
 */
export function checkpointWalletPage(db,{wallet,rows,priorAnchor=null,first=false,reached=false,
  observedAt=Date.now()}) {
  if (!wallet || !Array.isArray(rows)) throw new TypeError('wallet and signature page required');
  if (rows.some(r=>!r?.signature || typeof r.signature!=='string')) throw new Error('invalid signature page');
  initWalletSignatureCoverage(db);
  const newest=rows[0]?.signature ?? null,oldest=rows.at(-1)?.signature ?? null;
  const observation=first?'INITIAL_SAMPLE_ONLY':reached?'INCREMENTAL_ANCHOR_REACHED':'WINDOW_TRUNCATED_OR_ANCHOR_LOST';
  const own=!db.isTransaction;
  if(own)db.exec('BEGIN');
  try{
    const ins=db.prepare(`INSERT INTO wallet_sig_jobs(wallet,sig,block_time_ms,state,quiet,discovered_at_ms,updated_ms)
      VALUES(?,?,?,?,?,?,?) ON CONFLICT(wallet,sig) DO UPDATE SET
      block_time_ms=COALESCE(excluded.block_time_ms,wallet_sig_jobs.block_time_ms),
      updated_ms=excluded.updated_ms`);
    for(const row of rows)ins.run(wallet,row.signature,
      Number.isFinite(row.blockTime)?row.blockTime*1000:null,
      row.err?'CHAIN_FAILED':'DISCOVERED',first?1:0,observedAt,observedAt);
    db.prepare(`INSERT INTO wallet_sig_windows
      (wallet,checked_at_ms,previous_anchor,newest_sig,oldest_seen_sig,signatures_found,
       anchor_reached,observation,first_sample,gaps_seen,last_gap_at_ms,ever_initial_sample)
      VALUES(?,?,?,?,?,?,?,?,?,?,?,?)
      ON CONFLICT(wallet) DO UPDATE SET checked_at_ms=excluded.checked_at_ms,
      previous_anchor=excluded.previous_anchor,newest_sig=excluded.newest_sig,
      oldest_seen_sig=excluded.oldest_seen_sig,signatures_found=excluded.signatures_found,
      anchor_reached=excluded.anchor_reached,observation=excluded.observation,
      first_sample=excluded.first_sample,
      gaps_seen=wallet_sig_windows.gaps_seen+excluded.gaps_seen,
      last_gap_at_ms=COALESCE(excluded.last_gap_at_ms,wallet_sig_windows.last_gap_at_ms),
      ever_initial_sample=MAX(wallet_sig_windows.ever_initial_sample,excluded.ever_initial_sample)`)
      .run(wallet,observedAt,priorAnchor,newest,oldest,rows.length,reached?1:0,
        observation,first?1:0,(!first&&!reached)?1:0,(!first&&!reached)?observedAt:null,first?1:0);
    const changed=db.prepare('UPDATE wallets SET last_poll=?,last_sig=COALESCE(?,last_sig),backfilled=1 WHERE address=?')
      .run(observedAt,newest,wallet);
    if(changed.changes!==1)throw new Error('wallet cursor update missing');
    if(own)db.exec('COMMIT');
    return {wallet,newest,oldest,observation,signaturesFound:rows.length};
  }catch(e){if(own&&db.isTransaction)db.exec('ROLLBACK');throw e;}
}

/**
 * Queue only still-unknown signatures or interrupted captured RPCs. The
 * pre-existing econ_wallet_processing handles RETRY_REQUIRED and limits attempts.
 * No duplicate CAPTURED/COMPLETE journal is introduced by this module.
 */
export function pendingWalletSignatures(db,wallet,limit=120){
  initWalletSignatureCoverage(db);
  initEvidence(db);
  return db.prepare(`SELECT j.sig,j.block_time_ms AS t,j.quiet,p.state processing_state,p.attempts
    FROM wallet_sig_jobs j
    LEFT JOIN econ_wallet_processing p ON p.sig=j.sig AND p.wallet=j.wallet
    WHERE j.wallet=? AND j.state='DISCOVERED' AND
      (p.state IS NULL OR (p.state='CAPTURED' AND p.attempts<5))
    ORDER BY j.updated_ms DESC,j.block_time_ms DESC LIMIT ?`)
    .all(wallet,Math.max(1,Math.min(120,Number(limit)||120)));
}
export function walletSignatureCoverage(db,wallet){
  initWalletSignatureCoverage(db);
  const window=db.prepare('SELECT * FROM wallet_sig_windows WHERE wallet=?').get(wallet)||null;
  const counts=db.prepare('SELECT state,COUNT(*) n FROM wallet_sig_jobs WHERE wallet=? GROUP BY state').all(wallet);
  return {wallet,window,counts,historyComplete:false,
    unresolvedHistoricalRisk:Boolean(window?.gaps_seen||window?.ever_initial_sample),
    conclusion:window?.observation||'NO_SCAN_WINDOW_RECORDED',
    note:'No single incremental cursor proves lifetime coverage; reader consumption uses econ_wallet_processing.'};
}
