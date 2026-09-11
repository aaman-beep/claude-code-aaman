#!/usr/bin/env python3
"""Find cold-SMS conversations that span MORE THAN ONE of our sending numbers.

WHY THIS EXISTS
  We send through GoHighLevel using a rotating pool of phone numbers. A single lead's
  thread can end up with the opener from number A and a later follow-up / reply routed
  through number B. Leads notice ("Who is this? Different phone #?") and warm, ready-to-
  book prospects stall out. This sweeps every GHL-SMS client and quantifies how often it
  happens — per client and account-wide — with the warm leads (positive replies / power
  requests) surfaced first, because those are the ones it costs us.

THE SIGNAL (validated on live Scaletopia data)
  Per contact:  our_numbers = {outbound.from} ∪ {inbound.to}.  Flag if |our_numbers| > 1.
  It is NOT a separate conversationId — GHL keeps it one thread, two numbers. Two failure
  modes: workflow rotation (>1 automated `source=="workflow"` from-number) and a manual
  rep text from a line the workflow never used (`source!="workflow"`).

USAGE
  python tools/ghl_number_split_scan.py                       # all GHL clients, last 45d
  python tools/ghl_number_split_scan.py --since 60
  python tools/ghl_number_split_scan.py --clients scaletopia,kynship,gofish
  python tools/ghl_number_split_scan.py --all                 # full history (slow)

Credentials resolve from ~/.claude.json via the same MCP servers ghl_mine.py uses; a
client whose token doesn't resolve is skipped (logged), not fatal.
"""
import argparse, csv, datetime as dt, json, os, sys, urllib.request
from collections import defaultdict, Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ghl_mine as gm  # reuse: creds_from_mcp, req, get_messages, ROOT, REGISTRY

EVERGREEN = "https://knowledgebase-production-f52e.up.railway.app"

# registry key -> Evergreen client slug (for the warm-lead join). strike-tax is not yet
# loaded in Evergreen, so it gets prevalence only, no warm-lead join.
EV_SLUG = {"digital-resource": "digital_resource", "kynship": "kynship",
           "leadgenix": "leadgenix", "redo": "redo", "growth-lab": "growth_lab",
           "gofish": "go_fish", "scaletopia": "scaletopia",
           "wise-digital": "wise_digital", "chamber-media": "chamber_media",
           "big-leap": "big_leap", "seedx": "seedx", "acceler8": "acceler8",
           "nextleft": "nextleft"}

# deal stages that mean a real human engaged (warm). Booked = a meeting exists.
WARM_STAGES   = {"Positive Reply", '"Maybe"', "Maybe", "Next Stage", "Show",
                 "Meeting Booked", "Proposal Sent", "Won", "No Show"}
BOOKED_STAGES = {"Meeting Booked", "Show", "No Show", "Proposal Sent", "Won", "Next Stage"}


def our_num(m):   return m.get("from") if m.get("direction") == "outbound" else m.get("to")
def lead_num(m):  return m.get("to") if m.get("direction") == "outbound" else m.get("from")
def norm(p):
    d = "".join(c for c in (p or "") if c.isdigit())
    return d[-10:] if len(d) >= 10 else d
def pretty(p):
    d = norm(p)
    return f"{d[:3]}-{d[3:6]}-{d[6:]}" if len(d) == 10 else (p or "?")


# ---------------------------------------------------------------- detector (importable)
def group_contacts(msgs):
    """msgs -> {contactId: summary}. Only contacts with at least one outbound."""
    byc = defaultdict(list)
    for m in msgs:
        if m.get("contactId") and m.get("direction") in ("inbound", "outbound"):
            byc[m["contactId"]].append(m)
    contacts = {}
    for cid, ms in byc.items():
        ms.sort(key=lambda x: x.get("dateAdded", ""))
        out = [m for m in ms if m["direction"] == "outbound"]
        inb = [m for m in ms if m["direction"] == "inbound"]
        if not out:
            continue
        our = set(filter(None, (our_num(m) for m in ms)))
        opener = next((m.get("from") for m in out if m.get("from")), None)
        contacts[cid] = {
            "our_numbers": our,
            "opener": opener,
            "later": sorted(our - {opener}),
            "wf_nums": set(filter(None, (m.get("from") for m in out if m.get("source") == "workflow"))),
            "manual_nums": set(filter(None, (m.get("from") for m in out if m.get("source") != "workflow"))),
            "conv_ids": set(filter(None, (m.get("conversationId") for m in ms))),
            "has_inbound": bool(inb),
            # did a reply land on a number other than the opener the lead first saw?
            "reply_diff_number": any(m.get("to") and m["to"] != opener for m in inb),
            "lead_phone": next((lead_num(m) for m in ms if lead_num(m)), None),
            "n_out": len(out), "n_in": len(inb),
            "first": ms[0].get("dateAdded", "")[:10], "last": ms[-1].get("dateAdded", "")[:10],
        }
    return contacts


def failure_mode(c):
    modes = []
    if len(c["wf_nums"]) > 1:
        modes.append("rotation")
    if c["manual_nums"] - c["wf_nums"]:
        modes.append("manual")
    if not modes and len(c["our_numbers"]) > 1:
        modes.append("mixed")
    return "+".join(modes)


# ---------------------------------------------------------------- evergreen warm roster
def fetch_deals(slug):
    if not slug:
        return {}
    url = f"{EVERGREEN}/api/clients/{slug}/deals?channel=sms&limit=3000"
    try:
        r = urllib.request.Request(url, headers={"Accept": "application/json", "User-Agent": "curl/8.7.1"})
        with urllib.request.urlopen(r, timeout=90) as resp:
            deals = json.load(resp).get("deals", [])
    except Exception as e:
        print(f"    (evergreen deals unavailable for {slug}: {str(e)[:60]})")
        return {}
    by_phone = {}
    for d in deals:
        k = norm(d.get("phone"))
        if k:
            by_phone.setdefault(k, d)  # first (most recent) wins
    return by_phone


def deal_is_warm(d):
    return d.get("stage") in WARM_STAGES or bool(d.get("positive_reply_category"))
def deal_is_booked(d):
    return bool(d.get("meeting_booked_at")) or d.get("stage") in BOOKED_STAGES


# ---------------------------------------------------------------- per-client scan
def scan_client(key, cfg, since_date):
    sms = cfg.get("sms") or {}
    if sms.get("platform") != "ghl" or not sms.get("mcp") or not sms.get("locationId"):
        print(f"[{key}] no GHL SMS channel — skipped")
        return None
    try:
        pit = gm.creds_from_mcp(sms["mcp"])
    except SystemExit:
        print(f"[{key}] token for '{sms['mcp']}' not in ~/.claude.json — SKIPPED")
        return None
    loc = sms["locationId"]
    label = cfg.get("label", key)
    print(f"\n[{label}] location {loc} — messages since {since_date}")
    msgs = gm.get_messages(pit, loc, since_date)
    print(f"  {len(msgs):,} SMS messages")
    if not msgs:
        return {"key": key, "label": label, "contacts": 0, "repliers": 0, "flagged": 0,
                "flagged_repliers": 0, "pct_repliers_split": 0.0, "warm_split": 0,
                "bookings_at_risk": 0, "modes": {}, "rows": []}

    contacts = group_contacts(msgs)
    flagged = {cid: c for cid, c in contacts.items() if len(c["our_numbers"]) > 1}
    repliers = [c for c in contacts.values() if c["has_inbound"]]
    flagged_repliers = [c for c in flagged.values() if c["has_inbound"]]

    deals = fetch_deals(EV_SLUG.get(key))

    rows, modes, swaps = [], Counter(), Counter()
    warm_split = risk = 0
    for cid, c in flagged.items():
        mode = failure_mode(c)
        modes[mode] += 1
        for later in c["later"]:
            swaps[(c["opener"], later)] += 1
        d = deals.get(norm(c["lead_phone"]))
        warm = bool(d) and deal_is_warm(d)
        booked = bool(d) and deal_is_booked(d)
        if warm:
            warm_split += 1
            if not booked:
                risk += 1
        rows.append({
            "contact": (d or {}).get("contact") or (d or {}).get("opportunity") or "",
            "company": (d or {}).get("company") or "",
            "job_title": (d or {}).get("job_title") or "",
            "lead_phone": pretty(c["lead_phone"]),
            "stage": (d or {}).get("stage") or ("(no deal)" if not d else ""),
            "reply_category": (d or {}).get("positive_reply_category") or "",
            "campaign": ((d or {}).get("campaign_name") or "")[:45],
            "n_numbers": len(c["our_numbers"]),
            "numbers": " → ".join(pretty(n) for n in ([c["opener"]] + c["later"])),
            "failure_mode": mode,
            "reply_from_diff_number": c["reply_diff_number"],
            "warm": warm, "booked": booked,
            "conv_ids": len(c["conv_ids"]),
            "first_seen": c["first"], "last_seen": c["last"],
        })
    # warm-and-unbooked first, then warm, then the rest; each by reply-touch
    rows.sort(key=lambda r: (not (r["warm"] and not r["booked"]), not r["warm"],
                             not r["reply_from_diff_number"], r["company"] == ""))

    # write per-client csv
    out_dir = os.path.join(gm.ROOT, cfg.get("output", f"clients/{key}/output"))
    os.makedirs(out_dir, exist_ok=True)
    if rows:
        with open(os.path.join(out_dir, "number-split.csv"), "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader(); w.writerows(rows)

    pct = round(100 * len(flagged_repliers) / max(1, len(repliers)), 1)
    res = {"key": key, "label": label, "contacts": len(contacts), "repliers": len(repliers),
           "flagged": len(flagged), "flagged_repliers": len(flagged_repliers),
           "pct_repliers_split": pct, "warm_split": warm_split, "bookings_at_risk": risk,
           "modes": dict(modes), "swaps": swaps, "rows": rows, "out_dir": out_dir}

    # ---- View A + View B print
    print(f"  contacts {len(contacts):,} · repliers {len(repliers):,} · "
          f"FLAGGED {len(flagged):,} ({pct}% of repliers) · modes {dict(modes)}")
    warm_rows = [r for r in rows if r["warm"]]
    if warm_rows:
        print(f"  ⚠ {len(warm_rows)} WARM leads hit a number split "
              f"({risk} interested but NOT booked):")
        for r in warm_rows[:12]:
            book = "BOOKED" if r["booked"] else "no-book"
            who = f"{r['contact'] or '?'} @ {r['company'] or '?'}"[:38]
            print(f"      {book:7} {r['stage'][:16]:16} {who:38} {r['numbers']}  [{r['failure_mode']}]")
    if swaps:
        print("  top number swaps (opener → later):")
        for (a, b), n in swaps.most_common(5):
            print(f"      {pretty(a)} → {pretty(b)}   ×{n}")
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--clients", help="comma list of registry keys (default: all GHL-SMS clients)")
    ap.add_argument("--since", type=int, default=45, help="days back (default 45)")
    ap.add_argument("--all", action="store_true", help="full history (overrides --since)")
    a = ap.parse_args()

    reg = {k: v for k, v in json.load(open(gm.REGISTRY)).items() if not k.startswith("_")}
    if a.clients:
        keys = [k.strip() for k in a.clients.split(",")]
    else:
        keys = [k for k, v in reg.items()
                if (v.get("sms") or {}).get("platform") == "ghl"
                and (v.get("sms") or {}).get("mcp") and (v.get("sms") or {}).get("locationId")]
    since_date = "2019-01-01" if a.all else (
        dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=a.since)).strftime("%Y-%m-%d")

    print(f"Scanning {len(keys)} client(s) for split-number conversations since {since_date}:")
    print("  " + ", ".join(keys))
    results, skipped = [], []
    for k in keys:
        if k not in reg:
            print(f"[{k}] not in registry — skipped"); skipped.append(k); continue
        r = scan_client(k, reg[k], since_date)
        (results if r else skipped).append(r if r else k)

    results = [r for r in results if r]
    # ---- View C: cross-client rollup
    print("\n" + "=" * 78)
    print("VIEW C — CROSS-CLIENT ROLLUP (is it board-wide?)")
    print("=" * 78)
    hdr = f"{'client':16} {'contacts':>9} {'repliers':>9} {'flagged':>8} {'%repl':>6} {'warm':>5} {'@risk':>6}  mode"
    print(hdr); print("-" * len(hdr))
    for r in sorted(results, key=lambda x: -x["pct_repliers_split"]):
        dom = max(r["modes"].items(), key=lambda x: x[1])[0] if r["modes"] else "-"
        print(f"{r['label'][:16]:16} {r['contacts']:>9,} {r['repliers']:>9,} {r['flagged']:>8,} "
              f"{r['pct_repliers_split']:>5}% {r['warm_split']:>5} {r['bookings_at_risk']:>6}  {dom}")
    tot_risk = sum(r["bookings_at_risk"] for r in results)
    tot_flag = sum(r["flagged"] for r in results)
    print("-" * len(hdr))
    print(f"TOTAL flagged conversations: {tot_flag:,} · warm leads at risk (interested, not booked): {tot_risk}")
    if skipped:
        print(f"\nSKIPPED (no token/registry): {', '.join(str(s) for s in skipped)}")

    roll_dir = os.path.join(gm.ROOT, "clients", "_rollup")
    os.makedirs(roll_dir, exist_ok=True)
    with open(os.path.join(roll_dir, "number-split-rollup.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["client", "contacts", "repliers", "flagged", "pct_repliers_split",
                    "warm_split", "bookings_at_risk", "modes"])
        for r in results:
            w.writerow([r["label"], r["contacts"], r["repliers"], r["flagged"],
                        r["pct_repliers_split"], r["warm_split"], r["bookings_at_risk"],
                        json.dumps(r["modes"])])
    print(f"\nwrote clients/_rollup/number-split-rollup.csv + per-client number-split.csv")


if __name__ == "__main__":
    main()
