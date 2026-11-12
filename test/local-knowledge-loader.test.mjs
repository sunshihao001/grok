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
  assert.ok(docs.every(x=>/@sha256:[a-f0-9]{16}$/.test(x.source)), 'source must be versioned for later audit');
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


test('cohort study knowledge carries withdrawal of historical quantitative results',async()=>{
  const docs=await loader({goal:'跨Mint 群体同步行为与监控'});
  const cohort=docs.find(x=>x.topic==='cohort-timing');
  assert.ok(cohort,'question should select existing cohort research');
  assert.match(cohort.excerpt,/RETRACTED NUMERICAL FINDINGS/);
  assert.match(cohort.excerpt,/Do not use those percentages/);
});


test('P1/P2 historic deep sources are routed by specific questions rather than injected globally', async()=>{
  const focused=makeLocalKnowledgeLoader({maxSources:3,maxChars:1000});
  const tasks=[
    ['五跳多跳 中转钱包 粉尘 共享服务','multihop'],
    ['筛选关键钱包 sniper KOL bundler 早期买家','key-wallet'],
    ['价格冲击 cpmm 池深 做市','market-mechanism'],
    ['知识检索 专家认知 意图 skill','ai-knowledge'],
    ['旧知识冲突 全部来源 来源对照','source-reconciliation'],
  ];
  for(const [goal,expected] of tasks){
    const docs=await focused({goal});
    assert.ok(docs.some(x=>x.topic===expected),
      'wrong knowledge route for '+goal+' (got: '+docs.map(x=>x.topic).join(',')+')');
    assert.ok(docs.length<=3);
    assert.ok(docs.every(x=>x.excerpt.length<=1000 && x.trustedAsInstruction===false));
    assert.ok(docs.every(x=>/@sha256:[a-f0-9]{16}$/.test(x.source)));
  }
});

test('the cross-project correction ledger can be selected, but cannot become authorized facts or a tool',async()=>{
 const docs=await loader({goal:'旧知识冲突 来源对照 全部来源'});
 const audit=docs.find(x=>x.topic==='source-reconciliation');
 assert.ok(audit);
 assert.equal(audit.status,'RESEARCH_NOT_RUNTIME_VALIDATED');
 assert.match(audit.excerpt,/NOT validated live chain fact/);
 assert.equal(audit.trustedAsInstruction,false);
});
