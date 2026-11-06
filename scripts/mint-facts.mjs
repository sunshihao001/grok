// Explicit opt-in to query an already running local Blix. Not a server start command.
import { runCapability } from "../server/intelligence/index.mjs";
import { makeLocalBlixReader } from "../server/intelligence/local-reader.mjs";

const mint = process.argv[2] || "";
const port = Number(process.env.RADAR_PORT || 4420);
try {
  const result = await runCapability("mint-facts", { mint, read: makeLocalBlixReader({ port }) });
  process.stdout.write(JSON.stringify(result, null, 2) + "\n");
  if (result.status === "UNAVAILABLE" || result.status === "SOURCE_MISMATCH") process.exitCode = 2;
} catch (error) {
  process.stderr.write("Mint intelligence failed: " + String(error.message || error) + "\n");
  process.exitCode = 2;
}
