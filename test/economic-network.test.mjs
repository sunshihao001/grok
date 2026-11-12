import test from 'node:test';
import assert from 'node:assert/strict';
import { projectMintNetwork } from '../server/intelligence/economic-network.mjs';
const M='GTNHLKQWKZHaHpd6PjfMgfFZUDEuCviwXMwYbCcepump';
const row=(s,i,j,a,b,raw,more={})=>({signature:s,outerI:i,innerI:j,mint:M,fromOwner:a,toOwner:b,amountRaw:raw,blockTime:1000,slot:100,...more});
test('distinct CPI positions, duplicate exact events and BigInt transfer flows stay correct',()=>{
 const out=projectMintNetwork({mint:M,recipients:[row('s1',0,-1,'A','B','400000000000000000000'),row('s1',0,-1,'A','B','400000000000000000000'),row('s1',0,0,'A','B','200000000000000000000'),row('s2',0,0,'B','C','300000000000000000000')]});
 assert.equal(out.eventCount,3);assert.equal(out.distinctSignatureCount,2);assert.equal(out.knownRawTransferred,'900000000000000000000');
 assert.equal(out.edges.find(e=>e.fromOwner==='A').eventCount,2);assert.equal(out.edges.find(e=>e.fromOwner==='A').signatureCount,1);
 const b=out.walletFlows.find(w=>w.wallet==='B');assert.equal(b.observedInRaw,'600000000000000000000');assert.equal(b.observedNetTransferRaw,'300000000000000000000');
 assert.equal(b.currentBalance,'UNKNOWN');assert.equal(b.realizedPnl,'UNKNOWN');assert.equal(out.edges[0].relationIsCommonControl,false);
});
test('sender fan-out and later seller are investigation candidates, not controller or inventory proof',()=>{
 const g=projectMintNetwork({mint:M,recipients:[row('s1',0,-1,'A','B','100',{observedSells:[{sig:'sell-later'}]}),row('s2',0,-1,'A','C','50')]});
 assert.equal(g.distributionCandidates.length,1);assert.equal(g.distributionCandidates[0].recipientCount,2);
 assert.match(g.distributionCandidates[0].meaning,/NOT_A_COMMON_CONTROLLER/);
 assert.ok(g.walletFlows.find(w=>w.wallet==='B').roles.includes('LOCAL_SELL_SUMMARY_NOT_TRANSFER_INVENTORY_PROVENANCE'));
});
test('missing instruction identity, unknown amount and incompatible Mint never become fabricated facts',()=>{
 const g=projectMintNetwork({mint:M,recipients:[row('s1',undefined,undefined,'A','B','bad'),row('s1',undefined,undefined,'A','B','1'),row('s2',0,0,'A','C','0'),row('s3',0,0,'A','B','5',{mint:'wrong'}),row('s4',0,0,'A',null,'5')]});
 assert.equal(g.eventCount,3);assert.equal(g.skippedEvents,2);assert.equal(g.unknownAmountEvents,1);assert.equal(g.knownRawTransferred,'1');
 assert.ok(g.warnings.includes('SOME_EVENT_IDENTITIES_LACK_INSTRUCTION_POSITION'));
 assert.ok(g.warnings.includes('UNRESOLVED_OR_MISMATCHED_TRANSFER_EVENTS_SKIPPED'));
});
test('conflicting duplicate instruction is flagged not counted twice',()=>{
 const g=projectMintNetwork({mint:M,recipients:[row('s',0,1,'A','B','10'),row('s',0,1,'A','C','10')]});
 assert.equal(g.eventCount,1);assert.equal(g.conflictingEventIdentities,1);
});
test('bounded source makes truncation visible',()=>{
 const g=projectMintNetwork({mint:M,recipients:Array.from({length:230},(_,i)=>row('s'+i,0,-1,'A','B','1'))});
 assert.equal(g.eventCount,200);assert.equal(g.knownRawTransferred,'200');assert.equal(g.inputTruncated,true);
});


test('one observed sell or cross-Mint path attached to multiple receipts is counted once',()=>{
 const repeated={observedSells:[{sig:'same-sell'}],crossMintCandidates:[{
   fundingSig:'funding',buySig:'follow-buy',boughtMint:'OTHER',soldMint:M,
 }]};
 const graph=projectMintNetwork({mint:M,recipients:[
   row('transfer1',0,-1,'A','B','100',repeated),
   row('transfer2',0,-1,'A','B','200',repeated),
 ]});
 assert.equal(graph.eventCount,2);
 assert.equal(graph.edges[0].eventCount,2);
 assert.equal(graph.edges[0].crossMintCandidateCount,1);
 assert.equal(graph.walletFlows.find(x=>x.wallet==='B').localSellSummaryCount,1);
 assert.ok(graph.warnings.some(x=>/multiple hops/.test(x)));
});
