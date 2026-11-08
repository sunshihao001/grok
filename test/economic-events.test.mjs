import test from 'node:test';
import assert from 'node:assert/strict';
import { DatabaseSync } from 'node:sqlite';
import { decodeEvidence, persistEvidence, recipientCandidates, crossMintCandidates, transactionEvidence, missingEvidence, recipientOutcomes } from '../server/economic-events.mjs';
const A='A_OWNER', B='B_OWNER', C='C_OWNER', POOL='POOL_OWNER', M='MINT_M', N='MINT_N';
const TOKEN='TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA', SYSTEM='11111111111111111111111111111111';
const bal=(accountIndex, owner, mint, amount)=>({accountIndex, owner, mint, uiTokenAmount:{amount:String(amount),decimals:6}});
function tx({at=1000, instructions=[], innerInstructions=[], preTokenBalances=[],postTokenBalances=[], accounts=[A,B,'ATA_A','ATA_B','ATA_POOL',TOKEN,SYSTEM], err=null, slot=20}={}) {
 return {slot,blockTime:at,meta:{err,fee:5000,preTokenBalances,postTokenBalances,innerInstructions,preBalances:accounts.map(()=>1e9),postBalances:accounts.map(()=>1e9),logMessages:['test log']},transaction:{signatures:['signature_from_rpc'],message:{accountKeys:accounts.map(pubkey=>({pubkey})),instructions}}};
}
const transfer=(source,destination,amount,mint=M)=>({programId:TOKEN,program:'spl-token',parsed:{type:'transferChecked',info:{source,destination,mint,tokenAmount:{amount:String(amount),decimals:6}}}});
const solTransfer=(source,destination,lamports)=>({programId:SYSTEM,program:'system',parsed:{type:'transfer',info:{source,destination,lamports}}});
const setup=()=>{const d=new DatabaseSync(':memory:');d.exec('CREATE TABLE wallet_trades(sig TEXT,wallet TEXT,mint TEXT,side TEXT,t INTEGER,sol REAL)');return d;};
// Keep the RPC's first signature consistent with the caller; the mismatch test bypasses this helper.
const store = (db, sig, tx, provenance = {}) => { tx.transaction.signatures[0] = sig; return persistEvidence(db, sig, tx, Date.now(), provenance); };
function mixed(){return tx({at:1000,instructions:[{programId:'ROUTER',data:'opaque'},transfer('ATA_A','ATA_B',400_000_000)],innerInstructions:[{index:0,instructions:[transfer('ATA_POOL','ATA_A',1_000_000_000)]}],preTokenBalances:[bal(2,A,M,0),bal(3,B,M,0),bal(4,POOL,M,1_000_000_000)],postTokenBalances:[bal(2,A,M,600_000_000),bal(3,B,M,400_000_000),bal(4,POOL,M,0)]});}

test('preserves every original RPC field and both outer and CPI transfer positions',()=>{
 const d=setup();const t=mixed();const out=store(d,'s-buy-transfer',t);assert.equal(out.instructions,3);const got=transactionEvidence(d,'s-buy-transfer');assert.deepEqual(got.rpc,t);assert.equal(got.instructions.length,3);assert.deepEqual(got.instructions.map(e=>[e.outer_i,e.inner_i]),[[0,-1],[0,0],[1,-1]]);assert.equal(got.instructions[2].from_owner,A);assert.equal(got.instructions[2].to_owner,B);assert.equal(got.instructions[1].from_owner,POOL);d.close();
});
test('idempotent replay preserves a single set of events',()=>{const d=setup(),t=mixed();store(d,'s1',t);assert.equal(store(d,'s1',t).duplicate,true);assert.equal(d.prepare('SELECT COUNT(*) n FROM econ_instructions').get().n,3);d.close();});
test('transaction change refreshes evidence atomically without duplicate instruction rows',()=>{const d=setup(),t=mixed();store(d,'s1',t);const more=structuredClone(t);more.transaction.message.instructions.push(transfer('ATA_A','ATA_B',1));assert.equal(store(d,'s1',more).duplicate,false);assert.equal(d.prepare('SELECT COUNT(*) n FROM econ_instructions').get().n,4);d.close();});
test('recipient discovery reports A->B on same transaction with a swap, not the pool CPI',()=>{const d=setup();store(d,'s1',mixed());const r=recipientCandidates(d,A,M);assert.equal(r.rows.length,1);assert.equal(r.rows[0].to_owner,B);assert.equal(r.rows[0].amount_raw,'400000000');assert.match(r.interpretation,/CANDIDATE|not controlled/);d.close();});
test('two distinct recipients in one signature remain distinct, no balance-delta misattribution',()=>{const d=setup();const t=tx({instructions:[transfer('ATA_A','ATA_B',250),transfer('ATA_A','ATA_C',150)],accounts:[A,B,'ATA_A','ATA_B','ATA_C',TOKEN],preTokenBalances:[bal(2,A,M,400),bal(3,B,M,0),bal(4,C,M,0)],postTokenBalances:[bal(2,A,M,0),bal(3,B,M,250),bal(4,C,M,150)]});store(d,'two-receivers',t);const rows=recipientCandidates(d,A,M).rows;assert.deepEqual(rows.map(x=>[x.to_owner,x.amount_raw]),[[B,'250'],[C,'150']]);d.close();});
test('unknown token account owner remains null and is not invented as a candidate',()=>{const d=setup();const t=tx({instructions:[transfer('ATA_A','ATA_B',10)],preTokenBalances:[bal(2,A,M,10)],postTokenBalances:[bal(2,A,M,0)]});store(d,'missing-owner',t);assert.equal(recipientCandidates(d,A).rows.length,0);assert.equal(transactionEvidence(d,'missing-owner').instructions[0].to_owner,null);d.close();});
test('conflicting owner mappings fail closed instead of guessing',()=>{const d=setup();const t=tx({instructions:[transfer('ATA_A','ATA_B',10)],preTokenBalances:[bal(2,A,M,10),bal(3,B,M,0)],postTokenBalances:[bal(2,A,M,0),bal(3,C,M,10)]});store(d,'conflict',t);assert.equal(recipientCandidates(d,A).rows.length,0);d.close();});
test('failed chain transaction preserves evidence but produces no recipient candidate',()=>{const d=setup();const t=mixed();t.meta.err={InstructionError:[0,'Custom']};store(d,'failed',t);assert.equal(recipientCandidates(d,A).rows.length,0);assert.equal(transactionEvidence(d,'failed').status,'FAILED');d.close();});
test('cross Mint chain B sell M -> B sends SOL to C -> C buys N is candidate only',()=>{const d=setup();store(d,'B_to_C',tx({at:1200,instructions:[solTransfer(B,C,1_000_000_000)],accounts:[B,C,SYSTEM]}));d.prepare('INSERT INTO wallet_trades VALUES(?,?,?,?,?,?)').run('B_sells',B,M,'sell',1100_000,1.1);d.prepare('INSERT INTO wallet_trades VALUES(?,?,?,?,?,?)').run('C_buys',C,N,'buy',1300_000,1);const r=crossMintCandidates(d,B);assert.equal(r.rows.length,1);assert.equal(r.rows[0].funding_sig,'B_to_C');assert.equal(r.rows[0].bought_mint,N);assert.match(r.interpretation,/NOT_LAMPORT_PROVENANCE/);d.close();});
test('no cross Mint claim without explicit captured SOL transfer',()=>{const d=setup();store(d,'B_to_C_token',tx({at:1200,instructions:[transfer('ATA_A','ATA_B',1)]}));d.prepare('INSERT INTO wallet_trades VALUES(?,?,?,?,?,?)').run('B_sells',B,M,'sell',1100_000,1.1);d.prepare('INSERT INTO wallet_trades VALUES(?,?,?,?,?,?)').run('C_buys',C,N,'buy',1300_000,1);assert.equal(crossMintCandidates(d,B).rows.length,0);d.close();});
test('same Mint follow-up is not misclassified as cross Mint',()=>{const d=setup();store(d,'B_to_C',tx({at:1200,instructions:[solTransfer(B,C,1_000_000_000)],accounts:[B,C,SYSTEM]}));d.prepare('INSERT INTO wallet_trades VALUES(?,?,?,?,?,?)').run('B_sells',B,M,'sell',1100_000,1);d.prepare('INSERT INTO wallet_trades VALUES(?,?,?,?,?,?)').run('C_buys',C,M,'buy',1300_000,1);assert.equal(crossMintCandidates(d,B).rows.length,0);d.close();});
test('multi-swap and opaque program bytes never silently inferred as a verified purchase',()=>{const d=setup();const t=tx({instructions:[{programId:'ROUTER',data:'base64-or-opaque'}, {programId:'COMPUTE',data:'opaque'}]});store(d,'opaque',t);assert.deepEqual(transactionEvidence(d,'opaque').instructions.map(i=>i.kind),['OTHER','OTHER']);assert.equal(recipientCandidates(d,A).rows.length,0);d.close();});

test('missing evidence identifies legacy trade signatures and clears on archived replay',()=>{
 const d=setup();d.prepare('INSERT INTO wallet_trades VALUES(?,?,?,?,?,?)').run('legacy_sig',A,M,'buy',1000_000,2);
 assert.deepEqual(missingEvidence(d,A).rows.map(x=>x.sig),['legacy_sig']);
 store(d,'legacy_sig',mixed());assert.equal(missingEvidence(d,A).rows.length,0);d.close();
});

test('rejects RPC signature mismatch without creating a misleading record', () => {
 const d=setup();
 assert.throws(()=>persistEvidence(d,'wrong-signature',mixed()),/RPC signature mismatch/);
 assert.equal(d.prepare("SELECT COUNT(*) n FROM sqlite_master WHERE name='econ_transactions'").get().n,0);
 d.close();
});
test('Token-2022 transfer is identified by official program ID, without parsed program label',()=>{
 const d=setup(), t=mixed(), ix=t.transaction.message.instructions[1];
 ix.programId='TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb';delete ix.program;
 store(d,'token2022',t);
 assert.equal(recipientCandidates(d,A,M).rows[0]?.to_owner,B);d.close();
});
test('a missing owner on one balance is not a conflicting owner',()=>{
 const d=setup(), t=tx({instructions:[transfer('ATA_A','ATA_B',10)],
 preTokenBalances:[bal(2,A,M,10),{accountIndex:3,mint:M,uiTokenAmount:{amount:'0',decimals:6}}],
 postTokenBalances:[bal(2,A,M,0),bal(3,B,M,10)]});
 store(d,'partial-owner',t);
 assert.equal(recipientCandidates(d,A,M).rows[0]?.to_owner,B);
 assert.equal(transactionEvidence(d,'partial-owner').instructions[0].owner_conflict,0);d.close();
});
test('contradictory owners persist a conflict marker and never become recipients',()=>{
 const d=setup(),t=tx({instructions:[transfer('ATA_A','ATA_B',10)],
 preTokenBalances:[bal(2,A,M,10),bal(3,B,M,0)],
 postTokenBalances:[bal(2,A,M,0),bal(3,C,M,10)]});
 store(d,'conflict-persist',t);
 const r=transactionEvidence(d,'conflict-persist').instructions[0];
 assert.equal(r.owner_conflict,1);assert.equal(r.to_owner,null);
 assert.equal(recipientCandidates(d,A,M).rows.length,0);d.close();
});
test('recipient followup finds already observed sell and later cross Mint candidate only',()=>{
 const d=setup();store(d,'A-to-B',mixed());
 store(d,'B-to-C',tx({at:1200,instructions:[solTransfer(B,C,900_000_000)],accounts:[B,C,SYSTEM]}));
 d.prepare('INSERT INTO wallet_trades VALUES(?,?,?,?,?,?)').run('B-sell',B,M,'sell',1100_000,1);
 d.prepare('INSERT INTO wallet_trades VALUES(?,?,?,?,?,?)').run('C-buy',C,N,'buy',1300_000,1);
 const r=recipientOutcomes(d,A,M,20,24);
 assert.equal(r.rows.length,1);assert.equal(r.rows[0].to_owner,B);
 assert.equal(r.rows[0].observedSells[0].sig,'B-sell');
 assert.equal(r.rows[0].crossMintCandidates[0].bought_mint,N);
 assert.match(r.interpretation,/NOT transferred-inventory provenance/);d.close();
});
test('evidence GET paths never create missing tables',()=>{
 const d=setup();assert.equal(transactionEvidence(d,'none'),null);
 assert.equal(recipientCandidates(d,A,M).coverage,'EVIDENCE_NOT_INITIALIZED');
 assert.equal(recipientOutcomes(d,A,M).rows.length,0);
 assert.equal(d.prepare("SELECT COUNT(*) n FROM sqlite_master WHERE name LIKE 'econ_%'").get().n,0);
 d.close();
});
test('source provenance is retained with original RPC',()=>{
 const d=setup();store(d,'provenance',mixed(),{captureSource:'WALLET_RPC',commitment:'confirmed'});
 const r=transactionEvidence(d,'provenance');
 assert.equal(r.capture_source,'WALLET_RPC');assert.equal(r.commitment,'confirmed');d.close();
});
test('a conflicting token mint invalidates the inferred owner edge',()=>{
 const d=setup(),t=mixed();t.transaction.message.instructions[1].parsed.info.mint=N;
 store(d,'conflicting-mint',t);
 const r=transactionEvidence(d,'conflicting-mint').instructions[2];
 assert.equal(r.owner_conflict,1);assert.equal(r.mint,null);
 assert.equal(recipientCandidates(d,A,M).rows.length,0);d.close();
});
