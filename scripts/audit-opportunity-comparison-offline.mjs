#!/usr/bin/env node
// Replays one existing JSON file of frozen Blix Pulse inputs and two saved
// investigation receipts. No model/provider/RPC/network/database access or writes.
import { readFile, stat } from 'node:fs/promises';
import { compareObservedInvestigations } from '../server/intelligence/opportunity-read-comparison.mjs';

const args=process.argv.slice(2);
if(args.length!==2 || args[0]!=='--input' || !args[1]) {
  console.error('Usage: node scripts/audit-opportunity-comparison-offline.mjs --input EXISTING_FROZEN_A_B.json');
  process.exitCode=2;
}else{
  try {
    const info=await stat(args[1]);
    if(!info.isFile()||info.size>1024*1024)throw Error('EXISTING_BOUNDED_JSON_FILE_REQUIRED');
    const payload=JSON.parse(await readFile(args[1],'utf8'));
    const result=compareObservedInvestigations(payload);
    console.log(JSON.stringify(result,null,2));
  }catch(error){
    console.error('Read-only opportunity A/B audit failed:',String(error?.message||error));
    process.exitCode=1;
  }
}
