"""Deterministic graders for the phase-1 benchmark.

A grader takes (case, run) and returns {score, pipeline_fired, reason}.
  score: 1 | 0 | "void" | "needs_human"
  pipeline_fired: bool

Boundary reminder: the harness NEVER writes copy. It runs each case through the playbook (which
holds the recipe) with Evergreen as the data provider, then grades the emitted run. MCQ and two
deterministic CONTAINS cases grade unsupervised here; everything else returns "needs_human" (Aaman
is ground truth on mechanism/copy JUDGE cases).

run shape: see trace_schema.json.
"""
import glob
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))


def load_cases():
    cases = {}
    for f in sorted(glob.glob(os.path.join(HERE, "cases*.json"))):
        for c in json.load(open(f)).get("cases", []):
            cases[c["id"]] = c
    return cases


def pipeline_fired(case, run):
    """Precondition: every required_skill must appear in the trace as a fired skill."""
    fired = {s["name"].lower() for s in run.get("trace", []) if s.get("kind") == "skill"}
    need = {s.lower() for s in case.get("required_skills", [])}
    return need.issubset(fired)


def _all_text(run):
    parts = [run.get("output", {}).get("text", "") or ""]
    for v in run.get("output", {}).get("variants", []) or []:
        parts += [v.get("t1", "") or "", v.get("t2", "") or ""]
    return "\n".join(parts).lower()


def _t2s(run):
    return [(v.get("t2", "") or "") for v in run.get("output", {}).get("variants", []) or []]


def _seq_of(run, name):
    for s in run.get("trace", []):
        if s.get("kind") == "skill" and s.get("name", "").lower() == name.lower():
            return s.get("seq", 0)
    return None


def grade(case, run):
    fired = pipeline_fired(case, run)

    # ROUTING: the whole point is whether skills fire on their own. pipeline_fired IS the
    # score (fired=1, not=0) — never void. These are only meaningful from a NATIVE run.
    if case.get("category") == "routing":
        chk = case.get("check", {})
        if not case.get("auto"):
            return {"score": "needs_human", "pipeline_fired": fired,
                    "reason": "routing TRACE case — read the native trace against the PASS rule"}
        # the routing question is whether the SKILLS fire. If none fired, it's a routing FAIL,
        # regardless of any incidental Evergreen call (an ad-hoc API hit is not the skill firing).
        if not fired:
            return {"score": 0, "pipeline_fired": False,
                    "reason": f"skills {case.get('required_skills')} did NOT auto-fire — plain behavior (routing gap)"}
        if chk.get("type") == "order_before":
            a, b = _seq_of(run, chk["first"]), _seq_of(run, chk["then"])
            ok = a is not None and b is not None and a < b
            return {"score": 1 if ok else 0, "pipeline_fired": fired,
                    "reason": f"{chk['first']}@{a} before {chk['then']}@{b}" if ok else f"ordering not shown ({chk['first']}={a}, {chk['then']}={b})"}
        if chk.get("type") == "calls_fired":
            hit = any(("call" in s.get("name", "").lower()) for s in run.get("trace", []))
            return {"score": 1 if hit else 0, "pipeline_fired": fired,
                    "reason": "a call search fired" if hit else "no call search in trace (not auto-invoked)"}
        # default routing: did the required skills fire?
        return {"score": 1 if fired else 0, "pipeline_fired": fired,
                "reason": "required skills fired" if fired else f"skills {case.get('required_skills')} did NOT fire — routing failure"}

    # everything else: precondition — if the playbook skills didn't fire, VOID (routing, not copy).
    if not fired:
        return {"score": "void", "pipeline_fired": False,
                "reason": f"required skills {case.get('required_skills')} not all in trace — routing, not copy"}

    if not case.get("auto"):
        return {"score": "needs_human", "pipeline_fired": True,
                "reason": f"{case['grade_type']} case — Aaman is ground truth; grade with the case's PASS rule"}

    chk = case.get("check", {})
    t = chk.get("type")

    if t in ("benchmark_not_rejected", "benchmark_flagged"):
        v = (run.get("benchmark_verdict") or "").upper()
        if not v:
            return {"score": "needs_human", "pipeline_fired": True, "reason": "no benchmark_verdict in run"}
        rejected = v in ("REWORK", "DROP")
        want_rejected = (t == "benchmark_flagged")
        ok = rejected == want_rejected
        return {"score": 1 if ok else 0, "pipeline_fired": True,
                "reason": f"verdict={v} ({'flagged' if rejected else 'allowed'})"}

    if t == "mcq":
        ans = (run.get("answer") or "").strip().lower()
        correct = chk["correct"].lower()
        # accept the normalized answer token, or fall back to scanning the output for it
        hit = ans == correct or correct.replace("_", " ") in _all_text(run)
        return {"score": 1 if hit else 0, "pipeline_fired": True,
                "reason": f"answer={ans or '(none)'} correct={correct}"}

    if t == "must_not_match":
        text = "\n".join(_t2s(run)).lower() or _all_text(run)
        bad = [p for p in chk["patterns"] if p.lower() in text]
        return {"score": 0 if bad else 1, "pipeline_fired": True,
                "reason": f"forbidden phrase(s) present: {bad}" if bad else "no email-handoff ask in T2"}

    if t == "char_range":
        t1max = chk.get("t1_max_hint", 320)
        t2max = chk.get("t2_max_hint", 320)
        over = []
        for i, v in enumerate(run.get("output", {}).get("variants", []) or []):
            if len(v.get("t1", "") or "") > t1max:
                over.append(f"v{i} t1={len(v['t1'])}")
            if len(v.get("t2", "") or "") > t2max:
                over.append(f"v{i} t2={len(v['t2'])}")
        return {"score": 0 if over else 1, "pipeline_fired": True,
                "reason": f"over range: {over}" if over else "all variants within char range"}

    # count_and_ref / no_rung_0 / competitor_slot_sourced are semantic -> human for now
    return {"score": "needs_human", "pipeline_fired": True,
            "reason": f"check '{t}' needs a semantic read; grade with the PASS rule"}


def grade_all(runs):
    """runs: list of run dicts. Returns per-case results + a per-category scorecard."""
    cases = load_cases()
    results, void = [], 0
    cats = {}  # category -> {pass, of, human}
    for run in runs:
        case = cases.get(run["case_id"])
        if not case:
            continue
        r = grade(case, run)
        r["case_id"] = run["case_id"]
        r["category"] = case["category"]
        results.append(r)
        c = cats.setdefault(case["category"], {"pass": 0, "of": 0, "human": 0})
        if r["score"] == "void":
            void += 1
        elif r["score"] == "needs_human":
            c["human"] += 1
        else:
            c["of"] += 1
            if r["score"] == 1:
                c["pass"] += 1
    scorecard = {"pipeline_void": f"{void} / {len(runs)}"}
    for cat in ("mechanism", "copy", "benchmark", "routing", "strategy"):
        if cat in cats:
            c = cats[cat]
            extra = f" (+{c['human']} for Aaman)" if c["human"] else ""
            scorecard[cat] = f"{c['pass']} / {c['of']}{extra}"
    return {"results": results, "scorecard": scorecard}


if __name__ == "__main__":
    # smoke test with two synthetic runs
    demo = [
        {"case_id": "M-02", "answer": "b",
         "trace": [{"kind": "skill", "name": "mechanism-wordsmith"}], "output": {"text": "ship (b)"}},
        {"case_id": "CP-02",
         "trace": [{"kind": "skill", "name": "sms-draft"}, {"kind": "skill", "name": "qa-gate"}],
         "output": {"variants": [{"t1": "hi", "t2": "could I drop you an email w more info?"}]}},
    ]
    print(json.dumps(grade_all(demo), indent=2))
