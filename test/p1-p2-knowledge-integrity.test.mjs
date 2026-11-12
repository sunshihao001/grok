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
