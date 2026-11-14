import assert from "node:assert/strict";
import test from "node:test";
import fs from "node:fs";
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

test("research workspace distinguishes tracked wallet address counts from related actors and mixed transfers", () => {
  const ui = fs.readFileSync(new URL("../web/src/pages/Intelligence.tsx", import.meta.url), "utf8");
  assert.match(ui, /rawTrackedBuyerAddressCount/);
  assert.match(ui, /relatedHeuristicGroupCount/);
  assert.match(ui, /independentEconomicControllerCount/);
  assert.match(ui, /原版 Research 同口径/);
  assert.match(ui, /旧 WTrack 简化转账列表可能不显示混合交易/);
  assert.match(ui, /这里不将转账记为卖出/);
});

test("Coin to Intelligence deep link stays within existing Pulse and requires a manual model action", () => {
  const coin = fs.readFileSync(new URL("../web/src/pages/coin/AiCopilot.tsx", import.meta.url), "utf8");
  const workspace = fs.readFileSync(new URL("../web/src/pages/Intelligence.tsx", import.meta.url), "utf8");
  assert.match(coin, /#\\/intelligence\\//);
  assert.match(coin, /encodeURIComponent\\(mint\\)/);
  assert.match(coin, /encodeURIComponent\\(question\\.trim\\(\\)\\)/);
  assert.match(workspace, /setSearch\\(mint\\)/);
  assert.match(workspace, /setSelectedMint\\(mint\\)/);
  assert.match(workspace, /selected = candidates\\.find/);
  assert.match(workspace, /onClick=\\{\\(\\) => void runLocalResearch\\(\\)\\}/);
  assert.match(workspace, /disabled=\\{!c \\|\\| !goal\\.trim\\(\\)/);
});
