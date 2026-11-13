import test from 'node:test';
import assert from 'node:assert/strict';
import { projectMintNetwork } from '../server/intelligence/economic-network.mjs';
import { traceEconomicClaims } from '../server/intelligence/economic-claim-trace.mjs';
import { run as inspectMint } from '../server/intelligence/mint-economic-evidence.mjs';

const M='GTNHLKQWKZHaHpd6PjfMgfFZUDEuCviwXMwYbCcepump';
const A='4p7SeR6361WJ4T4icgsYTnzAUzfA5NwM4CwYD9kMBjuK';
const B='BTmCme13XXrD3VLxXFChL9VnmicJ5PjkVUpAsjrooEYh';
const row=(sig,verified=true,more={})=>({
 signature:sig,outerI:0,innerI:-1,mint:M,fromOwner:A,toOwner:B,
 fromAccount:'ATA_A',toAccount:'ATA_B',amountRaw:'100000000',
 blockTime:1700000000,slot:150,
 rpcSha256:verified?'a'.repeat(64):null,rpcHashVerified:verified,
 instructionVerifiedAgainstRpc:verified,captureSource:'SYNTHETIC_FIXTURE',
 observedSells:[{sig:'later-sale'}],...more,
});

test('claim keeps archived RPC reference, local sell as distinct evidence and knowledge as interpretation only',()=>{
 const network=projectMintNetwork({mint:M,recipients:[row('transfer') ]});
 const trace=traceEconomicClaims({mint:M,network});
 assert.equal(trace.kind,'READ_ONLY_ECONOMIC_CLAIM_LINEAGE');
 assert.equal(trace.claims.length,1);
 const claim=trace.claims[0];
 assert.equal(claim.factStatus,'LOCAL_ARCHIVE_VERIFIED_NOT_LIVE');
 assert.equal(claim.evidence[0].signature,'transfer');
 assert.equal(claim.evidence[0].archiveSha256,'a'.repeat(64));
 assert.equal(claim.evidence[0].outerI,0);
 assert.equal(claim.evidence[0].innerI,-1);
 assert.equal(claim.evidence[0].status,'LOCAL_RPC_DIGEST_AND_INDEX_CHECKED');
 assert.equal(claim.evidence[0].verificationScope,'ARCHIVED_BYTES_NOT_INDEPENDENT_MAINNET_REQUERY');
 assert.equal(claim.separateFollowup.evidence[0].signature,'later-sale');
 assert.equal(claim.separateFollowup.doesNotEstablish,'SALE_OF_THIS_RECEIVED_INVENTORY');
 assert.ok(claim.cannotEstablish.includes('COMMON_BENEFICIAL_CONTROL'));
 assert.ok(claim.knowledgeContext.some(k=>k.unit==='D04-K01'));
 assert.ok(claim.knowledgeContext.every(k=>/CONTEXT|HYPOTHESES/.test(k.role)));
 assert.equal(trace.sourceHistoryComplete,false);
 assert.equal(trace.modelInterpretationAudited,false);
});
test('unverified index or missing digest cannot become verified archival observation',()=>{
 const out=traceEconomicClaims({mint:M,network:projectMintNetwork({mint:M,recipients:[row('unverified',false)]})});
 assert.equal(out.claims[0].factStatus,'CAPTURED_REPORT_PARTIAL');
 assert.equal(out.claims[0].evidence[0].status,'ARCHIVE_OR_EVENT_IDENTITY_NOT_VERIFIED');
 assert.equal(out.claims[0].evidence[0].archiveSha256,null);
});
test('same event cannot be used across wrong Mint and trace is bounded independently of graph view',()=>{
 const network=projectMintNetwork({mint:M,recipients:[row('s1')]});
 assert.throws(()=>traceEconomicClaims({mint:'wrong',network}),/CLAIM_TRACE_NETWORK_INPUT_INVALID/);
 const rows=Array.from({length:150},(_,i)=>row('s'+i,false));
 const out=traceEconomicClaims({mint:M,network:projectMintNetwork({mint:M,recipients:rows})});
 assert.equal(out.claims.length,100);
 assert.equal(out.truncated,true);
});
test('existing Mint evidence capability includes reverse trace without provider, database or trading service',async()=>{
 const report={
  mode:'OFFLINE_READ_ONLY_SQLITE_MINT_REPORT',
  input:{mint:M},recipients:[row('transfer')],
  evidence:{indexedCoverage:'ONLY_CAPTURED_RPC_TX_AND_RESOLVED_TOKEN_ACCOUNT_OWNERS',
   knownSenderMintCaptures:1,senderDiscovery:{selectedSenders:1,truncated:false}},
 };
 let calls=0;
 const output=await inspectMint({mint:M,readEconomic:async({mint})=>{
   calls++;assert.equal(mint,M);return report;
 }});
 assert.equal(calls,1);
 assert.equal(output.facts.network.eventCount,1);
 assert.equal(output.facts.claimTrace.claims[0].evidence[0].archiveSha256,'a'.repeat(64));
 assert.equal(output.evidenceLevel,'CAPTURED_LOCAL_ARCHIVE_NOT_FULL_CHAIN_VERIFIED');
 assert.equal(output.facts.claimTrace.sourceHistoryComplete,false);
});
