import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const ROOT = fileURLToPath(new URL('../', import.meta.url));

test('fresh SQLite cold import can read pictures before optional Fomo modules create their tables', () => {
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'blix-people-cold-'));
  const data = path.join(tmp, 'data');
  try {
    const script = [
      "import assert from 'node:assert/strict';",
      "import { knownPic, notePic } from './server/people.js';",
      "import { db } from './server/db.js';",
      "assert.equal(db.prepare(\"SELECT name FROM sqlite_master WHERE name='fomo_traders'\").get(), undefined);",
      "assert.equal(knownPic('missing'), null);",
      "notePic('owner', 'https://example.invalid/owner.png');",
      "assert.equal(knownPic('owner'), 'https://example.invalid/owner.png');",
      "db.exec('CREATE TABLE fomo_traders (handle TEXT PRIMARY KEY, avatar TEXT)');",
      "db.prepare('INSERT INTO fomo_traders (handle, avatar) VALUES (?, ?)').run('later', 'https://example.invalid/later.png');",
      "assert.equal(knownPic('later'), 'https://example.invalid/later.png');",
      "console.log('BLIX_COLD_START_OPTIONAL_FOMO_TABLES_OK');",
    ].join('\n');
    const env = { ...process.env, RADAR_DATA: data };
    delete env.BLIX_APPROVED_LEGACY_RUNTIME;
    delete env.NODE_OPTIONS;
    const child = spawnSync(process.execPath, ['--input-type=module', '-e', script], {
      cwd: ROOT, env, encoding: 'utf8', timeout: 12000, windowsHide: true,
    });
    assert.equal(child.status, 0, child.stderr || String(child.error?.message || ''));
    assert.match(child.stdout, /BLIX_COLD_START_OPTIONAL_FOMO_TABLES_OK/);
    assert.equal(fs.existsSync(path.join(data, 'radar.db')), true);
  } finally {
    fs.rmSync(tmp, { recursive: true, force: true });
  }
});
