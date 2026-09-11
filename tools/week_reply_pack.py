#!/usr/bin/env python3
"""Every reply from one week that did NOT end in a booking — all clients, both channels.

WHY THIS EXISTS
  open_pr_rollup.py answers one category ("Power Request") and one definition of open
  (still parked at Positive Reply). That is a call list. This is the weekly REVIEW: every
  reply the inbox manager touched, whatever it was tagged, that has no meeting on the
  record — including the ones we disqualified or lost, because how a reply was handled is
  the thing under review, not whether it is still live.

WHAT IS IN
  * every Evergreen client, active or past — the client list is discovered live
  * SMS and email
  * every reply category EXCEPT the hard nos (Not Interested, Threat)
  * no meeting on the record: meeting_booked_at empty AND stage not in BOOKED_STAGES
  * threads nobody ever answered are kept and flagged — they sort to the top

WHAT IS NOT
  * Strike Tax is not loaded into Evergreen (no entry in ghl_number_split_scan.EV_SLUG),
    so it cannot appear here. It lives in the Airtable "Master Inbox & CRM" base.
  * website / linkedin / email / phone exist only on rows that became an Airtable deal.
    The /contacts endpoint returns name, title, company and a 1200-char conversation
    snippet and nothing else. Rows are marked `source: contact_only` so a blank field
    reads as "the CRM never had it", not "we lost it".
  * company LinkedIn is in no source. A LinkedIn company-search URL is derived from the
    company name instead and marked as derived.

USAGE
  python3 tools/week_reply_pack.py                                  # Mon-Fri of last week
  python3 tools/week_reply_pack.py --from 2026-08-24 --to 2026-08-28
  python3 tools/week_reply_pack.py --from 2026-08-24 --to 2026-08-28 --client scaletopia
"""
import argparse, csv, datetime as dt, json, os, re, sys, urllib.parse
from collections import Counter, OrderedDict
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ghl_mine as gm
import july_pr_register as reg
import open_pr_rollup as roll
import reply_handling_audit as audit

# Everything Evergreen tags except the hard nos. Ordered as we want to READ them:
# the ones that cost us a meeting first, the ones that were never going anywhere last.
CATEGORIES = [c for c in reg.CATEGORIES if c not in reg.EXCLUDE]

# Human gloss on each tag, shown once in the HTML legend so "Custom Response" is not
# a word the reader has to guess at.
GLOSS = {
    "Power Request":      "asked for the call outright",
    "Positive":           "warm, but stopped short of asking for a call",
    "More Info Request":  "asked us to send or show something",
    "Email Me Request":   "asked us to move it to email",
    "Objection Handling": "pushed back — price, timing, already-have-it",
    "Maybe":              "non-committal",
    "Referral Request":   "pointed us at someone else",
    "Future Request":     "not now, come back later",
    "Custom Response":    "a real reply that fits no other tag",
    "Neutral":            "acknowledged us and nothing more",
    "(uncategorised)":    "never tagged by anyone",
}


def all_clients():
    """Every client Evergreen knows, live or past — not just the active ones. A past
    client with zero replies this week costs one wasted call and buys certainty."""
    return [(c["slug"], c.get("status") or "", c.get("client") or c["slug"])
            for c in reg.ev_get("/api/clients")]


def linkedin_company_search(company):
    """No source in the stack carries a company LinkedIn URL. This is a SEARCH link built
    from the company name — one click to the right page, but it is derived, not data,
    and the UI labels it that way."""
    if not company:
        return ""
    q = urllib.parse.quote_plus(company.strip())
    return f"https://www.linkedin.com/search/results/companies/?keywords={q}"


def status_of(r):
    """Four states, and the fourth one matters. A thread whose snippet contains no inbound
    message at all was still TAGGED as a reply, so the reply happened — Evergreen just did
    not return it. Counting those as "never answered" invents a coverage failure out of a
    data gap, and on the 2026-08-24 week it would have overstated the number by six."""
    if not r["messages"] or r["intent"] in ("no_thread", "no_reply"):
        return "reply not in the record"
    if not r["answered"]:
        return "never answered"
    if r["they_wrote_last"]:
        return "ball with us"
    return "we spoke last"


def collect(slug, in_window):
    deals = reg.fetch_deals(slug, "all")
    threads = audit.fetch_cats(slug, CATEGORIES)
    rows, n_deals, n_threads, matched, _ = reg.build_rows(deals, threads, in_window,
                                                          channel="all")
    rows = roll.dedupe(rows)
    ov = roll.overrides_for(slug)
    keep, booked_n = [], 0
    for r in rows:
        if r["category"] not in CATEGORIES:
            continue
        r["client_slug"] = slug
        is_booked = bool(r["booked"]) or (r.get("stage") or "") in roll.BOOKED_STAGES
        if is_booked:
            booked_n += 1
            continue
        hit = reg.apply_overrides(r, ov)
        r["excluded"] = (hit or {}).get("verdict") == "exclude"
        r["override_reason"] = (hit or {}).get("reason", "")
        if r["excluded"]:
            continue
        r["n_messages"] = len(r["messages"])
        r["days_since_reply"] = roll.days_since(r.get("created_at"), NOW)
        r["thread_truncated"] = roll.truncated(r)
        r["company_linkedin_search"] = linkedin_company_search(r.get("company"))
        r["gloss"] = GLOSS.get(r["category"], "")
        r.pop("_deal_id", None)
        audit.analyse(r)
        r["status"] = status_of(r)
        keep.append(r)
    return keep, {"in_window": len(rows), "booked": booked_n, "unbooked": len(keep),
                  "deals": n_deals, "contacts": n_threads, "matched": matched}


# work order: worst failure first — nobody answered, then they wrote last and we stopped,
# then the ones where the last word was ours. Oldest first inside each band.
BAND = {"never answered": 0, "ball with us": 1, "we spoke last": 2,
        "reply not in the record": 3}


def sort_key(r):
    return (BAND[r["status"]], r.get("created_at") or "")


CSV_COLS = ["client", "contact", "job_title", "company", "website", "linkedin",
            "company_linkedin_search", "email", "phone", "location", "channel",
            "request_type", "gloss", "intent", "mistagged", "intent_tier", "stage",
            "status", "campaign_name", "copy_variant", "replied_at", "days_since",
            "answered", "speed_mins", "n_messages", "n_followups", "they_wrote_last",
            "thread_truncated", "source", "OPENER", "THEIR_REPLY", "OUR_ANSWER",
            "full_thread"]


def csv_row(r, label):
    return {
        "client": label, "contact": r.get("contact", ""), "job_title": r.get("job_title", ""),
        "company": r.get("company", ""), "website": r.get("website", ""),
        "linkedin": r.get("linkedin", ""),
        "company_linkedin_search": r.get("company_linkedin_search", ""),
        "email": r.get("email", ""), "phone": r.get("phone", ""),
        "location": r.get("location", ""), "channel": r.get("channel", ""),
        "request_type": r.get("category", ""), "gloss": r.get("gloss", ""),
        "intent": r.get("intent", ""), "mistagged": r.get("mistagged"),
        "intent_tier": r.get("intent_tier", ""), "stage": r.get("stage", ""),
        "status": r["status"], "campaign_name": r.get("campaign_name", ""),
        "copy_variant": r.get("copy_variant", ""),
        "replied_at": (r.get("created_at") or "")[:16].replace("T", " "),
        "days_since": r.get("days_since_reply"), "answered": r["answered"],
        "speed_mins": None if r["speed_mins"] is None else round(r["speed_mins"], 1),
        "n_messages": r["n_messages"], "n_followups": r["followups"],
        "they_wrote_last": r["they_wrote_last"], "thread_truncated": r["thread_truncated"],
        "source": r.get("source", ""), "OPENER": r.get("opener", ""),
        "THEIR_REPLY": r.get("their_reply", ""), "OUR_ANSWER": r.get("our_answer", ""),
        "full_thread": "\n".join(
            f"[{'IN ' if m['dir'] == 'inbound' else 'OUT' + (' auto' if m.get('automated') else '')}]"
            f" {m['when']}: {m['body']}" for m in r["messages"]),
    }


def main():
    global NOW
    ap = argparse.ArgumentParser()
    ap.add_argument("--from", dest="start", default="2026-08-24")
    ap.add_argument("--to", dest="end", default="2026-08-28")
    ap.add_argument("--client", help="one Evergreen slug; default is every client")
    ap.add_argument("--out", default=os.path.join(gm.ROOT, "clients/_rollup/output"))
    a = ap.parse_args()
    NOW = dt.datetime.now(dt.timezone.utc)

    in_window, wslug, wlabel = reg.make_window(None, a.start, a.end)
    pairs = [(a.client, "", a.client)] if a.client else all_clients()
    print(f"unbooked reply pack — {wlabel} — {len(pairs)} client(s), {len(CATEGORIES)} categories")

    def one(triple):
        slug, status, label = triple
        try:
            return slug, status, label, collect(slug, in_window), None
        except Exception as e:
            return slug, status, label, (None, None), str(e)[:80]

    results = list(ThreadPoolExecutor(6).map(one, pairs))

    rows, recon, failed, label_of = [], OrderedDict(), {}, {}
    for slug, status, label, (got, rc), err in results:
        label_of[slug] = label
        if err:
            failed[slug] = err
            print(f"  {slug:18s} FAILED: {err}")
            continue
        recon[slug] = dict(rc, status=status, label=label)
        rows += got
        if rc["in_window"]:
            print(f"  {slug:18s} replies={rc['in_window']:>4}  booked={rc['booked']:>3}  "
                  f"unbooked={rc['unbooked']:>4}")
    rows.sort(key=sort_key)

    os.makedirs(a.out, exist_ok=True)
    stem = os.path.join(a.out, f"{wslug}-unbooked-replies")

    payload = {"window": wlabel, "window_slug": wslug,
               "built_at": dt.datetime.now(dt.timezone.utc).isoformat()[:19] + "Z",
               "categories": CATEGORIES, "gloss": GLOSS, "labels": label_of,
               "reconciliation": recon, "failed": failed, "rows": rows}
    json.dump(payload, open(f"{stem}.json", "w"), indent=1)

    with open(f"{stem}.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=CSV_COLS)
        w.writeheader()
        for r in rows:
            w.writerow(csv_row(r, label_of.get(r["client_slug"], r["client_slug"])))

    n_never = sum(1 for r in rows if r["status"] == "never answered")
    n_ball = sum(1 for r in rows if r["status"] == "ball with us")
    print(f"\n  {len(rows)} unbooked replies · {n_never} never answered · {n_ball} ball with us")
    print(f"  by type: " + ", ".join(f"{k} {v}" for k, v in
                                     Counter(r["category"] for r in rows).most_common()))
    print(f"  -> {stem}.json\n  -> {stem}.csv")


if __name__ == "__main__":
    main()
