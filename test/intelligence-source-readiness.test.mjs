import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync,readFileSync,rmSync,existsSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { execFileSync,spawnSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import { DatabaseSync } from 'node:sqlite';

const script=fileURLToPath(new URL('../scripts/audit-intelligence-source-readiness.mjs',import.meta.url));
const mint='EYqygbhZjP7EbM4fSn8devctnksAvPAD1Bt57XBFpump';
const wallet='4p7SeR6361WJ4T4icgsYTnzAUzfA5NwM4CwYD9kMBjuK';
const receiver='BTmCme13XXrD3VLxXFChL9VnmicJ5PjkVUpAsjrooEYh';
const digest=p=>createHash('sha256').update(readFileSync(p)).digest('hex');

test('market/chain provenance audit checks an existing SQLite file without touching original bytes',()=>{
  const root=mkdtempSync(join(tmpdir(),'blix-ready-')),dbPath=join(root,'existing.sqlite');
  try{
    const db=new DatabaseSync(dbPath);
    db.exec('CREATE TABLE tokens(mint TEXT PRIMARY KEY,source TEXT,first_seen INTEGER,updated INTEGER);'
      +'CREATE TABLE snapshots(mint TEXT,t INTEGER);'
      +'CREATE TABLE signals(mint TEXT,t INTEGER);'
      +'CREATE TABLE early(mint TEXT,cp INTEGER);'
      +'CREATE TABLE econ_transactions(sig TEXT PRIMARY KEY,rpc_json TEXT,sha256 TEXT,status TEXT,observed_at INTEGER,slot INTEGER);'
      +'CREATE TABLE econ_instructions(sig TEXT,mint TEXT,kind TEXT,from_owner TEXT,to_owner TEXT,owner_conflict INTEGER);'
      +'CREATE TABLE wallet_sig_windows(wallet TEXT,anchor_reached INTEGER,gaps_seen INTEGER,checked_at_ms INTEGER);');
    db.prepare('INSERT INTO tokens VALUES(?,?,?,?)').run(mint,'pump-live',1000,2000);
    db.prepare('INSERT INTO snapshots VALUES(?,?)').run(mint,1100);
    db.prepare('INSERT INTO signals VALUES(?,?)').run(mint,1200);
    db.prepare('INSERT INTO early VALUES(?,?)').run(mint,30);
    const original={transaction:{signatures:['synthetic-only']},meta:{err:null,innerInstructions:[]}};
    const raw=JSON.stringify(original),sha=createHash('sha256').update(raw).digest('hex');
    db.prepare('INSERT INTO econ_transactions VALUES(?,?,?,?,?,?)')
      .run('synthetic-only',raw,sha,'RPC_OBSERVED',3000,77);
    db.prepare('INSERT INTO econ_instructions VALUES(?,?,?,?,?,?)')
      .run('synthetic-only',mint,'TOKEN_TRANSFER',wallet,receiver,0);
    db.prepare('INSERT INTO wallet_sig_windows VALUES(?,?,?,?)').run(wallet,0,1,2900);
    db.close();
    const before=digest(dbPath);
    const data=JSON.parse(execFileSync(process.execPath,['--no-warnings',script,
      '--db',dbPath,'--mint',mint],{encoding:'utf8'}));
    assert.equal(digest(dbPath),before);
    assert.equal(data.kind,'EXISTING_SQLITE_SOURCE_READINESS_NOT_FULL_MARKET_VERIFICATION');
    assert.equal(data.market.token.source,'pump-live');
    assert.equal(data.market.snapshots.n,1);
    assert.equal(data.market.earlyCheckpoints.checkpoints,1);
    assert.equal(data.market.timestampsProveFirstAvailable,false);
    assert.equal(data.chain.observed.capturedSignatures,1);
    assert.equal(data.chain.observed.tokenTransferRows,1);
    assert.equal(data.chain.integrity.status,'AVAILABLE_SAMPLED_NOT_COMPLETE');
    assert.equal(data.chain.integrity.hashMismatch,0);
    assert.equal(data.chain.walletSignatureWindows.withGaps,1);
    assert.equal(data.readiness.marketDiscovery,'LOCAL_MARKET_ROWS_ONLY_UNIVERSE_UNKNOWN');
    assert.equal(data.readiness.inventory,'NOT_RECONCILED_ASSET_BY_ASSET');
    assert.equal(data.readiness.tradableOpportunity,'NOT_VERIFIED_NO_TIME_VALID_EXECUTABLE_QUOTES');
    assert.equal(data.readiness.monitoring,'NOT_RUNNING');
    assert.ok(data.missing.includes('REAL_SOURCE_FIRST_AVAILABLE_TIME_UNKNOWN'));
    assert.ok(data.missing.includes('FULL_MINT_AND_WALLET_SIGNATURE_HISTORY_UNKNOWN'));
    assert.equal(data.chain.completeMintOrWalletHistory,false);
  }finally{rmSync(root,{recursive:true,force:true});}
});

test('partial schemas and no local rows remain UNKNOWN rather than proof of no activity',()=>{
  const root=mkdtempSync(join(tmpdir(),'blix-ready-')),file=join(root,'empty.sqlite');
  try{
    const db=new DatabaseSync(file);db.exec('CREATE TABLE tokens(mint TEXT PRIMARY KEY,source TEXT,first_seen INTEGER,updated INTEGER)');db.close();
    const before=digest(file);
    const data=JSON.parse(execFileSync(process.execPath,[script,'--db',file,'--mint',mint],{encoding:'utf8'}));
    assert.equal(before,digest(file));
    assert.equal(data.readiness.marketDiscovery,'NOT_SEEN_IN_LOCAL_FILE');
    assert.equal(data.readiness.originalTransactions,'NO_TRUSTWORTHY_CAPTURE_SAMPLE');
    assert.ok(data.missing.includes('ECONOMIC_EVIDENCE_SCHEMA_UNAVAILABLE'));
    assert.equal(data.market.snapshots,null);
  }finally{rmSync(root,{recursive:true,force:true});}
});

test('corrupted cached RPC bytes are detected while the input SQLite is unchanged',()=>{
  const root=mkdtempSync(join(tmpdir(),'blix-ready-')),file=join(root,'bad.sqlite');
  try{
    const db=new DatabaseSync(file);
    db.exec('CREATE TABLE econ_transactions(sig TEXT PRIMARY KEY,rpc_json TEXT,sha256 TEXT,status TEXT,observed_at INTEGER,slot INTEGER);'
      +'CREATE TABLE econ_instructions(sig TEXT,mint TEXT,kind TEXT,from_owner TEXT,to_owner TEXT,owner_conflict INTEGER)');
    db.prepare('INSERT INTO econ_transactions VALUES(?,?,?,?,?,?)')
      .run('bad-sig','{"transaction":{},"meta":{}}','not-really-sha256','RPC_OBSERVED',1234,5);
    db.prepare('INSERT INTO econ_instructions VALUES(?,?,?,?,?,?)')
      .run('bad-sig',mint,'TOKEN_TRANSFER',wallet,receiver,0);
    db.close();const before=digest(file);
    const data=JSON.parse(execFileSync(process.execPath,[script,'--db',file,'--mint',mint],{encoding:'utf8'}));
    assert.equal(before,digest(file));
    assert.equal(data.chain.integrity.status,'CORRUPT_SAMPLED_SOURCE');
    assert.equal(data.readiness.originalTransactions,'NO_TRUSTWORTHY_CAPTURE_SAMPLE');
    assert.ok(data.missing.includes('CORRUPT_ARCHIVED_RPC_IN_SAMPLED_DATA'));
  }finally{rmSync(root,{recursive:true,force:true});}
});

test('unknown paths, unapproved args and invalid Mint never create a database',()=>{
  const root=mkdtempSync(join(tmpdir(),'blix-ready-')),missing=join(root,'no.sqlite');
  try{
    let out=spawnSync(process.execPath,[script,'--db',missing,'--mint',mint],{encoding:'utf8'});
    assert.equal(out.status,2);
    assert.equal(existsSync(missing),false);
    out=spawnSync(process.execPath,[script,'--db',missing,'--mint',mint,'--token','evil'],{encoding:'utf8'});
    assert.equal(out.status,2);
    out=spawnSync(process.execPath,[script,'--db',missing,'--mint','wrong'],{encoding:'utf8'});
    assert.equal(out.status,2);
  }finally{rmSync(root,{recursive:true,force:true});}
});
