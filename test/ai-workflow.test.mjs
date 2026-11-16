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
