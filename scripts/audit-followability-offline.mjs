#!/usr/bin/env node
// Only reads an existing JSON fixture of explicit paper execution receipts.
// Never imports trading modules, connects to a provider or creates a position.
import { readFile,stat } from 'node:fs/promises';
import { evaluatePaperFollowabilityCases } from '../server/intelligence/followability-replay.mjs';
const args=process.argv.slice(2);
if(args.length!==2 || args[0]!=='--input' || !args[1]){
  console.error('Usage: node scripts/audit-followability-offline.mjs --input EXISTING_PAPER_RECEIPTS.json');
  process.exitCode=2;
}else{
  try{
    const info=await stat(args[1]);
    if(!info.isFile() || info.size>1024*1024)throw Error('EXISTING_BOUNDED_JSON_FILE_REQUIRED');
    const payload=JSON.parse(await readFile(args[1],'utf8'));
    const records=Array.isArray(payload)?payload:payload?.cases;
    const result=evaluatePaperFollowabilityCases(records);
    console.log(JSON.stringify(result,null,2));
  }catch(error){
    console.error('Read-only followability audit failed:',String(error?.message||error));
    process.exitCode=1;
  }
}
