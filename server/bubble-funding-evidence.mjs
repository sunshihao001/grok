// Bubble Map funding evidence: transaction instruction ≠ fee payer ≠ common control.
// Pure, bounded helpers so synthetic RPC cases can be tested without starting Blix.
const SYSTEM_PROGRAM = '11111111111111111111111111111111';
export const FUNDING_TRUNCATED = 'HISTORY_TRUNCATED';
export const FUNDING_DIRECT = 'DIRECT_SOL_OBSERVED';
const RETRY_MS = 60 * 60_000;

export function directSolFunding(tx, wallet) {
  if (!tx?.transaction?.message || tx.meta?.err) return null;
  const outer = tx.transaction.message.instructions || [];
  const inner = (tx.meta?.innerInstructions || []).flatMap(x => x.instructions || []);
  const candidates = new Map();
  for (const ix of [...outer, ...inner]) {
    if (ix?.program !== 'system' && ix?.programId !== SYSTEM_PROGRAM) continue;
    const kind = ix?.parsed?.type;
    if (kind !== 'transfer' && kind !== 'createAccount') continue;
    const info = ix?.parsed?.info || {};
    const to = kind === 'createAccount' ? info.newAccount : info.destination;
    const lamports = Number(info.lamports);
    if (to === wallet && info.source && info.source !== wallet && Number.isSafeInteger(lamports) && lamports > 0) {
      if (!candidates.has(info.source)) candidates.set(info.source, { funder: info.source, lamports: String(info.lamports), instruction: kind });
    }
  }
  if (candidates.size > 1) return { ambiguous: true, sources: [...candidates.keys()] };
  return candidates.values().next().value || null;
}

export function feePayer(tx) {
  const first = tx?.transaction?.message?.accountKeys?.[0];
  return typeof first === 'string' ? first : first?.pubkey || null;
}

// Stays bounded by maxPages; a 3,000-signature scan is not full historical proof.
// page(before) returns getSignaturesForAddress result, transaction(sig) returns jsonParsed RPC.
export async function traceWalletFunding(wallet, {
  page, transaction, cursor = null, lastSignature = null, retrySignature = null,
  maxPages = 3, pageSize = 1000,
} = {}) {
  if (typeof page !== 'function' || typeof transaction !== 'function') throw new Error('Read functions required');
  let oldest = lastSignature, before = cursor, exhausted = Boolean(retrySignature);
  if (retrySignature) oldest = retrySignature;
  let scanned = 0;
  if (!retrySignature) for (let i = 0; i < maxPages; i++) {
    const rows = await page(before);
    if (!Array.isArray(rows)) throw new Error('Invalid signature history response');
    if (!rows.length) { exhausted = true; break; }
    const last = rows[rows.length - 1]?.signature;
    if (typeof last !== 'string' || !last) throw new Error('Missing signature in history page');
    if (last === before) throw new Error('Signature history cursor did not advance');
    oldest = last;
    scanned += rows.length;
    if (rows.length < pageSize) { exhausted = true; break; }
    before = oldest;
  }
  if (!exhausted) return { status: FUNDING_TRUNCATED, funder: null, payer: null,
    signature: oldest || null, cursor: before || null, scanned };
  if (!oldest) return { status: 'NO_VISIBLE_HISTORY', funder: null, payer: null,
    signature: null, cursor: null, scanned };
  const tx = await transaction(oldest);
  if (!tx) return { status: 'EARLIEST_TX_UNAVAILABLE', funder: null, payer: null,
    signature: oldest, cursor: null, scanned };
  const payer = feePayer(tx);
  const transfer = directSolFunding(tx, wallet);
  return { status: transfer?.ambiguous ? 'MULTIPLE_DIRECT_SOL_SENDERS'
      : transfer ? FUNDING_DIRECT : payer && payer !== wallet ? 'FEE_PAYER_ONLY' : 'NO_DIRECT_SOL_IN_EARLIEST_TX',
    funder: transfer?.ambiguous ? null : transfer?.funder || null, payer, signature: oldest, cursor: null, scanned };
}

// Single existing cache is migrated in place. Old rows have unknown provenance:
// default UNVERIFIED_LEGACY prevents their funder values being used as edges.
export function initBubbleFundingCache(db) {
  db.exec('CREATE TABLE IF NOT EXISTS bubble_funders (wallet TEXT PRIMARY KEY, funder TEXT NOT NULL, t INTEGER NOT NULL)');
  const columns = new Set(db.prepare('PRAGMA table_info(bubble_funders)').all().map(x => x.name));
  const additions = {
    status: "ALTER TABLE bubble_funders ADD COLUMN status TEXT NOT NULL DEFAULT 'UNVERIFIED_LEGACY'",
    signature: 'ALTER TABLE bubble_funders ADD COLUMN signature TEXT',
    payer: 'ALTER TABLE bubble_funders ADD COLUMN payer TEXT',
    cursor: 'ALTER TABLE bubble_funders ADD COLUMN cursor TEXT',
  };
  for (const [name, sql] of Object.entries(additions)) if (!columns.has(name)) db.exec(sql);
}
export const verifiedFunder = row => row?.status === FUNDING_DIRECT && row.funder ? row.funder : null;
export function shouldRefreshFunding(row, nowMs = Date.now()) {
  if (!row || row.status === 'UNVERIFIED_LEGACY') return true;
  if (row.status === FUNDING_TRUNCATED && row.cursor) return nowMs - row.t >= RETRY_MS;
  if (row.status === 'EARLIEST_TX_UNAVAILABLE' && row.signature) return nowMs - row.t >= RETRY_MS;
  if (row.status === 'NO_VISIBLE_HISTORY') return nowMs - row.t >= 24 * RETRY_MS;
  return false;
}
