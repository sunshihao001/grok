#!/usr/bin/env node
// Blix research branch: a static, fail-closed startup audit, NOT a runtime sandbox.
// Reads project source only. No network calls, wallet access, signing, or AI requests.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
export const FINDINGS = Object.freeze([
  { id: 'WALLET_ACTIONS', file: 'server/accounts.js', re: /\/api\/account\/(?:buy|sell|withdraw|export|claim)/, severity: 'blocker', note: 'Real wallet transfer/signature pathways via Vault exist.' },
  { id: 'HOSTED_SWAP', file: 'server/hosted-accounts.js', re: /\/swap/, severity: 'blocker', note: 'Hosted-wallet swap pathway exists.' },
  { id: 'AUTO_CLAIM', file: 'server/autoclaim.js', re: /\/claim/, severity: 'blocker', note: 'Automatic on-chain claim workflow exists.' },
  { id: 'AI_AUTOMATION', file: 'server/settings.js', re: /researchAuto:\s*true/, severity: 'blocker', note: 'Default automated research may consume provider credits.' },
  { id: 'GROK_ENABLED', file: 'server/settings.js', re: /grokOff:\s*false/, severity: 'blocker', note: 'Default setting does not disable Grok calls.' },
  { id: 'DESK_AUTOMATION', file: 'server/settings.js', re: /desk:\s*true/, severity: 'blocker', note: 'Narrative desk can trigger model usage.' },
  { id: 'STARTUP_EXTERNAL_CALL', file: 'server/server.js', re: /detectVersion\(\)\.then\(grokTier\)\.then\(grokBilling\)/, severity: 'blocker', note: 'Startup invokes external billing/account checks.' },
  { id: 'LIVE_MARKET_FEEDS', file: 'server/settings.js', re: /marketFeeds:\s*true/, severity: 'review', note: 'External market feeds may consume RPC or supplier quota.' },
  { id: 'LEGACY_MCP_PAPER', file: 'public/mcp-tools.js', re: /name:\s*["']blix_paper_buy["']/, severity: 'review', note: 'Paper write tools still exist in the underlying catalog (not exposed in research MCP).' }
]);
export function inspectSource(root = ROOT, reader = (p) => fs.readFileSync(p, 'utf8')) {
  return FINDINGS.map((finding) => {
    try {
      const text = reader(path.join(root, finding.file));
      return { id: finding.id, severity: finding.severity, present: finding.re.test(text), file: finding.file, note: finding.note };
    } catch (error) {
      // Unreadable files must not be interpreted as a clean security result.
      return { id: finding.id, severity: 'blocker', present: true, file: finding.file, note: 'Source unreadable: ' + error.message };
    }
  });
}
export function gateDecision(findings, acknowledged = false) {
  const remaining = findings.filter((row) => row.present && row.severity === 'blocker');
  return { allowed: remaining.length === 0 || acknowledged, blockerCount: remaining.length, blockers: remaining.map((x) => x.id) };
}
const invoked = process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url);
if (invoked) {
  const findings = inspectSource();
  const isGate = process.argv.includes('--gate');
  // Not a read-only certification: this override restores the *unmodified upstream* startup only after
  // an operator explicitly approves its real-wallet, external-account and AI cost risks.
  const acknowledged = process.env.BLIX_APPROVED_LEGACY_RUNTIME === 'I_ACKNOWLEDGE_REAL_WALLET_AND_AI_COSTS';
  const result = gateDecision(findings, Boolean(isGate && acknowledged));
  process.stdout.write(JSON.stringify({ mode: isGate ? 'startup-gate' : 'audit', readOnlyCertified: false, findings, ...result }, null, 2) + '\n');
  if (isGate && !result.allowed) {
    process.stderr.write('Blix research startup blocked: the original server has unreviewed wallet/AI side effects. This is NOT a runtime sandbox.\n');
    process.exitCode = 2;
  }
}
