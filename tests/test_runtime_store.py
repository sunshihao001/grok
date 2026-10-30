"""Local handoff bus tests: durable, role-scoped, idempotent and fail-closed."""
from __future__ import annotations
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from solana_meme_os.runtime_store import LocalHandoffStore
from solana_meme_os.knowledge_system import ROOT

FIXTURE=ROOT/"fixtures/bot-handoff-brief.fixture.json"


class LocalRuntimeStoreTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.db=Path(self.tmp.name)/"runtime/handoffs.sqlite3"
        self.store=LocalHandoffStore(self.db)
        self.packet=json.loads(FIXTURE.read_text(encoding="utf-8"))

    def test_init_is_explicit_and_durable(self):
        with self.assertRaises(FileNotFoundError):
            self.store.inspect()
        self.assertEqual(self.store.init()["status"],"INITIALIZED")
        self.assertEqual(self.store.init()["status"],"INITIALIZED")
        self.assertEqual(LocalHandoffStore(self.db).inspect()["packets"],0)

    def test_fixture_is_rejected_from_live_market_claim(self):
        self.store.init()
        result=self.store.submit(self.packet)
        self.assertFalse(result["authenticated_market_evidence"])
        self.assertEqual(self.store.inspect()["deliveries_by_status"]["PENDING"],3)

    def test_exactly_once_submission_per_packet_id(self):
        self.store.init()
        first=self.store.submit(self.packet)
        second=self.store.submit(copy.deepcopy(self.packet))
        self.assertEqual(first["body_sha256"],second["body_sha256"])
        self.assertEqual(second["status"],"ALREADY_SUBMITTED")
        modified=copy.deepcopy(self.packet)
        modified["next_action"]="different task description"
        with self.assertRaisesRegex(ValueError,"packet_id conflict"):
            self.store.submit(modified)
        self.assertEqual(self.store.inspect()["packets"],1)

    def test_each_recipient_can_claim_once_independently(self):
        self.store.init()
        self.store.submit(self.packet)
        a=self.store.claim("B02")
        self.assertEqual(a["status"],"CLAIMED")
        self.assertEqual(a["packet_id"],self.packet["packet_id"])
        self.assertEqual(self.store.claim("B02")["status"],"EMPTY")
        self.assertEqual(self.store.claim("B03")["status"],"CLAIMED")
        self.assertEqual(self.store.claim("B05")["status"],"CLAIMED")
        self.assertEqual(LocalHandoffStore(self.db).inspect()["deliveries_by_status"]["CLAIMED"],3)

    def test_complete_requires_output_digest_and_claim(self):
        self.store.init()
        self.store.submit(self.packet)
        digest=hashlib.sha256(b"synthetic result").hexdigest()
        with self.assertRaisesRegex(ValueError,"CLAIMED"):
            self.store.complete(self.packet["packet_id"],"B02",digest)
        self.store.claim("B02")
        with self.assertRaisesRegex(ValueError,"64 lowercase"):
            self.store.complete(self.packet["packet_id"],"B02","not-a-hash")
        done=self.store.complete(self.packet["packet_id"],"B02",digest)
        self.assertEqual(done["status"],"COMPLETED")
        self.assertEqual(self.store.complete(self.packet["packet_id"],"B02",digest)["status"],
                         "ALREADY_COMPLETED")
        self.assertEqual(self.store.inspect(self.packet["packet_id"])["deliveries"][0]["status"],"COMPLETED")

    def test_block_requires_explicit_requeue_and_preserves_audit(self):
        self.store.init()
        self.store.submit(self.packet)
        self.store.claim("B02")
        self.assertEqual(self.store.block(self.packet["packet_id"],"B02","provider unavailable")["status"],
                         "BLOCKED")
        self.assertEqual(self.store.claim("B02")["status"],"EMPTY")
        self.store.requeue(self.packet["packet_id"],"B02","operator reviewed provider")
        self.assertEqual(self.store.claim("B02")["status"],"CLAIMED")
        self.assertEqual(self.store.inspect()["audit_events"],5)

    def test_cannot_requeue_claimed_or_pending(self):
        self.store.init()
        self.store.submit(self.packet)
        with self.assertRaisesRegex(ValueError,"only BLOCKED"):
            self.store.requeue(self.packet["packet_id"],"B02","x")
        self.store.claim("B02")
        with self.assertRaisesRegex(ValueError,"only BLOCKED"):
            self.store.requeue(self.packet["packet_id"],"B02","x")

    def test_monitor_recipient_is_prohibited(self):
        self.store.init()
        p=copy.deepcopy(self.packet)
        p["recipient_bot_ids"]=["B07"]
        with self.assertRaisesRegex(ValueError,"B07|Monitor|monitor|recipient"):
            self.store.submit(p)

    def test_monitor_bot_cannot_claim(self):
        self.store.init()
        with self.assertRaisesRegex(ValueError,"B01-B06"):
            self.store.claim("B07")

    def test_role_mismatch_is_rejected_by_existing_handoff_validator(self):
        self.store.init()
        p=copy.deepcopy(self.packet)
        p["producer_bot_id"]="B04"
        with self.assertRaisesRegex(ValueError,"wrong Bot"):
            self.store.submit(p)

    def test_cannot_claim_real_observation_without_explicit_operator_flag(self):
        self.store.init()
        p=copy.deepcopy(self.packet)
        p["mode"]="real_observation"
        with self.assertRaisesRegex(ValueError,"--allow-real-observation"):
            self.store.submit(p)

    def test_packet_size_bounded(self):
        self.store.init()
        p=copy.deepcopy(self.packet)
        p["population"]="X"*(1024*1024)
        with self.assertRaisesRegex(ValueError,"1 MiB"):
            self.store.submit(p)

    def test_does_not_execute_packet_as_shell_command(self):
        self.store.init()
        self.packet["next_action"]="rm -rf /workspace"
        self.store.submit(self.packet)
        result=self.store.claim("B02")
        self.assertEqual(result["packet"]["next_action"],"rm -rf /workspace")
        self.assertFalse(result["authenticated_actor"])
        self.assertFalse(self.store.inspect()["market_evidence_verified"])

    def test_claim_is_serialized_across_threads(self):
        from concurrent.futures import ThreadPoolExecutor
        self.store.init()
        self.store.submit(self.packet)
        with ThreadPoolExecutor(max_workers=6) as pool:
            claims=list(pool.map(lambda _: LocalHandoffStore(self.db).claim("B02"), range(6)))
        self.assertEqual(sum(x["status"]=="CLAIMED" for x in claims),1)
        self.assertEqual(sum(x["status"]=="EMPTY" for x in claims),5)

    def test_complete_cli_calculates_existing_file_digest(self):
        import os
        env=os.environ.copy()
        env["PYTHONPATH"]=str(ROOT/"src")
        self.store.init()
        self.store.submit(self.packet)
        self.store.claim("B02")
        path=Path(self.tmp.name)/"result.json"
        path.write_text('{"status":"synthetic"}',encoding="utf-8")
        cmd=[sys.executable,"-m","solana_meme_os.runtime_store","--db",str(self.db),
             "complete","--bot","B02","--packet-id",self.packet["packet_id"],
             "--result-file",str(path)]
        r=subprocess.run(cmd,cwd=ROOT,env=env,text=True,capture_output=True)
        self.assertEqual(r.returncode,0,r.stderr)
        self.assertEqual(json.loads(r.stdout)["status"],"COMPLETED")
        expected=hashlib.sha256(path.read_bytes()).hexdigest()
        deliveries=self.store.inspect(self.packet["packet_id"])["deliveries"]
        self.assertEqual(deliveries[0]["result_sha256"],expected)

    def test_cli_cycle_works_after_restart(self):
        root=self.db
        cmd=[sys.executable,"-m","solana_meme_os.runtime_store","--db",str(root)]
        import os
        env=os.environ.copy()
        env["PYTHONPATH"]=str(ROOT/"src")
        r=subprocess.run(cmd+["init"],cwd=ROOT,env=env,capture_output=True,text=True)
        self.assertEqual(r.returncode,0,r.stderr)
        r=subprocess.run(cmd+["submit","--input",str(FIXTURE)],cwd=ROOT,env=env,capture_output=True,text=True)
        self.assertEqual(r.returncode,0,r.stderr)
        r=subprocess.run(cmd+["claim","--bot","B02"],cwd=ROOT,env=env,capture_output=True,text=True)
        self.assertEqual(r.returncode,0,r.stderr)
        self.assertEqual(json.loads(r.stdout)["status"],"CLAIMED")


if __name__=="__main__":
    unittest.main()
