// Optional AI research workspace over the EXISTING Blix Pulse board and Coin page.
// Optional local isolated research calls only after user action and operator opt-in.
// A market observation is NOT a verified profitable trading opportunity.
import { useEffect, useMemo, useState } from "react";
import { usePulse, type ColKey } from "@/lib/pulse";
import { Page, Panel, money } from "@/components/page";
import { toast } from "@/components/ui/toast";
import { selectObservedCandidates, resolveResearchTarget, type ObservedStage } from "./intelligence/candidates";

const STAGES: { key: ObservedStage; label: string }[] = [
  { key: "all", label: "所有观察" }, { key: "stretch", label: "临近迁移" },
  { key: "migrated", label: "已迁移" }, { key: "new", label: "新币" },
  { key: "running", label: "活跃" },
];
const STAGE_LABEL: Record<ColKey, string> = {
  stretch: "Final stretch", migrated: "Migrated", new: "New pairs", running: "Running",
};
const PROMPTS = [
  "调查当前候选的买入、Token 转移和接收钱包卖出链路，标注证据缺口。",
  "判断这个代币是否具备信号之后的可成交机会，核查流动性、费用和退出条件。",
  "比较资金组织、关联钱包与正常市场需求等竞争性解释，找出最值得核查的问题。",
];
// Existing Blix sources already curated from Hermes, qb-, meme-, ai-d and native research.
// This client-only preview links to ORIGINAL sources; it does not read files, run a model,
// or claim the server actually retrieved or applied any knowledge during this page view.
const KNOWLEDGE_CANDIDATES = [
  { id: "wallets", label: "钱包角色与库存", heritage: "Hermes / Blix D04",
    path: "knowledge/mechanisms/wallet-roles-and-inventory.md",
    match: /钱包|接收|转仓|转移|持仓|bundle|holder|wallet|卖出|控制/i },
  { id: "key-wallet", label: "关键地址调查与设施区分", heritage: "qb- / Blix 旧报告",
    path: "knowledge/methods/key-wallet-investigation-brief.md",
    match: /重点地址|关键钱包|新钱包|早期买家|新地址|KOL|sniper/i },
  { id: "funds", label: "资金组织与资本关系", heritage: "Hermes / D05 / Why-Solana",
    path: "knowledge/mechanisms/capital-organization-and-incentives.md",
    match: /资金|同源|关联|共控|洗量|接力|fund|sol|出货/i },
  { id: "multihop", label: "多跳资金路径和误归因", heritage: "Why-Solana / 跨项目审计",
    path: "knowledge/references/multihop-funding-evidence-audit.md",
    match: /资金路径|多跳|跨币|跨mint|转给新钱包|非holder/i },
  { id: "strategy", label: "机会与执行经济", heritage: "meme- / Blix D08–D09",
    path: "knowledge/mechanisms/strategy-and-execution-economics.md",
    match: /交易|策略|成交|机会|参与|跟单|滑点|成本|退出|收益|可跟|流动性/i },
  { id: "market", label: "市场微观结构与价格机制", heritage: "meme- / Blix D03",
    path: "knowledge/mechanisms/market-price-mechanism-research.md",
    match: /价格|市场|机制|解释|做市|量价|拉升|上涨|诱多/i },
  { id: "validation", label: "证据、反例与失败条件", heritage: "Blix / Hermes / 参考项目反例",
    path: "knowledge/cases/independent-validation-and-failure-cases.md",
    match: /反证|竞争解释|证据|风险|失败|回测|误报|验收|不确定/i },
  { id: "intent", label: "AI 意图与知识选择", heritage: "ai-d / Blix D12",
    path: "knowledge/ai/intent-knowledge-selection-and-reasoning.md",
    match: /AI|知识|思考|研究|意图|专家|检索/i },
] as const;
const KNOWLEDGE_ROOT = "https://github.com/sunshihao001/grok/blob/integration/blix-evidence-readonly-20261108/";
type ResearchHealth = { ready: boolean; inspectionReady?: boolean; remainingInspections?: number; dataSource: string; remainingTasks: number; busy: boolean };
type DiscoveryResult = {
  status: string;
  discovery: {
    selectedMint: string | null; reason: string; candidateCount: number;
    source: string; marketCoverage: string; sourceFreshness: string;
    unknowns: string[]; modelSelectionVerified: false;
    knowledgeUse?: {stage:string;source:string;topic?:string;outcome:string}[];
  };
  investigation: ResearchResult | null;
  verifiedMarketOpportunity: false;
};
type EvidenceEdge = { fromOwner: string; toOwner: string; eventCount: number; observedRawTotal: string; localSellSummaryObserved: boolean; crossMintCandidateCount: number };
type ResearchEvidence = { capability: string; error?: string; result?: { status: string; unknowns?: string[]; sources?: { provider: string; coverage?: string }[]; facts?: {
  network?: { eventCount: number; coverage: string; edges: EvidenceEdge[]; inputTruncated: boolean };
  trackedWalletActivity?: { rawTrackedBuyerAddressCount: number | null; relatedHeuristicGroupCount: number | null; independentEconomicControllerCount: number | null; observationWindow: string; evidenceStatus: string };
  recipients?: { signature: string | null; fromOwner: string | null; toOwner: string | null; sameSignatureSenderBuySummaryObserved?: boolean }[];
} } };
type ResearchResult = {
  mint: string; status: string; error?: string; completedAt?: string; modelMode?: string;
  assessment?: { summary: string; hypotheses: string[]; alternativeExplanations: string[]; nextChecks: string[]; evidenceLevel: string } | null;
  calls: { capability: string; input: { mint: string } }[];
  evidence: ResearchEvidence[];
  knowledgeUse: { stage: string; source: string; topic?: string; sourceStatus?: string; outcome: string; suggestedCapabilities?: string[] }[];
  unknowns: string[]; verifiedMarketOpportunity: false; sourceMode: string;
  continuation?: {
    stages: {market:string;keyWallets:string;capitalAndInventory:string;
      crossMint:string;participation:string;monitoring:string};
    keyWalletCandidates: {wallet:string;observedTransferCount:number;localSellSummaryCount:number;
      addressClass:string; economicController:string}[];
    crossMintCandidates: {otherMint:string;candidateFundingSignature:string;candidateBuySignature:string;status:string}[];
    followability:{status:string;historicalNetPnl:string;outOfSampleAdvantage:string;decision:string};
    watch:{status:string;suggestedWallets:string[];comparisonMethod:string};
    limits:string[];
  };
};
const SIDECAR_URL = typeof window !== "undefined" &&
  window.location.protocol === "http:" && /^(?:localhost|127\.0\.0\.1)$/.test(window.location.hostname)
  ? "http://127.0.0.1:4547" : null;
const number = (n?: number | null) => n == null || !Number.isFinite(n) ? "未知" : Math.round(n).toLocaleString();
const percent = (n?: number | null) => n == null || !Number.isFinite(n) ? "未知" : n.toFixed(1) + "%";
const compact = (mint: string) => mint.length > 18 ? mint.slice(0, 7) + "…" + mint.slice(-6) : mint;

export function Intelligence() {
  const coins = usePulse(s => s.coins);
  const cols = usePulse(s => s.cols);
  const loaded = usePulse(s => s.loaded);
  const restored = usePulse(s => s.restored);
  const connected = usePulse(s => s.connected);
  const polling = usePulse(s => s.polling);
  const [stage, setStage] = useState<ObservedStage>("all");
  const [search, setSearch] = useState("");
  const [selectedMint, setSelectedMint] = useState<string | null>(null);
  const [explicitMint, setExplicitMint] = useState<string | null>(null);
  const [goal, setGoal] = useState(PROMPTS[1]);
  const [researchHealth, setResearchHealth] = useState<ResearchHealth | null>(null);
  const [researchResult, setResearchResult] = useState<ResearchResult | null>(null);
  const [discoveryResult, setDiscoveryResult] = useState<DiscoveryResult | null>(null);
  const [researchBusy, setResearchBusy] = useState(false);
  const [researchError, setResearchError] = useState("");
  // Coin deep-link: preserve the user's exact Mint even when Pulse did not index it.
  // Hash navigation never invents market observations or triggers a model request.
  useEffect(() => {
    const syncCoinLink = () => {
      const match = /^#\/intelligence\/([1-9A-HJ-NP-Za-km-z]{32,44})(?:\?(.*))?$/.exec(window.location.hash);
      if (!match) { setExplicitMint(null); return; }
      const mint = match[1];
      setExplicitMint(mint);
      setStage("all");
      setSearch(mint);
      setSelectedMint(mint);
      setResearchResult(null);
      setDiscoveryResult(null);
      setResearchError("");
      const requestedGoal = new URLSearchParams(match[2] || "").get("goal");
      if (requestedGoal && requestedGoal.trim() && requestedGoal.length <= 1600) setGoal(requestedGoal);
    };
    syncCoinLink();
    window.addEventListener("hashchange", syncCoinLink);
    return () => window.removeEventListener("hashchange", syncCoinLink);
  }, []);

  useEffect(() => {
    if (!SIDECAR_URL) return;
    const controller = new AbortController();
    fetch(SIDECAR_URL + "/health", { signal: controller.signal, credentials: "omit" })
      .then(r => r.ok ? r.json() : null)
      .then(v => { if (!controller.signal.aborted) setResearchHealth(v); })
      .catch(() => { if (!controller.signal.aborted) setResearchHealth(null); });
    return () => controller.abort();
  }, []);
  const candidateKnowledge = useMemo(() => KNOWLEDGE_CANDIDATES.filter(x => x.match.test(goal)).slice(0, 3), [goal]);
  const candidates = useMemo(() => selectObservedCandidates(coins, cols, stage, search), [coins, cols, stage, search]);
  // Independent of the visual filter: the AI may compare Pulse candidates the user
  // has not explicitly opened. No provider data is fetched for this shortlist.
  const discoveryCandidates = useMemo(() => selectObservedCandidates(coins, cols, "all", "", 12),
    [coins, cols]);
  const target = resolveResearchTarget(candidates, selectedMint, explicitMint);
  const selected = target.observed;
  const c = selected?.coin ?? null;
  const researchMint = target.mint;
  const manualArchiveOnly = target.evidenceSource === "USER_MINT_LOCAL_ARCHIVE_ONLY";
  const coinHref = c ? "#/coin/" + encodeURIComponent(c.mint) : "";
  const holderCount = c?.hl?.h ?? c?.holders;
  const top10 = c?.hl?.t10 ?? c?.top10;
  const devShare = c?.hl?.dev ?? c?.dev;
  const windowVol = c?.vol ?? c?.liveVol;
  const activity = c && (c.buys != null || c.sells != null)
    ? number(c.buys) + " 买 / " + number(c.sells) + " 卖" : "未知";
  const activeResearch = researchMint && researchResult?.mint === researchMint ? researchResult : null;
  const economicFacts = activeResearch?.evidence.find(x => x.capability === "mint-economic-evidence")?.result?.facts;
  const network = economicFacts?.network;
  const trackedWalletActivity = economicFacts?.trackedWalletActivity;
  const combinedBuyTransfers = economicFacts?.recipients?.filter(x => x.sameSignatureSenderBuySummaryObserved).slice(0, 8) || [];
  const sourceState = loaded ? (connected ? "实时流连接中" : polling ? "轮询更新中" : "数据连接待核实")
    : restored ? "历史缓存，可能过时" : "等待 Blix Pulse 数据";

  async function runLocalInspection() {
    if (!SIDECAR_URL || !researchMint || !researchHealth?.inspectionReady ||
        researchHealth.remainingInspections === 0 || researchBusy) return;
    // Free, deterministic view of the EXISTING local economic archive. No AI
    // model, trading endpoint, RPC, or browser-provided market facts are used.
    const mint = researchMint;
    setResearchBusy(true);
    setResearchError("");
    setResearchResult(null);
    setDiscoveryResult(null);
    try {
      const response = await fetch(SIDECAR_URL + "/inspect", {
        method: "POST", headers: {"Content-Type":"application/json"},
        credentials: "omit", redirect: "error",
        body: JSON.stringify({mint}),
        signal: AbortSignal.timeout(45_000),
      });
      const data = await response.json();
      if (!response.ok) {
        if (data?.error === "MINT_LOCAL_EVIDENCE_UNAVAILABLE")
          throw new Error("指定 Mint 未保存在当前本地经济归档；这不代表链上没有交易。");
        throw new Error(typeof data?.error === "string" ? data.error : "LOCAL_INSPECTION_FAILED");
      }
      if (!data || data.mint !== mint || data.modelMode !== "NOT_USED" ||
          !Array.isArray(data.evidence) || !Array.isArray(data.unknowns) ||
          !data.evidence.some((entry: ResearchEvidence) =>
            entry.capability === "mint-economic-evidence" && entry.result?.facts)) {
        throw new Error("LOCAL_INSPECTION_RESULT_INVALID");
      }
      setResearchResult(data as ResearchResult);
      toast("已读取指定 Mint 的本地经济归档；未调用模型，历史覆盖仍需核查");
    } catch(error) {
      setResearchError(error instanceof Error ? error.message.slice(0,160) : "LOCAL_INSPECTION_UNAVAILABLE");
    } finally {
      setResearchBusy(false);
      fetch(SIDECAR_URL + "/health", {credentials:"omit"})
        .then(r => r.ok ? r.json() : null).then(v => setResearchHealth(v))
        .catch(() => setResearchHealth(null));
    }
  }

  async function runLocalResearch() {
    if (!SIDECAR_URL || !researchMint || !goal.trim() || !researchHealth?.ready || researchBusy) return;
    const mint = researchMint;
    setResearchBusy(true);
    setResearchError("");
    setResearchResult(null);
    setDiscoveryResult(null);
    try {
      const response = await fetch(SIDECAR_URL + "/research", {
        method: "POST", headers: { "Content-Type": "application/json" },
        credentials: "omit", redirect: "error",
        body: JSON.stringify({ mint, goal: goal.trim() }),
        signal: AbortSignal.timeout(115_000),
      });
      const data = await response.json();
      if (!response.ok) {
        if (data?.error === "MINT_LOCAL_EVIDENCE_UNAVAILABLE")
          throw new Error("指定 Mint 未出现在当前本地经济归档索引中；没有调用模型，也不能推断链上无交易。");
        throw new Error(typeof data?.error === "string" ? data.error : "RESEARCH_REQUEST_FAILED");
      }
      if (!data || !Array.isArray(data.evidence) || !Array.isArray(data.knowledgeUse) || !Array.isArray(data.calls))
        throw new Error("RESEARCH_RESULT_INVALID");
      setResearchResult({ ...data, mint });
      // A model response is a bounded research draft, not a trading recommendation.
      toast("已收到本地只读调查结果；链上证据覆盖和模型解释仍需复核");
    } catch (error) {
      setResearchError(error instanceof Error ? error.message.slice(0, 160) : "RESEARCH_UNAVAILABLE");
    } finally {
      setResearchBusy(false);
      fetch(SIDECAR_URL + "/health", { credentials: "omit" })
        .then(r => r.ok ? r.json() : null).then(v => setResearchHealth(v)).catch(() => setResearchHealth(null));
    }
  }
  async function runPulseDiscovery() {
    if (!SIDECAR_URL || !researchHealth?.ready || researchBusy || !goal.trim() ||
        !loaded || !(connected || polling) || !discoveryCandidates.length) return;
    const shortlist = discoveryCandidates.map(({coin,stage:observedStage}) => ({
      mint:coin.mint, stage:observedStage, symbol:coin.symbol || "",
      mcap:coin.mcap ?? null, liq:coin.liq ?? null,
      vol:coin.vol ?? coin.liveVol ?? null,
      buys:coin.buys ?? null, sells:coin.sells ?? null,
      traders:coin.traders ?? null, chg1m:coin.chg1m ?? null,
    }));
    setResearchBusy(true);
    setResearchError("");
    setResearchResult(null);
    setDiscoveryResult(null);
    try {
      const response = await fetch(SIDECAR_URL + "/discover", {
        method: "POST", headers: { "Content-Type":"application/json" },
        credentials:"omit", redirect:"error", signal:AbortSignal.timeout(150_000),
        body:JSON.stringify({ goal:goal.trim(), candidates:shortlist,
          boardStatus:"BLIX_PULSE_LIVE_OR_POLLING",
          browserRecordedAtMs:Date.now() }),
      });
      const data = await response.json();
      if (!response.ok) throw new Error(typeof data?.error === "string" ? data.error : "DISCOVERY_REQUEST_FAILED");
      if (!data?.discovery || typeof data.discovery.reason !== "string" ||
          !data.discovery.source || !Array.isArray(data.discovery.unknowns))
        throw new Error("DISCOVERY_RESULT_INVALID");
      setDiscoveryResult(data);
      if (data.discovery.selectedMint) {
        // Switch to the selected object so the source graph and AI receipts can be viewed
        // alongside the ORIGINAL Blix Coin page. This never adds a new Mint to Blix.
        setStage("all");
        setSearch("");
        setExplicitMint(null);
        setSelectedMint(data.discovery.selectedMint);
        if (data.investigation) setResearchResult({ ...data.investigation,
          mint:data.discovery.selectedMint, sourceMode:data.sourceMode || "LOCAL_SQLITE_ONLY",
          verifiedMarketOpportunity:false });
      }
      toast(data.discovery.selectedMint
        ? "AI 已选择一个候选 Mint 进行本地归档调查；尚未验证交易机会"
        : "AI 未选择调查对象；当前市场资料不足以支持进一步结论");
    } catch(error) {
      setResearchError(error instanceof Error ? error.message.slice(0,160) : "DISCOVERY_UNAVAILABLE");
    } finally {
      setResearchBusy(false);
      fetch(SIDECAR_URL + "/health", {credentials:"omit"})
        .then(r=>r.ok?r.json():null).then(v=>setResearchHealth(v))
        .catch(()=>setResearchHealth(null));
    }
  }
  async function copyTask() {
    if (!researchMint || !goal.trim()) return;
    // These are Blix dashboard observations, not proof of independent on-chain facts.
    const content = [
      "BLIX AI RESEARCH TASK — READ ONLY / MODEL CALL NOT INITIATED",
      "Goal: " + goal.trim(),
      "Mint: " + researchMint,
      "Token: " + (c?.symbol || c?.name || "UNKNOWN_NOT_OBSERVED_IN_PULSE"),
      ...(c && selected ? [
        "Blix Pulse market-board snapshot; source freshness and completeness NOT independently verified:",
        "Board stage: " + STAGE_LABEL[selected.stage],
        "Market cap (reported USD): " + (c.mcap ?? "UNKNOWN"),
        "Liquidity (reported USD): " + (c.liq ?? "UNKNOWN"),
        "Volume (board window, USD): " + (windowVol ?? "UNKNOWN"),
        "Buys / sells (board window): " + (c.buys ?? "UNKNOWN") + " / " + (c.sells ?? "UNKNOWN"),
        "Holder count: " + (holderCount ?? "UNKNOWN"),
        "Top-10 holder concentration (%): " + (top10 ?? "UNKNOWN"),
        "Dev holding (%): " + (devShare ?? "UNKNOWN"),
        "Original Blix AI label (unverified): " + (c.ai?.verdict || c.ai?.grade || "UNKNOWN"),
      ] : ["Pulse market snapshot: NOT_OBSERVED_FOR_SPECIFIED_MINT; prices, liquidity, activity and holders UNKNOWN."]),
      "Historical knowledge references to consider (CLIENT PREVIEW ONLY; not actually retrieved or applied):",
      ...candidateKnowledge.map(x => x.heritage + " | " + x.path),
      "During server-side research, retrieve source-labelled knowledge before tool planning and refresh after evidence.",
      "Use permitted facts and professional knowledge. Separate observation, inference, alternative explanations and UNKNOWN.",
      "Check quote availability, timestamp, liquidity, fees, slippage, exit completeness and signal-followability before calling anything tradable.",
      "No live trades, signing, provider charges or automatic model API requests are authorized by this task.",
    ].join("\n");
    try {
      await navigator.clipboard.writeText(content);
      toast("已复制带当前 Blix 数据的研究任务；未调用 AI");
    } catch {
      toast("无法复制；请检查浏览器剪贴板权限");
    }
  }

  return (
    <Page title="AI 研究工作台" right={<span className="rounded-full border border-rule px-3 py-1.5 text-xs text-muted">
      {researchHealth?.ready ? "本地AI研究可用 · 只读" :
        researchHealth?.inspectionReady ? "本地经济证据可查看 · 无需模型" : "本地只读预览"}
    </span>}>
      <p className="text-sm text-ink-2">
        基于 Blix 已有 Pulse 市场看板组织调查。列表是<strong>市场观察候选</strong>，不是 AI 选币结果、买入信号或盈利预测。
      </p>
      <div className="grid gap-3 xl:grid-cols-[minmax(230px,0.85fr)_minmax(340px,1.65fr)_minmax(265px,1fr)]">
        <Panel title="市场观察" aside={sourceState}>
          <div className="flex flex-wrap gap-1.5 border-b border-rule p-3">
            {STAGES.map(s => (
              <button key={s.key} type="button" aria-pressed={stage === s.key}
                onClick={() => { setStage(s.key); if (explicitMint) { setExplicitMint(null); setSearch(""); setSelectedMint(null); }
                  setResearchResult(null); setDiscoveryResult(null); }}
                className={stage === s.key
                  ? "rounded-full bg-accent px-3 py-1.5 text-xs font-semibold text-accent-ink"
                  : "rounded-full border border-rule-2 px-3 py-1.5 text-xs text-muted hover:text-ink"}>
                {s.label}
              </button>
            ))}
          </div>
          <div className="p-3">
            <label className="sr-only" htmlFor="intelligence-coin-search">筛选代币</label>
            <input id="intelligence-coin-search" value={search} onChange={e => {
              setSearch(e.target.value); setExplicitMint(null); setSelectedMint(null);
              setResearchResult(null); setDiscoveryResult(null);
            }}
              placeholder="搜索名称、代号或 Mint"
              className="w-full rounded-control border border-rule-2 bg-paper px-3 py-2 text-sm text-ink outline-none focus:border-accent" />
            <p className="mt-2 text-xs text-muted">当前显示 {candidates.length} 条 · 保留 Blix 看板顺序，不做隐性机会打分</p>
            {explicitMint && <p role="status" className="mt-2 break-all text-xs text-ink">
              用户指定 Mint：{explicitMint} · {manualArchiveOnly ? "未在当前 Pulse 观察列表，行情未知；仅允许查本地归档" : "Pulse 有该 Mint 的观察记录"}
            </p>}
          </div>
          <div className="max-h-[min(66vh,760px)] overflow-y-auto border-t border-rule p-2">
            {!candidates.length && <p className="p-5 text-sm text-muted">{loaded || restored ? "当前条件下没有观察候选。" : "等待市场数据，不生成模拟代币。"}</p>}
            {candidates.map(({ coin, stage: stageName }) => (
              <button key={coin.mint} type="button" aria-pressed={selected?.coin.mint === coin.mint}
                onClick={() => { setExplicitMint(null); setSelectedMint(coin.mint);
                  setResearchResult(null); setDiscoveryResult(null); }}
                className={selected?.coin.mint === coin.mint
                  ? "mb-1 flex w-full min-w-0 items-start justify-between gap-2 rounded-control border border-accent/60 bg-accent/10 px-3 py-3 text-left"
                  : "mb-1 flex w-full min-w-0 items-start justify-between gap-2 rounded-control border border-transparent px-3 py-3 text-left hover:bg-paper-3"}>
                <span className="min-w-0">
                  <strong className="block truncate text-sm text-ink">{coin.symbol || coin.name || compact(coin.mint)}</strong>
                  <span className="block truncate text-xs text-muted">{STAGE_LABEL[stageName]} · {compact(coin.mint)}</span>
                </span>
                <span className="shrink-0 text-right">
                  <strong className="block text-sm text-ink">{money(coin.mcap)}</strong>
                  <span className="text-xs text-muted">市值</span>
                </span>
              </button>
            ))}
          </div>
        </Panel>

        <div className="flex min-w-0 flex-col gap-3">
          <Panel title="行情与证据入口" aside={c ? "原生 Blix 数据" : "未选择代币"}>
            {c ? (
              <div className="space-y-4 p-4">
                <div className="flex flex-wrap items-start justify-between gap-3">
                  <div className="min-w-0">
                    <h2 className="text-xl font-semibold">{c.symbol || c.name || "未知代币"}</h2>
                    <p className="break-all font-mono text-xs text-muted">{c.mint}</p>
                  </div>
                  <span className="rounded-full border border-rule px-2.5 py-1 text-xs text-muted">{STAGE_LABEL[selected!.stage]}</span>
                </div>
                <div className="grid grid-cols-2 gap-2 sm:grid-cols-3">
                  {[
                    ["市值", money(c.mcap)], ["流动性", money(c.liq)],
                    ["观察窗口成交量", money(windowVol)], ["买卖活动", activity],
                    ["Holder", number(holderCount)], ["Top 10 持仓", percent(top10)],
                  ].map(([label, value]) => (
                    <div key={label} className="rounded-control border border-rule bg-paper-3 px-3 py-3">
                      <div className="text-xs text-muted">{label}</div>
                      <div className="mt-1 break-words text-sm font-semibold text-ink">{value}</div>
                    </div>
                  ))}
                </div>
                <div className="flex flex-wrap gap-2">
                  <a href={coinHref} className="rounded-full bg-accent px-4 py-2 text-sm font-semibold text-accent-ink">打开原生 K 线与钱包图谱</a>
                  <a href={coinHref + "/assistant"} className="rounded-full border border-rule-2 px-4 py-2 text-sm font-semibold text-ink hover:border-accent">前往 Coin AI 助手</a>
                </div>
                <p className="text-xs leading-relaxed text-muted">原版 Coin 页面已有 K 线、交易标记、Bubble Map、Holder 与交易面板，本扩展不重建它们。部分聚合数据、身份标签及时间覆盖仍需逐字段复核。</p>
              </div>
            ) : manualArchiveOnly && researchMint ? (
              <div className="space-y-2 p-4" role="status">
                <h2 className="text-base font-semibold text-ink">用户指定的 Mint · 本地归档调查</h2>
                <p className="break-all font-mono text-xs text-muted">{researchMint}</p>
                <p className="text-xs leading-relaxed text-muted">
                  此 Mint 不在当前 Pulse 观察候选中，因此不显示价格、市值、流动性、Holder 或真实首次可得时间。
                  研究仅限现有本地 SQLite 经济记录；未归档时服务将明确拒绝，不会为该 Mint 付费调用模型。
                </p>
              </div>
            ) : <div className="p-6 text-sm text-muted">请先等待 Blix 数据或选择代币。</div>}
          </Panel>

          {discoveryResult && <Panel title="AI 自主选择的调查对象" aside={discoveryResult.status}>
            <div className="space-y-2 p-4 text-sm">
              <p className="font-semibold">
                {discoveryResult.discovery.selectedMint
                  ? "调查 Mint：" + compact(discoveryResult.discovery.selectedMint)
                  : "未找到足够依据选择调查对象"}
              </p>
              <p>{discoveryResult.discovery.reason}</p>
              <p className="text-xs text-muted">
                比较了 {discoveryResult.discovery.candidateCount} 个当前 Pulse 观察候选。
                {discoveryResult.discovery.marketCoverage}。这只是模型选择的调查目标，不是买入信号。
              </p>
              {!!discoveryResult.discovery.knowledgeUse?.length && <details>
                <summary className="cursor-pointer text-xs font-semibold">
                  选取 Mint 时提供的专业知识（{discoveryResult.discovery.knowledgeUse.length}）
                </summary>
                {discoveryResult.discovery.knowledgeUse.map((k,i)=><p key={i} className="mt-2 break-all text-xs text-muted">
                  {k.source} · {k.outcome}
                </p>)}
              </details>}
              <details><summary className="cursor-pointer text-xs font-semibold">来源与限制</summary>
                <p className="mt-2 text-xs text-muted">{discoveryResult.discovery.sourceFreshness}</p>
                <ul className="mt-1 list-disc pl-5 text-xs text-muted">
                  {discoveryResult.discovery.unknowns.map((x,i)=><li key={i}>{x}</li>)}
                </ul>
              </details>
            </div>
          </Panel>}
          {activeResearch && <Panel title={activeResearch.modelMode === "NOT_USED" ? "本地经济证据 · 未使用AI模型" : "本次模型研究 · 实际收据"} aside={activeResearch.status}>
            <div className="space-y-4 p-4 text-sm">
              <p className="break-words font-semibold">{activeResearch.modelMode === "NOT_USED"
                ? "已读取现有本地SQLite的经济证据；以下都是局部归档事实，不是模型解释。"
                : activeResearch.assessment?.summary || "模型未生成可用研究结论"}</p>
              <p className="text-xs text-muted">来源：{activeResearch.sourceMode}；结论级别：{activeResearch.modelMode === "NOT_USED"
                ? "CAPTURED_LOCAL_ARCHIVE_NOT_FULL_CHAIN_VERIFIED"
                : activeResearch.assessment?.evidenceLevel || "MODEL_NOT_VERIFIED"}。不代表完整历史、交易控制权或盈利机会。</p>
              {trackedWalletActivity && <div className="rounded-control border border-rule p-3">
                <p className="font-semibold">跟踪钱包买入地址统计 · 原版 Research 同口径</p>
                <p className="mt-1 text-xs">本地历史买入地址：{trackedWalletActivity.rawTrackedBuyerAddressCount ?? "UNKNOWN"}；启发式关系组：UNKNOWN；独立经济控制者：UNKNOWN。</p>
                <p className="mt-1 text-xs text-muted">{trackedWalletActivity.evidenceStatus} · {trackedWalletActivity.observationWindow}。这是已有钱包账本中被跟踪的不同地址数，不是独立聪明钱人数，也不代表完整链上历史。</p>
              </div>}
              {!!combinedBuyTransfers.length && <div className="rounded-control border border-rule p-3">
                <p className="font-semibold">同笔买入摘要＋Token 转移指令 · 已捕获候选</p>
                <p className="mt-1 text-xs text-muted">同一签名内的买入摘要和转账是不同事实。旧 WTrack 简化转账列表可能不显示混合交易；这里不将转账记为卖出，也不证明后续卖出的是这批库存。</p>
                {combinedBuyTransfers.map((x,i)=><p key={i} className="mt-2 break-all font-mono text-xs">{x.signature} · {x.fromOwner} → {x.toOwner}</p>)}
              </div>}
              {activeResearch.continuation && <div className="space-y-3 rounded-control border border-rule p-3">
                <h3 className="font-semibold">六个业务环节的实际证据状态</h3>
                {([
                  ["市场观察",activeResearch.continuation.stages.market],
                  ["关键钱包",activeResearch.continuation.stages.keyWallets],
                  ["资金与库存",activeResearch.continuation.stages.capitalAndInventory],
                  ["跨 Mint",activeResearch.continuation.stages.crossMint],
                  ["可参与性",activeResearch.continuation.stages.participation],
                  ["后续观察",activeResearch.continuation.stages.monitoring],
                ] as const).map(([label,status])=><p key={label} className="text-xs">
                  <strong>{label}：</strong><span className="break-all text-muted">{status}</span>
                </p>)}
                {!!activeResearch.continuation.keyWalletCandidates.length && <details>
                  <summary className="cursor-pointer text-sm font-semibold">
                    本地归档中的重点地址候选（{activeResearch.continuation.keyWalletCandidates.length}）
                  </summary>
                  {activeResearch.continuation.keyWalletCandidates.map(w=><p key={w.wallet}
                    className="mt-2 break-all text-xs">
                    {w.wallet} · 捕获事件 {w.observedTransferCount} · 后续卖出摘要 {w.localSellSummaryCount}
                    · {w.addressClass} · 控制者未知
                  </p>)}
                </details>}
                {!!activeResearch.continuation.crossMintCandidates.length && <details>
                  <summary className="cursor-pointer text-sm font-semibold">
                    跨币资金时序候选（{activeResearch.continuation.crossMintCandidates.length}）
                  </summary>
                  {activeResearch.continuation.crossMintCandidates.map((w,i)=><p key={i}
                    className="mt-2 break-all text-xs">
                    {compact(w.otherMint)} · 资金交易 {w.candidateFundingSignature} · 后续买入 {w.candidateBuySignature}
                    · 未证明同一资金来源或共同控制
                  </p>)}
                </details>}
                <p className="text-xs text-muted">
                  跟单可行性：{activeResearch.continuation.followability.status}；
                  没有可靠进出报价与费用收据，不产生收益判断。
                </p>
                <p className="text-xs text-muted">
                  监控：{activeResearch.continuation.watch.status}。
                  当前仅保留本次结果，尚未启动自主监听或跨会话持续调查。
                </p>
              </div>}
              {network && <div className="rounded-control border border-rule p-3">
                <p className="font-semibold">已捕获的 Token 资金/转移关系：{network.eventCount} 条</p>
                <p className="mt-1 text-xs text-muted">{network.coverage} {network.inputTruncated ? "· 样本截断" : ""}</p>
                <div className="mt-3 space-y-2">
                  {network.edges.slice(0, 10).map((e,i) => (
                    <div key={i} className="rounded-control bg-paper-3 p-2 text-xs">
                      <div className="flex flex-wrap items-center gap-2 font-mono">
                        <span title={e.fromOwner}>{compact(e.fromOwner)}</span><span>→</span>
                        <span title={e.toOwner}>{compact(e.toOwner)}</span>
                      </div>
                      <p className="mt-1 text-muted">{e.eventCount} 次捕获转移 · 原始量 {e.observedRawTotal} ·
                        {e.localSellSummaryObserved ? " 后续有本地卖出摘要（非同批库存证明）" : " 未见可确认卖出"} ·
                        跨币候选 {e.crossMintCandidateCount}</p>
                    </div>
                  ))}
                </div>
              </div>}
              {!!activeResearch.assessment?.alternativeExplanations?.length && <div>
                <p className="font-semibold">竞争解释</p>
                <ul className="mt-1 list-disc pl-5">{activeResearch.assessment.alternativeExplanations.map((x,i)=><li key={i}>{x}</li>)}</ul>
              </div>}
              {!!activeResearch.assessment?.nextChecks?.length && <div>
                <p className="font-semibold">下一步证据检查</p>
                <ul className="mt-1 list-disc pl-5">{activeResearch.assessment.nextChecks.map((x,i)=><li key={i}>{x}</li>)}</ul>
              </div>}
              <details className="border-t border-rule pt-3">
                <summary className="cursor-pointer font-semibold">真实工具调用（{activeResearch.evidence.length}）</summary>
                <div className="mt-2 space-y-2">{activeResearch.evidence.map((e,i)=><p key={i} className="rounded-control bg-paper-3 p-2 text-xs">
                  {e.capability} · {e.result?.status || e.error || "UNKNOWN"} · {e.result?.sources?.map(x=>x.provider).join(", ") || "无来源"}
                </p>)}</div>
              </details>
              {activeResearch.modelMode !== "NOT_USED" && <details className="border-t border-rule pt-3">
                <summary className="cursor-pointer font-semibold">提供给模型的知识来源（{activeResearch.knowledgeUse.length} 条阶段记录）</summary>
                <div className="mt-2 space-y-2">{activeResearch.knowledgeUse.map((k,i)=><p key={i} className="break-all rounded-control bg-paper-3 p-2 text-xs">
                  {k.stage} · {k.source} · {k.outcome}
                </p>)}</div>
                <p className="mt-2 text-xs text-muted">来源提供给模型不等于模型正确使用它。</p>
              </details>}
              {!!activeResearch.unknowns?.length && <details className="border-t border-rule pt-3" open>
                <summary className="cursor-pointer font-semibold">仍然未知（{activeResearch.unknowns.length}）</summary>
                <ul className="mt-2 list-disc pl-5 text-xs">{activeResearch.unknowns.slice(0, 14).map((x,i)=><li key={i}>{x}</li>)}</ul>
              </details>}
            </div>
          </Panel>}
          <Panel title="机会研究与反证" aside="候选 ≠ 可成交机会">
            <div className="grid gap-3 p-4 sm:grid-cols-2">
              <div className="rounded-control border border-rule bg-paper-3 p-4">
                <h3 className="text-sm font-semibold">已知的观察</h3>
                <p className="mt-2 text-sm leading-relaxed text-ink-2">
                  {c ? "Blix 当前记录：" + activity + "；Holder " + number(holderCount) + "；Top 10 " + percent(top10) + "。上述是界面来源数据，不等于独立验证。" : "暂无可引用的市场观察。"}
                </p>
                {c?.ai?.verdict && <p className="mt-2 text-xs text-muted">原 Blix AI 意见（未复核）：{c.ai.verdict}</p>}
              </div>
              <div className="rounded-control border border-rule bg-paper-3 p-4">
                <h3 className="text-sm font-semibold">尚未验证的关键问题</h3>
                <p className="mt-2 text-sm leading-relaxed text-ink-2">
                  资金关系是否真实独立？是否有刷量、关联转仓或公共基础设施？信号出现之后是否还能以合理滑点成交并完整退出？
                </p>
              </div>
            </div>
            <p className="border-t border-rule px-4 py-3 text-xs text-muted">
              市场观察来自原版 Blix；可选择本地只读模型研究（需要独立启用）。模型输出不能证明全链覆盖、盈利或真实成交。
            </p>
          </Panel>
        </div>

        <Panel title="AI 研究助手" aside="任务准备 / 本地只读调用">
          <div className="space-y-4 p-4">
            <div className="rounded-control border border-rule bg-paper-3 p-3 text-sm leading-relaxed text-ink-2">
              你可以用普通语言提出研究目的。独立服务启用后，模型可按需读取专业知识与已捕获的本地 SQLite 经济证据；否则仍可复制任务。本机以外的网页暂不开放研究调用。
            </div>
            <label htmlFor="intelligence-research-goal" className="block text-sm font-semibold">你希望 AI 研究什么？</label>
            <textarea id="intelligence-research-goal" rows={6} maxLength={1600} value={goal}
              onChange={e => setGoal(e.target.value)}
              className="w-full resize-y rounded-control border border-rule-2 bg-paper px-3 py-3 text-sm text-ink outline-none focus:border-accent" />
            <div className="flex flex-wrap gap-2">
              {PROMPTS.map((prompt, i) => (
                <button type="button" key={prompt} onClick={() => setGoal(prompt)}
                  className="rounded-full border border-rule-2 px-3 py-1.5 text-xs text-ink-2 hover:border-accent">
                  {["资金路径", "交易可行性", "竞争解释"][i]}
                </button>
              ))}
            </div>
            <details className="rounded-control border border-rule bg-paper-3 p-3" open>
              <summary className="cursor-pointer text-sm font-semibold text-ink">
                专业知识依据预览（{candidateKnowledge.length} 项候选）
              </summary>
              <p className="mt-2 text-xs leading-relaxed text-muted">
                对应 Blix 已承接的 Hermes、qb-、meme-、ai-d 等研究。此处只根据问题显示可能相关的来源，
                尚未运行服务器知识检索，也不代表 AI 实际采用了它们。
              </p>
              <div className="mt-3 space-y-2">
                {candidateKnowledge.length ? candidateKnowledge.map(x => (
                  <a key={x.id} href={KNOWLEDGE_ROOT + x.path} target="_blank" rel="noopener noreferrer"
                    className="block rounded-control border border-rule-2 px-3 py-2 text-sm hover:border-accent">
                    <span className="block font-semibold text-ink">{x.label}</span>
                    <span className="block text-xs text-muted">{x.heritage} · 查看来源与适用限制</span>
                  </a>
                )) : <p className="text-xs text-muted">此问题暂无静态匹配项；不代表历史资料中没有相关知识。</p>}
              </div>
              <p className="mt-3 text-xs text-muted">
                真正的模型运行记录应显示实际读取的来源、版本、工具调用及判断，而非这些推荐链接。
              </p>
            </details>
            <button type="button" onClick={() => void runPulseDiscovery()}
              disabled={!goal.trim() || !researchHealth?.ready || researchHealth.remainingTasks < 1 ||
                researchBusy || !loaded || !(connected || polling) || !discoveryCandidates.length}
              className="w-full rounded-full bg-accent px-4 py-2.5 text-sm font-semibold text-accent-ink disabled:cursor-not-allowed disabled:opacity-40">
              {researchBusy ? "正在研究…" : "AI 从当前 Pulse 候选中自主选择并调查"}
            </button>
            <p className="text-xs leading-relaxed text-muted">
              当前可比较 {discoveryCandidates.length} 个候选，来源为本浏览器显示的 Blix Pulse。
              只在实时流或轮询可用时开放。模型会增加一次选取步骤，可能产生模型 API 费用，
              但不会自动买卖、爬取全市场或宣称已发现盈利机会。
            </p>
            <button type="button" onClick={() => void runLocalInspection()}
              disabled={!researchMint || !researchHealth?.inspectionReady ||
                researchHealth.remainingInspections === 0 || researchBusy}
              className="w-full rounded-full border border-rule-2 px-4 py-2.5 text-sm font-semibold text-ink hover:border-accent disabled:cursor-not-allowed disabled:opacity-40">
              {researchBusy ? "正在检查本地证据…" : "免费查看指定 Mint 的本地经济证据（不使用AI）"}
            </button>
            <p className="text-xs leading-relaxed text-muted">
              直接读取已经存在的本地SQLite，不需要模型密钥、费用开关或Pulse行情；不能发现尚未归档的交易。
              {researchHealth?.inspectionReady
                ? " 本次进程剩余证据检查次数：" + (researchHealth.remainingInspections ?? "未知") + "。"
                : " 当前尚未连接可读的经济归档。"}
            </p>
            <button type="button" onClick={() => void runLocalResearch()}
              disabled={!researchMint || !goal.trim() || !researchHealth?.ready || researchHealth.remainingTasks < 1 || researchBusy}
              className="w-full rounded-full border border-accent px-4 py-2.5 text-sm font-semibold text-ink disabled:cursor-not-allowed disabled:opacity-40">
              {researchBusy ? "正在执行只读调查…" : manualArchiveOnly ? "调查指定 Mint 的本地经济归档" : "运行本地 AI 证据研究"}
            </button>
            <p className="text-xs text-muted">
              {SIDECAR_URL
                ? researchHealth?.ready
                  ? "独立只读服务已配置；本次进程剩余任务：" + researchHealth.remainingTasks + "。点击会调用已配置的模型 API，可能产生费用。"
                  : "模型尚未连接：需在本机单独启动研究服务，并配置已有 SQLite、模型密钥和显式费用开关。"
                : "当前不是本机 HTTP 页面；为避免公开页面绕过权限，请通过本机 Blix 页面使用研究服务。"}
            </p>
            {researchError && <p role="alert" className="rounded-control border border-rule p-2 text-xs text-ink">研究请求未完成：{researchError}</p>}
            <button type="button" onClick={() => void copyTask()} disabled={!researchMint || !goal.trim()}
              className="w-full rounded-full bg-accent px-4 py-2.5 text-sm font-semibold text-accent-ink disabled:cursor-not-allowed disabled:opacity-40">
              复制带数据的研究任务
            </button>
            <p className="text-xs leading-relaxed text-muted">
              本页不会自动调用模型。手动启动的独立研究只读本地既有归档，不向市场发送交易、签名或钱包指令；数据覆盖不等于全链。上方候选知识链接仍是静态预览，只有研究结果区才显示实际提供给模型的来源。
            </p>
          </div>
        </Panel>
      </div>
    </Page>
  );
}
