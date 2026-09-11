#!/usr/bin/env python3
"""
ghl_sms_daily.py — day-level cold-SMS stats for a Scaletopia (GHL) campaign.

Why this exists: Evergreen/Airtable only bucket by week/month and lag ~a day,
so a *brand-new* campaign (launched today/yesterday) is invisible there. This
hits GHL's message export directly and reconciles the way Scaletopia SMS
actually works: 2 texts per lead (opener + hook), so raw "sends" = ~2x leads.

Output per day: leads texted, sends, hook-variant split, inbound replies
classified (positive / soft-no / hard opt-out), opt-out %, and PR-per-lead.

Usage:
  export GHL_API_KEY=...            # LeadConnector private-integration / agency token
  export GHL_LOCATION_ID=TYVYHj7lX8bamHkOKz4s   # Scaletopia sub-account (default below)
  python3 tools/ghl_sms_daily.py                # yesterday (PT)
  python3 tools/ghl_sms_daily.py 2026-07-21     # a specific day
  python3 tools/ghl_sms_daily.py 2026-07-18 2026-07-21   # inclusive range
  python3 tools/ghl_sms_daily.py --contains "on clutch"  # only leads whose copy matches

Notes:
- Day boundaries are US/Pacific (the account's send timezone).
- Sends are split workflow (campaign) vs app (manual / n8n). Both are shown: counting
  only `workflow` hides manual sends, and counting only one number hides the rest.
- The sub-account is SHARED with Velox Media. Scaletopia's era starts 2026-08-03; older
  traffic in this location is not theirs (see clients/registry.json era_note).
- Positives here are a heuristic on reply text; treat the CRM/Evergreen deal
  log as the source of truth once it syncs. Opt-outs are reliable immediately.
"""
import os, sys, json, datetime, urllib.request, urllib.parse

API = "https://services.leadconnectorhq.com"
LOCATION_ID = os.environ.get("GHL_LOCATION_ID", "TYVYHj7lX8bamHkOKz4s")  # Scaletopia (live since 2026-08-03)
TOKEN = os.environ.get("GHL_API_KEY")
# NOTE: we deliberately do NOT filter by sending number. Scaletopia rotates several
# numbers (and the n8n app splits threads across them), so pinning one silently zeroes
# the report. Every number on the location is counted.
PT_OFFSET = datetime.timedelta(hours=-7)  # PDT; swap to -8 in standard time

# ---- reply classification -------------------------------------------------
# DEFECT FIXED 2026-08-28: this used to classify PER MESSAGE and count len(positives),
# so one person sending two replies scored as two PRs. It also matched "ok"/"time"/
# "works"/"sounds", and had no bucket for "I don't work there any more" - so
# "Not with Veza anymore but interested" scored POSITIVE. Both bugs inflated the PR
# count. Classification is now PER CONTACT, over that contact's whole thread, with
# explicit precedence. A PR is a person, not a message.

HARD_OPTOUT = ("stop", "unsubscribe", "remove me", "remove my", "opt out", "optout",
               "take me off", "do not text", "don't text", "dont text", "lose this number")
# they are not at the target company -> NOT a lead at all, regardless of sentiment
STALE = ("no longer", "not with", "haven't worked", "havent worked", "left the compan",
         "i'm retired", "im retired", "retired now", "wrong number", "wrong numbr",
         "wrong person", "wrong party", "wrong contact", "my name is not", "not at ",
         "years too late", "no christopher", "isn't here", "not here any")
# points at someone else -> a routing win, but not a PR
REFERRAL = ("reach out to", "speak to", "talk to", "contact ", "you'd have to", "suggest finding",
            "not the right person", "can't make any of those decisions", "cant make any of those")
SOFT_NO = ("no thanks", "not interested", "no thank", "no interest", "not in the",
           "not in a", "who is this", "not a fit", "we're good", "all set")
# tightened: removed ok/okay/time/works/sounds/send/info - they matched everything
POSITIVE = ("yes", "sure", "interested", "how does", "how do", "tell me more", "more info",
            "let's do", "lets do", "let's talk", "lets talk", "call me", "give you a call",
            "worth exploring", "worth a look", "curious", "open to", "book", "calendar",
            "what's the cost", "whats the cost", "how much", "pricing", "send me an email",
            "show me", "loom", "happy to")

def classify_thread(bodies) -> str:
    """Classify ONE CONTACT from all their inbound messages. Precedence matters:
    a stale contact who says 'interested' is still stale - they cannot buy for that company."""
    b = " ".join(bodies).lower().strip()
    if any(w in b for w in HARD_OPTOUT):  return "opt_out"
    if any(w in b for w in STALE):        return "stale_or_wrong"
    if any(w in b for w in REFERRAL):     return "referral"
    if any(w in b for w in SOFT_NO):      return "soft_no"
    if any(w in b for w in POSITIVE):     return "positive"
    return "unclear"

def classify(body: str) -> str:      # kept for callers that pass a single message
    return classify_thread([body])

def hook_variant(body: str) -> str:
    b = body.lower()
    if "on clutch" in b: return "clutch"
    if "heard great things" in b: return "heard"
    if "chamber media sign 18 retainers" in b: return "opener"
    return "other"

# ---- fetch ----------------------------------------------------------------
def export_messages(start_iso: str, end_iso: str):
    if not TOKEN:
        sys.exit("Set GHL_API_KEY (LeadConnector token) in the environment.")
    msgs, cursor = [], None
    while True:
        q = {"locationId": LOCATION_ID, "channel": "SMS", "limit": 1000,
             "sortBy": "createdAt", "sortOrder": "desc",
             "startDate": start_iso, "endDate": end_iso}
        if cursor: q["cursor"] = cursor
        url = f"{API}/conversations/messages/export?" + urllib.parse.urlencode(q)
        req = urllib.request.Request(url, headers={
            "Authorization": f"Bearer {TOKEN}",
            "Version": "2021-04-15",
            "Accept": "application/json",
            "User-Agent": "scaletopia-sms-daily/1.0",  # GHL 403s without a UA
        })
        with urllib.request.urlopen(req, timeout=60) as r:
            data = json.load(r)
        msgs.extend(data.get("messages", []))
        cursor = data.get("nextCursor")
        if not cursor:
            break
    return msgs

def day_bounds(d: datetime.date):
    start = datetime.datetime.combine(d, datetime.time()) - PT_OFFSET
    end = start + datetime.timedelta(days=1)
    fmt = "%Y-%m-%dT%H:%M:%S.000Z"
    return start.strftime(fmt), end.strftime(fmt)

# ---- report ---------------------------------------------------------------
def report(day_label, msgs, contains=None):
    out = [m for m in msgs if m["direction"] == "outbound" and m.get("source") == "workflow"]
    app = [m for m in msgs if m["direction"] == "outbound" and m.get("source") != "workflow"]
    inb = [m for m in msgs if m["direction"] == "inbound"]
    if contains:
        keep = {m["contactId"] for m in out if contains.lower() in m["body"].lower()}
        out = [m for m in out if m["contactId"] in keep]
        inb = [m for m in inb if m["contactId"] in keep]

    leads = {m["contactId"] for m in out}
    n_leads = len(leads)
    hooks = {}
    for m in out:
        hooks[hook_variant(m["body"])] = hooks.get(hook_variant(m["body"]), 0) + 1

    by_contact = {}
    for m in inb:
        by_contact.setdefault(m.get("contactId") or m.get("id"), []).append(m.get("body") or "")
    cls = {k: [] for k in ("positive", "referral", "soft_no", "opt_out", "stale_or_wrong", "unclear")}
    for cid, bodies in by_contact.items():
        cls[classify_thread(bodies)].append((cid, bodies))
    from_cohort = sum(1 for cid in by_contact if cid in leads)
    n_pos, n_opt = len(cls["positive"]), len(cls["opt_out"])

    print(f"\n===== {day_label} =====")
    print(f"leads texted        : {n_leads}")
    print(f"sends (workflow)    : {len(out)}   (~{len(out)/n_leads:.1f}/lead)" if n_leads else "sends (workflow)    : 0")
    print(f"sends (app/manual)  : {len(app)}")
    nums = {}
    for m in out + app:
        nums[m.get("from") or "?"] = nums.get(m.get("from") or "?", 0) + 1
    print(f"sending numbers     : " + ", ".join(f"{k}={v}" for k, v in sorted(nums.items(), key=lambda kv: -kv[1])))
    bad = sum(1 for m in out + app if m.get("status") in ("failed", "undelivered"))
    tot = len(out) + len(app)
    print(f"delivery failures   : {bad} ({bad/tot:.1%})" if tot else "delivery failures   : 0")
    print(f"hook split          : " + ", ".join(f"{k}={v}" for k, v in hooks.items() if k != "opener"))
    print(f"inbound msgs        : {len(inb)}   from {len(by_contact)} unique people ({from_cohort} in today's cohort)")
    print(f"  POSITIVE (people) : {n_pos}")
    print(f"  referral          : {len(cls['referral'])}")
    print(f"  stale / wrong ppl : {len(cls['stale_or_wrong'])}   <- not leads: left the company / wrong number")
    print(f"  soft no           : {len(cls['soft_no'])}")
    print(f"  hard opt-out      : {n_opt}")
    print(f"  unclear           : {len(cls['unclear'])}")
    if n_leads:
        print(f"PR / lead           : {n_pos/n_leads:.2%}")
        print(f"opt-out / lead      : {n_opt/n_leads:.2%}")
    for label in ("positive", "referral", "stale_or_wrong", "soft_no", "opt_out", "unclear"):
        for cid, bodies in cls[label]:
            print(f"    [{label:14}] {' || '.join(bodies)[:96]!r}")

def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    contains = None
    for a in sys.argv[1:]:
        if a.startswith("--contains"):
            contains = a.split("=", 1)[1] if "=" in a else sys.argv[sys.argv.index(a)+1]
    today = datetime.date.today()
    if not args:
        days = [today - datetime.timedelta(days=1)]
    elif len(args) == 1:
        days = [datetime.date.fromisoformat(args[0])]
    else:
        a, b = datetime.date.fromisoformat(args[0]), datetime.date.fromisoformat(args[1])
        days = [a + datetime.timedelta(days=i) for i in range((b - a).days + 1)]
    for d in days:
        s, e = day_bounds(d)
        report(d.isoformat(), export_messages(s, e), contains)

if __name__ == "__main__":
    main()
