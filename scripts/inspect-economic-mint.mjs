#!/usr/bin/env node
// Existing SQLite -> bounded offline Mint evidence report. NEVER starts the Blix server,
// contacts RPC, signs, trades, schedules work, or creates/migrates the input database.
import fs from 'node:fs';
import { DatabaseSync } from 'node:sqlite';
import { recipientOutcomes } from '../server/economic-events.mjs';

const args = process.argv.slice(2);
const allowed = new Set(['--db','--wallet','--mint','--hours']);
const opts = {};
let bad = args.length % 2 !== 0;
for (let i = 0; i < args.length; i += 2) {
  if (!allowed.has(args[i]) || opts[args[i]] !== undefined) bad = true;
  opts[args[i]] = args[i + 1];
}
const validAddress = s => /^[1-9A-HJ-NP-Za-km-z]{32,44}$/.test(s || '');
const hours = opts['--hours'] === undefined ? 24 : Number(opts['--hours']);
if (bad || !opts['--db'] || (opts['--wallet'] !== undefined && !validAddress(opts['--wallet']))
  || !validAddress(opts['--mint']) || !Number.isInteger(hours) || hours < 1 || hours > 168) {
  console.error('Usage: node scripts/inspect-economic-mint.mjs --db EXISTING.sqlite --mint MINT_BASE58 [--wallet SENDER_BASE58] [--hours 1..168]');
  process.exitCode = 2;
} else if (!fs.existsSync(opts['--db']) || !fs.statSync(opts['--db']).isFile()) {
  console.error('Refusing to create a new database: --db must be an existing SQLite file.');
  process.exitCode = 2;
} else {
  let db;
  try {
    db = new DatabaseSync(opts['--db'], { readOnly: true });
    db.exec('PRAGMA query_only=ON');
    const has = name => Boolean(db.prepare("SELECT 1 FROM sqlite_master WHERE type='table' AND name=?").get(name));
    const available = ['econ_transactions','econ_instructions','wallet_trades'].every(has);
    const wallet = opts['--wallet'], mint = opts['--mint'];
    // Mint-first discovery is bounded and uses only locally indexed, successful RPC transfers.
    // The selected senders are observed token-account owners, not proven traders or controllers.
    const discovered = available && !wallet ? db.prepare(`SELECT i.from_owner sender,
      COUNT(DISTINCT i.sig) capturedSignatures
      FROM econ_instructions i JOIN econ_transactions t ON t.sig=i.sig
      WHERE t.status='RPC_OBSERVED' AND i.kind='TOKEN_TRANSFER' AND i.owner_conflict=0
        AND i.mint=? AND i.from_owner IS NOT NULL AND i.to_owner IS NOT NULL
        AND i.to_owner!=i.from_owner
      GROUP BY i.from_owner ORDER BY capturedSignatures DESC, sender ASC LIMIT 11`).all(mint) : [];
    const senders = wallet ? [wallet] : discovered.slice(0, 10).map(x => x.sender);
    const observations = available
      ? senders.map(sender => recipientOutcomes(db, sender, mint, 20, hours))
      : [];
    const coverage = available
      ? 'ONLY_CAPTURED_RPC_TX_AND_RESOLVED_TOKEN_ACCOUNT_OWNERS'
      : 'LOCAL_EVIDENCE_OR_WALLET_SUMMARY_MISSING';
    const window = wallet && has('wallet_sig_windows')
      ? db.prepare('SELECT observation,checked_at_ms,signatures_found,anchor_reached,gaps_seen,ever_initial_sample FROM wallet_sig_windows WHERE wallet=?').get(wallet) || null
      : null;
    const captured = available
      ? db.prepare(`SELECT COUNT(DISTINCT t.sig) n
        FROM econ_transactions t JOIN econ_instructions i ON i.sig=t.sig
        WHERE t.status='RPC_OBSERVED' AND (? IS NULL OR i.from_owner=?) AND i.mint=?`).get(wallet ?? null,wallet ?? null,mint).n
      : 0;
    const recipients = observations.flatMap(result => result.rows).map(row => ({
      signature: row.sig, slot: row.slot, blockTime: row.block_time,
      fromAccount: row.from_account, toAccount: row.to_account,
      fromOwner: row.from_owner, toOwner: row.to_owner, amountRaw: row.amount_raw,
      sellObservation: row.sellObservation || 'TRANSFER_TIME_OR_MINT_UNKNOWN',
      observedSells: (row.observedSells || []).map(x => ({ sig: x.sig, mint: x.mint, t: x.t, sol: x.sol })),
      crossMintCandidates: (row.crossMintCandidates || []).map(x => ({
        soldMint: x.sold_mint, sellSig: x.sell_sig,
        fundingSig: x.funding_sig, boughtMint: x.bought_mint, buySig: x.buy_sig,
      })),
    }));
    console.log(JSON.stringify({
      mode: 'OFFLINE_READ_ONLY_SQLITE_MINT_REPORT',
      input: { wallet, mint, hours },
      evidence: { source: 'EXISTING_LOCAL_SQLITE', knownSenderMintCaptures: captured,
        walletSignatureWindow: window, lifetimeHistoryComplete: false,
        indexedCoverage: coverage,
        senderDiscovery: { method: wallet ? 'EXPLICIT_SENDER' : 'BOUNDED_LOCAL_TOKEN_TRANSFER_OWNER_INDEX',
          selectedSenders: senders.length, maxSenders: wallet ? 1 : 10,
          truncated: !wallet && discovered.length > 10,
          classification: 'UNCLASSIFIED_OWNER_CANDIDATES_INCLUDING_POSSIBLE_POOLS_OR_SERVICES' },
        note: 'Only transactions already captured in this SQLite database are observable.' },
      recipients,
      interpretation: observations[0]?.interpretation || 'No locally indexed candidate; absence does not prove no transfers',
      limitations: [
        'Not a live RPC or complete-wallet-history scan',
        'Mint-first discovery includes only a bounded subset of locally indexed sender owners, not all holders or traders',
        'Observed sender or recipient owner may be a pool, router, or shared service; control is UNKNOWN',
        'Observed later sells do not prove transferred-inventory provenance',
        'Cross-Mint temporal paths do not establish SOL provenance or common control',
        'Empty results mean NOT_OBSERVED_IN_CAPTURED_WINDOW, never confirmed inactivity',
      ],
    }, null, 2));
  } catch (e) {
    console.error('Offline evidence inspection failed:', e.message);
    process.exitCode = 1;
  } finally {
    db?.close();
  }
}
