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
if (bad || !opts['--db'] || !validAddress(opts['--wallet'])
  || !validAddress(opts['--mint']) || !Number.isInteger(hours) || hours < 1 || hours > 168) {
  console.error('Usage: node scripts/inspect-economic-mint.mjs --db EXISTING.sqlite --wallet SENDER_BASE58 --mint MINT_BASE58 [--hours 1..168]');
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
    const observations = available
      ? recipientOutcomes(db, wallet, mint, 20, hours)
      : { rows: [], coverage: 'LOCAL_EVIDENCE_OR_WALLET_SUMMARY_MISSING', interpretation: 'No negative inference from missing tables' };
    const window = has('wallet_sig_windows')
      ? db.prepare('SELECT observation,checked_at_ms,signatures_found,anchor_reached,gaps_seen,ever_initial_sample FROM wallet_sig_windows WHERE wallet=?').get(wallet) || null
      : null;
    const captured = available
      ? db.prepare(`SELECT COUNT(DISTINCT t.sig) n
        FROM econ_transactions t JOIN econ_instructions i ON i.sig=t.sig
        WHERE t.status='RPC_OBSERVED' AND i.from_owner=? AND i.mint=?`).get(wallet,mint).n
      : 0;
    const recipients = observations.rows.map(row => ({
      signature: row.sig, slot: row.slot, blockTime: row.block_time,
      fromAccount: row.from_account, toAccount: row.to_account,
      fromOwner: row.from_owner, toOwner: row.to_owner, amountRaw: row.amount_raw,
      sellObservation: row.sellObservation || 'NOT_OBSERVED_IN_CAPTURED_WINDOW',
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
        indexedCoverage: observations.coverage,
        note: 'Only transactions already captured in this SQLite database are observable.' },
      recipients,
      interpretation: observations.interpretation,
      limitations: [
        'Not a live RPC or complete-wallet-history scan',
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
