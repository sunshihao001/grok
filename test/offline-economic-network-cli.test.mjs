import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { createHash } from 'node:crypto';
import { execFileSync,spawnSync } from 'node:child_process';
import { DatabaseSync } from 'node:sqlite';
import { persistEvidence } from '../server/economic-events.mjs';
const script=new URL('../scripts/inspect-economic-network.mjs',import.meta.url).pathname;
const M='GTNHLKQWKZHaHpd6PjfMgfFZUDEuCviwXMwYbCcepump';
const N='EYqygbhZjP7EbM4fSn8devctnksAvPAD1Bt57XBFpump';
const A='4p7SeR6361WJ4T4icgsYTnzAUzfA5NwM4CwYD9kMBjuK';
const B='BTmCme13XXrD3VLxXFChL9VnmicJ5PjkVUpAsjrooEYh';
const C='9g6A3KLaijJCfj92JbTh27Kn8ovTL6B41GCKb4yUM4Tr';
const TOKEN='TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA';
const hash=f=>createHash('sha256').update(fs.readFileSync(f)).digest('hex');

function insert(db,sig,mint,from,to,index) {
  const bal=(accountIndex,owner,amount)=>({accountIndex,owner,mint,
    uiTokenAmount:{amount:String(amount),decimals:6}});
  persistEvidence(db,sig,{
    slot:100+index,blockTime:1700000000+index,
    transaction:{signatures:[sig],message:{accountKeys:[from,to,'ATA_FROM','ATA_TO',TOKEN],
      instructions:[{programId:TOKEN,parsed:{type:'transferChecked',info:{
        source:'ATA_FROM',destination:'ATA_TO',mint,tokenAmount:{amount:'1000',decimals:6},
      }}}],
    }},
    meta:{err:null,fee:5000,preBalances:[0,0,0,0,0],postBalances:[0,0,0,0,0],
      preTokenBalances:[bal(2,from,1000),bal(3,to,0)],
      postTokenBalances:[bal(2,from,0),bal(3,to,1000)],innerInstructions:[]},
  });
}
function archive(file,extra=false){
  const db=new DatabaseSync(file);
  db.exec('CREATE TABLE wallet_trades(sig TEXT,wallet TEXT,mint TEXT,side TEXT,sol REAL,t INTEGER)');
  insert(db,'mint-M-A-to-B',M,A,B,1);
  if(extra){
    insert(db,'mint-M-B-to-C',M,B,C,2);
    insert(db,'mint-N-B-to-A',N,B,A,3);
  }
  db.close();
}
test('read-only CLI gives graph, cross-Mint candidates, historical delta and selected knowledge with unchanged DB bytes',()=>{
  const dir=fs.mkdtempSync(path.join(os.tmpdir(),'blix-offline-network-'));
  const old=path.join(dir,'previous.sqlite'),current=path.join(dir,'current.sqlite');
  try {
    archive(old);archive(current,true);
    const beforeOld=hash(old),beforeCurrent=hash(current);
    const data=JSON.parse(execFileSync(process.execPath,[
      script,'--db',current,'--mint',M,'--previous-db',old,
      '--other-mint',N,'--goal','调查资金来源钱包转仓与跨Mint群体',
    ],{encoding:'utf8',timeout:30000,maxBuffer:3*1024*1024}));
    assert.equal(data.mode,'OFFLINE_READ_ONLY_PROFESSIONAL_NETWORK');
    assert.equal(data.economicEvidence.facts.network.eventCount,2);
    assert.equal(data.economicEvidence.facts.network.knownRawTransferred,'2000');
    assert.equal(data.economicEvidence.facts.network.edges.length,2);
    assert.equal(data.previousArchiveComparison.newlyVisible.length,1);
    assert.equal(data.previousArchiveComparison.newlyVisible[0].signature,'mint-M-B-to-C');
    assert.equal(data.previousArchiveComparison.liveChainEventChange,'UNKNOWN');
    assert.ok(data.crossMintOverlap.overlappingWallets.some(x=>x.wallet===B));
    assert.equal(data.crossMintOverlap.commonControl,'UNKNOWN');
    assert.ok(data.knowledgeSuggestions.length>0);
    assert.ok(data.knowledgeSuggestions.every(x=>x.status==='RESEARCH_NOT_RUNTIME_VALIDATED'));
    assert.equal(hash(current),beforeCurrent,'main archive must be byte-identical');
    assert.equal(hash(old),beforeOld,'previous archive must be byte-identical');
  }finally{fs.rmSync(dir,{recursive:true,force:true});}
});
test('CLI will not create a missing database or access unapproved arguments',()=>{
  const dir=fs.mkdtempSync(path.join(os.tmpdir(),'blix-network-safety-'));
  const missing=path.join(dir,'not-existent.sqlite');
  try{
    const cmd=[script,'--db',missing,'--mint',M];
    const x=spawnSync(process.execPath,cmd,{encoding:'utf8',timeout:15000});
    assert.equal(x.status,1);
    assert.equal(fs.existsSync(missing),false);
    const injected=spawnSync(process.execPath,[...cmd,'--url','https://evil.test'],{encoding:'utf8',timeout:15000});
    assert.equal(injected.status,2);
    assert.equal(fs.existsSync(missing),false);
  }finally{fs.rmSync(dir,{recursive:true,force:true});}
});
