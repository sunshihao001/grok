import test from 'node:test';
import assert from 'node:assert/strict';
import { runAiResearchTask } from '../server/intelligence/ai-workflow.mjs';

const mint = 'EYqygbhZjP7EbM4fSn8devctnksAvPAD1Bt57XBFpump';
const goal = `研究这个币有没有可疑钱包关系：${mint}`;
const capabilities = () => [
  { id: 'mint-facts', readonly: true },
  { id: 'buy-live', readonly: false },
];

const model = async ({ stage }) => stage === 'plan'
  ? { calls: [{ capability: 'mint-facts', input: { mint } }] }
  : { summary: '发现持仓标签，但不能确认控制关系', hypotheses: ['可能存在共同活动'], alternativeExplanations: ['公共服务'], nextChecks: ['核查签名与时间覆盖'] };

test('one natural-language goal -> allowed tool -> model hypothesis, preserving source unknowns', async () => {
  const invoked = [];
  const result = await runAiResearchTask({ goal, model, read: async () => {}, capabilities,
    execute: async (id, args) => { invoked.push({ id, mint: args.mint }); return { status: 'OBSERVED_UNVERIFIED', unknowns: ['History may be incomplete'], facts: { holders: 20 } }; },
    loadKnowledge: async () => [{ source: 'Hermes', excerpt: 'Shared funders may be services.' }],
    now: () => Date.parse('2026-11-09T00:00:00Z') });
  assert.equal(result.status, 'DRAFT_WITH_EVIDENCE');
  assert.deepEqual(invoked, [{ id: 'mint-facts', mint }]);
  assert.equal(result.assessment.evidenceLevel, 'UNVERIFIED_MODEL_INTERPRETATION');
  assert.deepEqual(result.unknowns, ['History may be incomplete']);
  assert.deepEqual(result.knowledgeSources, ['Hermes']);
});

test('model cannot authorize buy, new Mint, arbitrary URL, or duplicate calls', async () => {
  let executed = 0;
  for (const proposal of [
    { calls: [{ capability: 'buy-live', input: { mint } }] },
    { calls: [{ capability: 'mint-facts', input: { mint: 'So11111111111111111111111111111111111111112' } }] },
    { calls: [{ capability: 'mint-facts', input: { mint } }, { capability: 'buy-live', input: {} }] },
    { calls: [{ capability: 'mint-facts', input: { mint } }, { capability: 'mint-facts', input: { mint } }] },
  ]) {
    await assert.rejects(() => runAiResearchTask({ goal, capabilities,
      model: async () => proposal, read: async () => {}, execute: async () => { executed++; } }),
      /UNAUTHORIZED_TOOL|MINT_NOT_PRESENT|DUPLICATE_TOOL_REQUEST/);
  }
  assert.equal(executed, 0);
});

test('no model and no Mint require no read or trade side effects', async () => {
  let count = 0;
  const execute = () => { count++; };
  assert.equal((await runAiResearchTask({ goal, execute })).status, 'MODEL_NOT_CONFIGURED');
  assert.equal((await runAiResearchTask({ goal: '今天的市场情况', model, capabilities, execute })).status, 'NEEDS_SINGLE_MINT');
  assert.equal(count, 0);
});

test('model failures and missing evidence do not yield verified findings', async () => {
  const result = await runAiResearchTask({ goal, model, read: async () => {}, capabilities,
    execute: async () => ({ status: 'UNAVAILABLE', unknowns: ['No usable snapshot'] }) });
  assert.equal(result.status, 'DRAFT_WITH_INCOMPLETE_EVIDENCE');
  assert.ok(result.unknowns.includes('No usable snapshot'));
  const failed = await runAiResearchTask({ goal, model: async ({ stage }) => stage === 'plan'
    ? { calls: [{ capability: 'mint-facts', input: { mint } }] } : null, read: async () => {}, capabilities,
    execute: async () => ({ status: 'OBSERVED_UNVERIFIED' }) });
  assert.equal(failed.status, 'MODEL_INTERPRET_FAILED');
  assert.equal(failed.assessment, null);
});

test('integration with existing mint-facts registry: exactly two pre-existing GET paths', async () => {
  const requested = [];
  const result = await runAiResearchTask({ goal, model, read: async (path) => {
    requested.push(path);
    return path.includes('/token/')
      ? { ok: true, status: 200, data: { token: { mint, name: 'Synthetic Mint' } } }
      : { ok: true, status: 200, data: { holders: 3, partial: true, top: [{ wallet: 'A', pct: 20, tag: 'bundle' }] } };
  } });
  assert.equal(result.status, 'DRAFT_WITH_INCOMPLETE_EVIDENCE');
  assert.deepEqual(requested, ['/api/token/' + mint, '/api/holders/' + mint + '?top=25']);
  assert.equal(result.evidence[0].result.facts.token.name, 'Synthetic Mint');
  assert.equal(result.evidence[0].result.facts.holderLedger.top[0].sourceTag, 'bundle');
  assert.ok(result.unknowns.some((x) => /missing or unverified coverage/i.test(x)));
});


test('Coin-selected Mint is explicit scope even when a question mentions another wallet address', async () => {
  const wallet = '4p7SeR6361WJ4T4icgsYTnzAUzfA5NwM4CwYD9kMBjuK';
  const complexGoal = '调查Mint ' + mint + ' 中钱包 ' + wallet + ' 的转移历史';
  const requested = [];
  const boundModel = async ({stage,mints}) => {
    if (stage === 'plan') {
      assert.deepEqual(mints, [mint], 'selected Coin Mint controls the tool scope');
      return {calls:[{capability:'mint-facts',input:{mint}}]};
    }
    return {summary:'Source data observed only',hypotheses:[],alternativeExplanations:[],nextChecks:[]};
  };
  const result = await runAiResearchTask({
    goal:complexGoal,mint,model:boundModel,capabilities,
    read:async()=>{},execute:async (id,args)=>{
      requested.push([id,args.mint]);return {status:'OBSERVED_UNVERIFIED',unknowns:[]};
    },
  });
  assert.equal(result.status,'DRAFT_WITH_EVIDENCE');
  assert.deepEqual(requested,[['mint-facts',mint]]);
  assert.equal((await runAiResearchTask({goal:complexGoal,model:boundModel,capabilities,read:async()=>{}})).status,
    'NEEDS_SINGLE_MINT','unscoped multi-address goal cannot guess which address is Mint');
});

test('model cannot promote a mentioned wallet address into an authorized Mint', async () => {
  const wallet = '4p7SeR6361WJ4T4icgsYTnzAUzfA5NwM4CwYD9kMBjuK';
  let calls = 0;
  await assert.rejects(() => runAiResearchTask({
    goal:'调查 ' + mint + ' 与 ' + wallet + ' 的资金流',mint,
    model:async()=>({calls:[{capability:'mint-facts',input:{mint:wallet}}]}),
    capabilities,read:async()=>{calls++;},execute:async()=>{calls++;},
  }),/MINT_NOT_PRESENT_IN_USER_GOAL/);
  assert.equal(calls,0);
});


test('Coin assistant long contextual task is accepted, but unbounded task is rejected', async () => {
  // The textarea can contain 1600 characters, plus the displayed source context.
  const longGoal = goal + '\n' + ('研究持仓来源、Token转仓与经济控制权竞争解释。'.repeat(90));
  assert.ok(longGoal.length > 2000 && longGoal.length < 4096);
  const result = await runAiResearchTask({
    goal:longGoal,model,capabilities,read:async()=>{},execute:async()=>({
      status:'OBSERVED_UNVERIFIED',unknowns:['Source coverage requires verification'],
    }),
  });
  assert.equal(result.status,'DRAFT_WITH_EVIDENCE');
  assert.ok(result.unknowns.includes('Source coverage requires verification'));
  await assert.rejects(
    () => runAiResearchTask({goal:goal + 'a'.repeat(4096),model,capabilities,read:async()=>{}}),
    /INVALID_RESEARCH_GOAL/
  );
});
