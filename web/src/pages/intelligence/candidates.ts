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
