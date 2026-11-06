// A real read-only business capability: normalize the existing Blix Mint/Holder API.
// It does not import Blix's global server, open sockets, request keys, or schedule work.
export const manifest = Object.freeze({ id: "mint-facts", readonly: true, version: "0.1", inputs: ["mint"], outputs: ["facts", "sources", "unknowns"] });
const MINT = /^[1-9A-HJ-NP-Za-km-z]{32,44}$/;

export async function run({ mint, read, now = Date.now } = {}) {
  if (!MINT.test(String(mint || ""))) throw new Error("Invalid Solana Mint address");
  if (typeof read !== "function") throw new Error("A read-only data reader must be provided");
  const paths = ["/api/token/" + mint, "/api/holders/" + mint + "?top=25"];
  async function one(path) {
    try {
      const r = await read(path);
      return { path, ok: r?.ok === true, status: Number(r?.status) || 0, data: r?.data ?? null, error: r?.error ?? null };
    } catch (error) {
      return { path, ok: false, status: 0, data: null, error: String(error?.message || error) };
    }
  }
  const [token, holders] = await Promise.all(paths.map(one));
  const t = token.ok ? token.data?.token : null;
  const wrongMint = Boolean(t && t.mint !== mint);
  const validToken = Boolean(t && typeof t === "object" && t.mint === mint);
  const rawHolders = holders.ok && holders.data && typeof holders.data === "object" ? holders.data : null;
  const h = rawHolders && (Number.isFinite(rawHolders.holders) || Array.isArray(rawHolders.top)) ? rawHolders : null;
  const top = Array.isArray(h?.top) ? h.top.slice(0, 25) : [];
  const facts = {
    token: validToken ? {
      mint: t.mint, symbol: t.symbol ?? null, name: t.name ?? null,
      creatorCandidate: t.creator ?? null, dex: t.dex ?? null,
      firstSeen: t.first_seen ?? null, priceSource: t.fresh?.source ?? null,
      priceAgeMs: t.fresh?.ageMs ?? null,
    } : null,
    holderLedger: h ? {
      reportedHolders: h.holders ?? null, top10Pct: h.top10 ?? null,
      windowStart: h.since ?? null, lastObserved: h.last ?? null,
      sourceCoverage: h.partial === false ? "BLIX_REPORTS_NONPARTIAL" : "PARTIAL_OR_UNKNOWN",
      top: top.map((r) => ({
        observedAddress: r.wallet ?? null, pct: r.pct ?? null,
        sourceTag: r.tag ?? null, // A supplier tag, NOT shared-control evidence.
      })),
    } : null,
  };
  const unknowns = [
    "Wallet/address tags do not identify the ultimate economic controller.",
    "Token Account owners and fee payers are not independently resolved here.",
    "These Blix endpoints do not prove complete historical transfers, swaps or funding paths.",
    "No prediction, insider identity, coordinated control, or trading advantage is established.",
  ];
  if (h && h.partial !== false) unknowns.push("Holder ledger reports missing or unverified coverage.");
  if (!token.ok || !facts.token) unknowns.push("Token details are unavailable or mismatched.");
  if (!h) unknowns.push("Holder ledger is unavailable or malformed.");
  if (wrongMint) unknowns.push("Token response Mint does not match the requested Mint.");
  const status = wrongMint ? "SOURCE_MISMATCH" : validToken && h ? "OBSERVED_UNVERIFIED" : validToken || h ? "PARTIAL" : "UNAVAILABLE";
  return {
    schemaVersion: "0.1", capability: manifest.id, mint, status,
    observedAt: new Date(now()).toISOString(), evidenceLevel: "BLIX_API_NOT_INDEPENDENTLY_CHAIN_VERIFIED",
    sources: [token, holders].map(({ path, ok, status, error }) => ({ provider: "LOCAL_BLIX", method: "GET", path, ok, httpStatus: status, error })),
    facts, unknowns,
  };
}
