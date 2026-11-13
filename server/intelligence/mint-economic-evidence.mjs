// Bounded adapter over PR #23's existing local SQLite Mint report.
// Importing this module never starts a service, RPC, wallet or provider.
import { projectMintNetwork } from './economic-network.mjs';
export const manifest = Object.freeze({
  id: 'mint-economic-evidence', version: '0.1', readonly: true,
  inputs: ['mint'], outputs: ['facts', 'sources', 'unknowns'],
});
const MINT = /^[1-9A-HJ-NP-Za-km-z]{32,44}$/;

export async function run({ mint, readEconomic, now = Date.now } = {}) {
  if (!MINT.test(String(mint || ''))) throw new Error('Invalid Solana Mint address');
  if (typeof readEconomic !== 'function') throw new Error('APPROVED_OFFLINE_EVIDENCE_READER_REQUIRED');
  // Model supplies only the Mint; never file paths, wallet lists, SQL queries, or HTTP URLs.
  const report = await readEconomic({ mint });
  if (report?.mode !== 'OFFLINE_READ_ONLY_SQLITE_MINT_REPORT' || report.input?.mint !== mint ||
      !Array.isArray(report.recipients) || !report.evidence || typeof report.evidence !== 'object') {
    throw new Error('OFFLINE_EVIDENCE_CONTRACT_MISMATCH');
  }
  const discovery = report.evidence.senderDiscovery || {};
  const recipients = report.recipients.slice(0, 200).map((row) => ({
    signature: row.signature ?? null,
    rpcSha256: row.rpcSha256 ?? null, rpcHashVerified: row.rpcHashVerified === true,
    instructionVerifiedAgainstRpc: row.instructionVerifiedAgainstRpc === true,
    captureSource: row.captureSource ?? 'UNKNOWN', commitment: row.commitment ?? null,
    capturedAtMs: row.capturedAtMs ?? null,
    outerI: Number.isInteger(row.outerI) ? row.outerI : null,
    innerI: Number.isInteger(row.innerI) ? row.innerI : null,
    mint: row.mint ?? mint,
    slot: row.slot ?? null, blockTime: row.blockTime ?? null,
    fromOwner: row.fromOwner ?? null, toOwner: row.toOwner ?? null,
    fromAccount: row.fromAccount ?? null, toAccount: row.toAccount ?? null,
    amountRaw: row.amountRaw ?? null,
    sellObservation: row.sellObservation ?? 'TRANSFER_TIME_OR_MINT_UNKNOWN',
    observedSells: Array.isArray(row.observedSells) ? row.observedSells.slice(0, 5) : [],
    crossMintCandidates: Array.isArray(row.crossMintCandidates) ? row.crossMintCandidates.slice(0, 25) : [],
  }));
  const unknowns = [
    'Only captured local RPC history is visible; lifetime wallet history is not complete.',
    'Observed addresses may be pools, routers or public services, not unique controllers.',
    'A later sell does not prove that transferred tokens were the sold inventory.',
    'Cross-Mint temporal paths do not prove capital provenance or common control.',
    ...(Array.isArray(report.limitations) ? report.limitations.slice(0, 12) : []),
  ];
  if (discovery.truncated) unknowns.push('Mint-first discovery was limited to a subset of sender candidates.');
  const localIndexMissing = report.evidence.indexedCoverage === 'LOCAL_EVIDENCE_OR_WALLET_SUMMARY_MISSING';
  if (localIndexMissing) unknowns.push('Required local economic evidence tables are missing; zero recipients does not establish no transfers.');
  return {
    schemaVersion: '0.1', capability: manifest.id, mint,
    status: localIndexMissing ? 'UNAVAILABLE' : 'LOCAL_EVIDENCE_PARTIAL',
    evidenceLevel: 'CAPTURED_LOCAL_ARCHIVE_NOT_FULL_CHAIN_VERIFIED',
    observedAt: new Date(now()).toISOString(),
    sources: [{ provider: 'EXISTING_LOCAL_SQLITE', method: 'OFFLINE_READ_ONLY_REPORT',
      coverage: report.evidence.indexedCoverage ?? 'UNKNOWN' }],
    facts: { knownSenderMintCaptures: report.evidence.knownSenderMintCaptures ?? 0,
      senderDiscovery: discovery, lifetimeHistoryComplete: false, recipients,
      network: projectMintNetwork({ mint, recipients }) },
    unknowns: [...new Set(unknowns)],
  };
}
