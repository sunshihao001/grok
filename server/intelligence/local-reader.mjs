// Explicit local-only Blix API reader; no requests are made at import time.
// An external provider/API is never accepted as a URL from capability input.
const MINT = "[1-9A-HJ-NP-Za-km-z]{32,44}";
const ALLOWED = new RegExp("^(?:/api/token/" + MINT + "|/api/holders/" + MINT + "\\?top=25)$");

export function makeLocalBlixReader({ port = 4420, transport = fetch } = {}) {
  if (!Number.isInteger(port) || port < 1 || port > 65535) throw new Error("Invalid local Blix port");
  if (typeof transport !== "function") throw new Error("Invalid transport");
  return async (path) => {
    if (typeof path !== "string" || !ALLOWED.test(path)) throw new Error("Path is not an approved local Blix GET endpoint");
    const response = await transport("http://127.0.0.1:" + port + path, {
      method: "GET", redirect: "error", signal: AbortSignal.timeout(10000),
      headers: { accept: "application/json" },
    });
    const data = await response.json().catch(() => null);
    return { ok: response.ok, status: response.status, data, error: response.ok ? null : data?.error || "HTTP " + response.status };
  };
}
