// Actual loopback HTTP -> approved readonly SQLite adapter -> original archived
// economic report pipeline. Test data are SYNTHETIC, not historical chain proof.
import test from 'node:test';
import assert from 'node:assert/strict';
import { once } from 'node:events';
import { DatabaseSync } from 'node:sqlite';
import { mkdtempSync,readFileSync,rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { createHash } from 'node:crypto';
import { persistEvidence } from '../server/economic-events.mjs';
import { createResearchHttpServer } from '../server/intelligence/research-http.mjs';
import { makeOfflineEconomicReader,probeExistingEconomicArchive,probeExistingEconomicMint }
  from '../server/intelligence/offline-economic-reader.mjs';

const mint='GTNHLKQWKZHaHpd6PjfMgfFZUDEuCviwXMwYbCcepump';
const otherMint='EYqygbhZjP7EbM4fSn8devctnksAvPAD1Bt57XBFpump';
const fromOwner='4p7SeR6361WJ4T4icgsYTnzAUzfA5NwM4CwYD9kMBjuK';
const toOwner='BTmCme13XXrD3VLxXFChL9VnmicJ5PjkVUpAsjrooEYh';
const tokenProgram='TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA';
const digest=path=>createHash('sha256').update(readFileSync(path)).digest('hex');

test('no-model Blix Mint inspection reads a real disposable SQLite file through HTTP and never mutates it', async t=>{
  const root=mkdtempSync(join(tmpdir(),'blix-no-model-inspect-'));
  t.after(()=>rmSync(root,{recursive:true,force:true}));
  const file=join(root,'archive.sqlite');
  const db=new DatabaseSync(file);
  db.exec('CREATE TABLE wallet_trades(sig TEXT,wallet TEXT,mint TEXT,side TEXT,sol REAL,t INTEGER)');
  const bal=(accountIndex,owner,amount)=>({
    accountIndex,owner,mint,uiTokenAmount:{amount:String(amount),decimals:6},
  });
  const synthetic={slot:151,blockTime:1700000000,
    transaction:{signatures:['synthetic-transfer'],message:{
      accountKeys:[fromOwner,toOwner,'ATA_A','ATA_B',tokenProgram],
      instructions:[{programId:tokenProgram,parsed:{type:'transferChecked',info:{
        source:'ATA_A',destination:'ATA_B',mint,
        tokenAmount:{amount:'400000000',decimals:6},
      }}}],
    }},
    meta:{err:null,fee:5000,preBalances:[0,0,0,0,0],postBalances:[0,0,0,0,0],
      preTokenBalances:[bal(2,fromOwner,400000000),bal(3,toOwner,0)],
      postTokenBalances:[bal(2,fromOwner,0),bal(3,toOwner,400000000)],
      innerInstructions:[],logMessages:[],
    },
  };
  persistEvidence(db,'synthetic-transfer',synthetic);
  db.prepare('INSERT INTO wallet_trades(sig,wallet,mint,side,sol,t) VALUES(?,?,?,?,?,?)')
    .run('synthetic-local-sell',toOwner,mint,'sell',1,1700000080000);
  db.close();
  const hashBefore=digest(file);
  const server=createResearchHttpServer({
    model:null,
    readEconomic:makeOfflineEconomicReader({databasePath:file}),
    sourceReadiness:()=>probeExistingEconomicArchive({databasePath:file}),
    mintReadiness:m=>probeExistingEconomicMint({databasePath:file,mint:m}),
    maxInspections:2,maxTasks:1,
  });
  server.listen(0,'127.0.0.1');
  await once(server,'listening');
  t.after(()=>new Promise((resolve,reject)=>server.close(err=>err?reject(err):resolve())));
  const base='http://127.0.0.1:'+server.address().port;
  const health=await (await fetch(base+'/health')).json();
  assert.equal(health.ready,false);
  assert.equal(health.providerEnabled,false);
  assert.equal(health.inspectionReady,true);
  const inspect=async m=>fetch(base+'/inspect',{
    method:'POST',
    headers:{Origin:'http://localhost:4421','Content-Type':'application/json'},
    body:JSON.stringify({mint:m}),
  });
  let response=await inspect(otherMint);
  assert.equal(response.status,422,'no local indexed Mint: fail before reading or making any model request');
  assert.equal((await response.json()).error,'MINT_LOCAL_EVIDENCE_UNAVAILABLE');
  response=await inspect(mint);
  assert.equal(response.status,200);
  const report=await response.json();
  assert.equal(report.mint,mint);
  assert.equal(report.modelMode,'NOT_USED');
  assert.equal(report.sourceMode,'LOCAL_SQLITE_ONLY');
  assert.equal(report.verifiedMarketOpportunity,false);
  assert.equal(report.liveExecutionValidated,false);
  assert.equal(report.evidence[0].result.facts.recipients[0].signature,'synthetic-transfer');
  assert.equal(report.evidence[0].result.facts.recipients[0].fromOwner,fromOwner);
  assert.equal(report.evidence[0].result.facts.recipients[0].toOwner,toOwner);
  assert.equal(report.evidence[0].result.facts.recipients[0].sellObservation,
    'LOCAL_SELL_SUMMARY_OBSERVED');
  assert.equal(report.continuation.stages.monitoring,'NOT_RUNNING_NO_AUTONOMOUS_WATCHER');
  assert.ok(report.unknowns.some(x=>x.includes('complete')||x.includes('unknown')));
  const remaining=await (await fetch(base+'/health')).json();
  assert.equal(remaining.remainingTasks,1,'no paid model task was consumed');
  assert.equal(remaining.remainingInspections,1);
  assert.equal(digest(file),hashBefore,'SQLite bytes must remain unchanged');
});
