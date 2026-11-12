#!/usr/bin/env node
// Existing PR23 SQLite -> bounded professional network, knowledge and history
// comparison report. Never starts Blix server, network/RPC, wallets, trading,
// notification, model provider or any automatic background monitor.
import { makeOfflineEconomicReader } from '../server/intelligence/offline-economic-reader.mjs';
import { runCapability } from '../server/intelligence/index.mjs';
import { makeLocalKnowledgeLoader } from '../server/intelligence/local-knowledge-loader.mjs';
import { compareCapturedMintSnapshots, compareCapturedCrossMintWallets } from
  '../server/intelligence/economic-snapshot-review.mjs';

const args=process.argv.slice(2), allowed=new Set(['--db','--mint','--previous-db','--other-mint','--goal']);
const opts={};
let invalid=args.length%2!==0;
for(let i=0;i<args.length;i+=2){
  if(!allowed.has(args[i]) || opts[args[i]]!==undefined)invalid=true;
  opts[args[i]]=args[i+1];
}
const validMint=x=>typeof x==='string' && /^[1-9A-HJ-NP-Za-km-z]{32,44}$/.test(x);
if(invalid || !opts['--db'] || !validMint(opts['--mint']) ||
  opts['--other-mint']!==undefined && (!validMint(opts['--other-mint']) || opts['--other-mint']===opts['--mint']) ||
  opts['--goal']!==undefined && opts['--goal'].length>4096){
  console.error('Usage: node scripts/inspect-economic-network.mjs --db EXISTING.sqlite --mint MINT_BASE58 [--previous-db OTHER_EXISTING.sqlite] [--other-mint MINT_BASE58] [--goal "research question"]');
  process.exitCode=2;
}else{
  try{
    const mint=opts['--mint'];
    const inspect=async (db,m)=>runCapability('mint-economic-evidence',{
      mint:m,readEconomic:makeOfflineEconomicReader({databasePath:db}),
    });
    const current=await inspect(opts['--db'],mint);
    const previous=opts['--previous-db'] ? await inspect(opts['--previous-db'],mint) : null;
    const second=opts['--other-mint'] ? await inspect(opts['--db'],opts['--other-mint']) : null;
    const question=opts['--goal']||'';
    const knowledge=question
      ? await makeLocalKnowledgeLoader()({goal:question,evidence:[{capability:'mint-economic-evidence',result:current}]})
      : [];
    console.log(JSON.stringify({
      schemaVersion:'0.1',mode:'OFFLINE_READ_ONLY_PROFESSIONAL_NETWORK',
      input:{mint,otherMint:opts['--other-mint']??null,hasPreviousArchive:Boolean(previous)},
      economicEvidence:current,
      previousArchiveComparison:previous?compareCapturedMintSnapshots(previous,current):null,
      crossMintOverlap:second?compareCapturedCrossMintWallets(current,second):null,
      knowledgeSuggestions:knowledge,
      limitations:[
        'Only already archived local RPC evidence and pre-existing knowledge are used.',
        'Newly visible archive records are NOT necessarily new chain events.',
        'Transfer, shared wallet and prior sell summary are not proven common control, inventory provenance, PnL or copytrade advantage.',
        'No real model, monitoring scheduler, notification, trading or provider calls are performed.',
      ],
    },null,2));
  }catch(error){
    console.error('Offline professional network inspection failed:',String(error?.message||error));
    process.exitCode=1;
  }
}
