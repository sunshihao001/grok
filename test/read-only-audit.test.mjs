import test from 'node:test';
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { mkdtempSync, existsSync, rmSync, readFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
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

test('npm start fails closed before importing the trading-capable server or creating a database', () => {
  const root = dirname(fileURLToPath(new URL('../package.json', import.meta.url)));
  const script = JSON.parse(readFileSync(new URL('../package.json', import.meta.url), 'utf8')).scripts.start;
  assert.equal(script, 'node scripts/read-only-audit.mjs --gate && node --no-warnings server/server.js');
  const dir = mkdtempSync(join(tmpdir(), 'blix-safe-start-gate-'));
  const data = join(dir, 'not-created-radar-data');
  try {
    const env = { ...process.env, RADAR_DATA: data, npm_config_cache: join(dir, 'npm-cache') };
    delete env.BLIX_APPROVED_LEGACY_RUNTIME;
    delete env.NODE_OPTIONS;
    const cmd = process.platform === 'win32' ? 'npm.cmd' : 'npm';
    const child = spawnSync(cmd, ['run', '--silent', 'start'], {
      cwd: root, env, timeout: 15000, encoding: 'utf8', windowsHide: true,
    });
    assert.equal(child.error, undefined, String(child.error?.message || ''));
    assert.equal(child.status, 2, 'the guard must stop npm start before importing server.js');
    assert.match(child.stdout, /"readOnlyCertified": false/);
    assert.match(child.stderr, /startup blocked/);
    assert.equal(existsSync(data), false, 'no main Blix SQLite/database startup side effects');
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});
