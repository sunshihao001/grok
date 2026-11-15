import assert from "node:assert/strict";
import test from "node:test";
import fs from "node:fs";
import { selectObservedCandidates, resolveResearchTarget, validateMintResearchReceipt, validatePulseSelectionReceipt } from "../web/src/pages/intelligence/candidates.ts";

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

test("user Coin Mint stays the target even if Pulse has no matching candidate", () => {
  const observed = selectObservedCandidates(coins, cols, "all");
  const selected = resolveResearchTarget(observed, "aaa", "explicit-mint-not-seen");
  assert.equal(selected.mint, "explicit-mint-not-seen");
  assert.equal(selected.observed, null);
  assert.equal(selected.evidenceSource, "USER_MINT_LOCAL_ARCHIVE_ONLY");
  const known = resolveResearchTarget(observed, "aaa", "ccc");
  assert.equal(known.mint, "ccc");
  assert.equal(known.observed?.coin.mint, "ccc");
  const empty = resolveResearchTarget([], null, null);
  assert.equal(empty.mint, null);
  assert.equal(empty.observed, null);
  assert.equal(resolveResearchTarget(observed, "aaa", null).mint, "aaa");
});

test("Coin deep-link, manual read-only research and client address gate use the exact Mint", () => {
  const coin = fs.readFileSync(new URL("../web/src/pages/coin/AiCopilot.tsx", import.meta.url), "utf8");
  const workspace = fs.readFileSync(new URL("../web/src/pages/Intelligence.tsx", import.meta.url), "utf8");
  assert.ok(coin.includes('"#/intelligence/" + encodeURIComponent(mint)'));
  assert.ok(coin.includes("encodeURIComponent(question.trim())"));
  assert.ok(workspace.includes("setExplicitMint(mint)"));
  assert.ok(workspace.includes("window.addEventListener(\"hashchange\", syncCoinLink)"));
  assert.ok(workspace.includes("resolveResearchTarget(candidates, selectedMint, explicitMint)"));
  assert.ok(workspace.includes("const mint = researchMint;"));
  assert.ok(workspace.includes("researchResult?.mint === researchMint"));
  assert.ok(workspace.includes("NOT_OBSERVED_FOR_SPECIFIED_MINT"));
  assert.ok(workspace.includes("disabled={!researchMint || !goal.trim()"));
  assert.ok(workspace.includes("onClick={() => void runLocalResearch()}"));
  assert.ok(workspace.includes("127\\.0\\.0\\.1"));
  assert.ok(!workspace.includes("127\\\\.0\\\\.0\\\\.1"), "no double escaping the localhost IP regex");
});

test("Intelligence has a model-free exact-Mint archive path independent of paid AI readiness", () => {
  const ui = fs.readFileSync(new URL("../web/src/pages/Intelligence.tsx", import.meta.url), "utf8");
  assert.ok(ui.includes("async function runLocalInspection()"));
  assert.ok(ui.includes('SIDECAR_URL + "/inspect"'));
  assert.ok(ui.includes("JSON.stringify({mint})"));
  assert.ok(ui.includes("researchHealth?.inspectionReady"));
  assert.ok(ui.includes("researchHealth.remainingInspections === 0"));
  assert.ok(ui.includes('data.mint !== mint || data.modelMode !== "NOT_USED"'));
  assert.ok(ui.includes("免费查看指定 Mint 的本地经济证据（不使用AI）"));
  assert.ok(ui.includes("activeResearch.modelMode === \"NOT_USED\""));
  assert.ok(ui.includes("async function runLocalResearch()"));
  assert.ok(ui.includes('SIDECAR_URL + "/research"'));
});

test("existing Intelligence UI renders both research and trade anchors with inspectable evidence checks",()=>{
  const ui=fs.readFileSync(new URL("../web/src/pages/Intelligence.tsx",import.meta.url),"utf8");
  assert.match(ui,/目标锚点：调查价值 ≠ 实际交易机会/);
  assert.match(ui,/activeResearch\.continuation\.anchors\.researchPriority\.status/);
  assert.match(ui,/activeResearch\.continuation\.anchors\.tradeReadiness\.status/);
  assert.match(ui,/activeResearch\.continuation\.anchors\.nextEvidence\.map/);
  assert.match(ui,/knowledgeContext\.providedRecordCount/);
});

test("AI research receipt cannot silently attach another Mint's evidence to the selected coin", () => {
  const mint = "EYqygbhZjP7EbM4fSn8devctnksAvPAD1Bt57XBFpump";
  const other = "4p7SeR6361WJ4T4icgsYTnzAUzfA5NwM4CwYD9kMBjuK";
  const valid = { calls:[{capability:"mint-economic-evidence",input:{mint}}],
    evidence:[{capability:"mint-economic-evidence",input:{mint},
      result:{mint,status:"OBSERVED_UNVERIFIED"}}],knowledgeUse:[],
    verifiedMarketOpportunity:false,liveExecutionValidated:false };
  assert.equal(validateMintResearchReceipt(valid,mint),true);
  assert.equal(validateMintResearchReceipt({...valid,mint:other},mint),false);
  assert.equal(validateMintResearchReceipt({...valid,evidence:[{...valid.evidence[0],input:{mint:other}}]},mint),false);
  assert.equal(validateMintResearchReceipt({...valid,evidence:[{...valid.evidence[0],
    result:{mint:other,status:"OBSERVED_UNVERIFIED"}}]},mint),false);
  assert.equal(validateMintResearchReceipt({...valid,calls:[{capability:"mint-facts",input:{mint:other}}]},mint),false);
  assert.equal(validateMintResearchReceipt({...valid,verifiedMarketOpportunity:true},mint),false);
  assert.equal(validateMintResearchReceipt({...valid,liveExecutionValidated:true},mint),false);
  assert.equal(validateMintResearchReceipt({calls:[],evidence:[],knowledgeUse:[]},mint),true,
    "a no-evidence model plan can be shown as a non-verified draft");
  const workspace = fs.readFileSync(new URL("../web/src/pages/Intelligence.tsx", import.meta.url), "utf8");
  assert.match(workspace,/validateMintResearchReceipt\(data, mint\)/);
  assert.match(workspace,/RESEARCH_RESULT_MINT_OR_EVIDENCE_MISMATCH/);
});

test("Pulse discovery cannot substitute a Mint outside the actual submitted shortlist", () => {
  const mint = "EYqygbhZjP7EbM4fSn8devctnksAvPAD1Bt57XBFpump";
  const other = "4p7SeR6361WJ4T4icgsYTnzAUzfA5NwM4CwYD9kMBjuK";
  const base = {discovery:{selectedMint:mint,candidateCount:1},
    investigation:{calls:[],evidence:[],knowledgeUse:[]},verifiedMarketOpportunity:false};
  assert.equal(validatePulseSelectionReceipt(base,[mint]),true);
  assert.equal(validatePulseSelectionReceipt({...base,discovery:{...base.discovery,selectedMint:other}},[mint]),false);
  assert.equal(validatePulseSelectionReceipt({...base,discovery:{...base.discovery,candidateCount:2}},[mint]),false);
  assert.equal(validatePulseSelectionReceipt({...base,discovery:{selectedMint:null,candidateCount:1},investigation:null},[mint]),true);
  assert.equal(validatePulseSelectionReceipt({...base,discovery:{selectedMint:null,candidateCount:1}},[mint]),false);
  assert.equal(validatePulseSelectionReceipt({...base,investigation:{...base.investigation,
    evidence:[{input:{mint:other},result:{mint:other}}]}},[mint]),false);
  const workspace = fs.readFileSync(new URL("../web/src/pages/Intelligence.tsx", import.meta.url), "utf8");
  assert.match(workspace,/validatePulseSelectionReceipt\(data, shortlist\.map\(item => item\.mint\)\)/);
});
