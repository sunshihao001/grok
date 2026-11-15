// One optional professional-capability layer above the existing Blix market product.
// No market, wallet, signing, provider or background module is imported at startup.
const ENTRIES = Object.freeze({
  "mint-facts": Object.freeze({
    id: "mint-facts",
    title: "Mint facts from Blix",
    readonly: true,
    load: () => import("./mint-facts.mjs"),
  }),
  "mint-economic-evidence": Object.freeze({
    id: "mint-economic-evidence",
    title: "Captured local Mint economic evidence",
    readonly: true,
    load: () => import("./mint-economic-evidence.mjs"),
  }),
});

export function listCapabilities() {
  return Object.values(ENTRIES).map(({ id, title, readonly }) => ({ id, title, readonly }));
}

export async function runCapability(id, options) {
  const entry = Object.hasOwn(ENTRIES, id) ? ENTRIES[id] : null;
  if (!entry) throw new Error("Unknown or unauthorized intelligence capability");
  const module = await entry.load();
  if (module.manifest?.id !== entry.id || module.manifest?.readonly !== true || typeof module.run !== "function") {
    throw new Error("Intelligence capability contract mismatch");
  }
  return module.run(options);
}
