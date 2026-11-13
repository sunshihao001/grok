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
