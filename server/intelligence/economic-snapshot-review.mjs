// Compare immutable projections of already captured local SQLite evidence.
// This is NOT a live watcher, scheduler, PnL calculator or chain reorg detector.
// Later visibility may reflect RPC backfill, different sampling or added wallets.
function snap(value){
  const n=value?.facts?.network ?? value?.network ?? value;
  const observedAt=value?.observedAt ?? null;
  if(!n || typeof n.mint!=='string' || !Array.isArray(n.events) ||
    !Array.isArray(n.walletFlows)) throw Error('NETWORK_SNAPSHOT_INVALID');
  return {network:n,observedAt};
}
const identified = event => event?.hasInstructionIdentity===true &&
  typeof event.eventId==='string' && typeof event.signature==='string';
const narrow = events=>events.slice(0,200).map(e=>({
  eventId:e.eventId,signature:e.signature,slot:e.slot ?? null,
  blockTime:e.blockTime ?? null,fromOwner:e.fromOwner,toOwner:e.toOwner,
  amountRaw:e.amountRaw ?? null,
}));

export function compareCapturedMintSnapshots(before,after){
  const a=snap(before),b=snap(after);
  if(a.network.mint!==b.network.mint)throw Error('DIFFERENT_MINT_SNAPSHOTS');
  const first=a.network.events.filter(identified),second=b.network.events.filter(identified);
  const old=new Map(first.map(e=>[e.eventId,e])),newIds=new Set(second.map(e=>e.eventId));
  const additions=second.filter(e=>!old.has(e.eventId));
  const omissions=first.filter(e=>!newIds.has(e.eventId));
  const fingerprint=e=>JSON.stringify([e.fromOwner,e.toOwner,e.amountRaw,e.slot,e.blockTime,
    e.sellObservation,e.sellSignatures,e.crossMintCandidates]);
  const revisions=second.filter(e=>old.has(e.eventId)&&fingerprint(e)!==fingerprint(old.get(e.eventId)))
    .map(e=>({eventId:e.eventId,previous:narrow([old.get(e.eventId)])[0],current:narrow([e])[0],
      meaning:'LOCAL_EVIDENCE_METADATA_OR_FOLLOWUP_REVISED_NOT_A_NEW_CHAIN_EVENT'}));
  const warnings=['NEWLY_VISIBLE means newly present in a local sample, not newly emitted on Solana.',
    'No longer visible does not prove token was sold, wallet disappeared, or chain reversed.',
    'Neither snapshot establishes complete on-chain history.'];
  if(a.network.inputTruncated || b.network.inputTruncated)
    warnings.push('Input sample truncated; differences may be selection artifacts.');
  if(a.network.events.some(e=>!identified(e)) || b.network.events.some(e=>!identified(e)))
    warnings.push('Some events lack instruction positions and cannot be safely diffed.');
  if(a.observedAt && b.observedAt && Date.parse(b.observedAt)<Date.parse(a.observedAt))
    warnings.push('Snapshot capture order is reversed; temporal interpretation UNKNOWN.');
  return {
    schemaVersion:'0.1',mint:a.network.mint,kind:'LOCAL_ARCHIVE_VISIBILITY_DELTA',
    beforeObservedAt:a.observedAt,afterObservedAt:b.observedAt,
    hasCompleteWalletHistory:false,liveChainEventChange:'UNKNOWN',
    newlyVisible:narrow(additions),
    noLongerVisibleInSample:narrow(omissions),
    revisedCapturedEvents:revisions,
    persistingEventCount:second.filter(e=>old.has(e.eventId)).length,
    uncomparableEventCount:a.network.events.length-first.length +
      b.network.events.length-second.length,
    warnings,
  };
}

export function compareCapturedCrossMintWallets(first,second){
  const a=snap(first),b=snap(second);
  if(a.network.mint===b.network.mint)throw Error('CROSS_MINT_REQUIRES_DISTINCT_MINTS');
  const left=new Map(a.network.walletFlows.map(x=>[x.wallet,x]));
  const right=new Map(b.network.walletFlows.map(x=>[x.wallet,x]));
  const shared=[...left.keys()].filter(wallet=>right.has(wallet)).sort().slice(0,200)
    .map(wallet=>({
      wallet,firstMintRoles:left.get(wallet).roles,secondMintRoles:right.get(wallet).roles,
      addressClass:'UNCLASSIFIED_INCLUDES_INFRASTRUCTURE',economicController:'UNKNOWN',
      identityProof:'SAME_OBSERVED_ADDRESS_ONLY',
    }));
  return {
    schemaVersion:'0.1',kind:'CROSS_MINT_CAPTURED_WALLET_OVERLAP_CANDIDATE',
    mints:[a.network.mint,b.network.mint],overlappingWallets:shared,
    truncated:shared.length===200 || a.network.inputTruncated || b.network.inputTruncated,
    commonControl:'UNKNOWN',capitalProvenance:'UNKNOWN',walletHistoryComplete:false,
    limitations:[
      'Overlapping owner addresses are observed in bounded local captured transfers, not proven economic controllers.',
      'An exchange, pool, router or shared program may account for overlap.',
      'No two-Mint portfolio profit or strategy edge can be established by this overlap.',
    ],
  };
}
