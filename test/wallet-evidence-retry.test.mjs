// End-to-end offline wallet-reader regression. Never start Blix or access RPC.
import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
process.env.RADAR_DATA = fs.mkdtempSync(path.join(os.tmpdir(), "blix-economic-wallet-retry-"));
process.env.BLIX_MARKET_FEEDS = "0";
const wallets = await import("../server/wallets.js");
const { db } = await import("../server/db.js");
const { walletProcessing, transactionEvidence } = await import("../server/economic-events.mjs");
const A = "4p7SeR6361WJ4T4icgsYTnzAUzfA5NwM4CwYD9kMBjuK";
const B = "BTmCme13XXrD3VLxXFChL9VnmicJ5PjkVUpAsjrooEYh";
const M = "GTNHLKQWKZHaHpd6PjfMgfFZUDEuCviwXMwYbCcepump";
function fixture(sig) {
  return {
    slot: 191, blockTime: 1700000000,
    transaction: { signatures: [sig], message: {
      accountKeys: [{ pubkey: A, signer: true }, { pubkey: B }],
      instructions: [{ programId: "unparsed_fixture", data: "opaque", accounts: [A, B] }],
    } },
    meta: { err: null, fee: 5000, preBalances: [1000000000, 100000000],
      postBalances: [999995000, 100000000], preTokenBalances: [],
      postTokenBalances: [], innerInstructions: [], logMessages: ["offline"] },
  };
}
const job = sig => ({ sig, quiet: true, t: 1700000000000 });
const scan = address => ({ address, scan: true });

test("pre-existing live feed wallet_trades never replaces raw RPC capture", async () => {
  const sig = "prior-live-trade";
  db.prepare("INSERT INTO wallet_trades(sig,wallet,mint,side,tokens,sol,usd,t,payer) VALUES(?,?,?,?,?,?,?,?,?)")
    .run(sig,A,M,"buy",1,1,150,1700000000000,null);
  let n=0;
  wallets.onTx((w,tx,j) => { if (j.sig === sig) n++; });
  await wallets.readTx(scan(A),job(sig),null,fixture(sig));
  assert.equal(n,1);
  assert.equal(walletProcessing(db,sig,A).state,"COMPLETE");
  assert.equal(transactionEvidence(db,sig).rpc.transaction.signatures[0],sig);
});

test("failed downstream hook is RETRY_REQUIRED and replay uses persisted RPC without an HTTP call", async () => {
  const sig = "retry-hook", original = fixture(sig);
  let count = 0;
  wallets.onTx((w, tx, j) => {
    if (j.sig !== sig) return;
    count++;
    assert.equal(tx.transaction.signatures[0], sig);
    if (count === 1) throw new Error("injected downstream failure");
  });
  await assert.rejects(wallets.readTx(scan(A),job(sig),null,original),/injected downstream failure/);
  assert.equal(count,1);
  const failed=walletProcessing(db,sig,A);
  assert.equal(failed.state,"RETRY_REQUIRED");
  assert.equal(failed.attempts,1);
  assert.match(failed.last_error,/injected/);
  assert.deepEqual(transactionEvidence(db,sig).rpc,original);
  // No 'fetched' argument: RPC is deliberately unavailable in this offline test.
  // A successful second call necessarily uses the local captured evidence.
  await wallets.readTx(scan(A),job(sig));
  assert.equal(count,2);
  assert.equal(walletProcessing(db,sig,A).state,"COMPLETE");
  assert.equal(walletProcessing(db,sig,A).attempts,2);
  assert.equal(db.prepare("SELECT COUNT(*) n FROM econ_transactions WHERE sig=?").get(sig).n,1);
  await wallets.readTx(scan(A),job(sig));
  assert.equal(count,2,"completed signature is not consumed twice");
});

test("the same signature is processed separately for B using the shared stored transaction", async () => {
  const sig = "shared-by-two-wallets";
  const heard = [];
  wallets.onTx((w,tx,j) => { if(j.sig===sig) heard.push(w.address); });
  await wallets.readTx(scan(A),job(sig),null,fixture(sig));
  await wallets.readTx(scan(B),job(sig));
  assert.deepEqual(heard,[A,B]);
  assert.equal(walletProcessing(db,sig,A).state,"COMPLETE");
  assert.equal(walletProcessing(db,sig,B).state,"COMPLETE");
  assert.equal(db.prepare("SELECT COUNT(*) n FROM econ_transactions WHERE sig=?").get(sig).n,1);
});

test("missing or malformed RPC capture cannot be marked successfully processed", async () => {
  const sig = "bad-rpc";
  await assert.rejects(wallets.readTx(scan(A),job(sig),null,{transaction:{message:{}},meta:null}),/Missing transaction/);
  assert.equal(walletProcessing(db,sig,A),null);
});
