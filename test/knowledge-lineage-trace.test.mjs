import test from 'node:test';
import assert from 'node:assert/strict';
import {spawnSync} from 'node:child_process';
import {readFileSync,existsSync} from 'node:fs';
import {fileURLToPath} from 'node:url';

const cli=fileURLToPath(new URL('../scripts/audit-knowledge-trace.mjs',import.meta.url));
function run(...args){
 const result=spawnSync(process.execPath,[cli,...args],{encoding:'utf8',timeout:15000,maxBuffer:6*1024*1024});
 assert.equal(result.status,0,result.stderr||result.stdout);
 return JSON.parse(result.stdout);
}
test('full original lineage is mapped without claiming historical snapshots or AI runtime verification',()=>{
 const r=run('--all');
 assert.equal(r.kind,'READ_ONLY_STATIC_KNOWLEDGE_LINEAGE_AUDIT');
 assert.equal(r.counts.migratedFiles,21);
 assert.equal(r.counts.localTargetsPresent,21);
 assert.equal(r.counts.legacyUnits,152);
 assert.equal(r.counts.mappedUnits,144);
 assert.equal(r.counts.originalAtlasOnlyUnits,8);
 assert.equal(r.counts.historicalSnapshots,21);
 assert.equal(r.counts.snapshotBodiesImported,0);
 assert.equal(r.counts.runtimeAllowlistedSources,11);
 assert.equal(r.counts.runtimeAllowlistedExisting,11);
 assert.equal(r.sourceContext.recordedMigrationSourceRecheck.checked_entries,21);
 assert.equal(r.sourceContext.recordedMigrationSourceRecheck.matched_entries,21);
 assert.equal(r.sourceContext.recordedHistoricalSnapshotSourceRecheck.checked_entries,21);
 assert.equal(r.sourceContext.recordedHistoricalSnapshotSourceRecheck.local_snapshot_bodies_present,0);
 assert.equal(r.migrations?.[0]?.sourceBlobReverified,false,
   'offline audit must not falsely claim it has fetched upstream in this invocation');
 assert.deepEqual(r.migrationMissing,[]);
 assert.deepEqual(r.brokenRuntimeSourcePaths,[]);
 assert.deepEqual(r.originalAtlasOnlyUnitIds,
  Array.from({length:8},(_,i)=>'L0-K0'+(i+1)));
 assert.ok(r.units.every(x=>x.unitMeaningIndependentlyVerified===false));
 assert.ok(r.aiRuntimeAllowlist.every(x=>x.state==='ALLOWLISTED_FOR_OPTIONAL_CONTEXT_NOT_ACTUAL_MODEL_USE'));
 assert.ok(r.historicalSnapshotSources.every(x=>x.state==='SOURCE_MANIFEST_ONLY'));
 assert.ok(r.limitations.some(x=>/no upstream Git blob bytes/.test(x)));
});
test('a domain wallet unit can be traced to its immutable recorded origin and local target',()=>{
 const r=run('--unit','D04-K01');
 assert.equal(r.kind,'UNIT_TRACE');
 assert.equal(r.unit.id,'D04-K01');
 assert.equal(r.unit.state,'MAPPED_TO_IMPORTED_SOURCE_DOCUMENT');
 assert.ok(r.unit.localTargets.some(x=>x.path==='knowledge/mechanisms/wallet-roles-and-inventory.md'));
 assert.ok(r.unit.localTargets.some(x=>x.aiWhitelisted===true));
 assert.ok(r.unit.localTargets.every(x=>x.originalBlob?.length===40));
 assert.equal(r.unit.unitMeaningIndependentlyVerified,false);
});
test('original 8 foundation index entries remain remote references, never fake local copies',()=>{
 const r=run('--unit','L0-K01');
 assert.equal(r.unit.state,'HISTORICAL_INDEX_REFERENCE_ONLY');
 assert.deepEqual(r.unit.localTargets,[]);
 assert.match(r.unit.originalRouterAtlas,/\/blob\/[a-f0-9]{40}\//);
});
test('backward lookup from local file identifies related source, units and runtime allowlist status',()=>{
 const r=run('--target','knowledge/mechanisms/wallet-roles-and-inventory.md');
 assert.equal(r.kind,'LOCAL_KNOWLEDGE_TARGET_TRACE');
 assert.equal(r.aiWhitelisted,true);
 assert.ok(r.migration.originalPath?.includes('L3-wallet-actors.md'));
 assert.ok(r.legacyUnits.some(x=>x.id.startsWith('D04-')));
 assert.equal(r.aiActuallyUsed,'NOT_CHECKED');
});
test('unknown unit and invalid target cannot escape read-only scope',()=>{
 const badUnit=spawnSync(process.execPath,[cli,'--unit','D99-K99'],{encoding:'utf8'});
 assert.equal(badUnit.status,2);
 const pathTraversal=spawnSync(process.execPath,[cli,'--target','../../secret.json'],{encoding:'utf8'});
 assert.equal(pathTraversal.status,2);
});


test('source-to-proof knowledge lifecycle stays linked from existing knowledge entry points and records non-verified states',()=>{
  const file=new URL('../knowledge/references/knowledge-lineage-lifecycle-20261113.md',import.meta.url);
  const doc=readFileSync(file,'utf8');
  for(const word of ['QUESTION','SOURCE','OBSERVATION','CONCEPT','CLAIM','METHOD','CASE',
    'IMPLEMENTATION','DECISION','EVALUATION','REVISION','derived_from','tested_by',
    'source-coverage-v0.1.json','scripts/audit-knowledge-trace.mjs',
    'D04-K01','L0-K01','SOURCE_READ','OFFLINE_TEST']) {
    assert.ok(doc.includes(word),'missing traceability concept or example: '+word);
  }
  assert.match(doc,/文件级可追溯/);
  assert.match(doc,/不表示|不能宣称|不等于/);
  for(const target of [
    '../knowledge/README.md','../knowledge/references/README.md',
    '../docs/project/knowledge-use.md','../knowledge/ai/intent-knowledge-selection-and-reasoning.md',
  ]) {
    const p=new URL(target,import.meta.url);
    assert.ok(existsSync(p),'missing original navigation: '+target);
    assert.match(readFileSync(p,'utf8'),/knowledge-lineage-lifecycle-20261113\.md/,target);
  }
});


test('holistic source-to-ability guidance is discoverable from existing knowledge navigation',()=>{
 const audited='knowledge-lineage-lifecycle-audit-20261113.md';
 for(const file of [
   '../knowledge/README.md','../knowledge/references/README.md',
   '../docs/project/knowledge-use.md',
 ]){
   assert.ok(readFileSync(new URL(file,import.meta.url),'utf8').includes(audited),
     'existing knowledge entry must link lineage explanation: '+file);
 }
 const doc=readFileSync(new URL('../knowledge/references/'+audited,import.meta.url),'utf8');
 for(const term of [
   '获取 / Acquisition','承接 / Inheritance','证据归属 / Grounding',
   '反证 / Falsification','检索与选择 / Retrieval',
   '反馈与修订 / Revision','原始来源','W3C','OpenLineage',
   'D05-K01','历史快照','无法','UNKNOWN'
 ]){
   assert.ok(doc.includes(term),'lifecycle concept missing: '+term);
 }
});
