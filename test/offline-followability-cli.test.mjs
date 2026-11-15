import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { createHash } from 'node:crypto';
import { execFileSync,spawnSync } from 'node:child_process';
const script=new URL('../scripts/audit-followability-offline.mjs',import.meta.url).pathname;
const hash=p=>createHash('sha256').update(fs.readFileSync(p)).digest('hex');

test('offline P2 study outputs unknown when signal time is unobservable; existing JSON remains byte-identical',()=>{
  const dir=fs.mkdtempSync(path.join(os.tmpdir(),'blix-p2-audit-'));
  const file=path.join(dir,'cases.json');
  try{
    fs.writeFileSync(file,JSON.stringify({cases:[{
      id:'unknown-time',mint:'GTNHLKQWKZHaHpd6PjfMgfFZUDEuCviwXMwYbCcepump',
      signal:{chainEventAtMs:100},
    }]}));
    const before=hash(file);
    const r=JSON.parse(execFileSync(process.execPath,[script,'--input',file],{encoding:'utf8'}));
    assert.equal(r.kind,'OFFLINE_FOLLOWABILITY_ELIGIBILITY_AUDIT');
    assert.equal(r.cases[0].status,'UNKNOWN_SIGNAL_AVAILABILITY');
    assert.equal(r.cases[0].simulatedNetLamports,undefined);
    assert.equal(r.outOfSamplePerformance,'NOT_ESTABLISHED');
    assert.equal(hash(file),before);
  }finally{fs.rmSync(dir,{recursive:true,force:true});}
});

test('missing file is not silently created by followability audit',()=>{
  const dir=fs.mkdtempSync(path.join(os.tmpdir(),'blix-p2-missing-'));
  const missing=path.join(dir,'nope.json');
  try{
    const r=spawnSync(process.execPath,[script,'--input',missing],{encoding:'utf8',timeout:10000});
    assert.equal(r.status,1);assert.equal(fs.existsSync(missing),false);
    assert.equal(spawnSync(process.execPath,[script,'--url','https://example.test'],{encoding:'utf8'}).status,2);
  }finally{fs.rmSync(dir,{recursive:true,force:true});}
});
