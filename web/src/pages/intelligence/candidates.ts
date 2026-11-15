// Pulse already supplies a market board; this is a presentation-only shortlist.
// Order is stage priority / existing Blix order, NOT an AI opportunity score.
import type { Coin, ColKey } from "../../lib/pulse";

export type ObservedStage = "all" | ColKey;
export type ObservedCandidate = { coin: Coin; stage: ColKey };
const ALL_STAGES: ColKey[] = ["stretch", "migrated", "new", "running"];

export function selectObservedCandidates(
  coins: Record<string, Coin>,
  cols: Record<ColKey, string[]>,
  stage: ObservedStage,
  search = "",
  limit = 60,
): ObservedCandidate[] {
  const query = search.trim().toLowerCase();
  const stages = stage === "all" ? ALL_STAGES : [stage];
  const used = new Set<string>(), result: ObservedCandidate[] = [];
  for (const col of stages) {
    for (const mint of cols[col] || []) {
      if (used.has(mint)) continue;
      used.add(mint);
      const coin = coins[mint];
      if (!coin) continue;
      if (query && ![coin.symbol, coin.name, coin.mint].some((x) => x?.toLowerCase().includes(query))) continue;
      result.push({ coin, stage: col });
      if (result.length >= Math.max(1, Math.min(limit, 100))) return result;
    }
  }
  return result;
}

// A Coin deep link is an explicit user choice, NOT a Pulse market observation.
// Never fall back to another coin when its Mint is not in the visible shortlist.
export function resolveResearchTarget(
  candidates: ObservedCandidate[],
  selectedMint: string | null,
  explicitMint: string | null,
): { mint: string | null; observed: ObservedCandidate | null; evidenceSource: string } {
  if (explicitMint) {
    const observed = candidates.find(x => x.coin.mint === explicitMint) ?? null;
    return { mint: explicitMint, observed,
      evidenceSource: observed ? "USER_MINT_WITH_PULSE_OBSERVATION" : "USER_MINT_LOCAL_ARCHIVE_ONLY" };
  }
  const observed = candidates.find(x => x.coin.mint === selectedMint) ?? candidates[0] ?? null;
  return { mint: observed?.coin.mint ?? null, observed,
    evidenceSource: observed ? "PULSE_OBSERVED" : "NO_MINT_SELECTED" };
}

/**
 * Never relabel an AI/SQLite response with the requested Mint. Every returned
 * evidence tool call must remain scoped to that exact Mint, including errors.
 * An empty model plan may have no evidence, but it still cannot claim a different
 * Mint or a verified market opportunity.
 */
export function validateMintResearchReceipt(
  response: unknown, requestedMint: string,
): boolean {
  if (!response || typeof response !== "object" || !requestedMint) return false;
  const result = response as {
    mint?: unknown; verifiedMarketOpportunity?: unknown; liveExecutionValidated?: unknown;
    evidence?: unknown; calls?: unknown; knowledgeUse?: unknown;
  };
  if (result.mint !== undefined && result.mint !== requestedMint) return false;
  if (result.verifiedMarketOpportunity === true || result.liveExecutionValidated === true) return false;
  if (!Array.isArray(result.evidence) || !Array.isArray(result.calls) ||
      !Array.isArray(result.knowledgeUse)) return false;
  const sameMint = (value: unknown) => !!value && typeof value === "object" &&
    (value as {mint?: unknown}).mint === requestedMint;
  return result.evidence.every((entry: unknown) => {
    if (!entry || typeof entry !== "object") return false;
    const evidence = entry as { input?: unknown; result?: unknown };
    if (!sameMint(evidence.input)) return false;
    if (evidence.result !== undefined &&
        (!evidence.result || typeof evidence.result !== "object" ||
         !sameMint(evidence.result))) return false;
    return true;
  }) && result.calls.every((entry: unknown) => {
    if (!entry || typeof entry !== "object") return false;
    return sameMint((entry as {input?: unknown}).input);
  });
}

/** A discovery selection must be one of the actually submitted browser candidates. */
export function validatePulseSelectionReceipt(
  response: unknown, submittedMints: readonly string[],
): boolean {
  if (!response || typeof response !== "object") return false;
  const result = response as {
    discovery?: {selectedMint?: unknown; candidateCount?: unknown};
    investigation?: unknown; verifiedMarketOpportunity?: unknown;
  };
  if (result.verifiedMarketOpportunity === true ||
      !result.discovery || result.discovery.candidateCount !== submittedMints.length) return false;
  const selected = result.discovery.selectedMint;
  if (selected === null) return result.investigation === null;
  if (typeof selected !== "string" || !submittedMints.includes(selected)) return false;
  if (result.investigation === null) return true;
  return validateMintResearchReceipt(result.investigation, selected);
}
