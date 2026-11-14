// A truthful next-step view over already captured local economic evidence.
// It creates NO new evidence, no wallets, no scheduled monitoring and no trading
// signals. This is the six-part business goal rendered as evidence-dependent states.
const MINT=/^[1-9A-HJ-NP-Za-km-z]{32,44}$/;
const bounded=x=>typeof x==='string'?x.slice(0,120):null;

export function summarizeInvestigationContinuation({mint,investigation,marketObservation}={}) {
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
  // A user-specified Mint and a submitted Pulse browser snapshot are different
  // kinds of evidence. /research and /inspect never imply a Pulse observation.
  const hasPulseObservation=marketObservation?.selectedMint===mint &&
    marketObservation.source==='USER_BROWSER_BLIX_PULSE_SNAPSHOT_UNVERIFIED' &&
    Number.isSafeInteger(marketObservation.sourceRecordedAtMs) &&
    marketObservation.sourceRecordedAtMs>=0;
  const marketStatus=hasPulseObservation
    ? 'SUBMITTED_PULSE_BROWSER_OBSERVATION_NOT_SOURCE_VERIFIED'
    : 'NO_PULSE_MARKET_OBSERVATION_IN_THIS_RECEIPT';
  const known=observed?.status==='LOCAL_EVIDENCE_PARTIAL';
  const archivedSignatureVerified=events.some(e=>
    e.rpcHashVerified===true && e.instructionVerifiedAgainstRpc===true);
  const trace=observed?.facts?.claimTrace;
  const claimCount=Array.isArray(trace?.claims)?trace.claims.length:0;
  const knowledgeRecords=Array.isArray(investigation?.knowledgeUse)
    ? investigation.knowledgeUse.filter(x=>typeof x?.source==='string'):[];
  // Evidence-to-next-check map: converts existing D01–D12 knowledge into
  // falsifiable data requests. It does not select coins, assign AI scores,
  // infer controllers, request providers or run a model.
  // Align with the EXISTING O1–O6 outcome IDs in businessRouteGraph, rather
  // than inventing a second G1–G5 goal hierarchy. S1–S7 are support methods.
  const nextEvidence=[
    {anchor:'O1_MARKET_DISCOVERY',domains:['D02','D03','D07','D10','D11'],
      status:marketStatus,
      missing:'SOURCE_FIRST_AVAILABLE_SIGNAL_TIME_AND_COMPLETE_MARKET_COVERAGE',
      nextReadOnlyCheck:hasPulseObservation
        ? 'Compare the submitted browser snapshot with provider-origin timestamps and the original Blix opportunity candidate universe.'
        : 'Inspect existing Blix Pulse/Discover observations for this exact Mint; the local SQLite archive does not establish market appearance.'},
    {anchor:'O2_WALLET_ROLES',domains:['D01','D04','D05','D07','D10'],
      status:watches.length?'CAPTURED_OWNER_ADDRESS_CANDIDATES_NOT_ECONOMIC_ACTORS':'NO_RESOLVED_WALLET_ROLES_IN_CAPTURED_SAMPLE',
      missing:'ACCOUNT_OWNER_AUTHORITY_AND_POOL_ROUTER_CEX_CLASSIFICATION',
      nextReadOnlyCheck:watches.length
        ? 'Resolve Token Account versus Owner and screen pools, routers, shared services and custody before suggesting related wallets or controllers.'
        : 'Check the existing source wallet and owner coverage before interpreting a missing wallet list as no participants.'},
    {anchor:'O3_TOKEN_CAPITAL_INVENTORY',domains:['D01','D05','D06','D10','D11'],
      status:events.length
        ? archivedSignatureVerified?'SOME_ARCHIVED_INSTRUCTIONS_CHECKED_NOT_FULL_HISTORY':'CAPTURED_TRANSFER_REPORT_NEEDS_RAW_INSTRUCTION_CHECK'
        : 'NO_TRANSFER_EVIDENCE_IN_CAPTURED_SAMPLE',
      missing:events.length
        ? 'FULL_SIGNED_HISTORY_COST_BASIS_AND_TRANSFERRED_INVENTORY_PROVENANCE'
        : 'ARCHIVED_RAW_TRANSACTION_AND_OWNER_RESOLUTION_COVERAGE',
      nextReadOnlyCheck:events.length
        ? 'Recheck raw signatures, CPI and Token-2022 instruction positions; separate buy, transfer, recipient sell summary, actual remaining inventory and costs.'
        : 'Check completeness of the existing Mint economic archive and sender discovery before inferring absence of transfers.'},
    {anchor:'O4_CROSS_MINT_GROUP',domains:['D04','D05','D06','D07','D10','D11'],
      status:paths.length?'TEMPORAL_CANDIDATES_UNPROVEN_FUND_REUSE':'NO_CROSS_MINT_PATH_CONFIRMED',
      missing:'SIGNED_SOL_WSOL_FUND_FLOW_AND_INDEPENDENT_CONTROL_EVIDENCE',
      nextReadOnlyCheck:paths.length
        ? 'Check each funding and buy signature against SOL/WSOL changes, intermediate wallets and shared-service counterexamples.'
        : 'No cross-Mint path is proven from this bounded archive; revisit only if wallet/transfer evidence warrants it.'},
    {anchor:'O5_OPPORTUNITY_AND_FOLLOWABILITY',domains:['D03','D06','D08','D09','D10','D11'],
      status:'NOT_EVALUABLE_WITHOUT_FOLLOWER_VISIBLE_SIGNAL_AND_QUOTES',
      missing:'SIGNAL_FIRST_AVAILABLE_ENTRY_EXIT_QUOTES_POOL_DEPTH_FEES_LATENCY',
      nextReadOnlyCheck:'Use original Blix/Paper read-only receipts from signal-visible time, executable entry/exit quotes, size, fees, failures and exit liquidity; otherwise keep net outcome UNKNOWN.'},
    {anchor:'O6_CASE_MONITORING_AND_REVISION',domains:['D07','D10','D11','D12'],
      status:'NOT_RUNNING_NO_AUTONOMOUS_WATCHER',
      missing:'PERSISTENT_CASE_NEW_VS_BACKFILLED_EVENT_COMPARISON_AND_KNOWLEDGE_EFFECT_EVALUATION',
      nextReadOnlyCheck:'Reopen the same Mint after a new archive snapshot and distinguish new events from delayed backfill; evaluate relevant AI knowledge against the same-input no-knowledge baseline. No watcher is running.'},
  ];
  const anchors={
    researchPriority:{
      status:events.length?'LOCAL_EVENTS_AVAILABLE_FOR_REVIEW_NOT_PRIORITIZED':'INSUFFICIENT_CAPTURED_EVIDENCE_TO_PRIORITIZE',
      observedTransferEvents:events.length,localClaimTraces:claimCount,
      evaluatedAsInvestigationCandidate:false,
      note:'Having local events makes investigation possible; it does not prove unusual behavior or rank this Mint above others.',
    },
    tradeReadiness:{
      status:'NOT_EVALUABLE_WITHOUT_SIGNAL_AND_EXECUTION_RECEIPTS',
      modelGeneratedProfitEvidence:false,verifiedMarketOpportunity:false,
      liveExecutionValidated:false,
      note:'Price moves, wallet labels and Token-transfer paths cannot substitute for follower-visible signal time and tradable round-trip quotes.',
    },
    evidenceLineage:{
      source:'EXISTING_LOCAL_SQLITE_ONLY',
      pulseBrowserObservationPresent:hasPulseObservation,
      pulseBrowserRecordedAtMs:hasPulseObservation?marketObservation.sourceRecordedAtMs:null,
      sourceFirstAvailableAtMs:null,
      independentMainnetVerification:false,
      anyArchivedInstructionVerified:archivedSignatureVerified,
      historyComplete:false,
    },
    knowledgeContext:{providedRecordCount:knowledgeRecords.length,
      modelApplicationVerified:false,causalImprovementMeasured:false},
    nextEvidence,
  };
  return {
    schemaVersion:'0.1',mint,kind:'READ_ONLY_INVESTIGATION_CONTINUATION',
    stages:{
      market:marketStatus,
      keyWallets:watches.length?'LOCALLY_OBSERVED_ADDRESS_CANDIDATES_NOT_IDENTITIES':'UNKNOWN_NOT_OBSERVED_IN_CAPTURED_SAMPLE',
      capitalAndInventory:known&&events.length?'CAPTURED_TOKEN_TRANSFERS_ONLY_COST_BASIS_UNKNOWN':'NO_COMPLETE_ECONOMIC_EVIDENCE',
      crossMint:paths.length?'TEMPORAL_PATH_CANDIDATES_ONLY':'UNKNOWN_NO_VERIFIED_CROSS_MINT_PATH',
      participation:'UNASSESSED_NO_HISTORIC_EXECUTABLE_ENTRY_EXIT_QUOTES',
      monitoring:'NOT_RUNNING_NO_AUTONOMOUS_WATCHER',
    },
    keyWalletCandidates:watches,
    crossMintCandidates:paths,
    anchors,
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
