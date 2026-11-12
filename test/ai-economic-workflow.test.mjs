import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { createHash } from 'node:crypto';
import { DatabaseSync } from 'node:sqlite';
import { persistEvidence } from '../server/economic-events.mjs';
import { runAiResearchTask } from '../server/intelligence/ai-workflow.mjs';
import { makeOfflineEconomicReader } from '../server/intelligence/offline-economic-reader.mjs';

const M = 'GTNHLKQWKZHaHpd6PjfMgfFZUDEuCviwXMwYbCcepump';
const A = '4p7SeR6361WJ4T4icgsYTnzAUzfA5NwM4CwYD9kMBjuK';
const B = 'BTmCme13XXrD3VLxXFChL9VnmicJ5PjkVUpAsjrooEYh';
const TOKEN = 'TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA';
const goal = '调查这个 Mint 的接收钱包后续行为：' + M;
const hash = (file) => createHash('sha256').update(fs.readFileSync(file)).digest('hex');

function seededArchive(file) {
  const db = new DatabaseSync(file);
  db.exec('CREATE TABLE wallet_trades (sig TEXT,wallet TEXT,mint TEXT,side TEXT,sol REAL,t INTEGER)');
  const bal = (accountIndex, owner, amount) => ({ accountIndex, owner, mint:M,
    uiTokenAmount: { amount: String(amount), decimals:6 } });
  persistEvidence(db, 'evidence-transfer', {
    slot: 151, blockTime: 1700000000,
    transaction: { signatures: ['evidence-transfer'], message: {
      accountKeys: [A,B,'ATA_A','ATA_B',TOKEN],
      instructions: [{ programId:TOKEN, parsed:{ type:'transferChecked', info:{
        source:'ATA_A', destination:'ATA_B', mint:M, tokenAmount:{ amount:'400000000', decimals:6 }
      } } }],
    } },
    meta: {
      err:null,fee:5000,preBalances:[0,0,0,0,0],postBalances:[0,0,0,0,0],
      preTokenBalances:[bal(2,A,400000000),bal(3,B,0)],
      postTokenBalances:[bal(2,A,0),bal(3,B,400000000)],
      innerInstructions:[],logMessages:[],
    },
  });
  db.prepare('INSERT INTO wallet_trades(sig,wallet,mint,side,sol,t) VALUES (?,?,?,?,?,?)')
    .run('receiver-sells',B,M,'sell',1,1700000080000);
  db.close();
}

test('PR24 AI workflow calls PR23 offline evidence for one Mint; full SQLite remains unchanged',async()=>{
  const root=fs.mkdtempSync(path.join(os.tmpdir(),'blix-ai-economic-'));
  const file=path.join(root,'archive.sqlite');
  try {
    seededArchive(file);
    const before=hash(file);
    const seen=[];
    const model=async ({stage,permittedCapabilities,evidence})=>{
      if(stage==='plan'){
        assert.deepEqual(permittedCapabilities.map(x=>x.id),['mint-facts','mint-economic-evidence']);
        return {calls:[
          {capability:'mint-facts',input:{mint:M}},
          {capability:'mint-economic-evidence',input:{mint:M}},
        ]};
      }
      seen.push(...evidence.map(x=>x.capability));
      assert.equal(evidence[1].result.facts.recipients[0].toOwner,B);
      return {summary:'Local transfer A to B and later sell summary; common control unknown',
        hypotheses:['B may have sold after receiving tokens'],
        alternativeExplanations:['B may have sold previously held inventory'],
        nextChecks:['Verify full wallet history and pool classification']};
    };
    const result=await runAiResearchTask({
      goal,model,now:()=>Date.parse('2026-11-12T00:00:00Z'),
      read:async (url)=>url.includes('/token/')
        ? {ok:true,status:200,data:{token:{mint:M,name:'Fixture'}}}
        : {ok:true,status:200,data:{holders:2,partial:true,top:[]}},
      readEconomic:makeOfflineEconomicReader({databasePath:file}),
    });
    assert.deepEqual(seen,['mint-facts','mint-economic-evidence']);
    assert.equal(result.status,'DRAFT_WITH_INCOMPLETE_EVIDENCE');
    assert.equal(result.evidence[1].result.facts.recipients[0].observedSells[0].sig,'receiver-sells');
    assert.equal(result.evidence[1].result.facts.recipients[0].sellObservation,'LOCAL_SELL_SUMMARY_OBSERVED');
    assert.equal(result.evidence[1].result.evidenceLevel,'CAPTURED_LOCAL_ARCHIVE_NOT_FULL_CHAIN_VERIFIED');
    assert.equal(result.assessment.evidenceLevel,'UNVERIFIED_MODEL_INTERPRETATION');
    assert.ok(result.unknowns.some(x=>/history is not complete/.test(x)));
    assert.equal(hash(file),before,'AI economic tool must not modify existing archive');
  } finally {fs.rmSync(root,{recursive:true,force:true});}
});

test('invalid AI plans never call trading, wrong Mint, duplicate, arbitrary URL or over-budget tool',async()=>{
  let executed=0;
  const read=async()=>{executed++;throw Error('not allowed');};
  const readEconomic=async()=>{executed++;throw Error('not allowed');};
  const proposals=[
    {calls:[{capability:'buy-live',input:{mint:M}}]},
    {calls:[{capability:'mint-economic-evidence',input:{mint:'So11111111111111111111111111111111111111112'}}]},
    {calls:[{capability:'mint-economic-evidence',input:{mint:M}},{capability:'mint-economic-evidence',input:{mint:M}}]},
    {calls:[{capability:'mint-economic-evidence',input:{mint:M}},{capability:'mint-facts',input:{mint:M}},{capability:'mint-facts',input:{mint:M}}]},
    {calls:[{capability:'http-get',input:{url:'https://example.test/private',mint:M}}]},
  ];
  for(const proposal of proposals){
    await assert.rejects(()=>runAiResearchTask({
      goal,read,readEconomic,model:async()=>proposal,
    }),/UNAUTHORIZED_TOOL|MINT_NOT_PRESENT|DUPLICATE_TOOL_REQUEST|MODEL_TOOL_BUDGET/);
  }
  assert.equal(executed,0);
});

test('missing archived database is a tool error, not a claim of no transfers; no file created',async()=>{
  const root=fs.mkdtempSync(path.join(os.tmpdir(),'blix-ai-no-econ-'));
  const file=path.join(root,'missing.sqlite');
  try {
    const result=await runAiResearchTask({
      goal,readEconomic:makeOfflineEconomicReader({databasePath:file}),
      model:async ({stage})=>stage==='plan'
        ? {calls:[{capability:'mint-economic-evidence',input:{mint:M}}]}
        : {summary:'Evidence unavailable',hypotheses:[],alternativeExplanations:[],nextChecks:[]},
    });
    assert.equal(result.status,'DRAFT_WITH_INCOMPLETE_EVIDENCE');
    assert.equal(result.evidence[0].result,undefined);
    assert.ok(result.evidence[0].error);
    assert.equal(result.assessment.evidenceLevel,'UNVERIFIED_MODEL_INTERPRETATION');
    assert.equal(fs.existsSync(file),false);
  } finally {fs.rmSync(root,{recursive:true,force:true});}
});
