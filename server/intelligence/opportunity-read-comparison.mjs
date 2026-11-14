// Bounded, offline A/B audit of two already-produced Blix Pulse investigation receipts.
// It does NOT discover new Mints, call models/providers, simulate fills or score alpha.
// The equal-population requirement prevents wallet-led enrichment from silently
// broadening the baseline's observed Mint universe.
import { validatePulseDiscoveryInput } from './pulse-discovery.mjs';
import { evaluatePaperFollowabilityCases } from './followability-replay.mjs';

const MINT = /^[1-9A-HJ-NP-Za-km-z]{32,44}$/;
const isMs = n => Number.isSafeInteger(n) && n >= 0;

export function compareObservedInvestigations({
  snapshot, baseline, enhanced, supportingEvidence = [], paperReceipts = [],
} = {}) {
  if (!snapshot || !isMs(snapshot.browserRecordedAtMs)) throw Error('A_B_SNAPSHOT_MISSING');
  // Validate against the frozen client submission time, NOT Date.now().
  // Historical snapshots are replayable, but browser time is not provider first-available time.
  const clean = validatePulseDiscoveryInput(snapshot, snapshot.browserRecordedAtMs);
  const population = new Set(clean.candidates.map(x => x.mint));
  function validateRun(label, run) {
    const discovery = run?.discovery;
    if (!discovery || discovery.sourceRecordedAtMs !== clean.sourceRecordedAtMs ||
      discovery.marketCoverage !== clean.marketCoverage ||
      discovery.candidateCount !== clean.candidates.length ||
      !(discovery.selectedMint === null || population.has(discovery.selectedMint))) {
      throw Error('A_B_' + label + '_POPULATION_OR_TIME_MISMATCH');
    }
    return {
      selectedMint: discovery.selectedMint,
      reason: typeof discovery.reason === 'string' ? discovery.reason.slice(0,500) : '',
      investigationStatus: run.investigation?.status ?? null,
      originalSelectionVerified: discovery.modelSelectionVerified === true,
      verifiedMarketOpportunity: false,
    };
  }
  const a = validateRun('BASELINE',baseline), b = validateRun('ENHANCED',enhanced);
  if (!Array.isArray(supportingEvidence) || supportingEvidence.length > 100 ||
      !Array.isArray(paperReceipts) || paperReceipts.length > 200) throw Error('A_B_AUDIT_INPUT_LIMIT');
  const seen = new Set();
  let firstAvailableKnown = 0, firstAvailableUnknown = 0;
  for (const e of supportingEvidence) {
    if (!e || !MINT.test(e.mint || '') || !population.has(e.mint) ||
        typeof e.source !== 'string' || !e.source || e.source.length > 120 ||
        typeof e.kind !== 'string' || !e.kind || e.kind.length > 120) {
      throw Error('A_B_EVIDENCE_SCOPE_INVALID');
    }
    if (e.firstAvailableAtMs == null) {
      firstAvailableUnknown++;
      continue;
    }
    if (!isMs(e.firstAvailableAtMs)) throw Error('A_B_EVIDENCE_TIME_INVALID');
    if (e.firstAvailableAtMs > clean.sourceRecordedAtMs)
      throw Error('A_B_LOOKAHEAD_EVIDENCE_AFTER_FROZEN_SNAPSHOT');
    firstAvailableKnown++;
    if (e.id) {
      if (typeof e.id !== 'string' || e.id.length > 160 || seen.has(e.id))
        throw Error('A_B_EVIDENCE_ID_DUPLICATE_OR_INVALID');
      seen.add(e.id);
    }
  }
  for (const receipt of paperReceipts) {
    if (!receipt || !population.has(receipt.mint)) throw Error('A_B_PAPER_MINT_OUTSIDE_POPULATION');
  }
  const paper = evaluatePaperFollowabilityCases(paperReceipts);
  const paperStatusCounts = paper.counts;
  return {
    schemaVersion: '0.1', kind: 'OFFLINE_SAME_SNAPSHOT_A_B_INVESTIGATION_AUDIT',
    input: {
      observedMintCount: clean.candidates.length, snapshotRecordedAtMs: clean.sourceRecordedAtMs,
      marketCoverage: clean.marketCoverage, sourceFreshness: clean.sourceFreshness,
      comparisonPopulation: 'SAME_SUBMITTED_PULSE_MINTS_NOT_MARKET_UNIVERSE',
    },
    baseline: a, enhanced: b,
    selection: {
      changed: a.selectedMint !== b.selectedMint,
      sameSnapshotCandidatePopulation: true,
      newMintDiscoveredOutsideOriginalPulse: false,
      modelBenefitEstablished: false,
    },
    supportingEvidence: {
      observationCount: supportingEvidence.length, claimedAvailableBySnapshot: firstAvailableKnown,
      firstAvailableUnknown, availabilityIndependentlyVerified: false,
      note: 'User-supplied evidence timestamps are not independent proof; unknown/late sources cannot support a point-in-time improvement claim.',
    },
    paperFollowability: {
      receiptCount: paper.inputCount, statusCounts: paperStatusCounts,
      simulatedCasesNotLive: paperStatusCounts.PAPER_SCENARIO_CALCULATED_NOT_LIVE || 0,
      outOfSamplePerformance: paper.outOfSamplePerformance, liveTradeResults: paper.liveTradeResults,
    },
    verdict: 'ONLY_SELECTION_DIFFERENCE_MEASURED_NOT_REAL_MARKET_ADVANTAGE',
    unresolved: [
      'Browser snapshot only covers at most 12 submitted Blix Pulse Mints; no market-wide recall measured.',
      'Client-recorded observation time is not provider first-available or follower-visible signal time.',
      'Different model selections are not an accuracy, alpha or execution-quality improvement.',
      'Actual independent wallet controllers, complete historical coverage and real entry/exit quotes remain unverified.',
      'Enrichment found outside the frozen population requires a separate wallet-led discovery evaluation, not this matched-universe A/B.',
    ],
    permissions: {readonly:true, noModelCalls:true, noProviderCalls:true, noTradeExecution:true},
  };
}
