#!/usr/bin/env python3
"""
Find people who replied to a cold SMS but were NEVER categorised in Airtable.

This runs in the OPPOSITE direction to tools/july_pr_register.py. That script is
Evergreen-first: its universe is (deals + categorised contact-threads), then it repairs
threads from the GHL log. Its `contact_only` bucket means "categorised but no deal" --
strictly narrower than what we want here. A GHL replier with no Evergreen record at all
never enters it.

So: start from the raw GHL send log, take every inbound message in the window, and
anti-join against Evergreen. What falls through is the pile nobody worked.

This is the check that produced clients/wise-digital/AUTOPSY.md section 9 -- 35 people who
engaged and were never answered at all, median 64 days silent, invisible to every KPI
because "worked %" was measured only over replies that already had a deal record.

THE JOIN IS TWO-KEYED, and that is not a style choice:
  /deals    HAS phone  -> join on norm(phone). (`contact` is null on every deal record;
                          the name lives in `opportunity`.)
  /contacts has NO phone at all -> join on normalised name + company.
Phone matches are exact; name matches are fuzzy, so they are reported as such.

Usage:
  python3 tools/missed_replies_scan.py --all-clients --from 2026-08-17 --to 2026-08-24
  python3 tools/missed_replies_scan.py --client gofish --from 2026-08-17 --to 2026-08-24
  python3 tools/missed_replies_scan.py --client gofish --control 2026-06   # busy-window check
"""
import argparse, csv, datetime as dt, json, os, re, sys, urllib.parse, urllib.request
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ghl_mine as gm                      # creds_from_mcp, req, ROOT, REGISTRY, STOP_RX
from ghl_number_split_scan import norm, pretty, EV_SLUG

EVERGREEN = "https://knowledgebase-production-f52e.up.railway.app"

# Every category the /contacts endpoint will return. It requires one call per category.
CATEGORIES = ["Power Request", "Positive", "More Info Request", "Email Me Request",
              "Objection Handling", "Maybe", "Referral Request", "Future Request",
              "Custom Response", "Neutral", "Not Interested", "Threat"]

# Intent tiering. High+Medium is what the weekly scorecards count as a positive.
TIER = {"Power Request": "High", "Meeting Booked": "High", "Positive": "Medium",
        "More Info Request": "Medium", "Email Me Request": "Medium",
        "Objection Handling": "Medium", "Maybe": "Medium", "Custom Response": "Medium",
        "Future Request": "Low", "Referral Request": "Low", "Neutral": "Low",
        "Not Interested": "Low", "Threat": "Low", "(uncategorised)": "Low"}

# Reply-intent buckets. Deliberately conservative: anything not clearly a brush-off stays
# in `unclear` for a human to read, rather than being silently judged by keyword. The
# control pull turned up "Who are you and what do you do?" -- a real question a naive
# POSITIVE/SOFT_NO word list scores as negative.
# Wrong-number / left-the-company gets its own bucket. On the first Go Fish run ALL 16
# uncategorised replies were this -- a list-quality signal, not a missed yes. Folding them
# into "negative" would be technically true and practically useless: it buries the one
# real hand-raise in a pile of bounces.
WRONG_PERSON_RX = re.compile(
    r"(wrong number|wrong person|not who you think|this (?:is|isn'?t|ain'?t) not?\b|"
    r"this is not|i'?m not \w+|isn'?t \w+[.,!]|do ?n[o']?t work (?:at|for|there|here)|"
    r"no longer (?:work|with|at)|haven'?t worked|used to work|left (?:the )?(?:company|there)|"
    r"not (?:with|at) \w+ anymore|no one by that name)", re.I)
HARD_NO_RX = re.compile(
    r"\b(not interested|no thanks?|no thank you|stop texting|lose my number|"
    r"take me off|remove me|do ?n[o']?t (?:contact|text|message)|"
    r"unsubscribe|fuck|scam|spam|report you|sue)\b", re.I)
POSITIVE_RX = re.compile(
    r"\b(interested|sure|yes|yeah|yep|sounds good|let'?s (?:talk|do|chat|connect)|"
    r"send (?:me|over|it)|more info|tell me more|how much|what'?s the (?:cost|price)|"
    r"pricing|call me|book|schedule|calendar|available|free (?:this|next)|"
    r"what do you|who (?:are|is) (?:you|this)|what is this|worth a)\b", re.I)


# ------------------------------------------------------------------ Evergreen (no auth)
def ev_get(path, query=None):
    """Evergreen needs no auth but DOES need a non-Python User-Agent -- its host WAFs urllib."""
    url = EVERGREEN + path + ("?" + urllib.parse.urlencode(query) if query else "")
    for a in range(3):
        try:
            r = urllib.request.Request(url, headers={"Accept": "application/json",
                                                     "User-Agent": "curl/8.7.1"})
            with urllib.request.urlopen(r, timeout=90) as resp:
                return json.loads(resp.read().decode())
        except Exception as e:
            if a == 2:
                print(f"  !! evergreen {path} failed: {str(e)[:80]}", flush=True)
                return None


def nn(v):
    """Evergreen serialises a missing field as real JSON null on some clients and as the
    literal STRING "None" on others -- the two sit side by side inside one payload.
    bool("None") is True, so left alone the string form poisons every truthiness test."""
    return None if (v is None or (isinstance(v, str) and v.strip() in ("None", "nan", ""))) else v


def nkey(s):
    """Normalise a name or company for the fuzzy side of the join."""
    s = (nn(s) or "").lower()
    s = re.sub(r"\b(inc|llc|ltd|co|corp|company|group|the|and|&)\b", " ", s)
    return re.sub(r"[^a-z0-9]+", "", s)


# ------------------------------------------------------------------------------- GHL
def pull_messages(pit, loc, start_iso, end_iso):
    """Every SMS in the window. Cursor-paginated; dedupe on message id at window edges."""
    out, cur = [], None
    while True:
        q = {"locationId": loc, "limit": 1000, "channel": "SMS",
             "startDate": start_iso, "endDate": end_iso}
        if cur:
            q["cursor"] = cur
        d = gm.req(pit, "/conversations/messages/export", gm.V_CONV, query=q)
        if not d:
            break
        out += d.get("messages", [])
        cur = d.get("nextCursor")
        if not cur:
            break
    return list({m["id"]: m for m in out}.values())


def pull_contacts(pit, contact_ids):
    """Resolve replier identity. One human can span several contactIds (re-imports,
    retarget uploads), so callers merge on normalised phone afterwards."""
    got = {}

    def one(cid):
        d = gm.req(pit, f"/contacts/{cid}", gm.V_CONTACT)
        if d and d.get("contact"):
            got[cid] = d["contact"]

    with ThreadPoolExecutor(max_workers=8) as ex:
        list(ex.map(one, contact_ids))
    return got


# ------------------------------------------------------------------------------ scan
def scan_client(key, cfg, start, end, verbose=True):
    label = cfg.get("label", key)
    sms = cfg.get("sms") or {}
    server, loc = sms.get("mcp"), sms.get("locationId")
    res = {"key": key, "label": label, "runnable": False, "note": "", "misses": [],
           "sent": 0, "inbound": 0, "repliers": 0, "optouts": 0, "categorised": 0,
           "never_categorised": 0, "ev_loaded": key in EV_SLUG}

    if not server or not loc:
        res["note"] = "no GHL connector -- this check cannot run"
        return res

    pit = gm.creds_from_mcp(server)
    s_iso = f"{start}T00:00:00.000Z"
    e_iso = f"{end}T23:59:59.000Z"
    msgs = pull_messages(pit, loc, s_iso, e_iso)
    res["runnable"] = True

    outb = [m for m in msgs if m.get("direction") == "outbound"]
    inb = [m for m in msgs if m.get("direction") == "inbound"]
    res["sent"] = len(outb)
    res["inbound"] = len(inb)

    if verbose:
        print(f"  {label}: {len(msgs)} msgs ({len(outb)} out / {len(inb)} in)", flush=True)

    if not inb:
        res["note"] = ("no inbound SMS in window" if outb else
                       "NO SENDS AT ALL in window -- sending appears stopped")
        return res

    # ---- group inbound by contact, split opt-outs -------------------------------
    by_contact = defaultdict(list)
    for m in inb:
        by_contact[m["contactId"]].append(m)

    contacts = pull_contacts(pit, list(by_contact))

    # merge contactIds that are the same human (same phone)
    by_phone = defaultdict(lambda: {"cids": set(), "msgs": [], "contact": None})
    for cid, ms in by_contact.items():
        c = contacts.get(cid, {})
        ph = norm(c.get("phone") or (ms[0].get("from") if ms else ""))
        rec = by_phone[ph or cid]
        rec["cids"].add(cid)
        rec["msgs"] += ms
        if c and not rec["contact"]:
            rec["contact"] = c
    res["repliers"] = len(by_phone)

    # outbound index for the "did we answer?" test
    out_by_cid = defaultdict(list)
    for m in outb:
        out_by_cid[m["contactId"]].append(m)

    # ---- Evergreen side ---------------------------------------------------------
    ev_phones, ev_names, deals_n, threads_n = set(), {}, 0, 0
    slug = EV_SLUG.get(key)
    if slug:
        d = ev_get(f"/api/clients/{slug}/deals", {"channel": "sms", "limit": 3000})
        for dl in (d or {}).get("deals", []):
            deals_n += 1
            p = norm(nn(dl.get("phone")) or "")
            if p:
                ev_phones.add(p)
            nm = nkey(dl.get("opportunity") or dl.get("contact"))
            if nm:
                ev_names[nm] = nn(dl.get("positive_reply_category")) or nn(dl.get("stage")) or "deal"

        seen_thread = set()
        for cat in CATEGORIES:
            t = ev_get(f"/api/clients/{slug}/contacts", {"category": cat, "limit": 2000})
            for th in (t or {}).get("threads", []):
                if th.get("id") in seen_thread:
                    continue
                seen_thread.add(th.get("id"))
                threads_n += 1
                nm = nkey(th.get("name"))
                if nm:
                    ev_names.setdefault(nm, cat)
                cn = nkey(th.get("company"))
                if cn:
                    ev_names.setdefault("co:" + cn, cat)
    else:
        res["note"] = "not loaded in Evergreen -- categorisation cannot be checked"

    # ---- anti-join --------------------------------------------------------------
    for ph, rec in by_phone.items():
        ms = sorted(rec["msgs"], key=lambda m: m["dateAdded"])
        bodies = [(m.get("body") or "").strip() for m in ms]
        text = " | ".join(b for b in bodies if b)
        c = rec["contact"] or {}
        name = " ".join(x for x in [nn(c.get("firstName")), nn(c.get("lastName"))] if x).strip()
        company = nn(c.get("companyName")) or ""

        is_optout = any(gm.STOP_RX.match(b) for b in bodies)
        if is_optout:
            res["optouts"] += 1

        # matched in Evergreen?
        match, how = None, ""
        if ph and ph in ev_phones:
            match, how = "deal", "phone"
        elif nkey(name) and nkey(name) in ev_names:
            match, how = ev_names[nkey(name)], "name (fuzzy)"
        elif nkey(company) and ("co:" + nkey(company)) in ev_names:
            match, how = ev_names["co:" + nkey(company)], "company (fuzzy)"

        if match:
            res["categorised"] += 1
            continue
        if is_optout:
            continue                      # opted out and uncategorised is not a "miss"
        res["never_categorised"] += 1

        # did a human ever answer?
        first_in = ms[0]["dateAdded"]
        human_out = [m for m in sum((out_by_cid[c_] for c_ in rec["cids"]), [])
                     if m.get("source") != "workflow" and m["dateAdded"] > first_in]
        answered = bool(human_out)
        silent = (dt.datetime.now(dt.timezone.utc)
                  - gm.T(first_in)).days

        blob = " ".join(bodies)
        if WRONG_PERSON_RX.search(blob):
            intent = "wrong_person"       # checked first: "I'm not Emily, take me off"
        elif HARD_NO_RX.search(blob):     # is a bad number, not a rejection of the offer
            intent = "negative"
        elif POSITIVE_RX.search(blob):
            intent = "positive"
        else:
            intent = "unclear"

        res["misses"].append({
            "client": label, "name": name or "(unknown)", "company": company,
            "phone": pretty(ph), "replied_at": first_in[:16].replace("T", " "),
            "days_silent": silent, "answered": "yes" if answered else "NO",
            "intent": intent, "n_msgs": len(ms), "opted_out": "yes" if is_optout else "",
            "reply": text[:600],
        })

    order = {"positive": 0, "unclear": 1, "negative": 2, "wrong_person": 3}
    res["misses"].sort(key=lambda r: (order[r["intent"]], -r["days_silent"]))
    if verbose and slug:
        print(f"     evergreen: {deals_n} deals, {threads_n} threads | "
              f"repliers {res['repliers']} = categorised {res['categorised']} + "
              f"never {res['never_categorised']} + optout-uncat "
              f"{res['repliers'] - res['categorised'] - res['never_categorised']}", flush=True)
    return res


# ------------------------------------------------------------------------------ main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--client")
    ap.add_argument("--all-clients", action="store_true")
    ap.add_argument("--from", dest="start", default="2026-08-17")
    ap.add_argument("--to", dest="end", default="2026-08-24")
    ap.add_argument("--control", help="YYYY-MM busy-window check; prints volume only")
    ap.add_argument("--out", default=os.path.join(gm.ROOT, "clients", "_rollup"))
    a = ap.parse_args()

    reg = json.load(open(gm.REGISTRY))
    keys = ([a.client] if a.client else
            [k for k, v in reg.items()
             if not k.startswith("_") and (v.get("sms") or {}).get("locationId")])

    if a.control:
        y, m = a.control.split("-")
        nxt = f"{int(y)+1}-01" if m == "12" else f"{y}-{int(m)+1:02d}"
        for k in keys:
            cfg = reg[k]
            pit = gm.creds_from_mcp(cfg["sms"]["mcp"])
            n = pull_messages(pit, cfg["sms"]["locationId"],
                              f"{a.control}-01T00:00:00.000Z", f"{nxt}-01T00:00:00.000Z")
            print(f"{cfg.get('label',k):<24} control {a.control}: {len(n):>7,} msgs")
        return

    print(f"\nMissed-reply scan  {a.start} -> {a.end}   ({len(keys)} clients)\n" + "-" * 64)
    results = [scan_client(k, reg[k], a.start, a.end) for k in keys]

    os.makedirs(a.out, exist_ok=True)
    csv_path = os.path.join(a.out, f"{a.end}-missed-replies.csv")
    cols = ["client", "name", "company", "phone", "replied_at", "days_silent",
            "answered", "intent", "n_msgs", "opted_out", "reply"]
    with open(csv_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for r in results:
            for m in r["misses"]:
                w.writerow(m)

    print("\n" + "=" * 64)
    print(f"{'client':<20}{'sent':>7}{'in':>6}{'repl':>6}{'cat':>6}{'MISS':>6}  note")
    for r in results:
        print(f"{r['label'][:19]:<20}{r['sent']:>7,}{r['inbound']:>6}{r['repliers']:>6}"
              f"{r['categorised']:>6}{r['never_categorised']:>6}  {r['note']}")
    tot = sum(len(r["misses"]) for r in results)
    cnt = lambda i: sum(1 for r in results for m in r["misses"] if m["intent"] == i)
    print("-" * 64)
    print(f"{tot} never-categorised replies  ({cnt('positive')} positive, "
          f"{cnt('unclear')} unclear, {cnt('negative')} negative, "
          f"{cnt('wrong_person')} wrong-number/left-company)")
    print(f"csv: {csv_path}")
    json.dump(results, open(csv_path.replace(".csv", ".json"), "w"), indent=1)


if __name__ == "__main__":
    main()
