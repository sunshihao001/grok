"""Never infer historical tradability from event/block timestamps alone."""
import copy
import unittest

from solana_meme_os.asof_audit import audit_event, audit_batch


class AsOfAuditTests(unittest.TestCase):
    def setUp(self):
        self.record={
            "event_id":"SYNTHETIC-1",
            "source_ref":"synthetic:fixture",
            "capture_mode":"live_recorded",
            "event_at_utc":"2026-10-01T00:00:00Z",
            "provider_received_at_utc":"2026-10-01T00:00:03Z",
            "parsed_at_utc":"2026-10-01T00:00:05Z",
            "feature_available_at_utc":"2026-10-01T00:00:06Z",
            "decision_cutoff_utc":"2026-10-01T00:00:08Z",
        }

    def test_replay_timestamp_is_only_syntactically_eligible(self):
        value=audit_event(self.record)
        self.assertEqual(value["status"],"TIME_CUTOFF_ELIGIBLE_UNVERIFIED")
        self.assertFalse(value["eligible_as_decision_feature"])\n        self.assertTrue(value["time_order_consistent"])
        self.assertFalse(audit_batch([self.record])["external_source_authenticated"])

    def test_provider_received_after_decision_cannot_leak(self):
        modified=copy.deepcopy(self.record)
        modified["provider_received_at_utc"]="2026-10-01T00:00:10Z"
        modified["parsed_at_utc"]="2026-10-01T00:00:11Z"
        modified["feature_available_at_utc"]="2026-10-01T00:00:12Z"
        self.assertEqual(audit_event(modified)["status"],"POST_DECISION_UNAVAILABLE")

    def test_historical_backfill_cannot_prove_as_of_availability(self):
        modified=copy.deepcopy(self.record)
        modified["capture_mode"]="historical_backfill"
        self.assertEqual(audit_event(modified)["status"],"NO_CONTEMPORANEOUS_AVAILABILITY_PROOF")

    def test_null_or_untimed_is_not_zero(self):
        modified=copy.deepcopy(self.record)
        modified["provider_received_at_utc"]=None
        with self.assertRaisesRegex(ValueError,"timezone-aware"):
            audit_event(modified)

    def test_inconsistent_order_is_rejected(self):
        modified=copy.deepcopy(self.record)
        modified["parsed_at_utc"]="2026-09-30T23:59:59Z"
        self.assertEqual(audit_event(modified)["status"],"INCONSISTENT_TIME_ORDER")

    def test_missing_source_fails(self):
        modified=copy.deepcopy(self.record)
        modified["source_ref"]=""
        with self.assertRaisesRegex(ValueError,"source_ref"):
            audit_event(modified)

    def test_naive_datetime_fails(self):
        modified=copy.deepcopy(self.record)
        modified["decision_cutoff_utc"]="2026-10-01T00:00:08"
        with self.assertRaisesRegex(ValueError,"timezone-aware"):
            audit_event(modified)

    def test_offset_timezone_normalized(self):
        modified=copy.deepcopy(self.record)
        modified["decision_cutoff_utc"]="2026-10-01T09:00:08+09:00"
        self.assertEqual(audit_event(modified)["status"],"TIME_CUTOFF_ELIGIBLE_UNVERIFIED")\n        self.assertFalse(audit_event(modified)["eligible_as_decision_feature"])

    def test_null_blocktime_is_missing_not_fabricated(self):\n        modified=copy.deepcopy(self.record)\n        modified["event_at_utc"]=None\n        self.assertEqual(audit_event(modified)["status"],"EVENT_TIME_UNKNOWN")\n\n    def test_duplicate_event_id_fails(self):
        with self.assertRaisesRegex(ValueError,"duplicate event_id"):
            audit_batch([self.record,self.record])

    def test_invalid_future_receive_event_is_rejected(self):
        modified=copy.deepcopy(self.record)
        modified["event_at_utc"]="2026-10-01T00:00:12Z"
        self.assertEqual(audit_event(modified)["status"],"INCONSISTENT_TIME_ORDER")

    def test_batch_never_claims_market_or_trade_validity(self):
        value=audit_batch([self.record])
        self.assertFalse(value["market_edge_proven"])
        self.assertFalse(value["live_trade_authorized"])


if __name__=="__main__":
    unittest.main()
