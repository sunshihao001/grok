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
