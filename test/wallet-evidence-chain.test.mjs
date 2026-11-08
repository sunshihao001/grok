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
const { recipientOutcomes, recipientCandidates, transactionEvidence } = await import('../server/economic-events.mjs');
const { checkpointWalletPage, pendingWalletSignatures, walletSignatureCoverage } =
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
  assert.equal(pendingWalletSignatures(db,A)[0].state,'RPC_CAPTURED');
  // Balance-net summary has 600 tokens. The original instruction records 400 transferred
  // to B and 1,000 transferred from pool to A. These are DIFFERENT facts.
  const summary=db.prepare('SELECT tokens FROM wallet_trades WHERE sig=? AND wallet=?').get('buy-and-transfer',A);
  assert.equal(summary.tokens,600);
  const edges=recipientCandidates(db,A,M).rows;
  assert.equal(edges.length,1);assert.equal(edges[0].to_owner,B);
  assert.equal(edges[0].amount_raw,'400000000');
  assert.equal(recipientOutcomes(db,A,M).rows[0].sellObservation,'NOT_OBSERVED_IN_CAPTURED_WINDOW');
  // Retry without passing fetched tx; it must replay from SQLite and finish without network.
  await wallets.readTx({address:A},{sig:'buy-and-transfer',t:second*1000,quiet:false},()=>{});
  assert.deepEqual(pendingWalletSignatures(db,A),[]);
  assert.equal(walletSignatureCoverage(db,A).states.find(x=>x.state==='READER_FINISHED').count,1);

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
  assert.equal(result.rows[0].crossMintCandidates[0].buy_sig,'C-buys-N');
  assert.match(result.interpretation,/NOT transferred-inventory provenance or common control/);
  assert.equal(db.prepare('SELECT COUNT(*) n FROM econ_transactions').get().n,4);
 } finally {globalThis.fetch=original;}
});
