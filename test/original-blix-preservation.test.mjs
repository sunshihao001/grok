// Original Blix product preservation gate.
// This detects missing upstream files and unreviewed modifications to 28
// representative core surfaces. It is NOT a functional trading/safety test.
import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { createHash } from 'node:crypto';
import { fileURLToPath } from 'node:url';
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const baseline = JSON.parse(fs.readFileSync(path.join(root,'test/fixtures/blix-import-baseline.json'),'utf8'));
const fileAt = p => path.join(root,p);
const gitBlobSha = bytes => createHash('sha1')
  .update(`blob ${bytes.length}\0`).update(bytes).digest('hex');

test('all 767 paths from imported full Blix snapshot remain present', () => {
  assert.equal(baseline.imported_snapshot_commit,
    'e2c69d42dcdae7690f9d47e0d0e7e8257ed48326');
  assert.equal(baseline.full_original_file_paths.length,767);
  const missing = baseline.full_original_file_paths.filter(p => {
    try { return !fs.statSync(fileAt(p)).isFile(); } catch { return true; }
  });
  assert.deepEqual(missing, [], 'Original product files must not disappear silently');
});

test('28 selected original UI, market, accounts, trading, AI and deployment modules remain byte-identical', () => {
  const critical = Object.entries(baseline.protected_unchanged_core_blob_shas);
  assert.equal(critical.length,28);
  for(const [p,expected] of critical) {
    const bytes = fs.readFileSync(fileAt(p));
    assert.equal(gitBlobSha(bytes),expected,
      `${p} changed from imported original; review legacy behavior and update preservation manifest only with a documented regression check`);
  }
});

test('core modules intentionally extended by this branch remain present and retain original regression scripts', () => {
  const changed = Object.entries(baseline.reviewed_modified_original_modules);
  assert.ok(changed.length>=7);
  for(const [p,reason] of changed) {
    assert.equal(fs.statSync(fileAt(p)).isFile(),true,p);
    assert.ok(reason.length>=30, `Document why ${p} changed`);
  }
  const pkg=JSON.parse(fs.readFileSync(fileAt('package.json'),'utf8'));
  for(const script of ['start','test','test:security','test:metrics','test:browser','test:charts','test:pulse-order','test:trade-status']) {
    assert.equal(typeof pkg.scripts[script], 'string',`Original Blix script ${script} must remain available`);
  }
  assert.match(fs.readFileSync(fileAt('server/server.js'),'utf8'),/\/api\/discover/);
  assert.match(fs.readFileSync(fileAt('server/server.js'),'utf8'),/\/api\/wtrack/);
  assert.match(fs.readFileSync(fileAt('server/server.js'),'utf8'),/evidenceTx\s*=\s*p\.match/);
  // Preserving trading code does not authorize loading or invoking it.
});


test('Coin AI assistant is additive: original AI read, safety and trading entry remain', () => {
  const tabs = fs.readFileSync(fileAt('web/src/pages/coin/Tabs.tsx'), 'utf8');
  const assistant = fs.readFileSync(fileAt('web/src/pages/coin/AiCopilot.tsx'), 'utf8');
  assert.match(tabs, /\["ai", "AI read"\]/);
  assert.match(tabs, /\["safety", "Safety"\]/);
  assert.match(tabs, /\["copilot", "AI assistant"\]/);
  assert.match(tabs, /tab === "ai" && <AiGate><AiView/);
  assert.match(tabs, /tab === "copilot" && <AiGate>/);
  assert.match(tabs, /onRead=\{onPaper\}/);
  assert.match(assistant, /Preview · agent not connected/);
  assert.match(assistant, /Copy research task/);
  assert.match(assistant, /read-only, no trading/);
  assert.doesNotMatch(assistant, /fetch\s*\(/);
});


test('AI visual workspace is additive and keeps original market, chart and trading entry points', () => {
  const main = fs.readFileSync(fileAt('web/src/main.tsx'), 'utf8');
  const rail = fs.readFileSync(fileAt('web/src/shell/Rail.tsx'), 'utf8');
  const workspace = fs.readFileSync(fileAt('web/src/pages/Intelligence.tsx'), 'utf8');
  const tabs = fs.readFileSync(fileAt('web/src/pages/coin/Tabs.tsx'), 'utf8');

  for (const entry of ['Pulse', 'Coins', 'Coin', 'AiPicks', 'Wallets', 'Tracker']) {
    assert.ok(main.includes('const ' + entry + ' = page('), 'Original route component retained: ' + entry);
  }
  for (const route of ['coins', 'feed', 'narratives', 'tracker', 'ai-picks', 'account']) {
    assert.ok(rail.includes('["' + route + '",'), 'Original navigation retained: ' + route);
  }
  assert.match(main, /const Intelligence = page\(/);
  assert.match(main, /intelligence: Intelligence/);
  assert.match(rail, /\["intelligence", "AI research"/);
  assert.match(workspace, /selectObservedCandidates\(/);
  assert.match(workspace, /usePulse\(s => s\.coins\)/);
  assert.match(workspace, /coinHref \+ "\/assistant"/);
  assert.match(tabs, /viaWorkspace \? "copilot"/);
  assert.match(workspace, /模型尚未连接/);
  assert.doesNotMatch(workspace, /\b(?:fetch|sendTransaction|signTransaction)\s*\(/);
  assert.doesNotMatch(workspace, /\b(?:POST|api\/buy|api\/sell)\b/);
});
