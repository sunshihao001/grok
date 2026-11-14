#!/usr/bin/env node
// Explicit local opt-in. Never starts the original Blix server or scans the
// network automatically; no API requests occur until a person runs a task.
import { makeChatCompletionModel } from '../server/intelligence/chat-completion-model.mjs';
import { createResearchHttpServer } from '../server/intelligence/research-http.mjs';
import { makeOfflineEconomicReader, probeExistingEconomicArchive } from '../server/intelligence/offline-economic-reader.mjs';
import { makeLocalKnowledgeLoader } from '../server/intelligence/local-knowledge-loader.mjs';

const env = process.env;
const port = Number(env.BLIX_AI_PORT || '4547');
const maxTasks = Number(env.BLIX_AI_MAX_TASKS || '8');
if (!Number.isInteger(port) || port < 1024 || port > 65535 ||
    !Number.isInteger(maxTasks) || maxTasks < 1 || maxTasks > 100) {
  console.error('Invalid local research port or maximum research tasks');
  process.exit(2);
}
const enabled = env.BLIX_AI_ENABLE_PAID_MODELS === 'I_ACCEPT_MODEL_API_CHARGES';
const model = enabled && env.BLIX_AI_API_KEY && env.BLIX_AI_MODEL
  ? makeChatCompletionModel({
    apiKey: env.BLIX_AI_API_KEY, model:env.BLIX_AI_MODEL,
    url:env.BLIX_AI_CHAT_URL || 'https://api.openai.com/v1/chat/completions',
  }) : null;
const readEconomic = env.BLIX_AI_DB_PATH
  ? makeOfflineEconomicReader({ databasePath:env.BLIX_AI_DB_PATH }) : null;
const origins = (env.BLIX_AI_ALLOWED_ORIGINS ||
  'http://127.0.0.1:4420,http://localhost:4420,http://127.0.0.1:5173,http://localhost:5173')
  .split(',').map(x=>x.trim()).filter(Boolean);
const server = createResearchHttpServer({
  model, readEconomic, allowedOrigins:origins, maxTasks,
  sourceReadiness: env.BLIX_AI_DB_PATH
    ? () => probeExistingEconomicArchive({ databasePath:env.BLIX_AI_DB_PATH }) : null,
  loadKnowledge:makeLocalKnowledgeLoader(),
});
server.listen(port,'127.0.0.1',()=>{
  // Deliberately omit provider URL, DB paths, model credentials and user input.
  console.info('Blix read-only AI research service on local port '+port+
    ' | model:'+Boolean(model)+' archive:'+Boolean(readEconomic)+
    ' | explicit request budget:'+maxTasks);
});
