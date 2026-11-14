// Regression: a tracked-wallet alert must separate raw addresses from
// heuristic grouping. Neither co-trading nor a shared fee payer proves one
// operator, and near-simultaneous buys do not establish independent demand.
// Uses throwaway local SQLite, an injected safety result and no RPC/model/trade.
import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';

process.env.RADAR_DATA = fs.mkdtempSync(path.join(os.tmpdir(), 'blix-wallet-signal-'));
process.env.BLIX_MARKET_FEEDS = '0';
const { db } = await import('../server/db.js');
const wallets = await import('../server/wallets.js');

const A = '4p7SeR6361WJ4T4icgsYTnzAUzfA5NwM4CwYD9kMBjuK';
const B = 'BTmCme13XXrD3VLxXFChL9VnmicJ5PjkVUpAsjrooEYh';
const C = '9VQ3dtwAxUAxNPdD86ExhC1XsL1hiUcqEvzS4sAhUU1A';
const MINT = 'GTNHLKQWKZHaHpd6PjfMgfFZUDEuCviwXMwYbCcepump';

test('wallet signals retain raw address count, heuristic group count and non-control interpretation', async () => {
  const a = wallets.addWallet(A, 'Wallet A', 'you');
  wallets.addWallet(B, 'Wallet B', 'you');
  wallets.addWallet(C, 'Wallet C', 'you');

  // A/B share the third-party transaction fee payer C. C itself buys too.
  // There are three distinct addresses, but only two heuristic groups.
  const t = Date.now() - 25_000;
  const insert = db.prepare('INSERT INTO wallet_trades (sig,wallet,mint,side,tokens,sol,usd,t,payer) VALUES (?,?,?,?,?,?,?,?,?)');
  insert.run('synthetic-buy-A', A, MINT, 'buy', 100, 0.3, 30, t, C);
  insert.run('synthetic-buy-B', B, MINT, 'buy', 100, 0.3, 30, t + 4_000, C);
  insert.run('synthetic-buy-C', C, MINT, 'buy', 100, 0.3, 30, t + 9_000, null);

  const token = { mint: MINT, symbol: 'TEST', pair: 'synthetic-pool',
    asset_class: 'meme', safety_score: 88, score: 70, mcap: 40_000, price: 0.001 };
  const calls = [];
  const raise = (_token, kind, title, detail, _priority, mark) => {
    calls.push({ kind, title, detail, mark });
  };
  const adopt = (mint) => assert.equal(mint, MINT);
  await wallets.walletSignals(
    { wallet: a, trade: { side: 'buy', mint: MINT, sol: 0.3, usd: 30 } },
    raise, adopt, async () => ({ ok: true, token })
  );
  const smart = calls.find(x => x.kind === 'smart');
  assert.ok(smart, 'the observed tracked-wallet buys should still emit a smart activity alert');
  assert.match(smart.title, /^2 tracked-wallet groups bought \$TEST/);
  assert.match(smart.detail, /3 tracked wallet addresses/);
  assert.match(smart.detail, /2 heuristic groups/);
  assert.match(smart.detail, /independent economic actors UNKNOWN/);
  assert.match(smart.detail, /shared fee payer; that is not proof of common control/);
  assert.match(smart.detail, /timing alone does not establish common control or independent demand/);
  assert.doesNotMatch(smart.detail, /usually means one operator/);
  assert.deepEqual(smart.mark, {});

  // The same observed wallets never bypass the existing safety gate.
  const unsafe = [];
  await wallets.walletSignals(
    { wallet: a, trade: { side: 'buy', mint: MINT, sol: 0.3, usd: 30 } },
    (_tk, kind, title, detail, _p, mark) => unsafe.push({ kind, title, detail, mark }),
    adopt,
    async () => ({ ok: false, reasons: ['unsafe synthetic liquidity'], token })
  );
  const blocked = unsafe.find(x => x.kind === 'smart');
  assert.ok(blocked);
  assert.match(blocked.title, /failed safety/);
  assert.match(blocked.detail, /Not safety-screened: unsafe synthetic liquidity/);
  assert.equal(blocked.mark.safe, false);
});
