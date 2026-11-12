// Read-only acceptance of a concrete offline Mint report, including proof the input SQLite is unchanged.
import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { createHash } from 'node:crypto';
import { execFileSync, spawnSync } from 'node:child_process';
import { DatabaseSync } from 'node:sqlite';
import { persistEvidence } from '../server/economic-events.mjs';

const script = new URL('../scripts/inspect-economic-mint.mjs', import.meta.url).pathname;
const A = '4p7SeR6361WJ4T4icgsYTnzAUzfA5NwM4CwYD9kMBjuK';
const B = 'BTmCme13XXrD3VLxXFChL9VnmicJ5PjkVUpAsjrooEYh';
const M = 'GTNHLKQWKZHaHpd6PjfMgfFZUDEuCviwXMwYbCcepump';
const TOKEN = 'TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA';
const hash = file => createHash('sha256').update(fs.readFileSync(file)).digest('hex');
const args = (file, extra = []) => [script, '--db', file, '--wallet', A, '--mint', M, ...extra];
const mintArgs = (file, extra = []) => [script, '--db', file, '--mint', M, ...extra];
const bal = (accountIndex, owner, amount) =>
  ({ accountIndex, owner, mint:M, uiTokenAmount:{ amount:String(amount), decimals:6 } });

test('an existing local transaction archive yields a sender-to-recipient Mint report without modifying the database', () => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'blix-readonly-mint-'));
  const file = path.join(root, 'archive.sqlite');
  try {
    const db = new DatabaseSync(file);
    db.exec('CREATE TABLE wallet_trades (sig TEXT,wallet TEXT,mint TEXT,side TEXT,sol REAL,t INTEGER)');
    const original = {
      slot: 151, blockTime: 1700000000,
      transaction:{ signatures:['archive-only-transfer'], message:{
        accountKeys:[A,B,'ATA_A','ATA_B',TOKEN],
        instructions:[{
          programId:TOKEN, parsed:{ type:'transferChecked', info:{
            source:'ATA_A',destination:'ATA_B',mint:M,
            tokenAmount:{ amount:'400000000', decimals:6 }
          }}
        }]
      }},
      meta:{ err:null,fee:5000,preBalances:[1e9,1e9,0,0,0],postBalances:[1e9-5000,1e9,0,0,0],
        preTokenBalances:[bal(2,A,400000000),bal(3,B,0)],
        postTokenBalances:[bal(2,A,0),bal(3,B,400000000)],
        innerInstructions:[], logMessages:[] }
    };
    persistEvidence(db,'archive-only-transfer',original);
    db.prepare('INSERT INTO wallet_trades(sig,wallet,mint,side,sol,t) VALUES(?,?,?,?,?,?)')
      .run('recipient-later-sale',B,M,'sell',1,1700000080000);
    db.close();
    const before = hash(file);
    const report = JSON.parse(execFileSync(process.execPath,args(file),{encoding:'utf8',timeout:15000}));
    assert.equal(report.mode,'OFFLINE_READ_ONLY_SQLITE_MINT_REPORT');
    assert.equal(report.evidence.knownSenderMintCaptures,1);
    assert.equal(report.evidence.lifetimeHistoryComplete,false);
    assert.equal(report.recipients.length,1);
    assert.equal(report.recipients[0].toOwner,B);
    assert.equal(report.recipients[0].amountRaw,'400000000');
    assert.equal(report.recipients[0].sellObservation,'LOCAL_SELL_SUMMARY_OBSERVED');
    assert.deepEqual(report.recipients[0].observedSells.map(x=>x.sig),['recipient-later-sale']);
    assert.ok(!JSON.stringify(report).includes('rpc_json'),'report exposes metadata, not whole raw transaction');
    assert.equal(hash(file),before,'even in shared filesystem the report leaves the SQLite bytes unchanged');
    // The user-facing investigation starts with a Mint, not a preselected wallet.
    const mintReport = JSON.parse(execFileSync(process.execPath,mintArgs(file),{encoding:'utf8',timeout:15000}));
    assert.equal(mintReport.input.wallet,undefined);
    assert.equal(mintReport.input.mint,M);
    assert.equal(mintReport.evidence.senderDiscovery.method,'BOUNDED_LOCAL_TOKEN_TRANSFER_OWNER_INDEX');
    assert.equal(mintReport.evidence.senderDiscovery.selectedSenders,1);
    assert.equal(mintReport.evidence.senderDiscovery.truncated,false);
    assert.equal(mintReport.recipients[0].fromOwner,A);
    assert.equal(mintReport.recipients[0].toOwner,B);
    assert.equal(mintReport.recipients[0].sellObservation,'LOCAL_SELL_SUMMARY_OBSERVED');
    assert.equal(mintReport.evidence.lifetimeHistoryComplete,false);
    assert.equal(hash(file),before,'Mint-first discovery must not mutate the source archive');
    // Unknown transfer time is not a valid observation window, even if B has a sale summary.
    const edit = new DatabaseSync(file);
    edit.prepare('UPDATE econ_transactions SET block_time=NULL WHERE sig=?').run('archive-only-transfer');
    edit.close();
    const beforeUnknown = hash(file);
    const unknown = JSON.parse(execFileSync(process.execPath,args(file),{encoding:'utf8',timeout:15000}));
    assert.equal(unknown.recipients.length,1);
    assert.equal(unknown.recipients[0].sellObservation,'TRANSFER_TIME_OR_MINT_UNKNOWN');
    assert.deepEqual(unknown.recipients[0].observedSells,[]);
    assert.equal(hash(file),beforeUnknown,'unknown-time report must also remain read-only');
    const unknownMint = JSON.parse(execFileSync(process.execPath,mintArgs(file),{encoding:'utf8',timeout:15000}));
    assert.equal(unknownMint.recipients[0].sellObservation,'TRANSFER_TIME_OR_MINT_UNKNOWN');
    assert.equal(hash(file),beforeUnknown);
  } finally { fs.rmSync(root,{recursive:true,force:true}); }
});

test('missing local evidence tables remain UNKNOWN, not a false statement of no transfer', () => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(),'blix-empty-mint-'));
  const file = path.join(root,'empty.sqlite');
  try {
    const d = new DatabaseSync(file);
    d.close();
    const before=hash(file);
    const report=JSON.parse(execFileSync(process.execPath,args(file),{encoding:'utf8',timeout:15000}));
    assert.deepEqual(report.recipients,[]);
    assert.equal(report.evidence.indexedCoverage,'LOCAL_EVIDENCE_OR_WALLET_SUMMARY_MISSING');
    assert.equal(report.evidence.lifetimeHistoryComplete,false);
    assert.equal(hash(file),before);
    const mintOnly=JSON.parse(execFileSync(process.execPath,mintArgs(file),{encoding:'utf8',timeout:15000}));
    assert.equal(mintOnly.evidence.senderDiscovery.selectedSenders,0);
    assert.deepEqual(mintOnly.recipients,[]);
    assert.equal(mintOnly.evidence.lifetimeHistoryComplete,false);
    assert.equal(hash(file),before);
  } finally { fs.rmSync(root,{recursive:true,force:true}); }
});

test('missing DB or unbounded time range fails closed without creating files', () => {
  const root=fs.mkdtempSync(path.join(os.tmpdir(),'blix-missing-mint-'));
  const missing=path.join(root,'must-not-create.sqlite');
  try {
    const notFound=spawnSync(process.execPath,args(missing),{encoding:'utf8',timeout:15000});
    assert.equal(notFound.status,2);
    assert.equal(fs.existsSync(missing),false);
    const unbounded=spawnSync(process.execPath,args(missing,['--hours','999']),{encoding:'utf8',timeout:15000});
    assert.equal(unbounded.status,2);
  } finally { fs.rmSync(root,{recursive:true,force:true}); }
});


test('Mint-only discovery keeps a locally evidenced wallet visible when many unclassified senders compete for the top ten', () => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'blix-mint-sender-priority-'));
  const file = path.join(root, 'archive.sqlite');
  try {
    const db = new DatabaseSync(file);
    db.exec('CREATE TABLE wallet_trades (sig TEXT,wallet TEXT,mint TEXT,side TEXT,sol REAL,t INTEGER)');
    // A locally observed wallet is an investigation lead, NOT a verified private operator.
    db.prepare('INSERT INTO wallet_trades(sig,wallet,mint,side,sol,t) VALUES(?,?,?,?,?,?)')
      .run('known-buy', A, M, 'buy', 1, 1700000000000);
    const observed = (sender, sig, slot) => persistEvidence(db, sig, {
      slot, blockTime: 1700000000 + slot,
      transaction: { signatures: [sig], message: {
        accountKeys: [sender, B, 'SRC_TOKEN_ACCOUNT', 'DST_TOKEN_ACCOUNT', TOKEN],
        instructions: [{ programId: TOKEN, parsed: { type: 'transferChecked', info: {
          source: 'SRC_TOKEN_ACCOUNT', destination: 'DST_TOKEN_ACCOUNT', mint: M,
          tokenAmount: { amount: '1000', decimals: 6 },
        } } }],
      } },
      meta: {
        err: null, fee: 5000, preBalances: [0,0,0,0,0], postBalances: [0,0,0,0,0],
        preTokenBalances: [bal(2, sender, 1000), bal(3, B, 0)],
        postTokenBalances: [bal(2, sender, 0), bal(3, B, 1000)],
        innerInstructions: [],
      },
    });
    // These 11 addresses sort before A and would consume all ten slots in the
    // former count/address ranking. They are deliberately UNCLASSIFIED; do not
    // claim a pool, exchange or common controller without additional evidence.
    for (const [i, last] of [...'23456789ABC'].entries()) {
      observed('3'.repeat(33) + last, 'unclassified-' + i, i + 1);
    }
    observed(A, 'known-transfer', 25);
    db.close();
    const before = hash(file);
    const report = JSON.parse(execFileSync(process.execPath, mintArgs(file), { encoding: 'utf8', timeout: 15000 }));
    assert.equal(report.evidence.senderDiscovery.selectedSenders, 10);
    assert.equal(report.evidence.senderDiscovery.truncated, true);
    assert.equal(report.evidence.senderDiscovery.locallyObservedTradeSenders, 1);
    assert.match(report.evidence.senderDiscovery.priority, /LOCAL_WALLET_TRADE/);
    assert.match(report.evidence.senderDiscovery.classification, /POSSIBLE_POOLS_OR_SERVICES/);
    assert.equal(report.recipients[0].fromOwner, A,
      'bounded sender sample should include the locally corroborated wallet');
    assert.equal(report.recipients.filter(x => x.fromOwner === A).length, 1);
    assert.equal(new Set(report.recipients.map(x => x.fromOwner)).size, 10);
    assert.equal(report.evidence.lifetimeHistoryComplete, false);
    assert.equal(hash(file), before, 'priority selection must not mutate the offline archive');
  } finally {
    fs.rmSync(root, { recursive: true, force: true });
  }
});
