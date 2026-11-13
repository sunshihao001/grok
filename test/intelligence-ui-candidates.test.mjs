import assert from "node:assert/strict";
import test from "node:test";
import { selectObservedCandidates } from "../web/src/pages/intelligence/candidates.ts";

const coins = {
  "aaa": { mint: "aaa", name: "Alpha", symbol: "ALP", born: 1 },
  "bbb": { mint: "bbb", name: "Beta", symbol: "BTA", born: 2 },
  "ccc": { mint: "ccc", name: "Gamma", symbol: "GAM", born: 3 },
};
const cols = { new: ["aaa", "bbb"], stretch: ["bbb"], migrated: ["ccc"], running: ["aaa"] };

test("AI workspace preserves existing Pulse board order, not invented opportunity ratings", () => {
  assert.deepEqual(selectObservedCandidates(coins, cols, "all").map(x => x.coin.mint), ["bbb", "ccc", "aaa"]);
  assert.deepEqual(selectObservedCandidates(coins, cols, "new").map(x => x.coin.mint), ["aaa", "bbb"]);
});
test("stage filtering, query and missing rows do not change source labels", () => {
  assert.equal(selectObservedCandidates(coins, cols, "all", "gam")[0]?.stage, "migrated");
  assert.deepEqual(selectObservedCandidates(coins, {...cols, new: ["missing", "aaa"]}, "new").map(x => x.coin.mint), ["aaa"]);
  assert.deepEqual(selectObservedCandidates(coins, cols, "all", "absent"), []);
});
test("bounded shortlist and deduplication avoid multiplying one coin across stages", () => {
  assert.equal(selectObservedCandidates(coins, cols, "all", "", 1).length, 1);
  assert.equal(new Set(selectObservedCandidates(coins, cols, "all").map(x => x.coin.mint)).size, 3);
});
