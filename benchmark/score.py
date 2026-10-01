"""Score all saved run results and print the phase-1 scorecard + the phase-2 backlog column.

  python benchmark/score.py        # reads benchmark/results/*.json

Each result file is the JSON a run returned (see trace_schema.json). MCQ + string CONTAINS
score automatically; JUDGE and semantic cases print as needs_human for Aaman to grade.
"""
import glob
import json
import os

import graders  # noqa: E402  (same dir)

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    files = sorted(glob.glob(os.path.join(HERE, "results", "*.json"))
                   + glob.glob(os.path.join(HERE, "results-native", "*.json")))
    if not files:
        print("no results in benchmark/results[-native]/. Run cases first (see HOW-TO-RUN.md).")
        return
    # native runs win over emulated for the same case id
    byid = {}
    for f in files:
        r = json.load(open(f))
        byid[r["case_id"]] = r
    runs = list(byid.values())
    report = graders.grade_all(runs)

    print("=" * 60)
    print("PHASE-1 SCORECARD")
    for k, v in report["scorecard"].items():
        print(f"  {k:14} {v}")
    print("=" * 60)
    print(f"{'CASE':7}{'SCORE':10}{'FIRED':7}REASON")
    for r in report["results"]:
        print(f"{r['case_id']:7}{str(r['score']):10}{('yes' if r['pipeline_fired'] else 'no'):7}{r['reason']}")

    print("\nPHASE-2 BACKLOG (fill for every 0 / void: earliest stage that made it inevitable):")
    for r in report["results"]:
        if r["score"] in (0, "void"):
            run = next(x for x in runs if x["case_id"] == r["case_id"])
            print(f"  {r['case_id']}: ____________  (notes: {run.get('notes','')[:80]})")


if __name__ == "__main__":
    main()
