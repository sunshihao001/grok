import test from 'node:test';
import assert from 'node:assert/strict';
import { projectMintNetwork } from '../server/intelligence/economic-network.mjs';
import { compareCapturedMintSnapshots,compareCapturedCrossMintWallets } from '../server/intelligence/economic-snapshot-review.mjs';

const M='GTNHLKQWKZHaHpd6PjfMgfFZUDEuCviwXMwYbCcepump';
const N='EYqygbhZjP7EbM4fSn8devctnksAvPAD1Bt57XBFpump';
const row=(signature,fromOwner,toOwner,outerI=0,innerI=-1)=>({
  signature,outerI,innerI,fromOwner,toOwner,mint:M,amountRaw:'100',
  blockTime:1700000000,slot:1234,
});
const snap=(mint,recipients,date)=>({
  observedAt:date,facts:{network:projectMintNetwork({mint,recipients})},
});
test('late archive backfill is newly visible, not asserted new chain transfer',()=>{
  const a=snap(M,[row('sig1','A','B')],'2026-11-11T12:00:00Z');
  const b=snap(M,[row('sig1','A','B'),row('sig2','B','C')],'2026-11-12T12:00:00Z');
  const delta=compareCapturedMintSnapshots(a,b);
  assert.equal(delta.kind,'LOCAL_ARCHIVE_VISIBILITY_DELTA');
  assert.deepEqual(delta.newlyVisible.map(x=>x.signature),['sig2']);
  assert.equal(delta.noLongerVisibleInSample.length,0);
  assert.equal(delta.persistingEventCount,1);
  assert.equal(delta.liveChainEventChange,'UNKNOWN');
  assert.equal(delta.hasCompleteWalletHistory,false);
  assert.match(delta.warnings.join(' '),/not newly emitted/);
});
test('a captured event missing in later sample is NOT a sell or chain reversal',()=>{
  const a=snap(M,[row('sig1','A','B')],'2026-11-11T12:00:00Z');
  const b=snap(M,[],'2026-11-12T12:00:00Z');
  const delta=compareCapturedMintSnapshots(a,b);
  assert.equal(delta.noLongerVisibleInSample[0].signature,'sig1');
  assert.match(delta.warnings.join(' '),/does not prove token was sold/);
});
test('unpositioned legacy events are excluded from reliable snapshot identity comparison',()=>{
  const a=snap(M,[row('sig1','A','B',undefined,undefined)],'2026-11-11T12:00:00Z');
  a.facts.network.events[0].hasInstructionIdentity=false;
  const b=snap(M,[],'2026-11-12T12:00:00Z');
  const delta=compareCapturedMintSnapshots(a,b);
  assert.equal(delta.uncomparableEventCount,1);
  assert.equal(delta.noLongerVisibleInSample.length,0);
});
test('cross Mint repeat address is a weak overlap, not common control or profit',()=>{
  const a=snap(M,[row('m1','A','SHARED')],'2026-11-11T12:00:00Z');
  const b=snap(N,[{...row('m2','SHARED','C'),mint:N}],'2026-11-12T12:00:00Z');
  const r=compareCapturedCrossMintWallets(a,b);
  assert.equal(r.overlappingWallets.length,1);
  assert.equal(r.overlappingWallets[0].wallet,'SHARED');
  assert.equal(r.overlappingWallets[0].economicController,'UNKNOWN');
  assert.equal(r.commonControl,'UNKNOWN');
  assert.equal(r.capitalProvenance,'UNKNOWN');
  assert.equal(r.walletHistoryComplete,false);
  assert.match(r.limitations.join(' '),/No two-Mint portfolio profit/);
});
test('reject wrong-Mint snapshot pair or identical Mint for cross-Mint comparison',()=>{
  const a=snap(M,[],'2026-11-11T12:00:00Z');
  const b=snap(N,[],'2026-11-12T12:00:00Z');
  assert.throws(()=>compareCapturedMintSnapshots(a,b),/DIFFERENT_MINT/);
  assert.throws(()=>compareCapturedCrossMintWallets(a,a),/CROSS_MINT_REQUIRES_DISTINCT/);
});


test('a corrected amount on an already captured signature is a revision, not a new chain event',()=>{
  const a=snap(M,[row('same','A','B')],'2026-11-11T12:00:00Z');
  const changed={...row('same','A','B'),amountRaw:'200'};
  const b=snap(M,[changed],'2026-11-12T12:00:00Z');
  const delta=compareCapturedMintSnapshots(a,b);
  assert.equal(delta.newlyVisible.length,0);
  assert.equal(delta.noLongerVisibleInSample.length,0);
  assert.equal(delta.revisedCapturedEvents.length,1);
  assert.equal(delta.revisedCapturedEvents[0].eventId,'same:0:-1');
  assert.match(delta.revisedCapturedEvents[0].meaning,/NOT_A_NEW_CHAIN_EVENT/);
});
