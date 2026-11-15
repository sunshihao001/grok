import test from 'node:test';
import assert from 'node:assert/strict';
import { evaluatePaperFollowabilityCase,evaluatePaperFollowabilityCases }
  from '../server/intelligence/followability-replay.mjs';

const complete={
 id:'case1',mint:'GTNHLKQWKZHaHpd6PjfMgfFZUDEuCviwXMwYbCcepump',
 signal:{chainEventAtMs:100,firstAvailableAtMs:200},
 entry:{source:'PAPER_REPLAY',quoteObservedAtMs:210,fillAtMs:250,
   spentLamports:'1000000000',receivedTokensRaw:'1000000',
   feeLamports:'5000',slippageIncluded:true,maxQuoteAgeMs:1000},
 exit:{source:'PAPER_REPLAY',quoteObservedAtMs:310,fillAtMs:350,
   soldTokensRaw:'1000000',receivedLamports:'1200000000',
   feeLamports:'5000',slippageIncluded:true,maxQuoteAgeMs:1000},
 positionContinuityVerified:true,
};
test('complete simulated fills yield deterministic paper arithmetic without claiming live PnL',()=>{
 const a=evaluatePaperFollowabilityCase(complete);
 assert.equal(a.status,'PAPER_SCENARIO_CALCULATED_NOT_LIVE');
 assert.equal(a.followerLatencyMs,50);
 assert.equal(a.simulatedNetLamports,'199990000');
 assert.equal(a.simulatedOutcome,'POSITIVE');
 assert.equal(a.liveExecutionValidated,false);
 assert.equal(a.realizedWalletPnl,'UNKNOWN');
 assert.equal(a.source,'USER_SUPPLIED_PAPER_REPLAY_RECEIPTS');
});
test('a historical entry before the follower could know the signal is not followable',()=>{
 const a=evaluatePaperFollowabilityCase({...complete,
   entry:{...complete.entry,quoteObservedAtMs:150,fillAtMs:180}});
 assert.equal(a.status,'LOOKAHEAD_OR_UNFOLLOWABLE_ENTRY');
 assert.equal(a.simulatedNetLamports,undefined);
});
test('missing exit, partial inventory and unverified quote provenance never generate profit',()=>{
 const missing=evaluatePaperFollowabilityCase({...complete,exit:null});
 const partial=evaluatePaperFollowabilityCase({...complete,exit:{...complete.exit,soldTokensRaw:'500000'}});
 const unpriced=evaluatePaperFollowabilityCase({...complete,exit:{...complete.exit,slippageIncluded:false}});
 assert.equal(missing.status,'MISSING_OR_INVALID_EXIT_EXECUTION');
 assert.equal(partial.status,'UNRESOLVED_INVENTORY_OR_PARTIAL_EXIT');
 assert.equal(unpriced.status,'PAPER_FILL_PROVENANCE_INCOMPLETE');
 for(const x of [missing,partial,unpriced])assert.equal(x.simulatedNetLamports,undefined);
});
test('negative results remain negative; no selected set proves an alpha',()=>{
 const loss=evaluatePaperFollowabilityCase({...complete,
   exit:{...complete.exit,receivedLamports:'800000000'}});
 assert.equal(loss.simulatedOutcome,'NEGATIVE');
 const all=evaluatePaperFollowabilityCases([complete,{...complete,id:'loss',
   exit:{...complete.exit,receivedLamports:'800000000'}}]);
 assert.equal(all.inputCount,2);
 assert.equal(all.outOfSamplePerformance,'NOT_ESTABLISHED');
 assert.equal(all.measuredPopulationCoverage,'UNKNOWN');
 assert.equal(all.liveTradeResults,'NOT_MEASURED');
 assert.equal(all.noTradeExecution,true);
});
test('case count is bounded and invalid fees or source time cannot be implicitly inferred',()=>{
 assert.throws(()=>evaluatePaperFollowabilityCases(Array(201).fill(complete)),/FOLLOWABILITY_CASE_LIMIT/);
 assert.equal(evaluatePaperFollowabilityCase({...complete,
   signal:{chainEventAtMs:200,firstAvailableAtMs:100}}).status,'UNKNOWN_SIGNAL_AVAILABILITY');
 assert.equal(evaluatePaperFollowabilityCase({...complete,
   entry:{...complete.entry,feeLamports:'UNKNOWN'}}).status,'INVALID_EXECUTION_AMOUNTS');
});

test('stale quoted paper entry or missing freshness never generates a performance number',()=>{
 const missing=evaluatePaperFollowabilityCase({...complete,
   entry:{...complete.entry,maxQuoteAgeMs:undefined}});
 const stale=evaluatePaperFollowabilityCase({...complete,
   entry:{...complete.entry,quoteObservedAtMs:201,maxQuoteAgeMs:10}});
 assert.equal(missing.status,'QUOTE_FRESHNESS_UNKNOWN');
 assert.equal(stale.status,'STALE_EXECUTION_QUOTE');
 assert.equal(missing.simulatedNetLamports,undefined);
 assert.equal(stale.simulatedNetLamports,undefined);
});
