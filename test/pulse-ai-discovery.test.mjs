import test from 'node:test';
import assert from 'node:assert/strict';
import { once } from 'node:events';
import { validatePulseDiscoveryInput, discoverPulseInvestigation }
  from '../server/intelligence/pulse-discovery.mjs';
import { makeChatCompletionModel } from '../server/intelligence/chat-completion-model.mjs';
import { createResearchHttpServer } from '../server/intelligence/research-http.mjs';

const mintA='EYqygbhZjP7EbM4fSn8devctnksAvPAD1Bt57XBFpump';
const mintB='GTNHLKQWKZHaHpd6PjfMgfFZUDEuCviwXMwYbCcepump';
const notCandidate='4p7SeR6361WJ4T4icgsYTnzAUzfA5NwM4CwYD9kMBjuK';
const observedAt=Date.parse('2026-11-13T08:00:00Z');
const input={
  goal:'自动寻找值得进一步调查的市场候选，考虑流动性、资金和异常钱包',
  browserRecordedAtMs:observedAt,
  boardStatus:'BLIX_PULSE_LIVE_OR_POLLING',
  candidates:[
    {mint:mintA,stage:'new',symbol:'ALPHA',liq:20000,mcap:100000,vol:80000,buys:23,sells:14,traders:18,chg1m:3},
    {mint:mintB,stage:'migrated',symbol:'BETA',liq:2000,mcap:100000,vol:30000,buys:8,sells:17,traders:9,chg1m:-12},
  ],
};
function archived(mint) {
  return { mode:'OFFLINE_READ_ONLY_SQLITE_MINT_REPORT',input:{mint},
    evidence:{indexedCoverage:'ONLY_CAPTURED_RPC_TX_AND_RESOLVED_TOKEN_ACCOUNT_OWNERS',
      senderDiscovery:{selectedSenders:1,truncated:false}},
    recipients:[{mint,signature:'real-archive-digest-not-claimed',outerI:0,innerI:0,
      fromOwner:'A',toOwner:'B',amountRaw:'200',blockTime:1731484800,slot:4}],
  };
}
async function start(t,options) {
  const server=createResearchHttpServer(options);
  server.listen(0,'127.0.0.1');
  await once(server,'listening');
  t.after(()=>new Promise((resolve,reject)=>server.close(err=>err?reject(err):resolve())));
  return 'http://127.0.0.1:'+server.address().port;
}
const post=(base,body)=>fetch(base+'/discover',{method:'POST',
  headers:{Origin:'http://localhost:4420','Content-Type':'application/json'},
  body:JSON.stringify(body),
});

test('Pulse input strictly bounds candidates and preserves unavailable market fields as UNKNOWN',()=>{
  const clean=validatePulseDiscoveryInput(input,observedAt);
  assert.equal(clean.candidates.length,2);
  assert.equal(clean.source,'USER_BROWSER_BLIX_PULSE_SNAPSHOT_UNVERIFIED');
  assert.equal(clean.marketCoverage,'ONLY_SUBMITTED_BLIX_CANDIDATES_NOT_ALL_SOLANA');
  assert.equal(clean.candidates[0].liq,20000);
  const unknown=validatePulseDiscoveryInput({...input,
    candidates:[{mint:mintA,stage:'new',mcap:-1,liq:Infinity,vol:1e20}]},observedAt);
  assert.equal(unknown.candidates[0].liq,null);
  assert.equal(unknown.candidates[0].mcap,null);
  assert.equal(unknown.candidates[0].vol,null);
  assert.throws(()=>validatePulseDiscoveryInput({...input,browserRecordedAtMs:observedAt-31_000},observedAt),
    /STALE/);
  assert.throws(()=>validatePulseDiscoveryInput({...input,boardStatus:'RESTORED_FROM_BROWSER_CACHE'},observedAt),
    /STALE/);
  assert.throws(()=>validatePulseDiscoveryInput({...input,candidates:[...input.candidates,input.candidates[0]]},observedAt),
    /CANDIDATE_INVALID/);
  assert.throws(()=>validatePulseDiscoveryInput({...input,candidates:Array(13).fill(input.candidates[0])},observedAt),
    /STALE/);
  assert.throws(()=>validatePulseDiscoveryInput({...input,candidates:[
    {mint:mintA,stage:'new',url:'https://attacker.example'}]},observedAt),/CANDIDATE_INVALID/);
});

test('AI discovers only from a submitted market shortlist, then uses the existing Mint-scoped readonly workflow',async()=>{
  const calls=[],research=[];
  const result=await discoverPulseInvestigation({
    input,now:()=>observedAt,
    model:async args=>{
      calls.push(args.stage);
      assert.equal(args.stage,'discover');
      assert.equal(args.candidates.length,2);
      assert.equal(args.marketSource.marketCoverage,'ONLY_SUBMITTED_BLIX_CANDIDATES_NOT_ALL_SOLANA');
      return {mint:mintB,reason:'BETA shows an unusual price/volume combination; examine wallet evidence first.'};
    },
    readEconomic:async()=>archived(mintB),
    loadKnowledge:async()=>[],
    runResearch:async args=>{research.push(args);return {
      status:'DRAFT_WITH_INCOMPLETE_EVIDENCE',evidence:[],knowledgeUse:[],calls:[],assessment:null,unknowns:[],
    };},
  });
  assert.equal(result.status,'INVESTIGATION_DRAFT_ONLY');
  assert.equal(result.discovery.selectedMint,mintB);
  assert.equal(result.investigation.status,'DRAFT_WITH_INCOMPLETE_EVIDENCE');
  assert.equal(result.discovery.modelSelectionVerified,false);
  assert.equal(result.verifiedMarketOpportunity,false);
  assert.deepEqual(calls,['discover']);
  assert.equal(research.length,1);
  assert.equal(research[0].mint,mintB);
});

test('model may decline an unhelpful shortlist without falsely claiming a trade opportunity',async()=>{
  let investigated=0;
  const result=await discoverPulseInvestigation({
    input,now:()=>observedAt,
    model:async()=>({mint:null,reason:'None has enough evidence to justify investigation.'}),
    readEconomic:async()=>{},runResearch:async()=>{investigated++;},
  });
  assert.equal(investigated,0);
  assert.equal(result.status,'NO_INVESTIGATION_CANDIDATE_SELECTED');
  assert.equal(result.discovery.selectedMint,null);
});

test('unapproved Mint from model never triggers economic data reads or a second model stage',async()=>{
  let investigated=0;
  await assert.rejects(()=>discoverPulseInvestigation({
    input,now:()=>observedAt,
    model:async()=>({mint:notCandidate,reason:'I want another token'}),
    readEconomic:async()=>{},runResearch:async()=>{investigated++;},
  }),/DISCOVERY_MODEL_MINT_NOT_IN_SHORTLIST/);
  assert.equal(investigated,0);
});

test('Chat Completions discover stage sends only the limited shortlist',async()=>{
  let count=0;
  const model=makeChatCompletionModel({model:'mock',apiKey:'test-only',transport:async(url,init)=>{
    count++;
    const sent=JSON.parse(init.body),text=sent.messages[1].content;
    assert.match(text,/ALPHA/);
    assert.match(text,/ONLY_SUBMITTED_BLIX/);
    assert.doesNotMatch(text,/test-only/);
    return new Response(JSON.stringify({choices:[{message:{
      content:JSON.stringify({mint:mintA,reason:'Investigate the selected observed Mint'}),
    },finish_reason:'stop'}]}),{status:200});
  }});
  const answer=await model({stage:'discover',goal:input.goal,candidates:input.candidates,
    marketSource:{marketCoverage:'ONLY_SUBMITTED_BLIX_CANDIDATES_NOT_ALL_SOLANA'}});
  assert.equal(answer.mint,mintA);
  assert.equal(count,1);
});

test('loopback /discover route runs validated selection plus one bounded local archive investigation',async t=>{
  const stages=[],mints=[];
  const base=await start(t,{allowedOrigins:['http://localhost:4420'],maxTasks:1,
    model:async ({stage,candidates})=>{
      stages.push(stage);
      if(stage==='discover'){assert.equal(candidates.length,2);
        return {mint:mintA,reason:'Interesting observed market activity for investigation'};}
      if(stage==='plan')return {calls:[{capability:'mint-economic-evidence',input:{mint:mintA}}]};
      return {summary:'Partial local economic evidence, followability unknown',
        hypotheses:['Possible wallet linkage'],alternativeExplanations:['Pool service'],
        nextChecks:['Fetch missing historical coverage']};
    },
    readEconomic:async ({mint})=>{mints.push(mint);return archived(mint);},
    loadKnowledge:async()=>[{source:'Hermes@sha256:known',topic:'wallet-roles',excerpt:'Owner is not identity'}],
  });
  const response=await post(base,{...input,browserRecordedAtMs:Date.now()});
  assert.equal(response.status,200);
  const body=await response.json();
  assert.equal(body.discovery.selectedMint,mintA);
  assert.equal(body.investigation.evidence[0].capability,'mint-economic-evidence');
  assert.equal(body.investigation.evidence[0].result.facts.network.eventCount,1);
  assert.ok(body.investigation.knowledgeUse.some(x=>x.source==='Hermes@sha256:known'));
  assert.deepEqual(stages,['discover','plan','interpret']);
  assert.deepEqual(mints,[mintA]);
  assert.equal(body.verifiedMarketOpportunity,false);
  assert.equal(body.liveExecutionValidated,false);
  assert.equal((await post(base,{...input,browserRecordedAtMs:Date.now()})).status,429);
});

test('invalid origin or stale Pulse snapshot does not consume model budget',async t=>{
  let calls=0;
  const base=await start(t,{allowedOrigins:['http://localhost:4420'],maxTasks:1,
    model:async()=>{calls++;return {mint:null,reason:'No candidates'};},
    readEconomic:async()=>archived(mintA)});
  let res=await fetch(base+'/discover',{method:'POST',headers:{
    Origin:'https://malicious-site.example','Content-Type':'application/json'},body:JSON.stringify({...input,browserRecordedAtMs:Date.now()})});
  assert.equal(res.status,403);
  res=await post(base,input);
  assert.equal(res.status,400);
  assert.equal(calls,0);
  assert.equal((await (await fetch(base+'/health')).json()).remainingTasks,1);
});
