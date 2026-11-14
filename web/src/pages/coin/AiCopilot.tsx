// Context-aware investigation entry on a Coin page.
// This first UI slice prepares a real, Mint-bound research task without calling a model,
// making trades, or opening new provider/network connections.
import { useState } from "react";
import type { CoinData, TokenDetail } from "@/lib/coin";
import { toast } from "@/components/ui/toast";

const FOCUS = [
  { id: "wallets", label: "Wallet relationships", question: "Investigate holder concentration, suspected related wallets, shared funders and alternative explanations. Separate Token Accounts from owners; do not infer common control from labels alone." },
  { id: "transfers", label: "Buy → transfer → sell", question: "Look for the complete buy → token transfer → recipient sell path; check historical coverage, signature-level evidence, recipient discovery, and missing data." },
  { id: "creator", label: "Creator & supply", question: "Investigate creator history, inventory distribution, bundle candidates, supply concentration and which competing mechanisms could explain them." },
  { id: "market", label: "Market mechanism", question: "Explain recent price/volume/holder activity, market participation and what additional evidence would differentiate competing explanations." },
] as const;

type Props = { mint: string; token: TokenDetail; coin: CoinData | null };

const numeric = (v: number | null | undefined, digits = 0) =>
  typeof v === "number" && Number.isFinite(v) ? v.toFixed(digits) : "UNKNOWN";

export function CoinAiCopilot({ mint, token, coin }: Props) {
  const [focus, setFocus] = useState<(typeof FOCUS)[number]["id"]>("wallets");
  const [question, setQuestion] = useState<string>(FOCUS[0].question);
  const source = coin?.holders?.source || "Blix (source unspecified)";
  const coverage = coin?.holders ? (coin.holders.partial ? "PARTIAL" : "BLIX_REPORTED_NOT_PARTIAL") : "UNKNOWN";
  const research = token.research;

  function buildTask() {
    // Snapshot is descriptive only. Do not imply that a Blix dashboard tag or a stored AI
    // grade is independently verified, or that the whole history has been captured.
    return [
      "BLIX AI RESEARCH TASK (read-only, no trading)",
      `Current coin: ${token.token.name || "Unknown"} (${token.token.symbol || "?"})`,
      `Mint: ${mint}`,
      `User task: ${question.trim()}`,
      "Displayed context — Blix Coin page snapshot, NOT independently chain-verified:",
      `Holder source: ${source}`,
      `Holder coverage: ${coverage}`,
      `Holders shown by Blix: ${numeric(coin?.info?.holders ?? coin?.holders?.count)}`,
      `Top 10 concentration: ${numeric(coin?.info?.top10, 2)}%`,
      `Bundle-tagged group share: ${numeric(coin?.info?.bundle?.pct, 2)}%`,
      `Five-minute buy transactions: ${numeric(coin?.m5?.buys)}`,
      `Five-minute sell transactions: ${numeric(coin?.m5?.sells)}`,
      `Existing Blix AI read (not a verified fact): ${research?.verdict || "UNAVAILABLE"}`,
      "Investigate with approved tools. Separate observed data, source labels, competing",
      "interpretations and UNKNOWN. Identify relevant time windows and missing wallet",
      "history. Do not sign, trade, broadcast or spend model/provider credits without authorization.",
    ].join("\n");
  }

  const copyTask = async () => {
    if (!question.trim()) { toast("Enter a research question first"); return; }
    try {
      await navigator.clipboard.writeText(buildTask());
      toast("Mint-bound research task copied");
    } catch { toast("Could not copy the task"); }
  };

  return (
    <section aria-label="AI investigation assistant" className="flex flex-col gap-4 p-4">
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div className="min-w-0">
          <h3 className="text-lg font-semibold text-ink">AI investigation assistant</h3>
          <p className="mt-1 text-sm text-ink-2">
            Bound to the coin you have open. The original AI read, chart, trading and wallet tools remain unchanged.
          </p>
          <p className="mt-2 break-all font-mono text-xs text-muted" title={mint}>
            {token.token.symbol || "?"} · {mint}
          </p>
        </div>
        <span className="rounded-chip border border-rule-2 bg-paper-3 px-2.5 py-1 text-xs font-semibold text-ink-2">Preview · agent not connected</span>
      </div>

      <div className="flex flex-wrap gap-2" role="group" aria-label="Investigation focus">
        {FOCUS.map((item) => (
          <button key={item.id} type="button" onClick={() => { setFocus(item.id); setQuestion(item.question); }}
            aria-pressed={focus === item.id}
            className={focus === item.id
              ? "rounded-chip border border-accent bg-accent/15 px-3 py-2 text-sm font-semibold text-ink"
              : "rounded-chip border border-rule-2 bg-paper-3 px-3 py-2 text-sm text-ink-2 hover:text-ink"}>
            {item.label}
          </button>
        ))}
      </div>

      <label className="flex flex-col gap-2 text-sm font-semibold text-ink-2">
        Your question about this coin
        <textarea value={question} maxLength={1600} rows={3} onChange={(e) => setQuestion(e.target.value)}
          className="min-h-24 w-full resize-y rounded-control border border-rule-2 bg-paper-2 px-3 py-2 text-md font-normal text-ink outline-none focus:border-accent"
          placeholder="What should the AI investigate about this Mint?" />
      </label>

      <div className="grid grid-cols-2 gap-2 text-sm sm:grid-cols-4">
        <div className="rounded-control border border-rule bg-paper-3 p-2.5">
          <div className="text-xs text-muted">Observed holders</div>
          <div className="mt-1 font-semibold text-ink">{numeric(coin?.info?.holders ?? coin?.holders?.count)}</div>
        </div>
        <div className="rounded-control border border-rule bg-paper-3 p-2.5">
          <div className="text-xs text-muted">Top 10 share</div>
          <div className="mt-1 font-semibold text-ink">{numeric(coin?.info?.top10, 2)}%</div>
        </div>
        <div className="rounded-control border border-rule bg-paper-3 p-2.5">
          <div className="text-xs text-muted">Holder coverage</div>
          <div className="mt-1 font-semibold text-ink">{coverage}</div>
        </div>
        <div className="rounded-control border border-rule bg-paper-3 p-2.5">
          <div className="text-xs text-muted">Existing AI read</div>
          <div className="mt-1 font-semibold text-ink">{research?.grade || research?.status || "Unavailable"}</div>
        </div>
      </div>

      <div className="flex flex-wrap items-center justify-between gap-3 border-t border-rule pt-3">
        <p className="max-w-xl text-xs leading-relaxed text-muted">
          This version prepares a contextual task using data already visible in Blix. It does not
          independently verify the chain or run a new model. Connect the approved agent endpoint
          only after model permission, server isolation and full integration tests.
        </p>
        <button type="button" onClick={copyTask} disabled={!question.trim()}
          className="shrink-0 rounded-full bg-accent px-4 py-2 text-sm font-semibold text-accent-ink disabled:opacity-50">
          Copy research task
        </button>
      </div>
    </section>
  );
}
