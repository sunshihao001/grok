// Deterministic, network-free wallet ingestion checkpoints; no Blix server startup.
import test from 'node:test';
import assert from 'node:assert/strict';
import { DatabaseSync } from 'node:sqlite';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {
  checkpointWalletPage, pendingWalletSignatures, markWalletRpcCaptured,
  markWalletReaderFinished, markWalletReaderFailed, walletSignatureCoverage,
} from '../server/wallet-signature-coverage.mjs';

const A='TEST_WALLET_A', B='TEST_WALLET_B';
const walletDb=(db, address=A)=>{
  db.exec('CREATE TABLE IF NOT EXISTS wallets(address TEXT PRIMARY KEY,last_poll INTEGER,last_sig TEXT,backfilled INTEGER DEFAULT 0)');
  db.prepare('INSERT OR IGNORE INTO wallets(address) VALUES(?)').run(address);
  return db;
};
const open=()=>walletDb(new DatabaseSync(':memory:'));
const row=(sig,blockTime=1000,err=null)=>({signature:sig,blockTime,err});

test('checkpoint inserts discovered signatures and advances the wallet cursor atomically',()=>{
 const db=open();
 const r=checkpointWalletPage(db,{wallet:A,rows:[row('s-new',1200),row('s-old',1100)],first:true,reached:true,observedAt:5000});
 assert.equal(r.observation,'INITIAL_SAMPLE_ONLY');
 assert.equal(r.anchorReached,false);
 assert.equal(db.prepare('SELECT last_sig FROM wallets WHERE address=?').get(A).last_sig,'s-new');
 assert.deepEqual(pendingWalletSignatures(db,A).map(x=>x.sig),['s-new','s-old']);
 assert.deepEqual(pendingWalletSignatures(db,A).map(x=>x.quiet),[1,1]);
 assert.equal(walletSignatureCoverage(db,A).historyComplete,false);
 db.close();
});
test('a simulated restart preserves all signature jobs after advancing the cursor but before enqueue',()=>{
 const folder=fs.mkdtempSync(path.join(os.tmpdir(),'blix-sig-'));
 const filename=path.join(folder,'checkpoint.db');
 try{
  const d1=walletDb(new DatabaseSync(filename));
  checkpointWalletPage(d1,{wallet:A,rows:[row('s3',103),row('s2',102),row('s1',101)],first:true,reached:true,observedAt:1234});
  d1.close();
  const d2=new DatabaseSync(filename);
  assert.equal(d2.prepare('SELECT last_sig FROM wallets WHERE address=?').get(A).last_sig,'s3');
  assert.deepEqual(pendingWalletSignatures(d2,A).map(x=>x.sig),['s3','s2','s1']);
  // A restart may finish jobs without further signature RPC calls.
  markWalletRpcCaptured(d2,A,'s2');
  markWalletReaderFinished(d2,A,'s3');
  assert.deepEqual(pendingWalletSignatures(d2,A).map(x=>x.sig),['s2','s1']);
  assert.equal(walletSignatureCoverage(d2,A).states.find(x=>x.state==='READER_FINISHED').count,1);
  d2.close();
 } finally {fs.rmSync(folder,{recursive:true,force:true});}
});
test('SQLite failure before commit leaves old anchor and jobs unchanged',()=>{
 const d=open();d.prepare('UPDATE wallets SET last_sig=? WHERE address=?').run('old-cursor',A);
 // First create the evidence tables, then inject a failure on the second row.
 assert.equal(walletSignatureCoverage(d,A).historyComplete,false);
 d.exec(`CREATE TRIGGER fail_bad BEFORE INSERT ON wallet_sig_jobs
   WHEN NEW.sig='bad' BEGIN SELECT RAISE(ABORT,'fixture write rejected'); END;`);
 assert.throws(()=>checkpointWalletPage(d,{wallet:A,rows:[row('good',200),row('bad',100)],
   priorAnchor:'old-cursor',first:false,reached:true,observedAt:500}),/fixture write rejected/);
 assert.equal(d.prepare('SELECT last_sig FROM wallets WHERE address=?').get(A).last_sig,'old-cursor');
 assert.equal(d.prepare('SELECT COUNT(*) n FROM wallet_sig_jobs').get().n,0);
 assert.equal(d.prepare('SELECT COUNT(*) n FROM wallet_sig_windows').get().n,0);
 d.close();
});
test('incremental page reports a missing anchor as a gap rather than complete history',()=>{
 const d=open();
 checkpointWalletPage(d,{wallet:A,rows:[row('newer',3000),row('middle',2900)],priorAnchor:'missing',first:false,reached:false,observedAt:8000});
 const c=walletSignatureCoverage(d,A);
 assert.equal(c.conclusion,'WINDOW_TRUNCATED_OR_ANCHOR_LOST');
 assert.equal(c.window.anchor_reached,0);
 assert.equal(c.historyComplete,false);d.close();
});
test('later healthy incremental scan does not erase an earlier truncated window',()=>{
 const d=open();
 checkpointWalletPage(d,{wallet:A,rows:[row('gap-one')],priorAnchor:'old',first:false,reached:false,observedAt:2000});
 checkpointWalletPage(d,{wallet:A,rows:[row('new')],priorAnchor:'gap-one',first:false,reached:true,observedAt:3000});
 const c=walletSignatureCoverage(d,A);
 assert.equal(c.conclusion,'INCREMENTAL_ANCHOR_REACHED');
 assert.equal(c.window.gaps_seen,1);
 assert.equal(c.window.last_gap_at_ms,2000);
 assert.equal(c.unresolvedHistoricalRisk,true);d.close();
});
test('an anchor-reached incremental page is not proof of lifetime completeness',()=>{
 const d=open();checkpointWalletPage(d,{wallet:A,rows:[row('newer')],priorAnchor:'old',first:false,reached:true});
 assert.equal(walletSignatureCoverage(d,A).conclusion,'INCREMENTAL_ANCHOR_REACHED');
 assert.equal(walletSignatureCoverage(d,A).historyComplete,false);d.close();
});
test('duplicate polls are idempotent and retain completed states',()=>{
 const d=open(), p={wallet:A,rows:[row('once')],first:true,reached:true,observedAt:100};
 checkpointWalletPage(d,p);markWalletReaderFinished(d,A,'once');
 checkpointWalletPage(d,{...p,observedAt:200,first:false});
 assert.equal(d.prepare("SELECT COUNT(*) n FROM wallet_sig_jobs").get().n,1);
 assert.deepEqual(pendingWalletSignatures(d,A),[]);
 assert.equal(walletSignatureCoverage(d,A).states.find(x=>x.state==='READER_FINISHED').count,1);
 d.close();
});
test('RPC capture and reader completion are different crash-recovery states',()=>{
 const d=open();checkpointWalletPage(d,{wallet:A,rows:[row('captured'),row('unread')],first:true});
 markWalletRpcCaptured(d,A,'captured');
 assert.deepEqual(pendingWalletSignatures(d,A).map(x=>x.sig).sort(),['captured','unread']);
 markWalletReaderFinished(d,A,'captured');
 assert.deepEqual(pendingWalletSignatures(d,A).map(x=>x.sig),['unread']);d.close();
});
test('after explicit retry exhaustion a wallet signature remains visible, not silently complete',()=>{
 const d=open();checkpointWalletPage(d,{wallet:A,rows:[row('bad')],first:false});
 markWalletReaderFailed(d,A,'bad',true);
 assert.equal(pendingWalletSignatures(d,A).length,0);
 const c=walletSignatureCoverage(d,A);
 assert.equal(c.states.find(x=>x.state==='NEEDS_MANUAL_REPLAY').count,1);
 const reason=d.prepare('SELECT error_kind FROM wallet_sig_jobs WHERE wallet=?').get(A);
 assert.equal(reason.error_kind,'RPC_RATE_LIMIT');d.close();
});
test('identical signature used by two wallets has separate processing states',()=>{
 const d=open();walletDb(d,B);
 checkpointWalletPage(d,{wallet:A,rows:[row('shared')],first:true});
 checkpointWalletPage(d,{wallet:B,rows:[row('shared')],first:true});
 markWalletReaderFinished(d,A,'shared');
 assert.equal(pendingWalletSignatures(d,A).length,0);
 assert.equal(pendingWalletSignatures(d,B).length,1);d.close();
});
test('a chain-failed signature is indexed but not added to successful transaction jobs',()=>{
 const d=open();checkpointWalletPage(d,{wallet:A,rows:[row('failed',100,{InstructionError:[0,'Custom']})],first:true});
 assert.equal(pendingWalletSignatures(d,A).length,0);
 assert.equal(walletSignatureCoverage(d,A).states.find(x=>x.state==='CHAIN_FAILED').count,1);d.close();
});
