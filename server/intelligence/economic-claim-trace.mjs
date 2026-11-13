// Claim-level reverse trace over the SAME locally observed transfer events.
// No new fetch, database, model, expert system or inferred wallet controller.
// A trace explains where a statement came from; it is not proof that the
// economic mechanism behind that statement is true on the complete chain.
// Cross-layer contract BLX-K-INVENTORY-PROVENANCE:
// a later wallet sell summary MUST remain separate from evidence that the
// transferred inventory batch was actually sold; cost basis remains UNKNOWN.
// Trace: docs/project/cross-layer-anchor-map-20261113.md; test/economic-claim-trace.test.mjs.
const LIMIT=100;
const KNOWLEDGE=Object.freeze([
  {unit:'D01-K07',path:'knowledge/foundations/solana-chain-and-market.md',
    role:'PROTOCOL_INTERPRETATION_CONTEXT_NOT_TRANSACTION_EVIDENCE'},
  {unit:'D04-K01',path:'knowledge/mechanisms/wallet-roles-and-inventory.md',
    role:'WALLET_ROLE_INTERPRETATION_CONTEXT_NOT_IDENTITY_PROOF'},
  {unit:'D05-K01',path:'knowledge/mechanisms/capital-organization-and-incentives.md',
    role:'ECONOMIC_RELATION_HYPOTHESES_NOT_CONTROL_PROOF'},
]);
function evidenceRef(event) {
  const verified=event.rpcHashVerified===true &&
    event.instructionVerifiedAgainstRpc===true &&
    /^[a-f0-9]{64}$/.test(event.rpcSha256||'') &&
    event.hasInstructionIdentity===true;
  return {
    kind:'LOCAL_CAPTURED_RPC_TOKEN_INSTRUCTION',
    signature:event.signature,outerI:event.outerI,innerI:event.innerI,
    slot:event.slot,blockTime:event.blockTime,
    fromAccount:event.fromAccount,toAccount:event.toAccount,
    fromOwner:event.fromOwner,toOwner:event.toOwner,amountRaw:event.amountRaw,
    archiveSha256:event.rpcSha256??null,
    rpcHashVerified:event.rpcHashVerified===true,
    instructionVerifiedAgainstRpc:event.instructionVerifiedAgainstRpc===true,
    captureSource:event.captureSource??'UNKNOWN',
    commitment:event.commitment??null,
    status:verified?'LOCAL_RPC_DIGEST_AND_INDEX_CHECKED':'ARCHIVE_OR_EVENT_IDENTITY_NOT_VERIFIED',
    verificationScope:'ARCHIVED_BYTES_NOT_INDEPENDENT_MAINNET_REQUERY',
  };
}
export function traceEconomicClaims({mint,network}={}){
  if(typeof mint!=='string'||network?.mint!==mint||!Array.isArray(network.events))
    throw Error('CLAIM_TRACE_NETWORK_INPUT_INVALID');
  const entries=network.events.slice(0,LIMIT).map(event=>{
    const ref=evidenceRef(event);
    const strong=ref.status==='LOCAL_RPC_DIGEST_AND_INDEX_CHECKED';
    const sells=[...new Set((event.sellSignatures||[]).filter(x=>typeof x==='string'))]
      .slice(0,5).map(signature=>({
        kind:'LOCAL_WALLET_TRADE_SELL_SUMMARY',signature,
        evidenceLevel:'INDEXED_SUMMARY_NOT_INVENTORY_PROVENANCE',
      }));
    return {
      claimId:'observed-transfer:'+mint+':'+event.eventId,
      statement:'TOKEN_TRANSFER_BETWEEN_RESOLVED_TOKEN_ACCOUNT_OWNERS',
      factStatus:strong?'LOCAL_ARCHIVE_VERIFIED_NOT_LIVE':'CAPTURED_REPORT_PARTIAL',
      observed:{
        mint,fromOwner:event.fromOwner,toOwner:event.toOwner,
        rawAmount:event.amountRaw,blockTime:event.blockTime,
        tokenTransferEventId:event.eventId,
      },
      supports:['A captured token-transfer instruction connects the indicated token accounts and resolved owners.'],
      evidence:[ref],
      separateFollowup:{
        assertion:'LATER_LOCAL_SELL_SUMMARY_MAY_BE_PRESENT',
        status:sells.length?'OBSERVED_LOCAL_SUMMARY_ONLY':'NOT_OBSERVED_OR_NOT_COVERED',
        evidence:sells,
        doesNotEstablish:'SALE_OF_THIS_RECEIVED_INVENTORY',
      },
      alternativeExplanations:[
        'Wallet transfer/reorganization or third-party custody',
        'Pool/router/public-service infrastructure instead of a privately controlled wallet',
        'Later sale may involve other inventory held by the recipient',
      ],
      cannotEstablish:[
        'COMMON_BENEFICIAL_CONTROL','PROVEN_TRANSFERRED_INVENTORY_SALE',
        'PROFIT','FULL_WALLET_HISTORY','CROSS_MINT_LAMPORT_PROVENANCE',
      ],
      knowledgeContext:KNOWLEDGE.map(x=>({...x})),
      producedBy:[
        'server/economic-events.mjs',
        'scripts/inspect-economic-mint.mjs',
        'server/intelligence/economic-network.mjs',
        'server/intelligence/economic-claim-trace.mjs',
      ],
      offlineTestReferences:[
        'test/offline-mint-report.test.mjs',
        'test/economic-network.test.mjs',
        'test/economic-claim-trace.test.mjs',
      ],
      validation:'SOURCE_CODE_AND_OFFLINE_TEST_NOT_INDEPENDENT_LIVE_CHAIN',
      invalidateOrRecheckWhen:[
        'Raw RPC signature or digest does not match the captured archive',
        'Token account owner is ambiguous or an address is a common service',
        'History paging, Token-2022 fees or CPI changes the economic interpretation',
      ],
    };
  });
  return {
    schemaVersion:'0.1',kind:'READ_ONLY_ECONOMIC_CLAIM_LINEAGE',
    mint,claims:entries,
    truncated:network.events.length>LIMIT||network.inputTruncated===true,
    sourceHistoryComplete:false,modelInterpretationAudited:false,
    limitations:[
      'A provenance link is not evidence of verified economic control or a complete chain history.',
      'Knowledge domain references document interpretation methods; they are not independent confirmation of a given transaction.',
      'A sell summary is a different evidence type and cannot prove that transferred inventory was sold.',
    ],
  };
}
