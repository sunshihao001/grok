"""Static knowledge-system audit and literal cross-domain routing; NOT trade advice."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "knowledge" / "system"

def read(name: str) -> dict:
    return json.loads((BASE / name).read_text(encoding="utf-8"))

def validate_system(ontology=None, sources=None, units=None, catalog=None):
    o = ontology if ontology is not None else read("ontology.v1.json")
    s = sources if sources is not None else read("source-registry.v1.json")
    u = units if units is not None else read("research-units.v1.json")
    c = catalog if catalog is not None else json.loads((ROOT / "knowledge/catalog.v1.json").read_text(encoding="utf-8"))
    schema = json.loads((BASE / "research-unit.schema.json").read_text(encoding="utf-8"))
    if any(x.get("schema_version") != "1.0" for x in (o, s, u, c)):
        raise ValueError("version mismatch")
    if [x["id"] for x in o["layers"]] != [f"L{i}" for i in range(8)]:
        raise ValueError("invalid 8-layer ontology")
    ds = o["domains"]
    if [d["id"] for d in ds] != [f"D{i:02d}" for i in range(1, 13)]:
        raise ValueError("invalid 12-domain ontology")
    ids = {d["id"] for d in ds}
    if o.get("ontology_revision") != "1.1":
        raise ValueError("ontology V1.1 review contract missing")
    deps = {d["id"]: d["depends_on"] for d in ds}
    cards = []
    for d in ds:
        if d["layer"] not in {v["id"] for v in o["layers"]} or not d["keywords"]:
            raise ValueError("domain metadata missing")
        related = d.get("related_domains")
        if not d.get("domain_role") or not d.get("scope") or not isinstance(related, list):
            raise ValueError("missing V1.1 domain boundary contract")
        if (len(related) != len(set(related)) or set(related) - ids or
                d["id"] in related or set(related).intersection(deps[d["id"]])):
            raise ValueError("invalid contextual domain relationships")
        if len(deps[d["id"]]) != len(set(deps[d["id"]])) or set(deps[d["id"]]) - ids:
            raise ValueError("bad prerequisite")
        if d["primary_card_ids"]:
            if d["coverage"] != "legacy_seeded_unverified":
                raise ValueError("legacy evidence improperly marked verified")
        elif d["coverage"] != "declared_research_gap":
            raise ValueError("undeclared gap")
        cards += d["primary_card_ids"]
    if len(cards) != len(set(cards)) or set(cards) != {x["id"] for x in c["cards"]}:
        raise ValueError("legacy card domain mapping invalid")
    # These domain categories have no universally required subject-domain chain.
    for unconstrained in ("D07", "D08", "D09", "D10", "D11", "D12"):
        if deps[unconstrained]:
            raise ValueError("crosscut, strategy and contextual domains cannot force all topic prerequisites")
    done, active = set(), set()
    def visit(n):
        if n in active:
            raise ValueError("cyclic prerequisite graph")
        if n in done:
            return
        active.add(n)
        for parent in deps[n]:
            visit(parent)
        active.remove(n)
        done.add(n)
    for d in ids:
        visit(d)
    relations = set()
    for r in o["relations"]:
        if r["from"] not in ids or r["to"] not in ids or not r.get("guard"):
            raise ValueError("broken relationship")
        key = (r["from"], r["to"], r["kind"])
        if key in relations:
            raise ValueError("duplicate relationship")
        relations.add(key)
    sources_by_id = {}
    for e in s["source_entries"]:
        sha = e["commit"]
        if e["id"] in sources_by_id or len(sha) != 40 or any(ch not in "0123456789abcdef" for ch in sha):
            raise ValueError("invalid pinned source")
        if not e.get("boundary") or not e.get("license_review"):
            raise ValueError("missing source boundary")
        sources_by_id[e["id"]] = e
    index_path = ROOT / "knowledge/source_index.v1.json"
    index_items = json.loads(index_path.read_text(encoding="utf-8"))["items"] if index_path.exists() else []
    by_repo = {e["repository"]: e for e in sources_by_id.values()}
    for item in index_items:
        if item["repository"] not in by_repo or item["commit"] != by_repo[item["repository"]]["commit"]:
            raise ValueError("source-index pin conflicts with source-registry")
    units_by_id = {r["id"] for r in u["units"]}
    if len(units_by_id) != len(u["units"]):
        raise ValueError("duplicate research ID")
    req, allowed = set(schema["required"]), set(schema["properties"])
    if not req or req - allowed:
        raise ValueError("invalid schema")
    for r in u["units"]:
        if req - set(r) or set(r) - allowed:
            raise ValueError("research unit missing/unknown fields")
        if not r["domains"] or set(r["domains"]) - ids or len(r["domains"]) != len(set(r["domains"])):
            raise ValueError("invalid research domains")
        if r["primary_source"]["source_id"] not in sources_by_id or not r["primary_source"]["path"]:
            raise ValueError("unknown research source")
        if ".." in Path(r["primary_source"]["path"]).parts:
            raise ValueError("unsafe research path")
        for key in ("claim", "population", "decision_cutoff", "economic_status", "falsification_test"):
            if not isinstance(r[key], str) or not r[key].strip():
                raise ValueError("empty substantive field")
        for key in ("support", "counterevidence", "alternatives", "not_established"):
            if not isinstance(r[key], list) or not r[key] or not all(isinstance(x, str) and x.strip() for x in r[key]):
                raise ValueError("unbalanced research evidence")
        if set(r["links_to"]) - units_by_id or r["id"] in r["links_to"]:
            raise ValueError("broken research link")
        if r["status"] == "external_reported" and (r["runtime_policy"] != "research_reference_only" or r["local_replication"] != "not_attempted"):
            raise ValueError("externally reported finding cannot self-promote")
        if r["runtime_policy"] == "approved_monitor_only" and (r["status"] != "independently_validated" or r["local_replication"] != "independently_reviewed"):
            raise ValueError("research lacks independent validation")
    policy = read("filter-policy.v1.json")
    gates = policy.get("gates", [])
    if policy.get("schema_version") != "1.0" or policy.get("policy_revision") != "1.1":
        raise ValueError("filter policy version mismatch")
    if policy.get("no_automatic_pass") is not True or [g.get("id") for g in gates] != [f"F{i}" for i in range(7)]:
        raise ValueError("seven sequential no-auto-pass gates required")
    if len({g["id"] for g in gates}) != len(gates) or any(not g.get("requires") or not g.get("rejection") for g in gates):
        raise ValueError("incomplete filtering gate contract")
    expected_profiles = {"EXPLAIN":4, "PREDICT":5, "ECONOMIC":6, "MONITOR_RELEASE":7}
    for name, count in expected_profiles.items():
        if policy.get("objective_profiles", {}).get(name) != [f"F{i}" for i in range(count)]:
            raise ValueError("objective filtering gate coverage invalid")
    if policy.get("objective_profiles", {}).get("UNSPECIFIED") != [f"F{i}" for i in range(7)]:
        raise ValueError("unspecified research must expose the full gate checklist")
    return {"structure":"VALID", "epistemic_status":"NOT_AN_ECONOMIC_VALIDATION", "layers":len(o["layers"]),
            "domains":len(ds), "legacy_cards_mapped":len(cards),
            "gaps":[d["id"] for d in ds if d["coverage"] == "declared_research_gap"],
            "relations":len(relations), "sources":len(sources_by_id),
            "on_demand_source_pointers":len(index_items), "evidence_filter_gates":len(gates),
            "external_units":sum(r["status"] == "external_reported" for r in u["units"]),
            "production_trading_authorized":False}

def route_domains(question: str, ontology=None):
    if not isinstance(question, str) or not question.strip():
        raise ValueError("question required")
    o = ontology if ontology is not None else read("ontology.v1.json")
    ds = o["domains"]
    dm = {d["id"]: d for d in ds}
    q = question.casefold()
    matches = [d["id"] for d in ds if any(k.casefold() in q for k in d["keywords"])]
    selected = set()
    def add(d):
        if d in selected:
            return
        selected.add(d)
        for p in dm[d]["depends_on"]:
            add(p)
    for d in matches:
        add(d)
    # Contextual links may be useful, but must not be treated as prerequisites.
    contextual = sorted({r for d in matches for r in dm[d]["related_domains"]} - selected)
    return {"status":"DOMAIN_MATCH" if matches else "RESEARCH_GAP",
            "method":"literal_terms_and_domain_dependencies_not_semantic_reasoning",
            "matched_domains":matches, "required_domains":[d["id"] for d in ds if d["id"] in selected],
            "contextual_domain_candidates":contextual,
            "crosscut_evidence_controls":["D10","D11"],
            "legacy_card_ids":[card for d in ds if d["id"] in selected for card in d["primary_card_ids"]],
            "research_gaps":[d["id"] for d in ds if d["id"] in selected and d["coverage"] == "declared_research_gap"],
            "warning":"This is a research route, not evidence of predictive or executable alpha."}

def filter_plan(objective: str = "UNSPECIFIED", policy: dict | None = None) -> dict:
    """Outline stage requirements, never attest evidence or grant trade permission.

    A list of required fields is *not* equivalent to those fields having been
    independently authenticated. This function deliberately cannot return PASS.
    """
    spec = policy if policy is not None else read("filter-policy.v1.json")
    targets = spec.get("objective_profiles", {})
    if objective not in targets:
        raise ValueError("unknown research filter objective")
    active = set(targets[objective])
    gates = []
    for g in spec["gates"]:
        needed = g["id"] in active
        gates.append({
            "id":g["id"], "name":g["name"],
            "required_for_objective":None if objective == "UNSPECIFIED" else needed,
            "status":"NOT_EVALUATED" if (needed or objective == "UNSPECIFIED") else "NOT_APPLICABLE",
            "required_evidence":g["requires"],
            "insufficient_evidence_policy":g["rejection"],
            "next_research_action":g["continuation"],
        })
    return {
        "policy_revision":spec["policy_revision"], "objective":objective,
        "plan_only_no_evidence_verdict":True,
        "always_on":spec["always_on"],
        "gates":gates, "automatic_rule_promotion":False,
    }


def main():
    parser = argparse.ArgumentParser()
    args = parser.add_mutually_exclusive_group(required=True)
    args.add_argument("--audit", action="store_true")
    args.add_argument("--question")
    ns = parser.parse_args()
    try:
        result = validate_system() if ns.audit else route_domains(ns.question)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (ValueError, KeyError, TypeError, OSError, json.JSONDecodeError) as error:
        print(json.dumps({"status":"ERROR", "reason":str(error)}, ensure_ascii=False), file=sys.stderr)
        return 2

if __name__ == "__main__":
    sys.exit(main())
