// Explicitly configured offline reader for PR23's existing bounded SQLite report.
// Importing this file starts no server or provider; no model can set the database path.
import { execFile } from 'node:child_process';
import { promisify } from 'node:util';
import { stat } from 'node:fs/promises';
import { DatabaseSync } from 'node:sqlite';
import { fileURLToPath } from 'node:url';

const execFileAsync = promisify(execFile);
const SCRIPT = fileURLToPath(new URL('../../scripts/inspect-economic-mint.mjs', import.meta.url));
const MINT = /^[1-9A-HJ-NP-Za-km-z]{32,44}$/;


/**
 * Startup/health preflight for the EXISTING archive, never a Mint coverage claim.
 * No network access, SQLite creation, schema migration or model call.
 */
export async function probeExistingEconomicArchive({ databasePath } = {}) {
  if (typeof databasePath !== 'string' || !databasePath.trim())
    return { ready: false, status: 'ARCHIVE_PATH_NOT_CONFIGURED' };
  try {
    const info = await stat(databasePath);
    if (!info.isFile()) return { ready: false, status: 'EXISTING_ARCHIVE_NOT_A_FILE' };
  } catch { return { ready: false, status: 'EXISTING_ARCHIVE_NOT_FOUND' }; }
  let db;
  try {
    db = new DatabaseSync(databasePath, { readOnly: true });
    db.exec('PRAGMA query_only=ON');
    const required = {
      econ_transactions: ['sig', 'rpc_json', 'sha256', 'status', 'capture_source', 'commitment', 'observed_at'],
      econ_instructions: ['sig', 'kind', 'mint', 'from_owner', 'to_owner', 'owner_conflict', 'amount_raw'],
      wallet_trades: ['sig', 'wallet', 'mint', 'side', 't'],
    };
    for (const [table, columns] of Object.entries(required)) {
      const exists = db.prepare("SELECT 1 FROM sqlite_master WHERE type='table' AND name=?").get(table);
      if (!exists) return { ready: false, status: 'ECONOMIC_ARCHIVE_SCHEMA_UNAVAILABLE' };
      const names = new Set(db.prepare('PRAGMA table_info(' + table + ')').all().map(row => row.name));
      if (columns.some(name => !names.has(name)))
        return { ready: false, status: 'ECONOMIC_ARCHIVE_SCHEMA_UNAVAILABLE' };
    }
    return {
      ready: true, status: 'EXISTING_ARCHIVE_SCHEMA_READABLE',
      coverage: 'SCHEMA_ONLY_MINT_CONTENT_AND_HISTORY_NOT_VERIFIED',
    };
  } catch { return { ready: false, status: 'EXISTING_ARCHIVE_NOT_READABLE' }; }
  finally { try { db?.close(); } catch { /* already read-only; do not mask status */ } }
}

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
