import test from 'node:test';
import assert from 'node:assert/strict';
import { FINDINGS, inspectSource, gateDecision } from '../scripts/read-only-audit.mjs';

test('Blix audit detects the real research-branch hazards without importing the server', () => {
  const findings = inspectSource();
  assert.equal(findings.length, FINDINGS.length);
  for (const id of ['WALLET_ACTIONS', 'HOSTED_SWAP', 'AUTO_CLAIM', 'AI_AUTOMATION', 'GROK_ENABLED', 'DESK_AUTOMATION', 'STARTUP_EXTERNAL_CALL']) {
    assert.equal(findings.find((x) => x.id === id)?.present, true, id + ' should remain a blocker until fixed');
  }
  const decision = gateDecision(findings);
  assert.equal(decision.allowed, false);
  assert.ok(decision.blockerCount >= 7);
});

test('unreadable source fails closed', () => {
  const findings = inspectSource('/nonexistent', () => { throw new Error('unavailable'); });
  assert.equal(findings.every((x) => x.present), true);
  assert.equal(gateDecision(findings).allowed, false);
});

test('acknowledgement cannot be mistaken for read-only certification', () => {
  const findings = [{ id: 'WALLET', severity: 'blocker', present: true }];
  assert.equal(gateDecision(findings).allowed, false);
  assert.equal(gateDecision(findings, true).allowed, true);
});
