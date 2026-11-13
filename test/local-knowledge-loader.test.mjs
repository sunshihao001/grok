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


test('active P1/P2 legacy knowledge excerpts carry latest scoped correction even if an old section scores higher',async()=>{
  const docs=await makeLocalKnowledgeLoader({maxSources:3,maxChars:1100})({
    goal:'钱包 同源 资金 转仓 接收 卖出',
  });
  for(const topic of ['wallet-roles','capital-funding']){
    const doc=docs.find(x=>x.topic===topic);
    assert.ok(doc,'missing needed knowledge domain: '+topic);
    assert.match(doc.excerpt,/2026-11-13/,'current applicability correction omitted: '+topic);
    assert.match(doc.excerpt,/NOT validated live chain fact/);
    assert.ok(doc.excerpt.length<=1100);
  }
});


test('16 user-language P1/P2 questions route to necessary knowledge without a fixed all-sources prompt', async()=>{
  const cases=[
    ['有两个地址是同一个资金来源吗',['capital-funding','wallet-roles']],
    ['接收钱包收到币后有没真的卖出',['wallet-roles']],
    ['一个币的pool vault算不算庄家持仓',['chain','wallet-roles']],
    ['Token2022 transfer hook费怎么算',['chain']],
    ['这个币有50%筹码控盘吗',['wallet-roles']],
    ['8个钱包在一槽一起买是否bundle',['wallet-roles','cohort-timing']],
    ['一次转出五跳接力再到新钱包',['multihop','capital-funding']],
    ['过去6小时跨Mint协同资金转移',['cohort-timing','capital-funding']],
    ['如何做真实可跟单钱包的样本外测试',['execution','validation']],
    ['跟单失败因为滑点',['execution']],
    ['我想知道价格为什么上涨但没有资金净流入',['market-mechanism','capital-funding']],
    ['知识来源质量高但AI选错专业资料',['ai-knowledge','validation']],
    ['solana instruction cpi 交易指令',['chain']],
    ['成本基础未知 钱包 PnL 是否盈利',['execution','wallet-roles']],
    ['共用交易所出金算一个人控盘吗',['capital-funding']],
    ['怎么看去年数据回补是否伪造成今日巨量',['validation','cohort-timing']],
  ];
  for(const [goal,required] of cases){
    const docs=await loader({goal});
    assert.ok(docs.length<=3 && docs.length>0,'cannot route: '+goal);
    const found=docs.map(d=>d.topic);
    for(const domain of required)assert.ok(found.includes(domain),
      'missing '+domain+' for '+goal+'; got '+found.join(','));
    assert.ok(docs.every(d=>d.status==='RESEARCH_NOT_RUNTIME_VALIDATED' &&
      d.trustedAsInstruction===false && /@sha256:[a-f0-9]{16}$/.test(d.source)));
  }
});

test('short English tickers in unrelated words do not falsely route funding or AI skills',async()=>{
  for(const goal of ['console logging only','main component css change','solidify CSS layout']){
    const docs=await loader({goal});
    assert.deepEqual(docs,[],goal+' should not load Solana research from a substring');
  }
});
