import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { createHash } from 'node:crypto';
import { execFileSync,spawnSync } from 'node:child_process';
import { validatePulseDiscoveryInput } from '../server/intelligence/pulse-discovery.mjs';

const script=new URL('../scripts/audit-opportunity-comparison-offline.mjs',import.meta.url).pathname;
const A='EYqygbhZjP7EbM4fSn8devctnksAvPAD1Bt57XBFpump';
const B='GTNHLKQWKZHaHpd6PjfMgfFZUDEuCviwXMwYbCcepump';
const time=Date.parse('2026-11-01T03:23:31.969Z');
const hash=file=>createHash('sha256').update(fs.readFileSync(file)).digest('hex');
function fixture(){
  const snapshot={goal:'Compare two already observed Mint research decisions',
    browserRecordedAtMs:time,boardStatus:'BLIX_PULSE_LIVE_OR_POLLING',
    candidates:[{mint:A,stage:'migrated',liq:88618.5},{mint:B,stage:'new',liq:null}]};
  const clean=validatePulseDiscoveryInput(snapshot,time);
  const receipt=(mint)=>({discovery:{
    sourceRecordedAtMs:time,marketCoverage:clean.marketCoverage,
    candidateCount:2,candidateDigestSha256:clean.candidateDigestSha256,
    selectedMint:mint,reason:'Scripted selection, not a measured market outcome',
    modelSelectionVerified:false,
  },investigation:{status:'DRAFT_WITH_INCOMPLETE_EVIDENCE'}});
  return {snapshot,baseline:receipt(A),enhanced:receipt(B),supportingEvidence:[],paperReceipts:[]};
}
test('offline A/B CLI accepts a frozen matched-universe fixture and does not change source JSON',()=>{
  const dir=fs.mkdtempSync(path.join(os.tmpdir(),'blix-a-b-readonly-'));
  const file=path.join(dir,'comparison.json');
  try {
    fs.writeFileSync(file,JSON.stringify(fixture()));
    const before=hash(file);
    const result=JSON.parse(execFileSync(process.execPath,[script,'--input',file],{encoding:'utf8',timeout:10000}));
    assert.equal(result.kind,'OFFLINE_SAME_SNAPSHOT_A_B_INVESTIGATION_AUDIT');
    assert.equal(result.selection.changed,true);
    assert.equal(result.selection.modelBenefitEstablished,false);
    assert.equal(result.input.observedMintCount,2);
    assert.equal(result.verdict,'ONLY_SELECTION_DIFFERENCE_MEASURED_NOT_REAL_MARKET_ADVANTAGE');
    assert.equal(hash(file),before,'no edits to user-provided JSON');
  }finally{fs.rmSync(dir,{recursive:true,force:true});}
});
test('offline A/B CLI fails closed for changed snapshot and absent file or URL option',()=>{
  const dir=fs.mkdtempSync(path.join(os.tmpdir(),'blix-a-b-reject-'));
  const file=path.join(dir,'bad.json'),missing=path.join(dir,'missing.json');
  try {
    const data=fixture();
    data.enhanced.discovery.candidateDigestSha256='0'.repeat(64);
    fs.writeFileSync(file,JSON.stringify(data));
    const before=hash(file);
    const bad=spawnSync(process.execPath,[script,'--input',file],{encoding:'utf8',timeout:10000});
    assert.equal(bad.status,1);
    assert.match(bad.stderr,/POPULATION_OR_TIME_MISMATCH/);
    assert.equal(hash(file),before);
    assert.equal(spawnSync(process.execPath,[script,'--input',missing],{encoding:'utf8'}).status,1);
    assert.equal(fs.existsSync(missing),false);
    assert.equal(spawnSync(process.execPath,[script,'--url','https://example.test'],{encoding:'utf8'}).status,2);
  }finally{fs.rmSync(dir,{recursive:true,force:true});}
});
