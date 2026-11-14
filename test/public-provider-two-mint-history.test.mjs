// Uses a frozen, source-hashed public vendor snapshot recovered from an actual
// 2026-11-01 GitHub Actions artifact. No synthetic second Mint, API, wallet,
// trading, inferred Pulse board, or real-fill claims are permitted.
import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { evaluatePaperFollowabilityCase } from '../server/intelligence/followability-replay.mjs';
import { validatePulseDiscoveryInput } from '../server/intelligence/pulse-discovery.mjs';

const data=JSON.parse(readFileSync(new URL('./fixtures/public-provider-two-mints-20261101.json',import.meta.url),'utf8'));
const [bnb,sis]=data.snapshots;

test('two genuinely observed Mint queries belong to the same source run, not a Blix market candidate universe',()=>{
  assert.equal(data.originalActionRun,41266389009);
  assert.equal(data.snapshots.length,2);
  assert.equal(new Set(data.snapshots.map(x=>x.mint)).size,2);
  for(const s of data.snapshots){
    assert.match(s.providerRawSha256,/^[0-9a-f]{64}$/);
    assert.ok(s.main.liquidityUsd>0);
    assert.ok(s.thin.liquidityUsd>0);
  }
  assert.ok(Math.abs(Date.parse(bnb.retrievedAt)-Date.parse(sis.retrievedAt))<1000);
  assert.equal(data.signalFirstAvailableAtMs,null);
  assert.match(data.marketCoverage,/NOT_A_COMPLETE_BLIX_PULSE_BOARD/);
  // The historical vendor file is intentionally NOT a valid browser Pulse
  // shortlist. Making it look like one would fabricate original Blix coverage.
  assert.throws(()=>validatePulseDiscoveryInput({
    goal:'Historical observations were two explicit vendor queries',
    candidates:data.snapshots,
    browserRecordedAtMs:Date.parse(bnb.retrievedAt),
    boardStatus:'HISTORICAL_VENDOR_SNAPSHOT',
  },Date.parse(bnb.retrievedAt)),/DISCOVERY_INPUT_INVALID_OR_STALE/);
});

test('extra pool count and apparent cross-pool percentage gap cannot establish executable arbitrage',()=>{
  assert.equal(bnb.pairCount,5);
  assert.equal(sis.pairCount,7);
  // Seven returned pools do not mean seven comparably executable venues.
  assert.equal(sis.otherPoolObservations.unpriced,4);
  assert.ok(sis.main.liquidityUsd/sis.thin.liquidityUsd>1000);
  assert.ok(bnb.main.liquidityUsd/bnb.thin.liquidityUsd>1800);
  const apparentDifferencePct=(sis.thin.priceUsd/sis.main.priceUsd-1)*100;
  assert.ok(apparentDifferencePct<-24 && apparentDifferencePct>-26);
  assert.ok(sis.thin.liquidityUsd<60);
  assert.ok(data.limitations.includes('CROSS_POOL_MID_PRICE_DIFFERENCE_NOT_ARBITRAGE'));
  // Deliberately no advice/return here: missing synchronous executable quotes
  // for order size, both legs, pool curves and fees.
});

test('real observed prices with no follower-visible signal and no executable fills remain UNKNOWN',()=>{
  const m=Date.parse(bnb.retrievedAt);
  const noSignal=evaluatePaperFollowabilityCase({id:'real-snapshot-no-fill',mint:bnb.mint,
    signal:{chainEventAtMs:m,firstAvailableAtMs:null}});
  assert.equal(noSignal.status,'UNKNOWN_SIGNAL_AVAILABILITY');
  const noEntry=evaluatePaperFollowabilityCase({id:'real-snapshot-no-entry',mint:sis.mint,
    signal:{chainEventAtMs:m,firstAvailableAtMs:m}});
  assert.equal(noEntry.status,'MISSING_ENTRY_EXECUTION');
  assert.ok(data.limitations.includes('NO_REAL_MODEL_A_B_SELECTION_OR_ECONOMIC_ADVANTAGE_MEASURED'));
});
