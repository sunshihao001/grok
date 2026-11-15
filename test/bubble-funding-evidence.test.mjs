// Focused regression of Blix Bubble Map funding provenance; no network or Blix server.
import test from 'node:test';
import assert from 'node:assert/strict';
import { DatabaseSync } from 'node:sqlite';
import {
  directSolFunding, traceWalletFunding, feePayer, initBubbleFundingCache,
  verifiedFunder, shouldRefreshFunding, FUNDING_TRUNCATED, FUNDING_DIRECT,
} from '../server/bubble-funding-evidence.mjs';

const W='WALLET_HOLDER', P='PAYER_SERVICE', F='REAL_SOL_SENDER';
const SYS='11111111111111111111111111111111';
const transfer=(source,destination,lamports)=>({program:'system',programId:SYS,
  parsed:{type:'transfer',info:{source,destination,lamports}}});
const createAccount=(source,newAccount,lamports)=>({programId:SYS,
  parsed:{type:'createAccount',info:{source,newAccount,lamports}}});
function rpc(outer=[], {payer=P,inner=[],err=null}={}) {
  return {transaction:{message:{accountKeys:[{pubkey:payer},W,F],
    instructions:outer}},meta:{err,innerInstructions:inner}};
}
const one = (tx, sig='first') => traceWalletFunding(W,{
  page:async()=>[{signature:sig}],
  transaction:async got=>{assert.equal(got,sig);return tx;},
});

test('fee payer alone never becomes a direct funding relation or graph edge evidence',async()=>{
  const result=await one(rpc([{program:'system',parsed:{type:'assign',info:{account:W,owner:F}}}]));
  assert.equal(result.status,'FEE_PAYER_ONLY');
  assert.equal(result.payer,P);
  assert.equal(result.funder,null);
  assert.equal(verifiedFunder(result),null);
});

test('explicit positive native SOL transfer to wallet is a funding edge, even if fee payer differs',async()=>{
  const result=await one(rpc([transfer(F,W,1500000000)]));
  assert.equal(result.status,FUNDING_DIRECT);
  assert.equal(result.funder,F);
  assert.equal(result.payer,P);
  assert.equal(verifiedFunder(result),F);
  assert.equal(feePayer(rpc([])),P);
});

test('createAccount funding and parsed inner CPI transfer are independently recognized',async()=>{
  assert.equal(directSolFunding(rpc([createAccount(F,W,25000)]),W)?.funder,F);
  const cpi=rpc([],{inner:[{index:0,instructions:[transfer(F,W,5000)]}]});
  assert.equal(directSolFunding(cpi,W)?.funder,F);
});

test('two independent SOL senders in the same earliest transaction must not collapse into one funder',async()=>{
  const tx=rpc([transfer(F,W,1000),transfer('SECOND_SENDER',W,4000)]);
  const individual=directSolFunding(tx,W);
  assert.equal(individual.ambiguous,true);
  assert.deepEqual(individual.sources,[F,'SECOND_SENDER']);
  const result=await one(tx);
  assert.equal(result.status,'MULTIPLE_DIRECT_SOL_SENDERS');
  assert.equal(result.funder,null);
  assert.equal(verifiedFunder(result),null);
});

test('failed transactions, zero-lamport instructions and unrelated recipients do not fund target',async()=>{
  assert.equal(directSolFunding(rpc([transfer(F,W,2)],{err:{InstructionError:[0,'Custom']}}),W),null);
  assert.equal(directSolFunding(rpc([transfer(F,W,0)]),W),null);
  assert.equal(directSolFunding(rpc([transfer(F,'OTHER',20)]),W),null);
  const result=await one(rpc([transfer(F,W,100)],{err:{InstructionError:[0,'Custom']}}));
  assert.equal(result.funder,null);
  assert.equal(result.status,'FEE_PAYER_ONLY');
});

test('3 full pages are TRUNCATED not no-funder, then a bounded later read resumes from cursor',async()=>{
  let pageCount=0,txReads=0;
  const first=await traceWalletFunding(W,{
    page:async before=>{
      if(pageCount===0)assert.equal(before,null);
      else assert.equal(before,`page-${pageCount-1}-999`);
      const index=pageCount++;
      return Array.from({length:1000},(_,i)=>({signature:`page-${index}-${i}`}));
    },
    transaction:async()=>{txReads++;return rpc([transfer(F,W,123)]);},
    maxPages:3,
  });
  assert.equal(first.status,FUNDING_TRUNCATED);
  assert.equal(first.funder,null);
  assert.equal(first.payer,null);
  assert.equal(txReads,0);
});

test('durable history cursor resumes without rescanning, and only oldest observed tx may prove funding',async()=>{
  let n=0;const cursors=[];let txReads=0;
  const readPage=async before=>{
    cursors.push(before);
    if(n<3)return Array.from({length:1000},(_,i)=>({signature:`page-${n}-${i}`})).map(x=>x);
    return [{signature:'true-earliest'}];
  };
  const paged=async before=>{const r=await readPage(before);n++;return r;};
  const transaction=async signature=>{txReads++;assert.equal(signature,'true-earliest');return rpc([transfer(F,W,50)]);};
  const first=await traceWalletFunding(W,{page:paged,transaction});
  assert.equal(first.status,FUNDING_TRUNCATED);assert.equal(first.cursor,'page-2-999');assert.equal(txReads,0);
  const resumed=await traceWalletFunding(W,{
    page:paged,transaction,cursor:first.cursor,lastSignature:first.signature,
  });
  assert.equal(resumed.status,FUNDING_DIRECT);assert.equal(resumed.funder,F);
  assert.equal(resumed.signature,'true-earliest');assert.equal(resumed.cursor,null);assert.equal(txReads,1);
  assert.deepEqual(cursors,[null,'page-0-999','page-1-999','page-2-999']);
});

test('empty history and unavailable earliest transaction remain UNKNOWN rather than no-funder proof',async()=>{
  const empty=await traceWalletFunding(W,{page:async()=>[],transaction:async()=>{throw Error('should not call');}});
  assert.equal(empty.status,'NO_VISIBLE_HISTORY');assert.equal(empty.funder,null);
  const missing=await traceWalletFunding(W,{page:async()=>[{signature:'old'}],transaction:async()=>null});
  assert.equal(missing.status,'EARLIEST_TX_UNAVAILABLE');assert.equal(missing.signature,'old');
});

test('legacy cached fee-payer rows are unverified after in-place migration and never count as a funding edge',()=>{
  const db=new DatabaseSync(':memory:');
  try{
    db.exec('CREATE TABLE bubble_funders (wallet TEXT PRIMARY KEY,funder TEXT NOT NULL,t INTEGER NOT NULL)');
    db.prepare('INSERT INTO bubble_funders VALUES (?,?,?)').run(W,P,123);
    initBubbleFundingCache(db);
    initBubbleFundingCache(db); // migration idempotence
    const prior=db.prepare('SELECT * FROM bubble_funders WHERE wallet=?').get(W);
    assert.equal(prior.funder,P);
    assert.equal(prior.status,'UNVERIFIED_LEGACY');
    assert.equal(verifiedFunder(prior),null);
    assert.equal(shouldRefreshFunding(prior),true);
    db.prepare("UPDATE bubble_funders SET funder=?,status='DIRECT_SOL_OBSERVED',signature=? WHERE wallet=?")
      .run(F,'source-signature',W);
    const verified=db.prepare('SELECT * FROM bubble_funders WHERE wallet=?').get(W);
    assert.equal(verifiedFunder(verified),F);
  } finally {db.close();}
});

test('partial history is eligible for bounded retry, not permanently cached as no relation',()=>{
  const t=5000000000;
  const row={status:FUNDING_TRUNCATED,funder:'',cursor:'oldest-scanned',t};
  assert.equal(shouldRefreshFunding(row,t+5000),false);
  assert.equal(shouldRefreshFunding(row,t+60*60_000+1),true);
});
