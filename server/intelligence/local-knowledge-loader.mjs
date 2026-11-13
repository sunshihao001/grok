// Read only existing project professional knowledge. No remote search, arbitrary
// model-supplied paths, extra expert system, wallet database or prompt authority.
// This deterministic shortlist is OPTIONAL context, not a verified wallet label.
import { readFile } from 'node:fs/promises';
import { createHash } from 'node:crypto';

const SOURCES = Object.freeze([
  { id:'wallet-roles', path:'../../knowledge/mechanisms/wallet-roles-and-inventory.md',
    label:'knowledge/mechanisms/wallet-roles-and-inventory.md',
    cues:['钱包','wallet','holder','持仓','角色','库存','转仓','transfer','接收','卖出','控盘','bundle','地址','池地址','交易所','筹码','余额'] },
  { id:'capital-funding', path:'../../knowledge/mechanisms/capital-organization-and-incentives.md',
    label:'knowledge/mechanisms/capital-organization-and-incentives.md',
    cues:['资金','fund','sol','共同','同源','出资','关联','操盘','控制','洗量','funding','出金','接力','资金来源','净流入'] },
  { id:'cohort-timing', path:'../../knowledge/methods/anomaly-and-cohort-discovery.md',
    label:'knowledge/methods/anomaly-and-cohort-discovery.md',
    cues:['群体','同步','时间','hour','小时','异动','cohort','时序','协同','跨mint','监控','跨币','同槽','一槽','新发生','回补','今日'] },
  { id:'execution', path:'../../knowledge/mechanisms/strategy-and-execution-economics.md',
    label:'knowledge/mechanisms/strategy-and-execution-economics.md',
    cues:['跟单','策略','alpha','滑点','价格','流动性','成本','pnl','收益','止盈','回测','execution','成交','可跟','报价'] },
  { id:'chain', path:'../../knowledge/foundations/solana-chain-and-market.md',
    label:'knowledge/foundations/solana-chain-and-market.md',
    cues:['cpi','token-2022','owner','token account','rpc','指令','账户','wsol','fee payer','解析','token2022','transfer hook','手续费','pool','vault','池地址'] },
  { id:'validation', path:'../../knowledge/cases/independent-validation-and-failure-cases.md',
    label:'knowledge/cases/independent-validation-and-failure-cases.md',
    cues:['反证','样本','验证','失败','偏差','回放','误报','漏报','完整性','风险','unknown','历史回补','回补','选错','错判','资料误用'] },
  // Existing primary source material; narrow cues avoid injecting every old book.
  { id:'multihop', path:'../../knowledge/references/multihop-funding-evidence-audit.md',
    label:'knowledge/references/multihop-funding-evidence-audit.md',
    cues:['多跳','五跳','中转钱包','粉尘','dust','共享服务','bridge','隐蔽钱包','非holder','隐含资金','接力','转给新钱包'] },
  { id:'key-wallet', path:'../../knowledge/methods/key-wallet-investigation-brief.md',
    label:'knowledge/methods/key-wallet-investigation-brief.md',
    cues:['关键钱包','早期买家','sniper','kol','bundler','钱包榜单','跟单钱包','能否跟随'] },
  { id:'market-mechanism', path:'../../knowledge/mechanisms/market-price-mechanism-research.md',
    label:'knowledge/mechanisms/market-price-mechanism-research.md',
    cues:['价格冲击','盘口','池深','cpmm','avwap','poc','做市','流动性陷阱','库存压力','供需机制','二次启动','上涨','下跌','资金净流入'] },
  { id:'ai-knowledge', path:'../../knowledge/ai/intent-knowledge-selection-and-reasoning.md',
    label:'knowledge/ai/intent-knowledge-selection-and-reasoning.md',
    cues:['知识选择','知识检索','专家认知','提示词','意图','agent','模型评估','自主研究','skill','知识来源','专业资料','选错','路由','资料检索'] },
  { id:'source-reconciliation', path:'../../knowledge/references/p1-p2-knowledge-reconciliation-20261113.md',
    label:'knowledge/references/p1-p2-knowledge-reconciliation-20261113.md',
    cues:['来源对照','知识整合','旧知识冲突','全域审查','审计知识','知识修正','全部来源'] },
]);

function cueMatches(goal,cue) {
  // Short Latin terms (SOL, PnL, AI) must not match substrings of unrelated words
  // such as console or main. Chinese cues remain direct phrase matches.
  const term=cue.toLowerCase();
  if (/^[a-z]{1,3}$/.test(term)) {
    const escaped=term.replace(/[.*+?^${}()|[\]\\]/g,'\\function scoreTopic(topic,goal,evidence) {
  let score = topic.cues.filter(x=>goal.includes(x.toLowerCase())).length * 2;');
    return new RegExp('(^|[^a-z])'+escaped+'(?=$|[^a-z])').test(goal);
  }
  return goal.includes(term);
}
function scoreTopic(topic,goal,evidence) {
  let score = topic.cues.filter(x=>cueMatches(goal,x)).length * 2;
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
      terms.filter(x=>cueMatches(goal,x) && content.slice(0,1200).toLowerCase().includes(x.toLowerCase())).length;
    return {content,weight,i};
  }).sort((a,b)=>b.weight-a.weight || a.i-b.i);
  const chosen=ranked[0]?.content || doc;
  const warning='Historical research candidate; NOT validated live chain fact or a trading instruction.\n';
  // Carry the latest in-place applicability correction when the most relevant
  // historical subsection is selected. Never discard evidence/limit caveats
  // solely because they appear after a long legacy document.
  const corrected=sections.find(s=>/^## 2026-11-13｜/.test(s));
  if(corrected && corrected!==chosen) {
    const amendment=corrected.slice(0,Math.min(520,Math.floor(maxChars*0.52)));
    return (warning+'Latest scoped correction:\n'+amendment+'\nLegacy related excerpt:\n'+
      chosen.slice(0,Math.max(0,maxChars-warning.length-amendment.length-45))).slice(0,maxChars);
  }
  return (warning+chosen.slice(0,maxChars-warning.length)).slice(0,maxChars);
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
