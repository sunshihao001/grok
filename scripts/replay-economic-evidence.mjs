#!/usr/bin/env node
// Offline-only replay of archived getTransaction(jsonParsed) JSON into an explicit SQLite database.
// No RPC, signing, account access, service startup, or trade operations.
import fs from 'node:fs';
import { DatabaseSync } from 'node:sqlite';
import { persistEvidence } from '../server/economic-events.mjs';
const args = process.argv.slice(2);
const flag = name => { const i = args.indexOf(name); return i >= 0 ? args[i + 1] : null; };
const dbPath = flag('--db'), inputPath = flag('--input');
if (!dbPath || !inputPath || args.some(a => !['--db','--input',dbPath,inputPath].includes(a))) {
  console.error('Usage: node scripts/replay-economic-evidence.mjs --db EXISTING.sqlite --input ARCHIVED_JSON_FILE');
  process.exitCode = 2;
} else if (!fs.existsSync(dbPath) || !fs.existsSync(inputPath)) {
  console.error('Both the target database and archived JSON input must exist. Refusing to create/guess a DB.');
  process.exitCode = 2;
} else {
  const data = JSON.parse(fs.readFileSync(inputPath, 'utf8'));
  const entries = Array.isArray(data) ? data : Array.isArray(data.transactions) ? data.transactions : [data];
  if (entries.length > 500) throw new Error('More than 500 transactions: split archived input for bounded replay');
  const db = new DatabaseSync(dbPath);
  try {
    const results = [];
    for (const entry of entries) {
      const tx = entry.tx ?? entry;
      const sig = entry.sig || entry.signature || tx.transaction?.signatures?.[0];
      results.push(persistEvidence(db, sig, tx, Date.now(), { captureSource: 'OFFLINE_ARCHIVE', commitment: null }));
    }
    console.log(JSON.stringify({ mode: 'LOCAL_ARCHIVED_RPC_JSON_REPLAY', inputCount: entries.length,
      stored: results.filter(x => !x.duplicate).length, duplicates: results.filter(x => x.duplicate).length,
      note: 'No live history coverage or capital provenance is established' }, null, 2));
  } finally { db.close(); }
}
