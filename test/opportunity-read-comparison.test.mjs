import test from 'node:test';
import assert from 'node:assert/strict';
import { discoverPulseInvestigation } from '../server/intelligence/pulse-discovery.mjs';
import { compareObservedInvestigations } from '../server/intelligence/opportunity-read-comparison.mjs';

const M1='EYqygbhZjP7EbM4fSn8devctnksAvPAD1Bt57XBFpump';
const M2='GTNHLKQWKZHaHpd6PjfMgfFZUDEuCviwXMwYbCcepump';
const M3='4p7SeR6361WJ4T4icgsYTnzAUzfA5NwM4CwYD9kMBjuK';
const frozen=Date.parse('2026-11-13T08:00:00Z');
const snapshot={
  goal:'Find a Mint worth investigating; do not treat research priority as trade readiness',
  boardStatus:'BLIX_PULSE_LIVE_OR_POLLING',browserRecordedAtMs:frozen,
  candidates:[
    {mint:M1,stage:'new',symbol:'TEST_A',liq:20000,mcap:60000,vol:28000,buys:24,sells:13,traders:18},
    {mint:M2,stage:'migrated',symbol:'TEST_B',liq:700,mcap:45000,vol:10000,buys:4,sells:12,traders:5},
  ],
};
async function runVariant(enriched) {
  return discoverPulseInvestigation({
    input:snapshot,now:()=>frozen,
    model:async ({stage,knowledge,candidates})=>{
      assert.equal(stage,'discover');
      assert.equal(candidates.length,2);
      assert.equal(knowledge.length,enriched?1:0);
      return {mint:enriched?M2:M1,reason:enriched
        ? 'Investigate B for potentially unusual wallet distribution, NOT an executable opportunity.'
        : 'Investigate A based only on the frozen Pulse market shortlist.'};
    },
    readEconomic:async()=>{throw Error('No new provider requests allowed in selection-only audit');},
    loadKnowledge:async()=>enriched?[{
      source:'SYNTHETIC_GMGN_MILLION_STYLE_RESEARCH_NOT_CHAIN_PROOF',
      status:'SYNTHETIC_TEST_ONLY',topic:'wallet-roles',
      excerpt:'Wallet overlap is a hypothesis, not control, wallet PnL, trade readiness or chain proof.',
    }]:[],
    runResearch:async()=>({
      status:'DRAFT_WITH_INCOMPLETE_EVIDENCE',evidence:[],assessment:null,unknowns:[
        'No validated entry/exit quotes.'],calls:[],knowledgeUse:[],
    }),
  });
}
test('same Pulse snapshot A/B preserves the Mint universe and exposes change without claiming alpha',async()=>{
  const a=await runVariant(false), b=await runVariant(true);
  const report=compareObservedInvestigations({snapshot,baseline:a,enhanced:b,
    supportingEvidence:[{mint:M2,source:'SYNTHETIC_WALLET_NOTE',kind:'HYPOTHESIS',
      firstAvailableAtMs:frozen-5000,id:'known-frozen'},
      {mint:M1,source:'SYNTHETIC_PARTIAL_HISTORY',kind:'UNVERIFIED_HISTORY',
        firstAvailableAtMs:null}]});
  assert.equal(report.kind,'OFFLINE_SAME_SNAPSHOT_A_B_INVESTIGATION_AUDIT');
  assert.deepEqual([report.baseline.selectedMint,report.enhanced.selectedMint],[M1,M2]);
  assert.equal(report.selection.changed,true);
  assert.equal(report.input.observedMintCount,2);
  assert.match(report.input.candidateDigestSha256,/^[a-f0-9]{64}$/);
  assert.equal(report.selection.sameSnapshotCandidatePopulation,true);
  assert.equal(report.selection.newMintDiscoveredOutsideOriginalPulse,false);
  assert.equal(report.supportingEvidence.firstAvailableUnknown,1);
  assert.equal(report.supportingEvidence.availabilityIndependentlyVerified,false);
  assert.equal(report.paperFollowability.receiptCount,0);
  assert.equal(report.verdict,'ONLY_SELECTION_DIFFERENCE_MEASURED_NOT_REAL_MARKET_ADVANTAGE');
  assert.equal(report.permissions.noTradeExecution,true);
  assert.equal(report.baseline.verifiedMarketOpportunity,false);
  assert.equal(report.enhanced.verifiedMarketOpportunity,false);
});
test('post-snapshot wallet signal fails closed instead of creating hindsight discovery',async()=>{
  const a=await runVariant(false),b=await runVariant(true);
  assert.throws(()=>compareObservedInvestigations({snapshot,baseline:a,enhanced:b,
    supportingEvidence:[{mint:M2,source:'POST_EVENT_WALLET_PROFIT',kind:'WALLET_RESULT',
      firstAvailableAtMs:frozen+1}]}),/LOOKAHEAD_EVIDENCE_AFTER_FROZEN_SNAPSHOT/);
});
test('changed candidate population, mismatched clock and injected Mint are not A/B comparisons',async()=>{
  const a=await runVariant(false),b=await runVariant(true);
  const changed={...b,discovery:{...b.discovery,candidateCount:3}};
  const shifted={...b,discovery:{...b.discovery,sourceRecordedAtMs:frozen+1000}};
  const outside={...b,discovery:{...b.discovery,selectedMint:M3}};
  const fakeSameCount={...b,discovery:{...b.discovery,candidateDigestSha256:'0'.repeat(64)}};
  for(const enhanced of [changed,shifted,outside,fakeSameCount])
    assert.throws(()=>compareObservedInvestigations({snapshot,baseline:a,enhanced}),
      /ENHANCED_POPULATION_OR_TIME_MISMATCH/);
  assert.throws(()=>compareObservedInvestigations({snapshot:{...snapshot,
    boardStatus:'RESTORED_FROM_BROWSER_CACHE'},baseline:a,enhanced:b}),/STALE/);
});
test('paper receipt must stay inside population; a synthetic positive is never market alpha',async()=>{
  const a=await runVariant(false),b=await runVariant(true);
  const receipt={
    id:'synthetic-paper-only',mint:M2,
    signal:{chainEventAtMs:frozen-2000,firstAvailableAtMs:frozen-1000},
    entry:{source:'PAPER_REPLAY',quoteObservedAtMs:frozen+1000,fillAtMs:frozen+1100,
      maxQuoteAgeMs:1000,spentLamports:'1000000000',receivedTokensRaw:'1000000',
      feeLamports:'5000',slippageIncluded:true},
    exit:{source:'PAPER_REPLAY',quoteObservedAtMs:frozen+3000,fillAtMs:frozen+3100,
      maxQuoteAgeMs:1000,receivedLamports:'1200000000',soldTokensRaw:'1000000',
      feeLamports:'5000',slippageIncluded:true},
    positionContinuityVerified:true,
  };
  const report=compareObservedInvestigations({snapshot,baseline:a,enhanced:b,paperReceipts:[receipt]});
  assert.equal(report.paperFollowability.simulatedCasesNotLive,1);
  assert.equal(report.paperFollowability.outOfSamplePerformance,'NOT_ESTABLISHED');
  assert.equal(report.paperFollowability.liveTradeResults,'NOT_MEASURED');
  assert.equal(report.verdict,'ONLY_SELECTION_DIFFERENCE_MEASURED_NOT_REAL_MARKET_ADVANTAGE');
  assert.throws(()=>compareObservedInvestigations({snapshot,baseline:a,enhanced:b,
    paperReceipts:[{...receipt,mint:M3}]}),/A_B_PAPER_MINT_OUTSIDE_POPULATION/);
});
test('unknown historical first-available time is not silently filled from the browser clock',async()=>{
  const a=await runVariant(false),b=await runVariant(true);
  const report=compareObservedInvestigations({snapshot,baseline:a,enhanced:b,
    supportingEvidence:[{mint:M2,source:'WALLET_SNAPSHOT',kind:'WALLET_BUY',firstAvailableAtMs:null}]});
  assert.equal(report.supportingEvidence.claimedAvailableBySnapshot,0);
  assert.equal(report.supportingEvidence.firstAvailableUnknown,1);
  assert.match(report.unresolved.join(' '),/Client-recorded observation time is not provider first-available/);
});
