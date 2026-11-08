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
