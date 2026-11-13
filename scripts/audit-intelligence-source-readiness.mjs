#!/usr/bin/env node
// Existing-SQLite-only provenance readiness for ONE Mint. No Blix imports, network,
// model, schema changes, storage side effects or wallet-control assertions.
import { existsSync, statSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { DatabaseSync } from 'node:sqlite';
const MINT = /^[1-9A-HJ-NP-Za-km-z]{32,44}$/;
const TABLES = ['tokens','snapshots','signals','early','feed_events',
  'econ_transactions','econ_instructions','wallet_sig_windows'];
const args=process.argv.slice(2),opts={};
let invalid=args.length!==4;
for(let i=0;i<args.length;i+=2){
  if(!['--db','--mint'].includes(args[i])||opts[args[i]]!==undefined)invalid=true;
  opts[args[i]]=args[i+1];
}
function fail(message){ console.error(message); process.exitCode=2; }
if(invalid||typeof opts['--db']!=='string'||!MINT.test(opts['--mint']||'')){
  fail('Usage: --db EXISTING.sqlite --mint BASE58_MINT');
}else if(!existsSync(opts['--db'])||!statSync(opts['--db']).isFile()){
  fail('EXISTING_SQLITE_FILE_REQUIRED: no creation or migration');
}else{
  let db;
  try {
    db=new DatabaseSync(opts['--db'],{readOnly:true});
    db.exec('PRAGMA query_only=ON');
    const mint=opts['--mint'],available={},columns={};
    const tab=db.prepare("SELECT 1 FROM sqlite_master WHERE type='table' AND name=?");
    for(const t of TABLES){
      available[t]=Boolean(tab.get(t));
      columns[t]=new Set(available[t]?
        db.prepare('PRAGMA table_info('+t+')').all().map(x=>x.name):[]);
    }
    const has=(table,...names)=>available[table]&&names.every(n=>columns[table].has(n));
    const get=(sql,...params)=>db.prepare(sql).get(...params);
    const marketToken=has('tokens','mint','source','first_seen','updated')
      ? get('SELECT source,first_seen,updated FROM tokens WHERE mint=?',mint):null;
    const marketSnapshots=has('snapshots','mint','t')
      ? get('SELECT COUNT(*) n,MIN(t) firstT,MAX(t) lastT FROM snapshots WHERE mint=?',mint):null;
    const marketSignals=has('signals','mint','t')
      ? get('SELECT COUNT(*) n,MIN(t) firstT,MAX(t) lastT FROM signals WHERE mint=?',mint):null;
    const early=has('early','mint','cp')
      ? get('SELECT COUNT(*) n,COUNT(DISTINCT cp) checkpoints FROM early WHERE mint=?',mint):null;
    const feed=has('feed_events','mint','received')
      ? get('SELECT COUNT(*) n,MIN(received) firstReceived,MAX(received) lastReceived FROM feed_events WHERE mint=?',mint):null;
    const economicSchema=has('econ_transactions','sig','rpc_json','sha256','status','observed_at','slot')&&
      has('econ_instructions','sig','mint','kind','from_owner','to_owner','owner_conflict');
    let economic=null,integrity=null,windows=null;
    if(economicSchema){
      economic=get('SELECT COUNT(DISTINCT i.sig) capturedSignatures,COUNT(*) indexedInstructionRows,'
        +'MIN(t.slot) firstSlot,MAX(t.slot) lastSlot,'
        +'MIN(t.observed_at) firstCapturedAtMs,MAX(t.observed_at) lastCapturedAtMs,'
        +'SUM(CASE WHEN i.owner_conflict<>0 THEN 1 ELSE 0 END) ownerConflictRows,'
        +'SUM(CASE WHEN i.kind=? THEN 1 ELSE 0 END) tokenTransferRows,'
        +'SUM(CASE WHEN t.status<>? THEN 1 ELSE 0 END) unsuccessfulIndexedRows '
        +'FROM econ_instructions i JOIN econ_transactions t ON t.sig=i.sig WHERE i.mint=?',
        'TOKEN_TRANSFER','RPC_OBSERVED',mint);
      const sample=db.prepare('SELECT DISTINCT t.sig,t.rpc_json,t.sha256 '
        +'FROM econ_transactions t JOIN econ_instructions i ON i.sig=t.sig '
        +'WHERE i.mint=? ORDER BY t.sig LIMIT 13').all(mint);
      let hashMismatch=0,malformed=0;
      for(const row of sample.slice(0,12)){
        if(createHash('sha256').update(row.rpc_json).digest('hex')!==row.sha256)hashMismatch++;
        try{
          const tx=JSON.parse(row.rpc_json);
          if(!tx?.transaction||!tx?.meta)malformed++;
        }catch{malformed++;}
      }
      integrity={
        method:'VERIFY_STORED_RAW_JSON_SHA256_AND_BASIC_RPC_SHAPE',
        inspectedCaptures:Math.min(sample.length,12),
        sampleCapReached:sample.length>12,
        hashMismatch,malformed,
        fullEconomicInstructionVerification:false,
        allCapturedTransactionsChecked:false,
        status:hashMismatch||malformed?'CORRUPT_SAMPLED_SOURCE'
          : sample.length>12?'ONLY_FIRST_12_CHECKED':'AVAILABLE_SAMPLED_NOT_COMPLETE',
      };
      if(has('wallet_sig_windows','wallet','anchor_reached','gaps_seen','checked_at_ms')){
        const owners=db.prepare('SELECT DISTINCT wallet FROM ('
          +'SELECT from_owner wallet FROM econ_instructions WHERE mint=? AND from_owner IS NOT NULL '
          +'UNION SELECT to_owner wallet FROM econ_instructions WHERE mint=? AND to_owner IS NOT NULL'
          +') ORDER BY wallet LIMIT 8').all(mint,mint);
        const lookup=db.prepare('SELECT anchor_reached,gaps_seen FROM wallet_sig_windows WHERE wallet=?');
        let known=0,anchorNotReached=0,withGaps=0;
        for(const row of owners){
          const w=lookup.get(row.wallet);
          if(w){known++;if(!w.anchor_reached)anchorNotReached++;if(w.gaps_seen)withGaps++;}
        }
        windows={sampledOwnerCount:owners.length,ownersWithSignatureWindow:known,
          anchorNotReached,withGaps,sampleMayBeTruncated:owners.length===8,
          lifetimeHistoryComplete:false};
      }
    }
    const marketPresent=Boolean(marketToken||marketSnapshots?.n||marketSignals?.n||early?.n||feed?.n);
    const chainPresent=Boolean(economic?.capturedSignatures);
    const missing=[];
    if(!marketToken)missing.push('NO_LOCAL_TOKEN_METADATA_ROW');
    if(!marketPresent)missing.push('NO_LOCAL_MARKET_RECORDS');
    if(!economicSchema)missing.push('ECONOMIC_EVIDENCE_SCHEMA_UNAVAILABLE');
    else if(!chainPresent)missing.push('NO_LOCALLY_CAPTURED_RPC_INSTRUCTIONS_FOR_MINT');
    if(integrity?.status==='CORRUPT_SAMPLED_SOURCE')missing.push('CORRUPT_ARCHIVED_RPC_IN_SAMPLED_DATA');
    missing.push('MARKET_UNIVERSE_AND_SOURCE_DELIVERY_COVERAGE_UNKNOWN',
      'REAL_SOURCE_FIRST_AVAILABLE_TIME_UNKNOWN',
      'FULL_MINT_AND_WALLET_SIGNATURE_HISTORY_UNKNOWN',
      'COMPLETE_SWAP_LP_CPI_ASSET_AND_INVENTORY_RECONCILIATION_UNKNOWN',
      'HISTORICAL_EXECUTABLE_ENTRY_EXIT_QUOTES_UNKNOWN',
      'CONTINUOUS_AI_RESEARCH_MONITORING_NOT_RUNNING');
    console.log(JSON.stringify({
      schemaVersion:'0.1',
      kind:'EXISTING_SQLITE_SOURCE_READINESS_NOT_FULL_MARKET_VERIFICATION',
      mint,scope:'EXISTING_LOCAL_BLIX_SQLITE_READ_ONLY',
      tables:available,
      market:{
        token:marketToken?{source:marketToken.source,firstSeenMs:marketToken.first_seen,
          updatedMs:marketToken.updated,
          firstSeenMeaning:'BLIX_LOCAL_FIRST_SEEN_NOT_PROVIDER_FIRST_AVAILABLE'}:null,
        snapshots:marketSnapshots,signals:marketSignals,
        earlyCheckpoints:early,feedEvents:feed,
        timestampsProveFirstAvailable:false,
      },
      chain:{
        coverage:'MINT_MATCHES_ONLY_IN_ALREADY_CAPTURED_RPC_INSTRUCTIONS',
        observed:economic,integrity,walletSignatureWindows:windows,
        completeMintOrWalletHistory:false,
        commonEconomicControllerVerified:false,
      },
      readiness:{
        marketDiscovery:marketPresent?'LOCAL_MARKET_ROWS_ONLY_UNIVERSE_UNKNOWN':'NOT_SEEN_IN_LOCAL_FILE',
        originalTransactions:chainPresent&&integrity?.status!=='CORRUPT_SAMPLED_SOURCE'
          ?'PARTIAL_CAPTURED_RPC_ONLY':'NO_TRUSTWORTHY_CAPTURE_SAMPLE',
        walletIdentification:chainPresent?'PARTIAL_OWNER_CANDIDATES_UNCLASSIFIED':'UNKNOWN',
        inventory:'NOT_RECONCILED_ASSET_BY_ASSET',
        crossMint:'NOT_PROVEN_BY_SINGLE_MINT_PROVENANCE_CHECK',
        tradableOpportunity:'NOT_VERIFIED_NO_TIME_VALID_EXECUTABLE_QUOTES',
        monitoring:'NOT_RUNNING',
      },
      missing,
      caveats:[
        'A stored market event does not prove full launch or market coverage.',
        'No local record means UNKNOWN outside this file, not no on-chain activity.',
        'Capture time and browser display time do not prove the first tradable signal time.',
        'An indexed transfer does not prove complete wallet assets or funder control.',
        'Sample hash matches do not prove correctness of all parsed economic actions.',
      ],
      next:'Compare one Mint and bounded slot/time window against original source delivery logs, retained RPC signatures, and independent replay.',
    }));
  }catch(error){
    // Never leak database paths or private file contents into model/UI errors.
    fail('READONLY_DATA_READINESS_FAILED');
  }finally{try{db?.close();}catch{}}
}
