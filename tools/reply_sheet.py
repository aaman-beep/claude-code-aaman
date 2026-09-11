#!/usr/bin/env python3
"""Flatten the reply audit into ONE csv you can read, sort and grade by hand.

WHY
  The audit measures follow-up COUNT, which says nothing about whether any of those
  follow-ups were worth sending — and a 3rd follow-up is usually automated, so a low
  booking rate at 3+ may just be measuring automation, not cadence. That question can only
  be answered by reading them. This puts each follow-up in its own column next to the
  outcome, so quality can be graded instead of inferred.

  Pulls the months worth comparing: the best-converting month per channel and the month
  under suspicion, labelled so they can be filtered apart in a sheet.

USAGE
  python3 tools/reply_sheet.py --months 2026-08:august 2026-05:best-sms 2026-06:best-email
"""
import argparse, csv, json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ghl_mine as gm

# High-intent only: a real person asking for something. Drops autoresponders, wrong-number
# replies, opt-outs and rows whose thread text never came back.
KEEP_INTENT = {"call_ask", "info_ask", "soft_yes", "objection", "channel_switch", "other"}
KEEP_CATEGORY = {"Power Request", "More Info Request"}
MAX_FU = 5


def flatten(ms):
    return "\n".join(f"[{m['dir'].upper()}{' auto' if m['automated'] else ''}] "
                     f"{m['when']}: {m['body']}" for m in ms)


def followups(r):
    """Human outbounds after their LAST inbound — the chase, in order."""
    ms = r["messages"]
    li = next((i for i in range(len(ms) - 1, -1, -1) if ms[i]["dir"] == "inbound"), None)
    if li is None:
        return []
    return [m for m in ms[li + 1:] if m["dir"] == "outbound" and not m["automated"]]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--audit", default=None, help="audit json (default: newest in _rollup)")
    ap.add_argument("--months", nargs="+", required=True, help="YYYY-MM:label ...")
    ap.add_argument("--out", default=os.path.join(gm.ROOT, "clients/_rollup/output"))
    a = ap.parse_args()

    src = a.audit or os.path.join(gm.ROOT, "clients/_rollup/output",
                                  "2026-08-26-reply-handling-audit.json")
    rows = json.load(open(src))["rows"]
    want = dict(m.split(":") for m in a.months)

    out = []
    for r in rows:
        mo = (r.get("created_at") or "")[:7]
        if mo not in want or r["category"] not in KEEP_CATEGORY:
            continue
        if r["intent"] not in KEEP_INTENT or r["no_thread"]:
            continue
        fus = followups(r)
        row = {
            "month": mo, "bucket": want[mo], "client": r["client_slug"],
            "channel": r["channel"], "category": r["category"], "intent": r["intent"],
            "mistagged": r["mistagged"], "date": (r["created_at"] or "")[:10],
            "contact": r["contact"], "job_title": r["job_title"], "company": r["company"],
            "campaign": r["campaign_name"], "variant": r["copy_variant"],
            "BOOKED": "YES" if r["booked"] else "no", "stage": r.get("stage") or "",
            "has_outcome": r["has_outcome"], "source": r["source"],
            "speed_mins": "" if r["speed_mins"] is None else round(r["speed_mins"]),
            "n_followups": r["followups"], "repeat_followups": r["repeat_followups"],
            "stock_template": "YES" if r["is_stock"] else "",
            "wrong_question": "YES" if r["answer_mismatch"] else "",
            "they_wrote_last": "YES" if r["they_wrote_last"] else "",
            "opener_cta": r["opener_cta"] or "",
            "OPENER": r["opener"], "THEIR_REPLY": r["their_reply"],
            "OUR_ANSWER": r["our_answer"],
        }
        for i in range(MAX_FU):
            row[f"followup_{i+1}"] = fus[i]["body"] if i < len(fus) else ""
        row["full_thread"] = flatten(r["messages"])
        out.append(row)

    out.sort(key=lambda x: (x["bucket"], x["channel"], x["client"], x["date"]))
    cols = list(out[0].keys()) if out else []
    os.makedirs(a.out, exist_ok=True)
    path = os.path.join(a.out, "reply-grading-sheet.csv")
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(out)

    from collections import Counter
    print(f"{len(out)} rows -> {path}")
    for b in sorted({r['bucket'] for r in out}):
        sub = [r for r in out if r["bucket"] == b]
        wo = [r for r in sub if r["has_outcome"]]
        bk = sum(1 for r in wo if r["BOOKED"] == "YES")
        print(f"  {b:12s} n={len(sub):4d}  sms/email "
              f"{Counter(r['channel'] for r in sub)['sms']}/{Counter(r['channel'] for r in sub)['email']}"
              f"  · with outcome {len(wo)} booked {bk}"
              f" ({100*bk/len(wo):.0f}%)" if wo else "")
        print(f"               follow-ups: {Counter(r['n_followups'] for r in sub).most_common(5)}")


if __name__ == "__main__":
    main()
