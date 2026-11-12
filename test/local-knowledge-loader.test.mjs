import test from 'node:test';
import assert from 'node:assert/strict';
import { makeLocalKnowledgeLoader } from '../server/intelligence/local-knowledge-loader.mjs';
import { runAiResearchTask } from '../server/intelligence/ai-workflow.mjs';

const mint='GTNHLKQWKZHaHpd6PjfMgfFZUDEuCviwXMwYbCcepump';
const loader=makeLocalKnowledgeLoader({maxSources:3,maxChars:900});

test('specialized wallet/transfer questions retrieve limited existing professional knowledge with provenance',async()=>{
  const docs=await loader({goal:'调查资金同源钱包与token转仓接收后卖出，竞争解释'});
  assert.ok(docs.length>=2 && docs.length<=3);
  assert.ok(docs.some(x=>x.topic==='wallet-roles'));
  assert.ok(docs.some(x=>x.topic==='capital-funding'));
  assert.ok(docs.every(x=>x.source.startsWith('LOCAL_PROJECT_RESEARCH:knowledge/')));
  assert.ok(docs.every(x=>x.status==='RESEARCH_NOT_RUNTIME_VALIDATED'));
  assert.ok(docs.every(x=>!x.trustedAsInstruction && x.excerpt.length<=900));
  assert.ok(docs.every(x=>x.excerpt.includes('NOT validated live chain fact')));
});

test('evidence gaps can request validation sources without inventing a source',async()=>{
  const docs=await loader({goal:'调查该 Mint',evidence:[{error:'missing archive'}]});
  assert.ok(docs.some(x=>x.topic==='validation'));
});

test('no source matches produces no forced full-database knowledge injection',async()=>{
  const docs=await loader({goal:'你好，查看一个短问题'});
  assert.deepEqual(docs,[]);
});

test('knowledge selection participates in existing AI interpretation without granting tool authority',async()=>{
  let interpreted=false;
  const goal='调查该 Mint 的钱包资金来源与共同控制误判：'+mint;
  const output=await runAiResearchTask({
    goal,mint,read:async()=>{},loadKnowledge:loader,
    model:async({stage,knowledge})=>{
      if(stage==='plan')return {calls:[{capability:'mint-facts',input:{mint}}]};
      assert.ok(knowledge.length>0);
      assert.ok(knowledge.every(x=>x.trustedAsInstruction===false));
      interpreted=true;
      return {summary:'Wallet controller remains unverified',hypotheses:[],alternativeExplanations:['Shared service'],nextChecks:[]};
    },
    execute:async()=>({status:'PARTIAL',unknowns:['Wallet coverage incomplete']}),
  });
  assert.equal(interpreted,true);
  assert.ok(output.knowledgeSources.some(x=>x.includes('knowledge/')));
  assert.equal(output.assessment.evidenceLevel,'UNVERIFIED_MODEL_INTERPRETATION');
});

test('untrusted goal cannot specify an arbitrary file path or exceed knowledge limits',async()=>{
  assert.throws(()=>makeLocalKnowledgeLoader({maxSources:20}),/INVALID_LOCAL_KNOWLEDGE_LIMIT/);
  const docs=await loader({goal:'../../server/accounts.js /etc/passwd 秘密'});
  assert.deepEqual(docs,[]);
});
