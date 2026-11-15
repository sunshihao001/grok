// Offline followability study gate: evaluates supplied paper execution receipts,
// never sends orders or constructs fills from future OHLC. Not a strategy, trade
// recommendation, claim of positive expectancy or proof of real executable prices.
const MAX_CASES=200;
const lamports=x=>typeof x==='string' && /^\d+$/.test(x) ? BigInt(x) : null;
const clock=x=>Number.isSafeInteger(x) && x>=0;
const reply=(id,status,why,other={})=>({id,status,why,...other});
export function evaluatePaperFollowabilityCase(record) {
  const id=typeof record?.id==='string'?record.id.slice(0,100):'UNKNOWN';
  const signal=record?.signal, entry=record?.entry,exit=record?.exit;
  if(!signal || !clock(signal.chainEventAtMs) || !clock(signal.firstAvailableAtMs) ||
    signal.firstAvailableAtMs<signal.chainEventAtMs) {
    return reply(id,'UNKNOWN_SIGNAL_AVAILABILITY','Chain event time is not the follower-visible signal time.');
  }
  if(!entry || !clock(entry.fillAtMs) || !clock(entry.quoteObservedAtMs)) {
    return reply(id,'MISSING_ENTRY_EXECUTION','No timestamped entry paper fill and historical quote availability.');
  }
  if(entry.fillAtMs<signal.firstAvailableAtMs || entry.quoteObservedAtMs>entry.fillAtMs ||
    entry.quoteObservedAtMs<signal.firstAvailableAtMs) {
    return reply(id,'LOOKAHEAD_OR_UNFOLLOWABLE_ENTRY','Entry quote or fill predates the earliest available follower signal.');
  }
  if(!exit || !clock(exit.fillAtMs) || !clock(exit.quoteObservedAtMs) ||
    exit.fillAtMs<=entry.fillAtMs || exit.quoteObservedAtMs>exit.fillAtMs ||
    exit.quoteObservedAtMs<entry.fillAtMs) {
    return reply(id,'MISSING_OR_INVALID_EXIT_EXECUTION','No valid subsequent exit paper fill/available quote.');
  }
  if(!clock(entry.maxQuoteAgeMs) || entry.maxQuoteAgeMs<1 || entry.maxQuoteAgeMs>60000 ||
    !clock(exit.maxQuoteAgeMs) || exit.maxQuoteAgeMs<1 || exit.maxQuoteAgeMs>60000) {
    return reply(id,'QUOTE_FRESHNESS_UNKNOWN','Both paper fills require explicit max quote age (1..60000ms).');
  }
  if(entry.fillAtMs-entry.quoteObservedAtMs>entry.maxQuoteAgeMs ||
    exit.fillAtMs-exit.quoteObservedAtMs>exit.maxQuoteAgeMs) {
    return reply(id,'STALE_EXECUTION_QUOTE','A paper fill relied on quote data older than its stated maximum age.');
  }
  if(entry.source!=='PAPER_REPLAY' || exit.source!=='PAPER_REPLAY' ||
    entry.slippageIncluded!==true || exit.slippageIncluded!==true) {
    return reply(id,'PAPER_FILL_PROVENANCE_INCOMPLETE',
      'Paper fill provenance and explicit slippage inclusion required before illustrative PnL.');
  }
  const spent=lamports(entry.spentLamports),bought=lamports(entry.receivedTokensRaw);
  const sold=lamports(exit.soldTokensRaw),received=lamports(exit.receivedLamports);
  const feeIn=lamports(entry.feeLamports),feeOut=lamports(exit.feeLamports);
  if([spent,bought,sold,received,feeIn,feeOut].some(v=>v===null) || spent<=0n || bought<=0n ||
    sold<0n || sold>bought) {
    return reply(id,'INVALID_EXECUTION_AMOUNTS','All token and SOL raw quantities/fees must be explicit nonnegative integers.');
  }
  if(sold!==bought || record.positionContinuityVerified!==true) {
    return reply(id,'UNRESOLVED_INVENTORY_OR_PARTIAL_EXIT',
      'Partial exit or unverified transfers prevent whole-position PnL reconstruction.');
  }
  const net=received-spent-feeIn-feeOut;
  const investment=spent+feeIn;
  return reply(id,'PAPER_SCENARIO_CALCULATED_NOT_LIVE',
    'Arithmetic from timestamped paper fills only; no proof of live executable prices or positive strategy expectancy.',{
    mint:record.mint??null,followerLatencyMs:entry.fillAtMs-signal.firstAvailableAtMs,
    simulatedNetLamports:net.toString(),
    simulatedReturnBps:(net*10000n/investment).toString(),
    simulatedOutcome:net>0n?'POSITIVE':net<0n?'NEGATIVE':'FLAT',
    source:'USER_SUPPLIED_PAPER_REPLAY_RECEIPTS',
    liveExecutionValidated:false,realizedWalletPnl:'UNKNOWN',
  });
}
export function evaluatePaperFollowabilityCases(records) {
  if(!Array.isArray(records) || records.length>MAX_CASES) throw Error('FOLLOWABILITY_CASE_LIMIT');
  const cases=records.map(evaluatePaperFollowabilityCase);
  const counts=Object.fromEntries([...new Set(cases.map(x=>x.status))].sort()
    .map(status=>[status,cases.filter(x=>x.status===status).length]));
  return {
    schemaVersion:'0.1',kind:'OFFLINE_FOLLOWABILITY_ELIGIBILITY_AUDIT',
    cases,counts,inputCount:cases.length,
    measuredPopulationCoverage:'UNKNOWN',outOfSamplePerformance:'NOT_ESTABLISHED',
    liveTradeResults:'NOT_MEASURED',noTradeExecution:true,
    limitations:[
      'Wallet leader trade execution time is not when a follower could first know or fill the same trade.',
      'Only paper receipts with explicit quote availability and slippage included can produce illustrative arithmetic.',
      'A selected subset with positive paper results has survivorship and selection bias; no strategy expectancy is inferred.',
      'Live routing, slippage, failed trades, gas/rent and adverse selection require separate independent tests.',
    ],
  };
}
