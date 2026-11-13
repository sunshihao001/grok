// Pure read-only projection of PR23's captured Token transfer instructions.
// This is a graph VIEW over the existing economic journal, not an identity,
// PnL, ownership or new historical transaction index.
const LIMIT = 200;
const raw = x => typeof x === 'string' && /^\d+$/.test(x) ? BigInt(x) : null;
const chronological = (a,b) => (a.blockTime ?? Number.MAX_SAFE_INTEGER) -
  (b.blockTime ?? Number.MAX_SAFE_INTEGER) || (a.slot ?? 0) - (b.slot ?? 0) ||
  a.eventId.localeCompare(b.eventId);

export function projectMintNetwork({ mint, recipients = [] } = {}) {
  if (typeof mint !== 'string' || !Array.isArray(recipients)) throw Error('NETWORK_INPUT_INVALID');
  const events = [], seen = new Map(), warnings = [];
  let unidentified = 0, ambiguousPositions = 0, conflicts = 0;
  const inputTruncated = recipients.length > LIMIT;
  for (const [i, row] of recipients.slice(0, LIMIT).entries()) {
    if (!row || row.mint != null && row.mint !== mint ||
      typeof row.signature !== 'string' || !row.signature ||
      typeof row.fromOwner !== 'string' || !row.fromOwner ||
      typeof row.toOwner !== 'string' || !row.toOwner ||
      row.fromOwner === row.toOwner) { unidentified++; continue; }
    const positioned = Number.isInteger(row.outerI) && Number.isInteger(row.innerI);
    const eventId = positioned
      ? row.signature + ':' + row.outerI + ':' + row.innerI
      : row.signature + ':POSITION_UNKNOWN:' + i;
    if (!positioned) ambiguousPositions++;
    if (positioned && seen.has(eventId)) {
      const old = seen.get(eventId);
      if (old.fromOwner !== row.fromOwner || old.toOwner !== row.toOwner ||
        old.amountRaw !== row.amountRaw) conflicts++;
      continue;
    }
    const amount = raw(row.amountRaw);
    const event = {
      eventId, signature: row.signature, outerI: positioned ? row.outerI : null,
      innerI: positioned ? row.innerI : null, mint, fromOwner: row.fromOwner,
      toOwner: row.toOwner, fromAccount: row.fromAccount ?? null,
      toAccount: row.toAccount ?? null, amountRaw: amount?.toString() ?? null,
      blockTime: Number.isSafeInteger(row.blockTime) ? row.blockTime : null,
      slot: Number.isSafeInteger(row.slot) ? row.slot : null,
      kind: 'OBSERVED_TOKEN_TRANSFER', hasInstructionIdentity: positioned,
      sellObservation: row.sellObservation ?? 'UNKNOWN',
      sellSignatures: Array.isArray(row.observedSells)
        ? [...new Set(row.observedSells.map(x=>x?.sig).filter(x=>typeof x==='string'))].slice(0,5) : [],
      crossMintCandidates: Array.isArray(row.crossMintCandidates) ?
        row.crossMintCandidates.slice(0,25).map(x=>({
          fundingSig: x.fundingSig ?? null, buySig: x.buySig ?? null,
          boughtMint: x.boughtMint ?? null, soldMint: x.soldMint ?? null,
        })) : [],
    };
    seen.set(eventId,event);
    events.push(event);
  }
  events.sort(chronological);
  const nodes = new Map(), edges = new Map();
  const nodeOf = wallet => {
    if (!nodes.has(wallet)) nodes.set(wallet, {
      wallet, observedInRaw: 0n, observedOutRaw: 0n,
      hasUnknownAmount: false, sentEventCount: 0, receivedEventCount: 0,
      localSellSignatures: new Set(), roles: new Set(), addressClass: 'UNCLASSIFIED_INCLUDES_INFRASTRUCTURE',
      economicController: 'UNKNOWN',
    });
    return nodes.get(wallet);
  };
  let knownRawTotal = 0n, unknownAmountEvents = 0;
  for (const e of events) {
    const from=nodeOf(e.fromOwner),to=nodeOf(e.toOwner);
    from.sentEventCount++; from.roles.add('OBSERVED_TOKEN_SENDER');
    to.receivedEventCount++; to.roles.add('OBSERVED_TOKEN_RECEIVER');
    if (e.sellSignatures.length) {
      for(const signature of e.sellSignatures) to.localSellSignatures.add(signature);
      to.roles.add('LOCAL_SELL_SUMMARY_NOT_TRANSFER_INVENTORY_PROVENANCE');
    }
    const quantity=raw(e.amountRaw);
    if (quantity === null) {
      unknownAmountEvents++;
      from.hasUnknownAmount=true;to.hasUnknownAmount=true;
    } else {
      from.observedOutRaw+=quantity;to.observedInRaw+=quantity;
      knownRawTotal+=quantity;
    }
    const key=JSON.stringify([e.fromOwner,e.toOwner]);
    if (!edges.has(key)) edges.set(key,{
      fromOwner:e.fromOwner,toOwner:e.toOwner,kind:'OBSERVED_TOKEN_TRANSFER',
      count:0,rawTotal:0n,amountCoverage:'COMPLETE_FOR_LISTED_EVENTS',
      signatureSet:new Set(), eventIds:[],minTime:null,maxTime:null,
      localSellSummaryObserved:false, crossMintCandidateKeys:new Set(),
      relationIsCommonControl:false, addressClassesVerified:false,
    });
    const edge=edges.get(key);edge.count++;
    edge.signatureSet.add(e.signature);edge.eventIds.push(e.eventId);
    if (quantity===null) edge.amountCoverage='PARTIAL_UNKNOWN_AMOUNT';
    else edge.rawTotal+=quantity;
    if(e.blockTime!==null) {
      edge.minTime=edge.minTime===null?e.blockTime:Math.min(edge.minTime,e.blockTime);
      edge.maxTime=edge.maxTime===null?e.blockTime:Math.max(edge.maxTime,e.blockTime);
    }
    if(e.sellSignatures.length) edge.localSellSummaryObserved=true;
    for(const candidate of e.crossMintCandidates) {
      edge.crossMintCandidateKeys.add(JSON.stringify([candidate.fundingSig,candidate.buySig,candidate.boughtMint,candidate.soldMint]));
    }
  }
  const walletFlows=[...nodes.values()].map(n=>({
    wallet:n.wallet,roles:[...n.roles].sort(),observedInRaw:n.observedInRaw.toString(),
    observedOutRaw:n.observedOutRaw.toString(),
    observedNetTransferRaw:(n.observedInRaw-n.observedOutRaw).toString(),
    amountCoverage:n.hasUnknownAmount?'PARTIAL_UNKNOWN_AMOUNT':'KNOWN_FOR_CAPTURED_EVENTS_ONLY',
    sentEventCount:n.sentEventCount,receivedEventCount:n.receivedEventCount,
    localSellSummaryCount:n.localSellSignatures.size,addressClass:n.addressClass,
    economicController:n.economicController,
    currentBalance:'UNKNOWN',costBasis:'UNKNOWN',realizedPnl:'UNKNOWN',
  })).sort((a,b)=>a.wallet.localeCompare(b.wallet));
  const relationEdges=[...edges.values()].map(e=>({
    fromOwner:e.fromOwner,toOwner:e.toOwner,kind:e.kind,eventCount:e.count,
    signatureCount:e.signatureSet.size,observedRawTotal:e.rawTotal.toString(),
    amountCoverage:e.amountCoverage,firstBlockTime:e.minTime,lastBlockTime:e.maxTime,
    eventIds:e.eventIds,localSellSummaryObserved:e.localSellSummaryObserved,
    crossMintCandidateCount:e.crossMintCandidateKeys.size,
    relationIsCommonControl:false,addressClassesVerified:false,
  })).sort((a,b)=>a.fromOwner.localeCompare(b.fromOwner)||a.toOwner.localeCompare(b.toOwner));
  const outgoing=new Map();
  for(const e of relationEdges){
    if(!outgoing.has(e.fromOwner))outgoing.set(e.fromOwner,new Set());
    outgoing.get(e.fromOwner).add(e.toOwner);
  }
  const distributionCandidates=[...outgoing].filter(([,recipients])=>recipients.size>=2)
    .map(([sender, receivers])=>({sender,recipientCount:receivers.size,
      meaning:'ONE_OBSERVED_SENDER_TO_MULTIPLE_RECIPIENTS_NOT_A_COMMON_CONTROLLER',
      needs:'Exclude airdrop, exchange, pool and public infrastructure'}));
  if(inputTruncated)warnings.push('NETWORK_INPUT_LIMIT_200_EVENTS');
  if(ambiguousPositions)warnings.push('SOME_EVENT_IDENTITIES_LACK_INSTRUCTION_POSITION');
  if(conflicts)warnings.push('CONFLICTING_DUPLICATE_INSTRUCTION_IDENTITIES');
  if(unidentified)warnings.push('UNRESOLVED_OR_MISMATCHED_TRANSFER_EVENTS_SKIPPED');
  if(unknownAmountEvents)warnings.push('RAW_TRANSFER_AMOUNT_UNKNOWN_FOR_SOME_EVENTS');
  warnings.push('Transfer graph does not establish ultimate controller, trade or current inventory.');
  warnings.push('Gross transfers across multiple hops may count the same circulating Token more than once; not independent demand or supply.');
  warnings.push('Token-2022 transfer fees may make gross instruction amount differ from freely spendable recipient balance; withheld fee is not reconstructed here.');
  return {
    schemaVersion:'0.1',mint,provenance:'CAPTURED_LOCAL_INSTRUCTION_PROJECTION',
    coverage:'PARTIAL_ARCHIVED_SENDER_SAMPLE_NOT_COMPLETE_MINT_HISTORY',
    eventCount:events.length, distinctSignatureCount:new Set(events.map(x=>x.signature)).size,
    knownRawTransferred:knownRawTotal.toString(),unknownAmountEvents,
    skippedEvents:unidentified,conflictingEventIdentities:conflicts,
    inputTruncated, walletFlows,edges:relationEdges,
    distributionCandidates,events,warnings,
  };
}
