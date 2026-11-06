import test from "node:test";
import assert from "node:assert/strict";
import { listCapabilities, runCapability } from "../server/intelligence/index.mjs";
import { makeLocalBlixReader } from "../server/intelligence/local-reader.mjs";

const mint = "EYqygbhZjP7EbM4fSn8devctnksAvPAD1Bt57XBFpump";

test("one allowlisted capability is visible; no implicit execution", async () => {
  assert.deepEqual(listCapabilities().map((x) => x.id), ["mint-facts"]);
  await assert.rejects(() => runCapability("../server/accounts.js", { mint }), /Unknown or unauthorized/);
});

test("Mint and Holder facts preserve provenance, partial coverage and source tags", async () => {
  const called = [];
  const read = async (path) => {
    called.push(path);
    return path.includes("/token/") ?
      { ok: true, status: 200, data: { token: { mint, symbol: "EX", name: "Example", creator: "candidate", fresh: { source: "blix-feed", ageMs: 300 } } } } :
      { ok: true, status: 200, data: { holders: 10, top10: 45.2, partial: true, top: [{ wallet: "address1", pct: 12, tag: "bundle" }] } };
  };
  assert.equal(called.length, 0);
  const result = await runCapability("mint-facts", { mint, read, now: () => Date.parse("2026-11-06T00:00:00Z") });
  assert.equal(called.length, 2);
  assert.equal(result.status, "OBSERVED_UNVERIFIED");
  assert.equal(result.facts.holderLedger.sourceCoverage, "PARTIAL_OR_UNKNOWN");
  assert.equal(result.facts.holderLedger.top[0].sourceTag, "bundle");
  assert.equal(result.facts.holderLedger.top[0].observedAddress, "address1");
  assert.match(result.unknowns.join(" "), /controller/);
  assert.equal(result.observedAt, "2026-11-06T00:00:00.000Z");
});

test("unavailable ledger is not silently called complete", async () => {
  const read = async (p) => p.includes("/token/") ?
    { ok: true, status: 200, data: { token: { mint } } } :
    { ok: false, status: 404, error: "not tracked" };
  const result = await runCapability("mint-facts", { mint, read });
  assert.equal(result.status, "PARTIAL");
  assert.equal(result.facts.holderLedger, null);
  assert.equal(result.sources[1].httpStatus, 404);
});

test("mismatching source Mint is reported, never accepted", async () => {
  const read = async () => ({ ok: true, status: 200, data: { token: { mint: "wrong" } } });
  const result = await runCapability("mint-facts", { mint, read });
  assert.equal(result.status, "SOURCE_MISMATCH");
  assert.equal(result.facts.token, null);
});

test("local API reader only issues fixed GET routes on loopback", async () => {
  const calls = [];
  const read = makeLocalBlixReader({ port: 4420, transport: async (url, options) => {
    calls.push({ url, method: options.method });
    return { ok: true, status: 200, json: async () => ({ ok: true }) };
  } });
  await assert.rejects(() => read("/api/account/buy"), /not an approved/);
  await assert.rejects(() => read("https://evil.test/api/token/" + mint), /not an approved/);
  await read("/api/token/" + mint);
  assert.deepEqual(calls, [{ url: "http://127.0.0.1:4420/api/token/" + mint, method: "GET" }]);
});
