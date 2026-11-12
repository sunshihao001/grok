// Explicitly configured offline reader for PR23's existing bounded SQLite report.
// Importing this file starts no server or provider; no model can set the database path.
import { execFile } from 'node:child_process';
import { promisify } from 'node:util';
import { stat } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';

const execFileAsync = promisify(execFile);
const SCRIPT = fileURLToPath(new URL('../../scripts/inspect-economic-mint.mjs', import.meta.url));
const MINT = /^[1-9A-HJ-NP-Za-km-z]{32,44}$/;

export function makeOfflineEconomicReader({ databasePath, timeoutMs = 20000 } = {}) {
  if (typeof databasePath !== 'string' || !databasePath.trim()) {
    throw new Error('EXISTING_DATABASE_PATH_REQUIRED');
  }
  if (!Number.isInteger(timeoutMs) || timeoutMs < 1000 || timeoutMs > 60000) {
    throw new Error('INVALID_OFFLINE_READER_TIMEOUT');
  }
  return async ({ mint } = {}) => {
    if (!MINT.test(String(mint || ''))) throw new Error('INVALID_OFFLINE_READER_MINT');
    const info = await stat(databasePath);
    if (!info.isFile()) throw new Error('EXISTING_DATABASE_FILE_REQUIRED');
    // No shell. The existing CLI opens only an existing SQLite file with
    // readOnly and query_only; scope is fixed to one Mint and 24 hours.
    const result = await execFileAsync(process.execPath,
      ['--no-warnings', SCRIPT, '--db', databasePath, '--mint', mint, '--hours', '24'],
      { encoding: 'utf8', timeout: timeoutMs, maxBuffer: 4 * 1024 * 1024, windowsHide: true });
    return JSON.parse(result.stdout);
  };
}
