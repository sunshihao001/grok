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
const domainModel=json('knowledge/DOMAIN-MODEL.v1.json');
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
if(a.length===0)result={...summary,example:'--unit D05-K01 | --target knowledge/mechanisms/wallet-roles-and-inventory.md | --axes | --routes | --all'};
else if(a.length===1&&a[0]==='--all')
  result={...summary,migrations:entries,units,historicalSnapshotSources:snapRecords,aiRuntimeAllowlist:runtimeRecords};
else if(a.length===1&&a[0]==='--axes') {
  const alignment=domainModel.cross_axis_alignment;
  if(!alignment || !Array.isArray(alignment.independentAxes) || !Array.isArray(alignment.linkKinds)) {
    console.error('CROSS_AXIS_MODEL_MISSING');process.exit(2);
  }
  result={
    kind:'READ_ONLY_CROSS_AXIS_KNOWLEDGE_ALIGNMENT',
    schemaVersion:domainModel.schema_version,
    alignmentVersion:alignment.revision,
    alignmentStatus:alignment.status,
    legacyAxes:{goals:domainModel.goals.length,knowledgeLayers:domainModel.layers.length,
      domains:domainModel.domains.length,storageTypes:domainModel.structure.storage_axis},
    independentAxes:alignment.independentAxes,
    linkKinds:alignment.linkKinds,
    proofBoundaries:alignment.proofBoundaries,
    sampleTask:alignment.sampleTask,
    canonicalGuides:alignment.canonicalGuides,
    interpretationCapabilities:alignment.interpretationCapabilities||[],
    networkViews:alignment.networkViews||[],
    placementDecision:alignment.placementDecision||null,
    limits:[
      'This is a declarative knowledge relation map, not a source-of-truth of observed market relationships.',
      'Conceptual link is not an RPC event; source provenance is not independent validation.',
      'Implemented_by and tested_by do not prove deployed or production correctness.',
      'No AI retrieval or economic controller inference is performed by this command.',
    ],
  };
}
else if(a.length===1&&a[0]==='--routes') {
  // Static referential closure only: these are business/concept handoffs,
  // never permission, runtime orchestration, wallet control or market Alpha.
  const g=domainModel.cross_axis_alignment.businessRouteGraph;
  if(!g){console.error('MEME_ROUTE_GRAPH_MISSING');process.exit(2)}
  const errors=[];
  const unique=(arr,label,key='id')=>{
    const ids=arr.map(x=>x[key]);
    if(new Set(ids).size!==ids.length)errors.push(label+'_DUPLICATE_ID');
    return new Set(ids);
  };
  const outcomes=unique(g.businessOutcomes,'OUTCOME');
  const conceptIds=unique(g.conceptCarriers,'CONCEPT');
  const routes=unique(g.entryRoutes,'ENTRY');
  const loops=unique(g.feedbackLoops,'FEEDBACK');
  const knownDomains=new Set(domainModel.domains.map(x=>x.id));
  const caps=new Set((domainModel.cross_axis_alignment.interpretationCapabilities||[]).map(x=>x.id));
  const axes=new Set(domainModel.cross_axis_alignment.independentAxes.map(x=>x.id));
  const requiredOutcomes=['O1','O2','O3','O4','O5','O6'];
  for(const id of requiredOutcomes)if(!outcomes.has(id))errors.push('MISSING_'+id);
  if(outcomes.size!==requiredOutcomes.length)errors.push('UNEXPECTED_BUSINESS_OUTCOME');
  const requiredPaths=[];
  for(const x of g.businessOutcomes){
    if(!x.domainRefs?.length||x.domainRefs.some(id=>!knownDomains.has(id)))errors.push(x.id+'_BAD_DOMAINS');
    if(!x.capabilityRefs?.length||x.capabilityRefs.some(id=>!caps.has(id)))errors.push(x.id+'_BAD_CAPABILITIES');
    if(!x.codeRefs?.length)errors.push(x.id+'_MISSING_IMPLEMENTATION_REFERENCE');
    requiredPaths.push(...(x.codeRefs||[]));
    if(!x.output||!x.verification)errors.push(x.id+'_MISSING_OUTPUT_OR_LIMIT');
  }
  for(const x of g.conceptCarriers){
    if(!caps.has(x.supportCapability)||!axes.has(x.axis))errors.push(x.id+'_MISALIGNED_EXISTING_AXIS');
    if(!x.meaning||!x.neverAssume||!x.canonicalPath)errors.push(x.id+'_MISSING_SEMANTIC_LIMIT');
    requiredPaths.push(x.canonicalPath);
  }
  for(const id of ['S1','S2','S3','S4','S5','S6','S7'])
    if(!g.conceptCarriers.some(x=>x.supportCapability===id))errors.push('MISSING_CONCEPT_CARRIER_'+id);
  if(g.handoffs.some(x=>x.relation!=='CONDITIONAL_BUSINESS_HANDOFF_NOT_INFERRED_ECONOMIC_EDGE'))
    errors.push('BUSINESS_HANDOFF_MASQUERADES_AS_ONCHAIN_EVIDENCE');
  const edges=unique(g.handoffs.map((x,i)=>({...x,id:x.from+'->'+x.to})),'HANDOFF');
  for(const x of g.handoffs){
    if(!outcomes.has(x.from)||!outcomes.has(x.to)||!x.minimumHandoff||!x.condition||!x.result)
      errors.push('INVALID_HANDOFF_'+x.from+'_'+x.to);
  }
  const checkPath=(id,path,loop=false)=>{
    if(!Array.isArray(path)||path.length<2)errors.push(id+'_PATH_TOO_SHORT');
    else{
      if(loop&&path[0]!==path.at(-1))errors.push(id+'_NOT_CLOSED');
      for(const node of path)if(!outcomes.has(node))errors.push(id+'_UNKNOWN_NODE_'+node);
      for(let i=1;i<path.length;i++)
        if(!edges.has(path[i-1]+'->'+path[i]))errors.push(id+'_MISSING_HANDOFF_'+path[i-1]+'_'+path[i]);
    }
  };
  for(const r of g.entryRoutes){
    checkPath(r.id,r.path);
    if(!r.entry||!r.gate)errors.push(r.id+'_MISSING_ENTRY_OR_STOP');
    for(const detour of r.optionalDetours||[])checkPath(r.id+'_DETOUR',detour.split('→'));
  }
  for(const l of g.feedbackLoops){
    checkPath(l.id,l.path,true);
    if(!l.reopenWhen||!l.change)errors.push(l.id+'_MISSING_FEEDBACK_TRIGGER');
  }
  const life=unique(g.knowledgeLifecycle,'LIFECYCLE');
  for(let i=1;i<=9;i++){
    const id='K'+i;
    if(!life.has(id))errors.push('MISSING_'+id);
  }
  for(const k of g.knowledgeLifecycle){
    if(!caps.has(k.supportCapability)||!k.role||!k.failureOrCorrection)errors.push(k.id+'_MISSING_KNOWLEDGE_BRIDGE');
    requiredPaths.push(k.canonicalPath);
  }
  if(!g.stopBoundaries?.length||!/NOT_|UNVERIFIED|DECLARATIVE/.test(g.status||''))errors.push('LIMITS_OR_DECLARATIVE_STATUS_MISSING');
  requiredPaths.push(g.sourceOfTruth);
  const badPaths=Array.from(new Set(requiredPaths.filter(p=>!fileExists(p))));
  if(badPaths.length)errors.push('BROKEN_REFERENCED_PATHS');
  // Route inventory must connect every O node, not merely list orphan domains.
  const touched=new Set([...g.entryRoutes.flatMap(x=>x.path),...g.feedbackLoops.flatMap(x=>x.path)]);
  for(const id of requiredOutcomes)if(!touched.has(id))errors.push('UNREACHABLE_OUTCOME_'+id);
  if(errors.length){console.error('MEME_ROUTE_GRAPH_INVALID '+JSON.stringify({errors,badPaths}));process.exit(2)}
  result={
    kind:'READ_ONLY_MEME_MULTI_ROUTE_GRAPH_AUDIT',
    status:g.status,revision:g.revision,sourceOfTruth:g.sourceOfTruth,
    counts:{outcomes:outcomes.size,concepts:conceptIds.size,entryRoutes:routes.size,
      handoffs:edges.size,feedbackLoops:loops.size,knowledgeStages:life.size,brokenPaths:badPaths.length},
    businessOutcomes:g.businessOutcomes,conceptCarriers:g.conceptCarriers,
    entryRoutes:g.entryRoutes,handoffs:g.handoffs,feedbackLoops:g.feedbackLoops,
    knowledgeLifecycle:g.knowledgeLifecycle,stopBoundaries:g.stopBoundaries,
    staticGraphChecked:true,
    runtimeMarketClosureVerified:false,actualAIUseVerified:false,followabilityVerified:false,
    limitations:[
      'Graph edges are conditional conceptual handoffs, not observed wallet relations, market events or authorization.',
      'This validates existing file references and graph connectivity, not model execution or economic source completeness.',
      'Historical/real-time case quality, data-provider first availability, execution quotes and business benefit remain separate tests.'
    ]
  };
}
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
  console.error('Usage: node scripts/audit-knowledge-trace.mjs [--axes | --routes | --all | --unit D05-K01 | --target knowledge/path.md]');
  process.exit(2);
}
console.log(JSON.stringify(result,null,2));
