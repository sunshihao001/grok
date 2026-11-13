// A truthful next-step view over already captured local economic evidence.
// It creates NO new evidence, no wallets, no scheduled monitoring and no trading
// signals. This is the six-part business goal rendered as evidence-dependent states.
const MINT=/^[1-9A-HJ-NP-Za-km-z]{32,44}$/;
const bounded=x=>typeof x==='string'?x.slice(0,120):null;

export function summarizeInvestigationContinuation({mint,investigation}={}) {
  if(!MINT.test(mint||''))throw Error('INVESTIGATION_MINT_INVALID');
  const observed=Array.isArray(investigation?.evidence)
    ? investigation.evidence.find(x=>x?.capability==='mint-economic-evidence' &&
        x?.result?.facts?.network?.mint===mint)?.result : null;
  const network=observed?.facts?.network;
  const events=Array.isArray(network?.events)?network.events:[];
  const walletFlows=Array.isArray(network?.walletFlows)?network.walletFlows:[];
  const watches=walletFlows.slice(0,100).filter(x=>typeof x?.wallet==='string')
    .map(x=>({
      wallet:bounded(x.wallet),
      observedTransferCount:(x.receivedEventCount||0)+(x.sentEventCount||0),
      roles:Array.isArray(x.roles)?x.roles.slice(0,8):[],
      observedNetTransferRaw:x.observedNetTransferRaw??null,
      localSellSummaryCount:x.localSellSummaryCount||0,
      addressClass:x.addressClass||'UNCLASSIFIED_INCLUDES_INFRASTRUCTURE',
      economicController:'UNKNOWN',
    }))
    .sort((a,b)=>b.observedTransferCount-a.observedTransferCount||
      a.wallet.localeCompare(b.wallet)).slice(0,12);
  const paths=[],seen=new Set();
  for(const event of events.slice(0,200)) {
    for(const p of (Array.isArray(event?.crossMintCandidates)?event.crossMintCandidates:[]).slice(0,25)) {
      if(!MINT.test(p?.boughtMint||'')||p.boughtMint===mint||
         typeof p.fundingSig!=='string'||!p.fundingSig||
         typeof p.buySig!=='string'||!p.buySig)continue;
      const key=p.boughtMint+'|'+p.fundingSig+'|'+p.buySig;
      if(seen.has(key))continue;
      seen.add(key);
      paths.push({
        sourceMint:mint,otherMint:p.boughtMint,
        observedTransferSignature:bounded(event.signature),
        candidateFundingSignature:bounded(p.fundingSig),
        candidateBuySignature:bounded(p.buySig),
        status:'LOCAL_TEMPORAL_CROSS_MINT_CANDIDATE_NOT_CAPITAL_PROVENANCE',
        commonController:'UNKNOWN',
      });
      if(paths.length===15)break;
    }
    if(paths.length===15)break;
  }
  const known=observed?.status==='LOCAL_EVIDENCE_PARTIAL';
  return {
    schemaVersion:'0.1',mint,kind:'READ_ONLY_INVESTIGATION_CONTINUATION',
    stages:{
      market:'USER_SUBMITTED_OR_SELECTED_PULSE_OBSERVATION_NOT_VERIFIED_OPPORTUNITY',
      keyWallets:watches.length?'LOCALLY_OBSERVED_ADDRESS_CANDIDATES_NOT_IDENTITIES':'UNKNOWN_NOT_OBSERVED_IN_CAPTURED_SAMPLE',
      capitalAndInventory:known&&events.length?'CAPTURED_TOKEN_TRANSFERS_ONLY_COST_BASIS_UNKNOWN':'NO_COMPLETE_ECONOMIC_EVIDENCE',
      crossMint:paths.length?'TEMPORAL_PATH_CANDIDATES_ONLY':'UNKNOWN_NO_VERIFIED_CROSS_MINT_PATH',
      participation:'UNASSESSED_NO_HISTORIC_EXECUTABLE_ENTRY_EXIT_QUOTES',
      monitoring:'NOT_RUNNING_NO_AUTONOMOUS_WATCHER',
    },
    keyWalletCandidates:watches,
    crossMintCandidates:paths,
    followability:{
      status:'UNASSESSED_NO_HISTORIC_EXECUTABLE_ENTRY_EXIT_QUOTES',
      signalFirstAvailableAtMs:null,entryQuote:null,exitQuote:null,
      historicalNetPnl:'UNKNOWN',outOfSampleAdvantage:'UNKNOWN',
      decision:'NOT_A_TRADING_SIGNAL',
    },
    watch:{
      status:'NOT_RUNNING_NO_AUTONOMOUS_WATCHER',
      suggestedWallets:watches.map(x=>x.wallet).slice(0,8),
      comparisonMethod:'REOPEN_AND_COMPARE_NEWLY_CAPTURED_EVIDENCE_TO_PRIOR_SNAPSHOT',
      onChainEventChange:'UNKNOWN_UNTIL_NEW_EVIDENCE',
    },
    limits:[
      'Wallet candidates include possible liquidity pools, routers and shared services.',
      'Observation of a later sell does not prove sale of the transferred inventory.',
      'Cross-Mint time paths do not prove that the same funds were reused.',
      'No automated monitoring, validated followability or profitable opportunity is established.',
      'Missing records may reflect the bounded archive rather than inactivity.',
    ],
  };
}
