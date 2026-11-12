// Read only existing project professional knowledge. No remote search, arbitrary
// model-supplied paths, extra expert system, wallet database or prompt authority.
// This deterministic shortlist is OPTIONAL context, not a verified wallet label.
import { readFile } from 'node:fs/promises';
import { createHash } from 'node:crypto';

const SOURCES = Object.freeze([
  { id:'wallet-roles', path:'../../knowledge/mechanisms/wallet-roles-and-inventory.md',
    label:'knowledge/mechanisms/wallet-roles-and-inventory.md',
    cues:['钱包','wallet','holder','持仓','角色','库存','转仓','transfer','接收','卖出','控盘','bundle'] },
  { id:'capital-funding', path:'../../knowledge/mechanisms/capital-organization-and-incentives.md',
    label:'knowledge/mechanisms/capital-organization-and-incentives.md',
    cues:['资金','fund','sol','共同','同源','出资','关联','操盘','控制','洗量','funding'] },
  { id:'cohort-timing', path:'../../knowledge/methods/anomaly-and-cohort-discovery.md',
    label:'knowledge/methods/anomaly-and-cohort-discovery.md',
    cues:['群体','同步','时间','hour','小时','异动','cohort','时序','协同','跨mint','监控','跨币'] },
  { id:'execution', path:'../../knowledge/mechanisms/strategy-and-execution-economics.md',
    label:'knowledge/mechanisms/strategy-and-execution-economics.md',
    cues:['跟单','策略','alpha','滑点','价格','流动性','成本','pnl','收益','止盈','回测','execution'] },
  { id:'chain', path:'../../knowledge/foundations/solana-chain-and-market.md',
    label:'knowledge/foundations/solana-chain-and-market.md',
    cues:['cpi','token-2022','owner','token account','rpc','指令','账户','wsol','fee payer','解析'] },
  { id:'validation', path:'../../knowledge/cases/independent-validation-and-failure-cases.md',
    label:'knowledge/cases/independent-validation-and-failure-cases.md',
    cues:['反证','样本','验证','失败','偏差','回放','误报','漏报','完整性','风险','unknown'] },
]);

function scoreTopic(topic,goal,evidence) {
  let score = topic.cues.filter(x=>goal.includes(x.toLowerCase())).length * 2;
  const entries = Array.isArray(evidence) ? evidence : [];
  if (topic.id==='wallet-roles' && entries.some(x=>x.result?.facts?.network?.eventCount>0)) score+=2;
  if (topic.id==='capital-funding' && entries.some(x=>x.result?.facts?.network?.distributionCandidates?.length>0)) score+=2;
  if (topic.id==='validation' && entries.some(x=>x.error || x.result?.status==='UNAVAILABLE' ||
    x.result?.facts?.senderDiscovery?.truncated)) score+=3;
  if (topic.id==='cohort-timing' && entries.some(x=>x.result?.facts?.network?.events?.some(e=>e.crossMintCandidates?.length>0))) score+=2;
  return score;
}
function extractSection(doc,goal,terms,maxChars) {
  const sections=doc.split(/(?=^#{2,4}\s)/m);
  const ranked=sections.map((content,i)=>{
    const header=content.split('\n')[0].toLowerCase();
    const weight=terms.filter(x=>header.includes(x.toLowerCase())).length*3 +
      terms.filter(x=>goal.includes(x.toLowerCase()) && content.slice(0,1200).toLowerCase().includes(x.toLowerCase())).length;
    return {content,weight,i};
  }).sort((a,b)=>b.weight-a.weight || a.i-b.i);
  const chosen=ranked[0]?.content || doc;
  // Prepend source-status warning even when the selected passage lacks it.
  return ('Historical research candidate; NOT validated live chain fact or a trading instruction.\n' +
    chosen.slice(0,maxChars-90)).slice(0,maxChars);
}

export function makeLocalKnowledgeLoader({maxSources=3,maxChars=1500}={}) {
  if (!Number.isInteger(maxSources) || maxSources<1 || maxSources>5 ||
      !Number.isInteger(maxChars) || maxChars<300 || maxChars>1600) {
    throw Error('INVALID_LOCAL_KNOWLEDGE_LIMIT');
  }
  return async ({goal='',evidence=[]}={})=>{
    const q=typeof goal==='string'?goal.toLowerCase().slice(0,4096):'';
    const choices=SOURCES.map(x=>({...x,score:scoreTopic(x,q,evidence)}))
      .filter(x=>x.score>0).sort((a,b)=>b.score-a.score).slice(0,maxSources);
    const output=[];
    for(const item of choices) {
      // Each path is a hardcoded repository-relative file. Model content never
      // selects another file or changes the read permission.
      const doc=await readFile(new URL(item.path,import.meta.url),'utf8');
      const version=createHash('sha256').update(doc).digest('hex').slice(0,16);
      const excerpt=extractSection(doc,q,item.cues,maxChars);
      const caveat=item.id==='cohort-timing' ?
        'RETRACTED NUMERICAL FINDINGS: The RED-COHORT study cited by this knowledge source withdrew quantitative results. Do not use those percentages or significance claims.\n' : '';
      output.push({source:'LOCAL_PROJECT_RESEARCH:'+item.label+'@sha256:'+version,
        excerpt:(caveat+excerpt).slice(0,maxChars),
        trustedAsInstruction:false,
        status:'RESEARCH_NOT_RUNTIME_VALIDATED',
        topic:item.id});
    }
    return output;
  };
}
