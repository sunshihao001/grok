// Standalone loopback research HTTP service. Never imports Blix's trading server.
// CORS, JSON-only requests, host checking and request budgets are intentionally
// independent of the trading terminal's authentication or GET semantics.
import { createServer } from 'node:http';
import { runAiResearchTask } from './ai-workflow.mjs';
import { discoverPulseInvestigation, validatePulseDiscoveryInput } from './pulse-discovery.mjs';
import { summarizeInvestigationContinuation } from './investigation-continuation.mjs';

const MINT = /^[1-9A-HJ-NP-Za-km-z]{32,44}$/;
const MAX_BODY = 12_000;
const MAX_RESPONSE = 512_000;
const DEFAULT_ORIGINS = Object.freeze([
  'http://127.0.0.1:4420', 'http://localhost:4420',
  // Original Blix React UI is served on 4421 by server/webapp.js.
  'http://127.0.0.1:4421', 'http://localhost:4421',
  'http://127.0.0.1:5173', 'http://localhost:5173',
]);
const json = (res, code, payload) => {
  const body = JSON.stringify(payload);
  if (Buffer.byteLength(body, 'utf8') > MAX_RESPONSE) {
    res.writeHead(500, { 'Content-Type': 'application/json; charset=utf-8' });
    return res.end('{"error":"RESULT_EXCEEDS_UI_BUDGET"}');
  }
  res.writeHead(code, {
    'Content-Type': 'application/json; charset=utf-8',
    'Cache-Control': 'no-store',
    'X-Content-Type-Options': 'nosniff',
    'Referrer-Policy': 'no-referrer',
  });
  res.end(body);
};
async function readBody(req, route) {
  let bytes = 0;
  const parts = [];
  for await (const piece of req) {
    bytes += piece.length;
    if (bytes > MAX_BODY) throw new Error('REQUEST_TOO_LARGE');
    parts.push(piece);
  }
  let data;
  try { data = JSON.parse(Buffer.concat(parts).toString('utf8')); }
  catch { throw new Error('REQUEST_NOT_JSON'); }
  if (route === '/discover') { validatePulseDiscoveryInput(data); return data; }
  if (!data || typeof data !== 'object' || Array.isArray(data) ||
      Object.keys(data).some(x => !['goal','mint'].includes(x)) ||
      typeof data.goal !== 'string' || data.goal.trim().length < 2 ||
      data.goal.length > 1600 || typeof data.mint !== 'string' || !MINT.test(data.mint)) {
    throw new Error('REQUEST_INVALID_SCOPE');
  }
  return { mint: data.mint, goal: data.goal.trim() };
}
function errorCode(error) {
  const message = String(error?.message || '');
  return new Set([
    'REQUEST_TOO_LARGE','REQUEST_NOT_JSON','REQUEST_INVALID_SCOPE',
    'MODEL_CONTEXT_BUDGET_EXCEEDED','MODEL_OUTPUT_NOT_JSON_OBJECT',
    'MODEL_OUTPUT_MISSING','MODEL_OUTPUT_TRUNCATED','MODEL_PROVIDER_RESPONSE_INVALID',
    'MODEL_PROVIDER_RESPONSE_TOO_LARGE','MODEL_PROVIDER_TIMEOUT',
    'MODEL_PLAN_INVALID','MODEL_TOOL_BUDGET_EXCEEDED','UNAUTHORIZED_TOOL',
    'MINT_NOT_PRESENT_IN_USER_GOAL','DUPLICATE_TOOL_REQUEST',
    'DISCOVERY_INPUT_INVALID_OR_STALE','DISCOVERY_CANDIDATE_INVALID',
    'DISCOVERY_MODEL_SELECTION_INVALID','DISCOVERY_MODEL_MINT_NOT_IN_SHORTLIST',
  ]).has(message) ? message : 'RESEARCH_FAILED';
}

export function createResearchHttpServer({
  model = null, readEconomic = null, loadKnowledge = null, sourceReadiness = null,
  mintReadiness = null,
  allowedOrigins = DEFAULT_ORIGINS, maxTasks = 8,
} = {}) {
  if (!Array.isArray(allowedOrigins) || !allowedOrigins.length ||
      allowedOrigins.some(x => typeof x !== 'string' || !/^https?:\/\/[^/]+$/.test(x)) ||
      !Number.isInteger(maxTasks) || maxTasks < 1 || maxTasks > 100 ||
      (sourceReadiness !== null && typeof sourceReadiness !== 'function') ||
      (mintReadiness !== null && typeof mintReadiness !== 'function')) {
    throw new Error('RESEARCH_SERVER_CONFIGURATION_INVALID');
  }
  const origins = new Set(allowedOrigins);
  let tasksStarted = 0, busy = false;
  // Unlike function-presence checks, production startup explicitly probes the
  // existing SQLite archive. A broken path or missing schema must never enable
  // a paid-model request and then fail only after billing begins.
  const readiness = async () => {
    if (typeof model !== 'function' || typeof readEconomic !== 'function')
      return { ready: false, archiveStatus: 'MODEL_OR_READER_NOT_CONFIGURED' };
    if (!sourceReadiness)
      return { ready: true, archiveStatus: 'ARCHIVE_PREFLIGHT_NOT_CONFIGURED_FOR_INJECTED_READER' };
    try {
      const result = await sourceReadiness();
      return {
        ready: result?.ready === true,
        archiveStatus: typeof result?.status === 'string' ? result.status.slice(0, 80) : 'ARCHIVE_READINESS_UNKNOWN',
      };
    } catch {
      return { ready: false, archiveStatus: 'ARCHIVE_READINESS_PROBE_FAILED' };
    }
  };
  const server = createServer(async (req, res) => {
    const remote = req.socket.remoteAddress || '';
    if (!['127.0.0.1','::1','::ffff:127.0.0.1'].includes(remote)) {
      json(res, 403, { error:'LOOPBACK_ONLY' });return;
    }
    const origin = String(req.headers.origin || '');
    const localPort = server.address()?.port;
    const host = String(req.headers.host || '');
    if (!localPort || !['127.0.0.1:'+localPort,'localhost:'+localPort].includes(host)) {
      json(res, 403, { error:'LOCAL_HOST_REQUIRED' });return;
    }
    if (origin && origins.has(origin)) {
      res.setHeader('Access-Control-Allow-Origin', origin);
      res.setHeader('Access-Control-Allow-Methods', 'POST, GET, OPTIONS');
      res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
      res.setHeader('Vary','Origin');
    }
    if (req.url === '/health' && req.method === 'GET') {
      const status = await readiness();
      json(res, 200, { service:'blix-research-readonly', ...status,
        dataSource:'EXISTING_LOCAL_SQLITE_ONLY',
        providerEnabled:typeof model === 'function',
        remainingTasks:Math.max(0,maxTasks-tasksStarted), busy });
      return;
    }
    if (!['/research','/discover'].includes(req.url) || !['OPTIONS','POST'].includes(req.method)) {
      json(res, 404, {error:'ROUTE_NOT_FOUND'});return;
    }
    if (!origin || !origins.has(origin)) {
      json(res, 403, {error:'ORIGIN_NOT_AUTHORIZED'});return;
    }
    if (req.method === 'OPTIONS') {res.writeHead(204);res.end();return;}
    if (!(req.headers['content-type'] || '').toLowerCase().startsWith('application/json')) {
      json(res,415,{error:'JSON_ONLY'});return;
    }
    const source = await readiness();
    if (!source.ready) {
      json(res,503,{error:'RESEARCH_NOT_CONFIGURED',
        ...(sourceReadiness ? {archiveStatus:source.archiveStatus} : {})});return;
    }
    if (busy) {json(res,429,{error:'RESEARCH_BUSY'});return;}
    if (tasksStarted >= maxTasks) {json(res,429,{error:'TASK_BUDGET_EXHAUSTED'});return;}
    let input;
    try { input = await readBody(req, req.url); }
    catch (error) {json(res,400,{error:errorCode(error)});return;}
    // A manually specified Mint may be absent from this PARTICULAR local archive.
    // Stop before consuming the model budget; do not call it to invent missing facts.
    if (req.url === '/research' && mintReadiness) {
      let archive;
      try { archive = await mintReadiness(input.mint); }
      catch { json(res,503,{error:'MINT_ARCHIVE_PREFLIGHT_FAILED'});return; }
      if (archive?.ready !== true) {
        json(res,422,{error:'MINT_LOCAL_EVIDENCE_UNAVAILABLE',mint:input.mint,
          archiveStatus:typeof archive?.status === 'string'
            ? archive.status.slice(0,80) : 'MINT_ARCHIVE_PREFLIGHT_UNAVAILABLE'});
        return;
      }
    }
    busy = true;tasksStarted++;
    try {
      const result = req.url === '/discover'
        ? await discoverPulseInvestigation({
          input, model, readEconomic, loadKnowledge, runResearch:runAiResearchTask,
        })
        : await runAiResearchTask({ ...input, model, readEconomic, loadKnowledge });
      const output=req.url==='/discover'
        ? {
          ...result,
          ...(result.investigation&&result.discovery?.selectedMint
            ? { investigation:{
              ...result.investigation,
              continuation:summarizeInvestigationContinuation({
                mint:result.discovery.selectedMint,investigation:result.investigation,
              }),
            } } : {}),
        }
        : { ...result, continuation:summarizeInvestigationContinuation({mint:input.mint,investigation:result}) };
      json(res, 200, {
        ...output, sourceMode:'LOCAL_SQLITE_ONLY',
        modelMode:'OPT_IN_SERVER_MODEL_API',
        verifiedMarketOpportunity:false, liveExecutionValidated:false,
      });
    } catch (error) {
      json(res, 422, {error:errorCode(error)});
    } finally {busy=false;}
  });
  return server;
}
