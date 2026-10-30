"""SQLite handoff inbox for Grok's shared-computer, read-only research workflows.

It persists and serializes work *requests*. It does not execute tools, authenticate a
Bot, verify market facts, or grant access to the B07 monitoring runtime.
"""
from __future__ import annotations

import argparse
from contextlib import closing
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import sqlite3
import sys
from typing import Any

from .bot_knowledge import validate_handoff

DEFAULT_DB = Path(".runtime/research-handoff.sqlite3")
RESEARCH_RECIPIENTS = frozenset(f"B{i:02d}" for i in range(1, 7))
SHA256 = re.compile(r"^[a-f0-9]{64}$")
MAX_PACKET_BYTES = 1024 * 1024


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _canonical(packet: dict[str, Any]) -> bytes:
    return json.dumps(packet, sort_keys=True, ensure_ascii=False,
                      separators=(",", ":"), allow_nan=False).encode("utf-8")


class LocalHandoffStore:
    """Task-scoped, durable inbox: submit -> claim -> complete/block -> review/requeue."""

    def __init__(self, db_path: Path | str = DEFAULT_DB):
        self.db_path = Path(db_path)

    def _connect(self, create: bool = False) -> sqlite3.Connection:
        if not create and not self.db_path.is_file():
            raise FileNotFoundError("handoff database not initialized; run init")
        if create:
            self.db_path.parent.mkdir(parents=True, exist_ok=True)
        db = sqlite3.connect(str(self.db_path), timeout=5.0, isolation_level=None)
        db.row_factory = sqlite3.Row
        db.execute("PRAGMA foreign_keys=ON")
        db.execute("PRAGMA busy_timeout=5000")
        return db

    def init(self) -> dict[str, Any]:
        with closing(self._connect(create=True)) as db:
            db.execute("PRAGMA journal_mode=WAL")
            db.executescript("""
                CREATE TABLE IF NOT EXISTS packets (
                  packet_id TEXT PRIMARY KEY,
                  task_id TEXT NOT NULL,
                  producer_bot_id TEXT NOT NULL,
                  packet_type TEXT NOT NULL,
                  mode TEXT NOT NULL,
                  body_json TEXT NOT NULL,
                  body_sha256 TEXT NOT NULL,
                  recorded_at_utc TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS deliveries (
                  packet_id TEXT NOT NULL REFERENCES packets(packet_id),
                  recipient_bot_id TEXT NOT NULL,
                  status TEXT NOT NULL CHECK(status IN ('PENDING','CLAIMED','COMPLETED','BLOCKED')),
                  claimed_at_utc TEXT,
                  finished_at_utc TEXT,
                  result_sha256 TEXT,
                  error_reason TEXT,
                  attempts INTEGER NOT NULL DEFAULT 0,
                  PRIMARY KEY(packet_id, recipient_bot_id)
                );
                CREATE INDEX IF NOT EXISTS deliveries_pending
                  ON deliveries(recipient_bot_id, status, packet_id);
                CREATE TABLE IF NOT EXISTS audit_events (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  packet_id TEXT NOT NULL,
                  recipient_bot_id TEXT,
                  action TEXT NOT NULL,
                  recorded_at_utc TEXT NOT NULL,
                  details_json TEXT NOT NULL
                );
            """)
        return {"status":"INITIALIZED","db_path":str(self.db_path),
                "trading_authorized":False,"grok_bot_authenticated":False}

    @staticmethod
    def _audit(db: sqlite3.Connection, packet_id: str, bot_id: str | None,
               action: str, details: dict[str, Any]) -> None:
        db.execute(
            "INSERT INTO audit_events(packet_id, recipient_bot_id, action, recorded_at_utc, details_json) VALUES (?,?,?,?,?)",
            (packet_id, bot_id, action, _now(),
             json.dumps(details, sort_keys=True, ensure_ascii=False)))

    def submit(self, packet: dict[str, Any],
               allow_real_observation: bool = False) -> dict[str, Any]:
        # Reuse existing domain, source, gate and role checks rather than create a competing contract.
        validate_handoff(packet)
        if packet["mode"] == "real_observation" and not allow_real_observation:
            raise ValueError("real observations require explicit --allow-real-observation; metadata remains unverified")
        if packet["packet_type"] == "monitor_observation" or "B07" in packet["recipient_bot_ids"]:
            raise ValueError("B07 monitoring data and releases cannot be dispatched over the research inbox")
        recipients = packet["recipient_bot_ids"]
        if not recipients or set(recipients) - RESEARCH_RECIPIENTS:
            raise ValueError("at least one B01-B06 research recipient is required")
        body = _canonical(packet)
        if len(body) > MAX_PACKET_BYTES:
            raise ValueError("packet exceeds bounded 1 MiB payload")
        digest = hashlib.sha256(body).hexdigest()
        packet_id = packet["packet_id"]
        with closing(self._connect()) as db, db:
            db.execute("BEGIN IMMEDIATE")
            found = db.execute("SELECT body_sha256 FROM packets WHERE packet_id=?", (packet_id,)).fetchone()
            if found:
                if found["body_sha256"] != digest:
                    raise ValueError("packet_id conflict: same ID but different content")
                return {"status":"ALREADY_SUBMITTED", "packet_id":packet_id,
                        "body_sha256":digest,"recipients":recipients,
                        "authenticated_market_evidence":False}
            db.execute(
                """INSERT INTO packets(packet_id,task_id,producer_bot_id,packet_type,mode,body_json,body_sha256,recorded_at_utc)
                   VALUES(?,?,?,?,?,?,?,?)""",
                (packet_id, packet["task_id"], packet["producer_bot_id"], packet["packet_type"],
                 packet["mode"], body.decode("utf-8"), digest, _now()))
            for recipient in recipients:
                db.execute(
                    "INSERT INTO deliveries(packet_id,recipient_bot_id,status) VALUES (?,?,?)",
                    (packet_id, recipient, "PENDING"))
            self._audit(db, packet_id, None, "SUBMITTED", {"sha256":digest,"recipients":recipients})
        return {"status":"SUBMITTED", "packet_id":packet_id,
                "body_sha256":digest,"recipients":recipients,
                "authenticated_market_evidence":False}

    @staticmethod
    def _check_bot(bot_id: str) -> None:
        if bot_id not in RESEARCH_RECIPIENTS:
            raise ValueError("research inbox only supports B01-B06 as recipients")

    def claim(self, bot_id: str) -> dict[str, Any]:
        self._check_bot(bot_id)
        with closing(self._connect()) as db, db:
            db.execute("BEGIN IMMEDIATE")
            row = db.execute(
                """SELECT p.packet_id,p.body_json,p.body_sha256
                   FROM deliveries d JOIN packets p ON d.packet_id=p.packet_id
                   WHERE d.recipient_bot_id=? AND d.status='PENDING'
                   ORDER BY p.recorded_at_utc,p.packet_id LIMIT 1""",
                (bot_id,)).fetchone()
            if not row:
                return {"status":"EMPTY","recipient_bot_id":bot_id}
            changed = db.execute(
                """UPDATE deliveries SET status='CLAIMED',claimed_at_utc=?,attempts=attempts+1
                   WHERE packet_id=? AND recipient_bot_id=? AND status='PENDING'""",
                (_now(), row["packet_id"], bot_id)).rowcount
            if changed != 1:
                raise RuntimeError("failed transactional claim")
            self._audit(db,row["packet_id"],bot_id,"CLAIMED",{})
        return {"status":"CLAIMED","recipient_bot_id":bot_id,
                "packet_id":row["packet_id"],"body_sha256":row["body_sha256"],
                "packet":json.loads(row["body_json"]),
                "authenticated_actor":False,
                "next_step":"Read and independently verify the packet; this command never runs its requested tool."}

    def _transition(self, packet_id: str, bot_id: str, destination: str,
                    result_sha256: str | None = None, reason: str | None = None) -> dict[str, Any]:
        self._check_bot(bot_id)
        if destination == "COMPLETED":
            if not isinstance(result_sha256, str) or not SHA256.fullmatch(result_sha256):
                raise ValueError("completion requires 64 lowercase-hex SHA256 of separately saved result")
        elif destination == "BLOCKED":
            if not isinstance(reason, str) or not reason.strip() or len(reason) > 500:
                raise ValueError("blocking requires a short non-secret reason")
        else:
            raise ValueError("unsupported delivery transition")
        with closing(self._connect()) as db, db:
            db.execute("BEGIN IMMEDIATE")
            row = db.execute(
                "SELECT status,result_sha256 FROM deliveries WHERE packet_id=? AND recipient_bot_id=?",
                (packet_id, bot_id)).fetchone()
            if row is None:
                raise ValueError("delivery not found")
            if row["status"] == destination and (
                destination != "COMPLETED" or row["result_sha256"] == result_sha256
            ):
                return {"status":"ALREADY_"+destination, "packet_id":packet_id,"recipient_bot_id":bot_id}
            if row["status"] != "CLAIMED":
                raise ValueError("delivery must be CLAIMED before complete/block")
            db.execute(
                """UPDATE deliveries SET status=?,finished_at_utc=?,result_sha256=?,error_reason=?
                   WHERE packet_id=? AND recipient_bot_id=?""",
                (destination,_now(),result_sha256,reason,packet_id,bot_id))
            self._audit(db,packet_id,bot_id,destination,
                        {"result_sha256":result_sha256} if destination=="COMPLETED" else
                        {"reason":reason})
        return {"status":destination,"packet_id":packet_id,"recipient_bot_id":bot_id}

    def complete(self, packet_id: str, bot_id: str, result_sha256: str) -> dict[str, Any]:
        return self._transition(packet_id,bot_id,"COMPLETED",result_sha256=result_sha256)

    def block(self, packet_id: str, bot_id: str, reason: str) -> dict[str, Any]:
        return self._transition(packet_id,bot_id,"BLOCKED",reason=reason)

    def requeue(self, packet_id: str, bot_id: str, reason: str) -> dict[str, Any]:
        """Explicit operator action only. There is no silent lease stealing or auto retry."""
        self._check_bot(bot_id)
        if not isinstance(reason,str) or not reason.strip() or len(reason)>500:
            raise ValueError("requeue requires a short reason")
        with closing(self._connect()) as db, db:
            db.execute("BEGIN IMMEDIATE")
            row=db.execute(
                "SELECT status FROM deliveries WHERE packet_id=? AND recipient_bot_id=?",
                (packet_id,bot_id)).fetchone()
            if row is None or row["status"] != "BLOCKED":
                raise ValueError("only BLOCKED deliveries can be manually requeued")
            db.execute(
                """UPDATE deliveries SET status='PENDING',claimed_at_utc=NULL,finished_at_utc=NULL,
                   result_sha256=NULL,error_reason=NULL WHERE packet_id=? AND recipient_bot_id=?""",
                (packet_id,bot_id))
            self._audit(db,packet_id,bot_id,"REQUEUED",{"reason":reason})
        return {"status":"PENDING","packet_id":packet_id,"recipient_bot_id":bot_id}

    def inspect(self, packet_id: str | None = None) -> dict[str, Any]:
        with closing(self._connect()) as db:
            if packet_id:
                row=db.execute(
                    "SELECT packet_id,task_id,producer_bot_id,packet_type,mode,body_sha256,recorded_at_utc FROM packets WHERE packet_id=?",
                    (packet_id,)).fetchone()
                if row is None:
                    raise ValueError("packet not found")
                deliveries=[dict(x) for x in db.execute(
                    "SELECT recipient_bot_id,status,claimed_at_utc,finished_at_utc,result_sha256,error_reason,attempts FROM deliveries WHERE packet_id=? ORDER BY recipient_bot_id",
                    (packet_id,))]
                return {"status":"LOCAL_QUEUE_ONLY","packet":dict(row),"deliveries":deliveries,
                        "grok_bot_authenticated":False, "market_evidence_verified":False}
            counts={row["status"]:row["n"] for row in db.execute(
                "SELECT status,COUNT(*) AS n FROM deliveries GROUP BY status")}
            total=db.execute("SELECT COUNT(*) FROM packets").fetchone()[0]
            events=db.execute("SELECT COUNT(*) FROM audit_events").fetchone()[0]
        return {"status":"LOCAL_QUEUE_ONLY","packets":total,
                "deliveries_by_status":counts,"audit_events":events,
                "grok_bot_authenticated":False,"market_evidence_verified":False}


def main() -> int:
    p=argparse.ArgumentParser(description="SQLite research handoff inbox (never executes Bot tools/trades)")
    p.add_argument("--db",type=Path,default=DEFAULT_DB)
    commands=p.add_subparsers(dest="command",required=True)
    commands.add_parser("init")
    submit=commands.add_parser("submit")
    submit.add_argument("--input",type=Path,required=True)
    submit.add_argument("--allow-real-observation",action="store_true")
    claim=commands.add_parser("claim")
    claim.add_argument("--bot",required=True)
    finish=commands.add_parser("complete")
    finish.add_argument("--bot",required=True)
    finish.add_argument("--packet-id",required=True)
    finish.add_argument("--result-sha256",required=True)
    block=commands.add_parser("block")
    block.add_argument("--bot",required=True)
    block.add_argument("--packet-id",required=True)
    block.add_argument("--reason",required=True)
    retry=commands.add_parser("requeue")
    retry.add_argument("--bot",required=True)
    retry.add_argument("--packet-id",required=True)
    retry.add_argument("--reason",required=True)
    status=commands.add_parser("status")
    status.add_argument("--packet-id")
    args=p.parse_args()
    store=LocalHandoffStore(args.db)
    try:
        if args.command=="init":
            result=store.init()
        elif args.command=="submit":
            content=args.input.read_bytes()
            if len(content)>MAX_PACKET_BYTES:
                raise ValueError("packet exceeds 1 MiB")
            result=store.submit(json.loads(content),args.allow_real_observation)
        elif args.command=="claim":
            result=store.claim(args.bot)
        elif args.command=="complete":
            result=store.complete(args.packet_id,args.bot,args.result_sha256)
        elif args.command=="block":
            result=store.block(args.packet_id,args.bot,args.reason)
        elif args.command=="requeue":
            result=store.requeue(args.packet_id,args.bot,args.reason)
        else:
            result=store.inspect(args.packet_id)
        print(json.dumps(result,ensure_ascii=False,indent=2))
        return 0
    except (OSError,ValueError,KeyError,TypeError,sqlite3.DatabaseError,RuntimeError,
            json.JSONDecodeError) as exc:
        print(json.dumps({"status":"ERROR","error":str(exc),"no_trading":True},ensure_ascii=False),file=sys.stderr)
        return 2


if __name__=="__main__":
    sys.exit(main())
