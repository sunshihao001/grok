// An opt-in AI-selected investigation from Blix's EXISTING Pulse board snapshot.
// The browser provides a bounded observation shortlist; it is not a market-wide
// source, a verified feed or a claim that an opportunity can be traded.
// The model can ONLY select a Mint already present in the validated shortlist.
const MINT=/^[1-9A-HJ-NP-Za-km-z]{32,44}$/;
const STAGES=new Set(['new','stretch','migrated','running']);
const MAX_CANDIDATES=12;
const safeNumber=(n,max)=>typeof n==='number'&&Number.isFinite(n)&&n>=0&&n<=max?n:null;
const safeText=(s,max)=>typeof s==='string'?s.slice(0,max):'';

export function validatePulseDiscoveryInput(value,now=Date.now()) {
  if(!value||typeof value!=='object'||Array.isArray(value)||
     Object.keys(value).some(x=>!['goal','candidates','browserRecordedAtMs','boardStatus'].includes(x))||
     typeof value.goal!=='string'||value.goal.trim().length<2||value.goal.length>1600||
     !Array.isArray(value.candidates)||!value.candidates.length||
     value.candidates.length>MAX_CANDIDATES||
     value.boardStatus!=='BLIX_PULSE_LIVE_OR_POLLING'||
     !Number.isSafeInteger(value.browserRecordedAtMs)||
     Math.abs(now-value.browserRecordedAtMs)>30_000)
    throw Error('DISCOVERY_INPUT_INVALID_OR_STALE');
  const seen=new Set(),candidates=[];
  for(const c of value.candidates) {
    if(!c||typeof c!=='object'||Array.isArray(c)||!MINT.test(c.mint||'')||
       !STAGES.has(c.stage)||seen.has(c.mint)||
       Object.keys(c).some(x=>!['mint','stage','symbol','mcap','liq','vol','buys','sells','traders','chg1m'].includes(x)))
      throw Error('DISCOVERY_CANDIDATE_INVALID');
    seen.add(c.mint);
    candidates.push({
      mint:c.mint,stage:c.stage,symbol:safeText(c.symbol,42),
      mcap:safeNumber(c.mcap,1e15),liq:safeNumber(c.liq,1e15),
      vol:safeNumber(c.vol,1e15),buys:safeNumber(c.buys,1e9),
      sells:safeNumber(c.sells,1e9),traders:safeNumber(c.traders,1e9),
      chg1m:typeof c.chg1m==='number'&&Number.isFinite(c.chg1m)&&Math.abs(c.chg1m)<=100000?c.chg1m:null,
    });
  }
  return {
    goal:value.goal.trim(),candidates,
    source:'USER_BROWSER_BLIX_PULSE_SNAPSHOT_UNVERIFIED',
    sourceRecordedAtMs:value.browserRecordedAtMs,
    sourceFreshness:'CLIENT_RECORDED_AT_NOT_INDEPENDENT_PROVIDER_TIMESTAMP',
    marketCoverage:'ONLY_SUBMITTED_BLIX_CANDIDATES_NOT_ALL_SOLANA',
  };
}

export async function discoverPulseInvestigation({input,model,readEconomic,loadKnowledge,
  now=Date.now,runResearch}={}) {
  const candidate=validatePulseDiscoveryInput(input,now());
  if(typeof model!=='function'||typeof readEconomic!=='function'||typeof runResearch!=='function')
    throw Error('DISCOVERY_DEPENDENCIES_MISSING');
  const proposal=await model({
    stage:'discover',goal:candidate.goal,
    candidates:candidate.candidates,
    marketSource:{source:candidate.source,sourceRecordedAtMs:candidate.sourceRecordedAtMs,
      sourceFreshness:candidate.sourceFreshness,marketCoverage:candidate.marketCoverage},
    constraints:[
      'Choose the most useful next investigation among the submitted Mint candidates, not necessarily the biggest price gainer.',
      'Market fields are browser observations, not chain proof or executable fill quotes.',
      'Never infer trade profitability, controller identity, or complete market coverage from Pulse.',
      'If all candidates lack usable data, return mint:null with reason.',
    ],
  });
  if(!proposal||typeof proposal!=='object'||Array.isArray(proposal)||
     !(proposal.mint===null || typeof proposal.mint==='string')||
     typeof proposal.reason!=='string'||!proposal.reason.trim()||proposal.reason.length>500)
    throw Error('DISCOVERY_MODEL_SELECTION_INVALID');
  const selected=proposal.mint===null?null:candidate.candidates.find(x=>x.mint===proposal.mint);
  if(proposal.mint!==null&&!selected)throw Error('DISCOVERY_MODEL_MINT_NOT_IN_SHORTLIST');
  const discovery={
    kind:'AI_PULSE_INVESTIGATION_SELECTION_NOT_TRADE_RECOMMENDATION',
    source:candidate.source,marketCoverage:candidate.marketCoverage,
    sourceRecordedAtMs:candidate.sourceRecordedAtMs,
    sourceFreshness:candidate.sourceFreshness,
    candidateCount:candidate.candidates.length,
    selectedMint:selected?.mint??null,selectedObservation:selected??null,
    reason:proposal.reason.trim(),modelSelectionVerified:false,
    unknowns:[
      'The Pulse shortlist may omit other tokens and wallet-driven opportunities.',
      'Browser-recorded time does not independently prove provider quote freshness.',
      'A selected investigation target is not a verified profitable or tradable opportunity.',
    ],
  };
  if(!selected)return{status:'NO_INVESTIGATION_CANDIDATE_SELECTED',discovery,investigation:null,
    verifiedMarketOpportunity:false,liveExecutionValidated:false};
  // Crucially: model-selected Mint is validated against the browser shortlist and then
  // becomes the only authorised Mint for the already existing bounded read-only workflow.
  const investigation=await runResearch({
    goal:candidate.goal, mint:selected.mint,
    model,readEconomic,loadKnowledge,
  });
  return{status:'INVESTIGATION_DRAFT_ONLY',discovery,investigation,
    verifiedMarketOpportunity:false,liveExecutionValidated:false};
}
