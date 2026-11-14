import test from 'node:test';
import assert from 'node:assert/strict';
import { projectMintNetwork } from '../server/intelligence/economic-network.mjs';
import { summarizeInvestigationContinuation } from '../server/intelligence/investigation-continuation.mjs';
const mint='EYqygbhZjP7EbM4fSn8devctnksAvPAD1Bt57XBFpump';
const other='GTNHLKQWKZHaHpd6PjfMgfFZUDEuCviwXMwYbCcepump';

test('evidence-only continuation extracts local wallet and other-Mint candidates with explicit UNKNOWN control and profit',()=>{
  const recipients=[
    {mint,signature:'transfer1',outerI:0,innerI:0,fromOwner:'Sender',toOwner:'Receiver',
      amountRaw:'1000000000000000000000',blockTime:1700000000,slot:1,
      observedSells:[{sig:'later-sell'}],crossMintCandidates:[
        {fundingSig:'fund1',buySig:'buy2',boughtMint:other,soldMint:mint},
        {fundingSig:'fund1',buySig:'buy2',boughtMint:other,soldMint:mint},
      ]},
    {mint,signature:'transfer2',outerI:0,innerI:0,fromOwner:'Sender',toOwner:'Another',
      amountRaw:'500000000000000000000',blockTime:1700000001,slot:2},
  ];
  const network=projectMintNetwork({mint,recipients});
  const report=summarizeInvestigationContinuation({mint,investigation:{
    evidence:[{capability:'mint-economic-evidence',result:{status:'LOCAL_EVIDENCE_PARTIAL',
      facts:{network}}}],
  }});
  assert.equal(report.keyWalletCandidates.length,3);
  assert.equal(report.crossMintCandidates.length,1);
  assert.equal(report.crossMintCandidates[0].otherMint,other);
  assert.equal(report.crossMintCandidates[0].commonController,'UNKNOWN');
  assert.equal(report.stages.capitalAndInventory,'CAPTURED_TOKEN_TRANSFERS_ONLY_COST_BASIS_UNKNOWN');
  assert.equal(report.stages.crossMint,'TEMPORAL_PATH_CANDIDATES_ONLY');
  assert.equal(report.watch.status,'NOT_RUNNING_NO_AUTONOMOUS_WATCHER');
  assert.equal(report.followability.historicalNetPnl,'UNKNOWN');
  assert.equal(report.followability.decision,'NOT_A_TRADING_SIGNAL');
  assert.equal(report.keyWalletCandidates.some(x=>x.localSellSummaryCount>0),true);
  assert.equal(report.keyWalletCandidates.every(x=>x.economicController==='UNKNOWN'),true);
});

test('no locally captured transactions does not turn missing evidence into absence or profitable signals',()=>{
  const report=summarizeInvestigationContinuation({mint,investigation:{
    status:'NO_EVIDENCE_REQUESTED',evidence:[],
  }});
  assert.deepEqual(report.keyWalletCandidates,[]);
  assert.deepEqual(report.crossMintCandidates,[]);
  assert.equal(report.stages.keyWallets,'UNKNOWN_NOT_OBSERVED_IN_CAPTURED_SAMPLE');
  assert.equal(report.stages.crossMint,'UNKNOWN_NO_VERIFIED_CROSS_MINT_PATH');
  assert.equal(report.stages.participation,'UNASSESSED_NO_HISTORIC_EXECUTABLE_ENTRY_EXIT_QUOTES');
  assert.equal(report.watch.onChainEventChange,'UNKNOWN_UNTIL_NEW_EVIDENCE');
  assert.throws(()=>summarizeInvestigationContinuation({mint:'bad',investigation:{}}),/MINT_INVALID/);
});

test('cross-Mint candidates without valid destination Mint and distinct funding/buy evidence are skipped',()=>{
  const graph=projectMintNetwork({mint,recipients:[{mint,signature:'transfer1',outerI:0,innerI:0,
    fromOwner:'Sender',toOwner:'Receiver',amountRaw:'100',crossMintCandidates:[
      {fundingSig:'fund',buySig:'buy',boughtMint:'OTHER',soldMint:mint},
      {fundingSig:'fund',buySig:'buy',boughtMint:mint,soldMint:mint},
      {fundingSig:null,buySig:'buy',boughtMint:other,soldMint:mint},
    ]}]});
  const report=summarizeInvestigationContinuation({mint,investigation:{
    evidence:[{capability:'mint-economic-evidence',result:{status:'LOCAL_EVIDENCE_PARTIAL',
      facts:{network:graph}}}],
  }});
  assert.equal(report.crossMintCandidates.length,0);
  assert.equal(report.followability.status,'UNASSESSED_NO_HISTORIC_EXECUTABLE_ENTRY_EXIT_QUOTES');
});

test('goal anchors turn locally observed economic mechanisms into bounded next evidence without ranking profitability',()=>{
  const graph=projectMintNetwork({mint,recipients:[{
    mint,signature:'archive-trans-1',outerI:0,innerI:1,
    rpcHashVerified:true,instructionVerifiedAgainstRpc:true,
    fromOwner:'Sender',toOwner:'Receiver',amountRaw:'1000',
    crossMintCandidates:[{fundingSig:'fund',buySig:'buy',boughtMint:other,soldMint:mint}],
  }]});
  const investigation={evidence:[{capability:'mint-economic-evidence',result:{
    status:'LOCAL_EVIDENCE_PARTIAL',facts:{network:graph,claimTrace:{claims:[{claimId:'observed-transfer'}]}}}}],
    knowledgeUse:[{source:'LOCAL_PROJECT_RESEARCH:wallet-roles@sha256:123',stage:'plan'}]};
  const direct=summarizeInvestigationContinuation({mint,investigation});
  assert.equal(direct.stages.market,'NO_PULSE_MARKET_OBSERVATION_IN_THIS_RECEIPT');
  assert.equal(direct.anchors.evidenceLineage.pulseBrowserObservationPresent,false);
  assert.equal(direct.anchors.evidenceLineage.anyArchivedInstructionVerified,true);
  assert.equal(direct.anchors.evidenceLineage.independentMainnetVerification,false);
  assert.equal(direct.anchors.researchPriority.observedTransferEvents,1);
  assert.equal(direct.anchors.researchPriority.localClaimTraces,1);
  assert.equal(direct.anchors.researchPriority.evaluatedAsInvestigationCandidate,false);
  assert.equal(direct.anchors.tradeReadiness.verifiedMarketOpportunity,false);
  assert.equal(direct.anchors.tradeReadiness.liveExecutionValidated,false);
  assert.equal(direct.anchors.knowledgeContext.providedRecordCount,1);
  assert.equal(direct.anchors.knowledgeContext.modelApplicationVerified,false);
  assert.equal(direct.anchors.nextEvidence.length,5);
  assert.equal(direct.anchors.nextEvidence[2].status,'TEMPORAL_CANDIDATES_UNPROVEN_FUND_REUSE');
  assert.equal(direct.anchors.nextEvidence[3].anchor,'G4_TRADE_PARTICIPATION');
  assert.ok(direct.anchors.nextEvidence[3].missing.includes('ENTRY_EXIT_QUOTES'));
  const pulse=summarizeInvestigationContinuation({mint,investigation,marketObservation:{
    selectedMint:mint,source:'USER_BROWSER_BLIX_PULSE_SNAPSHOT_UNVERIFIED',
    sourceRecordedAtMs:1770000000000,
  }});
  assert.equal(pulse.stages.market,'SUBMITTED_PULSE_BROWSER_OBSERVATION_NOT_SOURCE_VERIFIED');
  assert.equal(pulse.anchors.evidenceLineage.pulseBrowserRecordedAtMs,1770000000000);
  assert.equal(pulse.anchors.evidenceLineage.sourceFirstAvailableAtMs,null);
  const wrong=summarizeInvestigationContinuation({mint,investigation,marketObservation:{
    selectedMint:other,source:'USER_BROWSER_BLIX_PULSE_SNAPSHOT_UNVERIFIED',
    sourceRecordedAtMs:1770000000000,
  }});
  assert.equal(wrong.stages.market,'NO_PULSE_MARKET_OBSERVATION_IN_THIS_RECEIPT');
  const forged=summarizeInvestigationContinuation({mint,investigation,marketObservation:{
    selectedMint:mint,source:'CHAIN_VERIFIED_PRICE_FEED',sourceRecordedAtMs:1770000000000,
  }});
  assert.equal(forged.anchors.evidenceLineage.pulseBrowserObservationPresent,false);
});

test('empty or unindexed evidence does not create research candidates, AI benefit or executable opportunity',()=>{
  const result=summarizeInvestigationContinuation({mint,investigation:{evidence:[],knowledgeUse:[]}});
  assert.equal(result.anchors.researchPriority.status,'INSUFFICIENT_CAPTURED_EVIDENCE_TO_PRIORITIZE');
  assert.equal(result.anchors.tradeReadiness.status,'NOT_EVALUABLE_WITHOUT_SIGNAL_AND_EXECUTION_RECEIPTS');
  assert.equal(result.anchors.knowledgeContext.providedRecordCount,0);
  assert.equal(result.anchors.nextEvidence[1].status,'NO_TRANSFER_EVIDENCE_IN_CAPTURED_SAMPLE');
  assert.equal(result.anchors.nextEvidence[2].status,'NO_CROSS_MINT_PATH_CONFIRMED');
  assert.equal(result.anchors.evidenceLineage.anyArchivedInstructionVerified,false);
  assert.equal(result.followability.historicalNetPnl,'UNKNOWN');
  assert.equal(result.watch.status,'NOT_RUNNING_NO_AUTONOMOUS_WATCHER');
});
