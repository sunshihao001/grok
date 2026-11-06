import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

const state = JSON.parse(readFileSync(new URL('../docs/project/state.json', import.meta.url), 'utf8'));
test('goal graph has unique, resolvable nodes', () => {
  const ids = new Set(state.goals.map(g => g.id));
  assert.equal(ids.size, state.goals.length);
  for (const [a,b,relation] of state.links) {
    assert.ok(ids.has(a) && ids.has(b), 'dangling goal relation');
    assert.ok(relation);
  }
  for (const item of state.next) assert.ok(ids.has(item.goal_id));
});
test('user decision is distinguished from production verification', () => {
  assert.equal(state.branch,'blix');
  assert.equal(state.decision.status,'USER_CONFIRMED');
  assert.equal(state.decision.live_state,'NOT_VERIFIED');
  assert.ok(state.next.every(t => t.status === 'NOT_RUN'));
});
test('both independent AI and historical market references remain', () => {
  assert.ok(state.sources.some(s=>s.id==='AI-D' && s.evidence==='DRAFT_RESEARCH'));
  assert.ok(state.sources.some(s=>s.id==='GROK-KNOWLEDGE'));
});
