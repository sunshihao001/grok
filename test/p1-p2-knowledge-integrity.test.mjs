import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync,existsSync} from 'node:fs';
import {fileURLToPath} from 'node:url';
import {resolve,dirname} from 'node:path';

const root=resolve(dirname(fileURLToPath(import.meta.url)),'..');
const read=p=>readFileSync(resolve(root,p),'utf8');
const sources=[
 'knowledge/foundations/solana-chain-and-market.md',
 'knowledge/mechanisms/wallet-roles-and-inventory.md',
 'knowledge/mechanisms/capital-organization-and-incentives.md',
 'knowledge/mechanisms/market-price-mechanism-research.md',
 'knowledge/methods/anomaly-and-cohort-discovery.md',
 'knowledge/mechanisms/strategy-and-execution-economics.md',
 'knowledge/cases/independent-validation-and-failure-cases.md',
 'knowledge/ai/intent-knowledge-selection-and-reasoning.md',
];

test('P1/P2 knowledge corrections live in original D01–D12 source documents',()=>{
 for(const path of sources){
   const body=read(path);
   assert.match(body,/2026-11-13/,'missing current evidence section: '+path);
   assert.match(body,/p1-p2-knowledge-reconciliation-20261113\.md/,'not linked to primary audit: '+path);
   assert.ok(body.length>700,'must preserve original historical research: '+path);
 }
});
test('cross-project source audit preserves 12 domains, primary references and non-production status',()=>{
 const audit=read('knowledge/references/p1-p2-knowledge-reconciliation-20261113.md');
 for(let i=1;i<=12;i++){
   assert.ok(audit.includes('D'+String(i).padStart(2,'0')),'missing D'+i);
 }
 for(const token of ['sunshihao001/-','sunshihao001/qb-','sunshihao001/meme-',
    'sunshihao001/ai-d','Why-Solana','token-finder','trading-portfolio','skill-reach',
    'solana.com/docs','OFFLINE_TEST','UNKNOWN','Token-2022']){
   assert.ok(audit.includes(token),'missing known source or applicability limit: '+token);
 }
 assert.match(audit,/不等于真实主网|没有.*真实主网/);
});
test('main knowledge navigation points at current implemented source audit',()=>{
 for(const path of ['knowledge/README.md','knowledge/references/README.md',
   'knowledge/INTEGRATION-CROSSWALK.md','docs/project/README.md',
   'docs/project/knowledge-use.md','docs/project/knowledge-to-capability-integration-v0.1.md']){
   assert.match(read(path),/p1-p2-knowledge-reconciliation-20261113\.md/,path);
 }
});
test('eleven optional runtime knowledge sources are local whitelisted readable files',()=>{
 const loader=read('server/intelligence/local-knowledge-loader.mjs');
 const all=[...loader.matchAll(/path:'(\.\.\/\.\.\/knowledge\/[^']+)'/g)];
 assert.equal(all.length,11,'no implicit or broad unreviewed source injection');
 for(const [,relative] of all){
   const full=resolve(root,'server/intelligence',relative);
   assert.ok(full.startsWith(resolve(root,'knowledge')+'/'),'only in-repo professional material');
   assert.ok(existsSync(full),'missing selected knowledge source: '+relative);
 }
 assert.match(loader,/trustedAsInstruction:false/);
 assert.match(loader,/RETRACTED NUMERICAL FINDINGS/);
});

test('all twelve professional domains have one existing main narrative and retain complete source coverage', () => {
  const model = JSON.parse(read('knowledge/DOMAIN-MODEL.v1.json'));
  assert.equal(model.layers.length, 8);
  assert.equal(model.domains.length, 12);
  const main = read('knowledge/README.md');
  const routes = {
    D01: 'knowledge/foundations/solana-chain-and-market.md',
    D02: 'knowledge/foundations/solana-chain-and-market.md',
    D03: 'knowledge/mechanisms/market-price-mechanism-research.md',
    D04: 'knowledge/mechanisms/wallet-roles-and-inventory.md',
    D05: 'knowledge/mechanisms/capital-organization-and-incentives.md',
    D06: 'knowledge/mechanisms/wallet-roles-and-inventory.md',
    D07: 'knowledge/methods/anomaly-and-cohort-discovery.md',
    D08: 'knowledge/mechanisms/strategy-and-execution-economics.md',
    D09: 'knowledge/mechanisms/strategy-and-execution-economics.md',
    D10: 'knowledge/foundations/solana-chain-and-market.md',
    D11: 'knowledge/cases/independent-validation-and-failure-cases.md',
    D12: 'knowledge/ai/intent-knowledge-selection-and-reasoning.md',
  };
  assert.deepEqual(Object.keys(routes), model.domains.map(x => x.id));
  for (const [domain, file] of Object.entries(routes)) {
    assert.ok(existsSync(resolve(root, file)), domain + ' lost its current professional narrative');
    assert.ok(main.includes(file.replace('knowledge/', '')), domain + ' missing from main knowledge index');
    assert.match(read(file), /2026-11-14｜全域归位：/, domain + ' missing in-place professional synthesis');
  }
  for (const retained of [
    'knowledge/references/synapse-methodology-full-taxonomy-20261114.md',
    'knowledge/references/source-coverage-v0.1.json',
    'knowledge/methods/hermes-multidimensional-reasoning-original.md',
    'knowledge/methods/hermes-reverse-discovery-original.md',
    'knowledge/foundations/legacy-grok-domain-core.md',
    'knowledge/ai/intent-knowledge-selection-and-reasoning.md',
  ]) assert.ok(existsSync(resolve(root, retained)), 'do not lose source provenance: ' + retained);
  for (const token of ['14/14', '65', '152', 'USER_PARAPHRASE', 'CONNECTED_READONLY_RUNTIME']) {
    assert.ok(main.includes(token), 'missing source/evidence distinction: ' + token);
  }
  const build = read('docs/project/intelligence-layer.md');
  for (const token of ['P0-A', 'P0-B', 'P0-C', 'P1-A', 'P1-B', 'P1-C', 'P2-A', 'P2-B']) {
    assert.ok(build.includes(token), 'missing product acceptance contract: ' + token);
  }
  assert.match(build, /NOT_DEPLOYED/);
});
