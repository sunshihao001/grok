// Offline cross-module smoke test: wallet reader -> economic instruction evidence ->
// recipient follow-up -> cross-Mint temporal candidate, including post-capture failure.
// Does NOT start the main server or connect to a real wallet/RPC.
import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';

const folder=fs.mkdtempSync(path.join(os.tmpdir(),'blix-chain-'));
process.env.RADAR_DATA=folder;
process.env.BLIX_MARKET_FEEDS='0';
const { db } = await import('../server/db.js');
const wallets=await import('../server/wallets.js');
const wtrack=await import('../server/wtrack.js');
const { decodeEvidence, recipientOutcomes, recipientCandidates, transactionEvidence, walletProcessing, recordBlockTransactionOrder } = await import('../server/economic-events.mjs');
const { checkpointWalletPage, pendingWalletSignatures } =
  await import('../server/wallet-signature-coverage.mjs');

const A='4p7SeR6361WJ4T4icgsYTnzAUzfA5NwM4CwYD9kMBjuK';
const B='BTmCme13XXrD3VLxXFChL9VnmicJ5PjkVUpAsjrooEYh';
const C='9VQ3dtwAxUAxNPdD86ExhC1XsL1hiUcqEvzS4sAhUU1A';
const M='GTNHLKQWKZHaHpd6PjfMgfFZUDEuCviwXMwYbCcepump';
const N='EYqygbhZjP7EbM4fSn8devctnksAvPAD1Bt57XBFpump';
const POOL='4p7SeR6361WJ4T4icgsYTnzAUzfA5NwM4CwYD9kMBjuM';
const TOKEN='TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA';
const SYS='11111111111111111111111111111111';
const second=Math.floor(Date.now()/1000)-600;
const bal=(index,owner,mint,amount)=>({accountIndex:index,owner,mint,uiTokenAmount:{amount:String(amount),decimals:6}});
const tok=(from,to,mint,amount)=>({programId:TOKEN,program:'spl-token',parsed:{type:'transferChecked',info:{source:from,destination:to,mint,tokenAmount:{amount:String(amount),decimals:6}}}});
const sol=(from,to,lamports)=>({programId:SYS,program:'system',parsed:{type:'transfer',info:{source:from,destination:to,lamports}}});
const tx=(sig,at,keys,{pre,post,preToken=[],postToken=[],ix=[],inner=[]})=>({
 slot:1000+at-second,blockTime:at,meta:{err:null,fee:5000,preBalances:pre,postBalances:post,
 preTokenBalances:preToken,postTokenBalances:postToken,innerInstructions:inner,logMessages:[]},
 transaction:{signatures:[sig],message:{accountKeys:keys,instructions:ix}}
});
test.after(()=>{try{db.close();}catch{}fs.rmSync(folder,{recursive:true,force:true});});

test('fresh evidence schema and versioned ALT account indexes remain decodable',()=>{
  const columns=db.prepare('PRAGMA table_info(econ_transactions)').all().map(r=>r.name);
  assert.ok(columns.includes('status'),'fresh evidence schema must include the status column used by persistEvidence');
  const versioned={
    slot:2000, blockTime:2000,
    meta:{
      err:null,
      preTokenBalances:[bal(2,B,M,400_000_000),bal(3,POOL,M,0)],
      postTokenBalances:[bal(2,B,M,0),bal(3,POOL,M,400_000_000)],
      innerInstructions:[],logMessages:[]
    },
    transaction:{signatures:['ALT-sell'],message:{
      // Actual jsonParsed shape: lookup-table accounts are already in message.accountKeys.
      accountKeys:[
        {pubkey:B,source:'transaction',signer:true,writable:true},
        {pubkey:POOL,source:'transaction',signer:false,writable:true},
        {pubkey:'ALT_ATA_B',source:'lookupTable',signer:false,writable:true},
        {pubkey:'ALT_ATA_POOL',source:'lookupTable',signer:false,writable:true},
      ],
      instructions:[tok('ALT_ATA_B','ALT_ATA_POOL',M,400_000_000)]
    }}
  };
  const rows=decodeEvidence(versioned).filter(r=>r.kind==='TOKEN_TRANSFER');
  assert.equal(rows.length,1);
  assert.equal(rows[0].from_account,'ALT_ATA_B');
  assert.equal(rows[0].to_account,'ALT_ATA_POOL');
  assert.equal(rows[0].from_owner,B);
  assert.equal(rows[0].to_owner,POOL);
  assert.equal(rows[0].owner_conflict,false);
});


test('recipient candidate ordering prefers canonical slot over estimated block time',()=>{
  const SENDER='SLOT_ORDER_SENDER';
  const rows=[
    {sig:'slot-200',slot:200,blockTime:1001,amount:'10'},
    {sig:'slot-201',slot:201,blockTime:1000,amount:'20'},
  ];
  const insertTx=db.prepare(`INSERT INTO econ_transactions
    (sig,slot,block_time,status,rpc_json,sha256,observed_at,capture_source,commitment)
    VALUES (?,?,?,?,?,?,?,?,?)`);
  const insertIx=db.prepare(`INSERT INTO econ_instructions
    (sig,outer_i,inner_i,kind,program,mint,from_account,to_account,from_owner,to_owner,amount_raw,owner_conflict,raw_json)
    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)`);
  for (const r of rows) {
    insertTx.run(r.sig,r.slot,r.blockTime,'RPC_OBSERVED','{}','slot-order-'+r.sig,Date.now(),'OFFLINE_ARCHIVE','confirmed');
    insertIx.run(r.sig,0,0,'TOKEN_TRANSFER',TOKEN,M,'ATA_SENDER_'+r.sig,'ATA_B_'+r.sig,SENDER,B,r.amount,0,'{}');
  }
  const candidates=recipientCandidates(db,SENDER,M,10).rows;
  assert.deepEqual(candidates.map(x=>[x.sig,x.slot,x.block_time]),[
    ['slot-201',201,1000],
    ['slot-200',200,1001],
  ]);
});

test('unanchored incremental signature polling reports a capped window as a gap, not an reached cursor',async()=>{
 const calls=[];
 const fullPage=async options=>{
   calls.push(options);
   return Array.from({length:50},(_,i)=>({signature:'bounded-'+calls.length+'-'+i,blockTime:1000-i}));
 };
 const bounded=await wallets.pageSignatures(fullPage,{first:false,lastSig:null,pages:2});
 assert.equal(calls.length,2,'scanner must respect provider page budget');
 assert.equal(bounded.all.length,100);
 assert.equal(bounded.reached,false,'page cap without an anchor is not evidence of a continuous history');
 assert.equal(calls[1].before,'bounded-1-49');
 const exhausted=await wallets.pageSignatures(
   async()=>[{signature:'only-one',blockTime:1000}],
   {first:false,lastSig:null,pages:2});
 assert.equal(exhausted.reached,true,'a short page can end the bounded scan');
 assert.equal(exhausted.all.length,1);
 const anchored=await wallets.pageSignatures(
   async options=>{assert.equal(options.until,'previous-sig');return [{signature:'new',blockTime:1000}];},
   {first:false,lastSig:'previous-sig',pages:2});
 assert.equal(anchored.reached,true,'existing valid anchor behavior stays intact');
});

test('full read-only economic chain survives a post-capture failure and keeps candidate-only interpretations',async()=>{
 const original=globalThis.fetch;
 globalThis.fetch=async()=>{throw new Error('test has no network access');};
 try {
  for(const wallet of [A,B,C]) wallets.addWallet(wallet,'','you');
  const first=tx('buy-and-transfer',second,
   [A,B,'ATA_A','ATA_B','ATA_POOL',POOL,TOKEN],
   {pre:[5e9,1e9,0,0,0,1e9,0],post:[4e9-5000,1e9,0,0,0,2e9,0],
    preToken:[bal(2,A,M,0),bal(3,B,M,0),bal(4,POOL,M,1_000_000_000)],
    postToken:[bal(2,A,M,600_000_000),bal(3,B,M,400_000_000),bal(4,POOL,M,0)],
    ix:[tok('ATA_A','ATA_B',M,400_000_000)],
    inner:[{index:0,instructions:[tok('ATA_POOL','ATA_A',M,1_000_000_000)]}]
   });
  checkpointWalletPage(db,{wallet:A,rows:[{signature:'buy-and-transfer',blockTime:second}],first:true,reached:true});
  // Crash after wallet_trades and original RPC evidence were saved, before readSigs completion.
  await assert.rejects(
   wallets.readTx({address:A},{sig:'buy-and-transfer',t:second*1000,quiet:false},
     ()=>{throw new Error('fixture downstream interruption')},first),
   /fixture downstream interruption/);
  assert.ok(transactionEvidence(db,'buy-and-transfer')?.rpc);
  assert.equal(walletProcessing(db,'buy-and-transfer',A)?.state,'RETRY_REQUIRED');
  // Balance-net summary has 600 tokens. The original instruction records 400 transferred
  // to B and 1,000 transferred from pool to A. These are DIFFERENT facts.
  const summary=db.prepare('SELECT tokens FROM wallet_trades WHERE sig=? AND wallet=?').get('buy-and-transfer',A);
  assert.equal(summary.tokens,600);
  const edges=recipientCandidates(db,A,M).rows;
  assert.equal(edges.length,1);assert.equal(edges[0].to_owner,B);
  assert.equal(edges[0].amount_raw,'400000000');
  // The legacy WTrack net-balance transfer summarizer cannot represent this
  // combined swap + outward transfer. A null WTrack summary MUST NOT be
  // treated as negative evidence: the captured instruction proves A -> B.
  assert.equal(wtrack.parseTransfer(first,A),null);
  assert.equal(recipientOutcomes(db,A,M).rows[0].sellObservation,'NOT_OBSERVED_IN_CAPTURED_WINDOW');
  // Retry without passing fetched tx; it must replay from SQLite and finish without network.
  await wallets.readTx({address:A},{sig:'buy-and-transfer',t:second*1000,quiet:false},()=>{});
  assert.deepEqual(pendingWalletSignatures(db,A),[]);
  assert.equal(walletProcessing(db,'buy-and-transfer',A)?.state,'COMPLETE');

  // B sold M after its received holdings were transferred; it need not be in a current holder list.
  const sell=tx('B-sells-M',second+80,[B,POOL,'ATA_B','ATA_POOL',TOKEN],
   {pre:[1e9,1e9,0,0,0],post:[1.75e9-5000,0.25e9,0,0,0],
    preToken:[bal(2,B,M,400_000_000),bal(3,POOL,M,0)],
    postToken:[bal(2,B,M,0),bal(3,POOL,M,400_000_000)],
    ix:[tok('ATA_B','ATA_POOL',M,400_000_000)]});
  await wallets.readTx({address:B},{sig:'B-sells-M',t:(second+80)*1000,quiet:true},()=>{},sell);

  const transfer=tx('B-sends-C-sol',second+120,[B,C,SYS],
   {pre:[1.75e9,1e9,0],post:[1.25e9-5000,1.5e9,0],
    ix:[sol(B,C,500_000_000)]});
  await wallets.readTx({address:B},{sig:'B-sends-C-sol',t:(second+120)*1000,quiet:true},()=>{},transfer);

  const buyN=tx('C-buys-N',second+170,[C,POOL,'ATA_C','ATA_POOL_N',TOKEN],
   {pre:[1.5e9,1e9,0,0,0],post:[1.1e9-5000,1.4e9,0,0,0],
    preToken:[bal(2,C,N,0),bal(3,POOL,N,1_000_000_000)],
    postToken:[bal(2,C,N,200_000_000),bal(3,POOL,N,800_000_000)],
    ix:[tok('ATA_POOL_N','ATA_C',N,200_000_000)]});
  await wallets.readTx({address:C},{sig:'C-buys-N',t:(second+170)*1000,quiet:true},()=>{},buyN);
  const result=recipientOutcomes(db,A,M);
  assert.equal(result.rows.length,1);
  assert.equal(result.rows[0].sellObservation,'LOCAL_SELL_SUMMARY_OBSERVED');
  assert.equal(result.rows[0].observedSells[0].sig,'B-sells-M');
  assert.equal(result.rows[0].observedSells[0].sellDeltaRaw,'-400000000');
  assert.deepEqual(result.rows[0].inventoryProvenance,['AMOUNT_COMPATIBLE_BUT_PROVENANCE_UNPROVEN']);
  assert.equal(result.rows[0].crossMintCandidates[0].buy_sig,'C-buys-N');
  assert.match(result.interpretation,/NOT transferred-inventory provenance or common control/);

  // Counterexample: a later same-Mint sell can exceed the transferred amount.
  // It is still a real local sell observation, but cannot be fully attributed to A's single transfer.
  const largerSell=tx('B-sells-more-M',second+100,[B,POOL,'ATA_B','ATA_POOL',TOKEN],
   {pre:[1.75e9,1e9,0,0,0],post:[2.75e9-5000,0,0,0,0],
    preToken:[bal(2,B,M,800_000_000),bal(3,POOL,M,0)],
    postToken:[bal(2,B,M,0),bal(3,POOL,M,800_000_000)],
    ix:[tok('ATA_B','ATA_POOL',M,800_000_000)]});
  await wallets.readTx({address:B},{sig:'B-sells-more-M',t:(second+100)*1000,quiet:true},()=>{},largerSell);
  const withCounterexample=recipientOutcomes(db,A,M);
  const larger=withCounterexample.rows[0].observedSells.find(x=>x.sig==='B-sells-more-M');
  assert.equal(larger.sellDeltaRaw,'-800000000');
  assert.equal(larger.inventoryLink,'CANNOT_BE_FULLY_SOURCED_FROM_THIS_SINGLE_TRANSFER');
  assert.ok(withCounterexample.rows[0].inventoryProvenance.includes('CANNOT_BE_FULLY_SOURCED_FROM_THIS_SINGLE_TRANSFER'));

  // Counterexample: a Token-2022 transfer fee means the gross transfer amount
  // and spendable received amount differ. The follow-up sell is deliberately
  // larger than the net received amount but smaller than gross.
  const feeTransfer=tx('A-fee-transfer',second+90,[A,B,'ATA_A_FEE','ATA_B_FEE','ATA_POOL_FEE',TOKEN],{
    pre:[1e9,1e9,0,0,0,0],post:[0.6e9-5000,1.4e9,0,0,0,0],
    preToken:[bal(2,A,M,400_000_000),bal(3,B,M,0),bal(4,'FEE',M,0)],
    postToken:[bal(2,A,M,0),bal(3,B,M,395_000_000),bal(4,'FEE',M,0)],
    ix:[{programId:'TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb',program:'spl-token-2022',
      parsed:{type:'transferCheckedWithFee',info:{source:'ATA_A_FEE',destination:'ATA_B_FEE',mint:M,
        tokenAmount:{amount:'400000000',decimals:6},feeAmount:'5000000'}}}]
  });
  await wallets.readTx({address:A},{sig:'A-fee-transfer',t:(second+90)*1000,quiet:true},()=>{},feeTransfer);
  const feeSell=tx('B-sells-token2022-fee-case',second+105,[B,POOL,'ATA_B_FEE','ATA_POOL_FEE',TOKEN],{
    pre:[1e9,1e9,0,0,0],post:[1.395e9-5000,0.605e9,0,0,0],
    preToken:[bal(2,B,M,395_000_000),bal(3,POOL,M,0)],
    postToken:[bal(2,B,M,0),bal(3,POOL,M,395_000_000)],
    ix:[tok('ATA_B_FEE','ATA_POOL_FEE',M,395_000_000)]
  });
  await wallets.readTx({address:B},{sig:'B-sells-token2022-fee-case',t:(second+105)*1000,quiet:true},()=>{},feeSell);
  const feeCase=recipientOutcomes(db,A,M);
  const feeRow=feeCase.rows.find(x=>x.sig==='A-fee-transfer')?.observedSells.find(x=>x.sig==='B-sells-token2022-fee-case');
  assert.equal(feeRow.transferFeeRaw,'5000000');
  assert.equal(feeRow.transferNetAmountRaw,'395000000');
  assert.equal(feeRow.inventoryLink,'TOKEN_2022_TRANSFER_FEE_PRESENT_PROVENANCE_UNPROVEN');
  // Counterexample: a single swap-like transaction can receive and send the same Mint.
  // The owner's net delta can equal the original transfer even though the gross outbound
  // amount was larger; net balance alone cannot establish inventory provenance.
  const mixedFlow=tx('B-mixed-M-flow',second+110,[B,'OTHER',POOL,'ATA_B_IN','ATA_B_OUT','ATA_POOL',TOKEN],{
    pre:[1e9,1e9,1e9,0,500_000_000,0,0],
    post:[1.4e9-5000,0.6e9,1e9,100_000_000,0,0,0],
    preToken:[bal(3,B,M,0),bal(4,B,M,500_000_000),bal(5,POOL,M,0)],
    postToken:[bal(3,B,M,100_000_000),bal(4,B,M,0),bal(5,POOL,M,500_000_000)],
    ix:[
      tok('OTHER','ATA_B_IN',M,100_000_000),
      tok('ATA_B_OUT','ATA_POOL',M,500_000_000)
    ]
  });
  await wallets.readTx({address:B},{sig:'B-mixed-M-flow',t:(second+110)*1000,quiet:true},()=>{},mixedFlow);
  const mixed=recipientOutcomes(db,A,M);
  const mixedRow=mixed.rows[0].observedSells.find(x=>x.sig==='B-mixed-M-flow');
  assert.equal(mixedRow.sellDeltaRaw,'-400000000');
  assert.equal(mixedRow.inventoryLink,'INTRA_TRANSACTION_NET_DELTA_AMBIGUOUS');
  assert.ok(mixed.rows[0].inventoryProvenance.includes('INTRA_TRANSACTION_NET_DELTA_AMBIGUOUS'));

  // Counterexample: blockTime has only second precision. A same-second/same-slot sell
  // cannot be proven to occur after the transfer, so it must stay out of the follow-up set.
  const sameSlotSell=tx('B-sells-same-slot',second,[B,POOL,'ATA_B','ATA_POOL',TOKEN],
   {pre:[1e9,1e9,0,0,0],post:[1.75e9-5000,0.25e9,0,0,0],
    preToken:[bal(2,B,M,400_000_000),bal(3,POOL,M,0)],
    postToken:[bal(2,B,M,0),bal(3,POOL,M,400_000_000)],
    ix:[tok('ATA_B','ATA_POOL',M,400_000_000)]});
  await wallets.readTx({address:B},{sig:'B-sells-same-slot',t:second*1000,quiet:true},()=>{},sameSlotSell);
  const ordered=recipientOutcomes(db,A,M);
  assert.equal(ordered.rows[0].observedSells.some(x=>x.sig==='B-sells-same-slot'),false);

  // A complete getBlock response can provide deterministic ordering inside one slot.
  // Indexing is optional evidence: until both transactions are present in that block,
  // same-slot ordering remains UNKNOWN.
  const blockSlot=ordered.rows[0].slot;
  const order=recordBlockTransactionOrder(db,{
    slot:blockSlot,
    transactions:[
      {transaction:{signatures:['buy-and-transfer']}},
      {transaction:{signatures:['B-sells-same-slot']}},
    ],
  });
  assert.equal(order.matched,2);
  const orderedWithBlock=recipientOutcomes(db,A,M);
  assert.equal(orderedWithBlock.rows[0].observedSells.some(x=>x.sig==='B-sells-same-slot'),true);

  // Coverage counterexample: more than five valid follow-up sells must not silently
  // look like a complete five-row history.
  for (let i=0;i<4;i++) {
    const extra=tx('B-sells-extra-'+i,second+200+i,[B,POOL,'ATA_B','ATA_POOL',TOKEN],
      {pre:[2e9,1e9,0,0,0],post:[2.25e9-5000,0.75e9,0,0,0],
       preToken:[bal(2,B,M,100_000_000),bal(3,POOL,M,0)],
       postToken:[bal(2,B,M,0),bal(3,POOL,M,100_000_000)],
       ix:[tok('ATA_B','ATA_POOL',M,100_000_000)]});
    await wallets.readTx({address:B},{sig:'B-sells-extra-'+i,t:(second+200+i)*1000,quiet:true},()=>{},extra);
  }
  const capped=recipientOutcomes(db,A,M);
  assert.equal(capped.rows[0].observedSells.length,5);
  assert.equal(capped.rows[0].observedSellsTruncated,true);

  assert.equal(db.prepare('SELECT COUNT(*) n FROM econ_transactions').get().n,10);
 } finally {globalThis.fetch=original;}
});