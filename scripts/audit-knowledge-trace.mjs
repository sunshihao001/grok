#!/usr/bin/env node
// Static knowledge provenance audit. Read-only; no RPC, model, dependency,
// network, trade, GitHub write or inference that a source was independently verified.
// Maps the existing historical router, migration inventory, snapshots and
// runtime whitelist. The manifests, not this file, remain the source of truth.
import { readFileSync, existsSync } from 'node:fs';
import { resolve,dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const root=resolve(dirname(fileURLToPath(import.meta.url)),'..');
const read=path=>readFileSync(resolve(root,path),'utf8');
const json=path=>JSON.parse(read(path));
const migrate=json('knowledge/MIGRATION.json');
const router=json('docs/project/legacy-knowledge-routing.v1.json');
const snapshots=json('knowledge/references/legacy-snapshot-sources.v1.json');
const coverage=json('knowledge/references/source-coverage-v0.1.json');
const loader=read('server/intelligence/local-knowledge-loader.mjs');
const fileExists=path=>typeof path==='string' && existsSync(resolve(root,path));
const sourceToLocal=new Map();
const entries=migrate.items.map(item=>{
  const record={
    sourceRepository:item.source_repo,
    originalRef:item.source_ref,
    originalPath:item.source_path,
    originalBlob:item.source_blob_sha,
    originalUrl:item.source_url,
    localPath:item.target,
    localExists:fileExists(item.target),
    recordedMigrationStatus:item.migration_status,
    sourceBlobReverified:false,
    liveRuntimeKnowledgeVerified:false,
  };
  if(!sourceToLocal.has(item.source_path))sourceToLocal.set(item.source_path,[]);
  sourceToLocal.get(item.source_path).push(record);
  return record;
});
const runtime=[...loader.matchAll(/label:'(knowledge\/[^']+)'/g)].map(match=>match[1]);
const loaderSet=new Set(runtime);
const legacyIndexUrl='https://github.com/sunshihao001/grok/blob/'+
  router.source_commit+'/'+router.source_atlas;
const units=router.units.map(unit=>{
  const targets=sourceToLocal.get(unit.source)||[];
  return {
    id:unit.id,title:unit.title,question:unit.question??null,
    primary:unit.primary,related:unit.related??[],
    historicalSourcePath:unit.source,
    originalRouterCommit:router.source_commit,
    originalRouterAtlas:legacyIndexUrl,
    localTargets:targets.map(x=>({
      path:x.localPath,exists:x.localExists,recordedMigrationStatus:x.recordedMigrationStatus,
      originalUrl:x.originalUrl,originalBlob:x.originalBlob,
      aiWhitelisted:loaderSet.has(x.localPath),
    })),
    state:targets.length?'MAPPED_TO_IMPORTED_SOURCE_DOCUMENT':'HISTORICAL_INDEX_REFERENCE_ONLY',
    // This crosswalk is document-level: do not claim unit text was separately
    // reviewed, correctly retrieved, or tested in a production AI task.
    unitMeaningIndependentlyVerified:false,
  };
});
const snapRecords=snapshots.documents.map(x=>({
  originalRepository:x.source_repository,originalCommit:x.source_commit,
  originalPath:x.source_path,originalBlob:x.source_git_blob_sha,
  originalUrl:x.source_url,legacySnapshotPath:x.snapshot_path,
  bodyImportedLocally:fileExists(x.snapshot_path),
  state:fileExists(x.snapshot_path)?'SOURCE_BODY_LOCALLY_AVAILABLE':'SOURCE_MANIFEST_ONLY',
}));
const runtimeRecords=runtime.map(path=>({
  path,exists:fileExists(path),
  importedFromLegacy:entries.some(x=>x.localPath===path),
  state:'ALLOWLISTED_FOR_OPTIONAL_CONTEXT_NOT_ACTUAL_MODEL_USE',
}));
const missing=entries.filter(x=>!x.localExists);
const unmapped=units.filter(x=>!x.localTargets.length);
const brokenRuntime=runtimeRecords.filter(x=>!x.exists);
const provenanceErrors=entries.filter(x=>
  !/^[a-f0-9]{40}$/.test(x.originalBlob||'') || !x.originalUrl ||
  !x.originalPath || !x.sourceRepository);
const summary={
  schemaVersion:'0.1',kind:'READ_ONLY_STATIC_KNOWLEDGE_LINEAGE_AUDIT',
  scope:'EXISTING_MANIFESTS_AND_LOCAL_PATHS_ONLY',
  sourceContext:{
    historicalUnitRouterStatus:router.status,
    sourceCoverageDate:coverage.as_of,
    recordedMigrationSourceRecheck:migrate.upstream_source_blob_check??null,
    recordedHistoricalSnapshotSourceRecheck:snapshots.upstream_snapshot_blob_check??null,
    sourceRepoStates:coverage.repo_sources.map(x=>({
      repo:x.repo,treeFiles:x.tree_files,status:x.status,
    })),
    externalProjectFirstPassCount:coverage.external_reference_first_pass.length,
    sourceContentReviewExhaustive:coverage.exhaustive_content_review_completed,
  },
  counts:{
    migratedFiles:entries.length,localTargetsPresent:entries.length-missing.length,
    legacyUnits:units.length,mappedUnits:units.length-unmapped.length,
    originalAtlasOnlyUnits:unmapped.length,
    historicalSnapshots:snapRecords.length,
    snapshotBodiesImported:snapRecords.filter(x=>x.bodyImportedLocally).length,
    runtimeAllowlistedSources:runtimeRecords.length,
    runtimeAllowlistedExisting:runtimeRecords.length-brokenRuntime.length,
  },
  migrationMissing:missing.map(x=>x.localPath),
  unanchoredMigrationProvenance:provenanceErrors.map(x=>x.localPath),
  brokenRuntimeSourcePaths:brokenRuntime.map(x=>x.path),
  originalAtlasOnlyUnitIds:unmapped.map(x=>x.id),
  limitations:[
    'Historical source ref/blob comes from existing manifests; no upstream Git blob bytes were re-fetched by this audit.',
    'Document-level mapping does not verify a specific unit, idea, author intention, claim, or derivation.',
    'Manifest-only snapshots are NOT locally imported; do not interpret 21 indexed entries as 21 reviewed bodies.',
    'An allowlisted local source is NOT evidence that an AI model retrieved, applied or evaluated that knowledge.',
    'Original references, authorship, citations, and license of individual external claims require independent inspection.',
    'GitHub mergeability, CI, real-chain history, model A/B and trading outcomes are outside this static check.',
  ],
};
const a=process.argv.slice(2);
let result;
if(a.length===0)result={...summary,example:'--unit D05-K01 | --target knowledge/mechanisms/wallet-roles-and-inventory.md | --all'};
else if(a.length===1&&a[0]==='--all')
  result={...summary,migrations:entries,units,historicalSnapshotSources:snapRecords,aiRuntimeAllowlist:runtimeRecords};
else if(a.length===2&&a[0]==='--unit') {
  const unit=units.find(x=>x.id===a[1]);
  if(!unit){console.error('UNKNOWN_LEGACY_UNIT');process.exit(2)}
  result={kind:'UNIT_TRACE',unit,limitations:summary.limitations};
}else if(a.length===2&&a[0]==='--target'){
  const target=a[1];
  if(!/^(knowledge|docs)\/[a-zA-Z0-9/_-]+\.(md|json)$/.test(target)){
    console.error('INVALID_LOCAL_TRACE_TARGET');process.exit(2);
  }
  const entry=entries.find(x=>x.localPath===target);
  result={kind:'LOCAL_KNOWLEDGE_TARGET_TRACE',target,
    localExists:fileExists(target),migration:entry??null,
    legacyUnits:units.filter(x=>x.localTargets.some(y=>y.path===target))
      .map(x=>({id:x.id,title:x.title,historicalSourcePath:x.historicalSourcePath})),
    aiWhitelisted:loaderSet.has(target),aiActuallyUsed:'NOT_CHECKED',
    limitations:summary.limitations};
}else{
  console.error('Usage: node scripts/audit-knowledge-trace.mjs [--all | --unit D05-K01 | --target knowledge/path.md]');
  process.exit(2);
}
console.log(JSON.stringify(result,null,2));
