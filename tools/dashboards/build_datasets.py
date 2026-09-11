#!/usr/bin/env python3
"""Merge GHL batches + EmailBison + Evergreen into one dashboard dataset per client."""
import json, os, re, sys, datetime as dt
from collections import defaultdict

ROOT = "/Users/aamanahmed/ICP-development"
SP = os.path.dirname(os.path.abspath(__file__))
EV = os.path.join(SP, "evergreen")
OUT = os.path.join(SP, "data")
os.makedirs(OUT, exist_ok=True)

REG = json.load(open(f"{ROOT}/clients/registry.json"))
CLIENTS = ["gofish", "leadgenix", "strike-tax", "growth-lab", "redo", "kynship"]

UNCONVERTED = {"Positive Reply", '"Maybe"', "Maybe", "No Show"}
CONVERTED = {"Meeting Booked", "Show", "Won"}


def month_of(iso):
    return iso[:7] if iso else None


def month_range(start, end):
    y, m = int(start[:4]), int(start[5:7])
    ey, em = int(end[:4]), int(end[5:7])
    out = []
    while (y, m) <= (ey, em):
        out.append(f"{y:04d}-{m:02d}")
        m += 1
        if m == 13: y, m = y + 1, 1
    return out


def months_overlap(first, last):
    """Months a batch was live in (from its first/last send dates)."""
    if not first: return []
    return month_range(first[:7] + "-01", (last or first)[:7] + "-01")


def norm(t):
    return re.sub(r"\s+", " ", re.sub(r"\{\{[^}]*\}\}|\{[^}|]*\}", "", (t or "").lower())).strip()


def sim(a, b):
    """Cheap token-overlap similarity for copy matching."""
    ta, tb = set(norm(a).split()), set(norm(b).split())
    if not ta or not tb: return 0.0
    return len(ta & tb) / min(len(ta), len(tb))


def load(path):
    try:
        return json.load(open(path))
    except Exception:
        return None


def build(client):
    cfg = REG.get(client, {})
    outdir = os.path.join(ROOT, cfg.get("output", f"clients/{client}/output"))
    batches = load(os.path.join(outdir, "batches.json")) or []
    eb = load(os.path.join(outdir, "emailbison.json")) or {"campaigns": []}
    ev = load(os.path.join(EV, f"{client}.json")) or {}

    stats = ev.get("stats") if isinstance(ev.get("stats"), dict) else {}
    kpi = (stats.get("stats") or {}).get("kpi") or {}
    periods = (stats.get("stats") or {}).get("periods") or {}
    live_campaigns = stats.get("campaigns") or []
    deals = (ev.get("deals") or {}).get("deals") or []
    replies_meta = ev.get("replies") if isinstance(ev.get("replies"), dict) else {}
    copies = (ev.get("copies") or {}).get("copies") or []
    ev_missing = not deals and not kpi

    # ---- monthly scoreboard ----
    # "positives" matches the Airtable KPI counter: excludes Disqualified AND "Maybe"
    # (verified against the live This-Month stats for go_fish: 18 = 27 deals - 9 Maybe)
    pos_by_m, booked_by_m, maybe_by_m = defaultdict(int), defaultdict(int), defaultdict(int)
    for d in deals:
        m = month_of(d.get("created_at"))
        if not m: continue
        if d.get("stage") in ('"Maybe"', "Maybe"):
            maybe_by_m[m] += 1
        elif d.get("stage") != "Disqualified":
            pos_by_m[m] += 1
        booked_m = month_of(d.get("meeting_booked_at")) or m
        if d.get("stage") in CONVERTED | {"No Show"}:
            booked_by_m[booked_m] += 1

    camps_by_m = defaultdict(set)          # campaign names live per month
    sms_sent_by_m = defaultdict(float)     # approx: prospects*2 spread over live days
    for b in batches:
        f, l = b.get("first_sent"), b.get("last_sent") or b.get("first_sent")
        if not f: continue
        days = max((dt.date.fromisoformat(l) - dt.date.fromisoformat(f)).days + 1, 1)
        per_day = b["prospects"] * b.get("texts_in_batch", 2) / days
        cur = dt.date.fromisoformat(f)
        endd = dt.date.fromisoformat(l)
        while cur <= endd:
            sms_sent_by_m[cur.isoformat()[:7]] += per_day
            camps_by_m[cur.isoformat()[:7]].add(b["campaign"])
            cur += dt.timedelta(days=1)
    # real monthly email volume, from the per-month EmailBison stats pull
    email_by_m = defaultdict(lambda: {"sent": 0, "replies": 0, "interested": 0})
    for c in eb["campaigns"]:
        for m, s in (c.get("monthly") or {}).items():
            camps_by_m[m].add(c["name"] + " (email)")
            email_by_m[m]["sent"] += s.get("sent") or 0
            email_by_m[m]["replies"] += s.get("replies") or 0
            email_by_m[m]["interested"] += s.get("interested") or 0
        if not c.get("monthly") and (c.get("sent") or 0) > 0:
            m = month_of(c.get("created_at"))          # fallback: no per-month data
            if m:
                camps_by_m[m].add(c["name"] + " (email)")

    all_months = sorted(set(list(pos_by_m) + list(booked_by_m) + list(camps_by_m) + list(email_by_m)))
    monthly = []
    tgt_pos = round(kpi["weeklyPositives"] * 52 / 12, 1) if kpi.get("weeklyPositives") else None
    tgt_book = kpi.get("monthlyBooked")
    for m in all_months:
        pos, bkd = pos_by_m.get(m, 0), booked_by_m.get(m, 0)
        em = email_by_m.get(m, {})
        monthly.append({
            "month": m,
            "campaigns": sorted(camps_by_m.get(m, [])),
            "sms_sent_est": int(sms_sent_by_m.get(m, 0)),
            "email_sent": em.get("sent", 0),
            "email_replies": em.get("replies", 0),
            "email_interested": em.get("interested", 0),
            "positives": pos, "maybes": maybe_by_m.get(m, 0), "booked": bkd,
            "pos_target": tgt_pos, "book_target": tgt_book,
            "pos_hit": (pos >= tgt_pos) if tgt_pos else None,
            "book_hit": (bkd >= tgt_book) if tgt_book else None,
        })

    # ---- missed positive replies ----
    missed = []
    for d in deals:
        if d.get("stage") in UNCONVERTED:
            missed.append({
                "stage": d.get("stage"), "category": d.get("positive_reply_category"),
                "contact": d.get("contact"), "company": d.get("company"),
                "job_title": d.get("job_title"), "channel": d.get("channel"),
                "variant": d.get("copy_variant"), "campaign": d.get("campaign_name"),
                "created_at": (d.get("created_at") or "")[:10],
                "phone": d.get("phone"), "email": d.get("email"),
                "conversation": (d.get("conversation") or "")[:600],
            })
    missed.sort(key=lambda x: x["created_at"], reverse=True)

    # ---- evergreen copy cross-check (per GHL batch, best match) ----
    seen_t1 = {}
    for b in batches:
        key = norm(b["T1"])[:150]
        if key in seen_t1: continue
        best, best_s = None, 0.0
        for cp in copies:
            s = max(sim(b["T1"], cp.get("t1")), sim(b["T2"], cp.get("t2")))
            if s > best_s: best, best_s = cp, s
        seen_t1[key] = {
            "t1_preview": b["T1"][:110],
            "in_evergreen": best_s >= 0.6,
            "ev_status": (best or {}).get("status"),
            "ev_lever": (best or {}).get("lever"),
            "match_score": round(best_s, 2),
        }
    crosscheck = list(seen_t1.values())

    data = {
        "client": client, "label": cfg.get("label", client),
        "built_at": dt.datetime.now(dt.timezone.utc).isoformat()[:16],
        "kpi": kpi, "periods": periods, "ev_missing": ev_missing,
        "monthly": monthly,
        "sms_batches": batches,
        "email_campaigns": eb["campaigns"],
        "live_campaigns": live_campaigns,
        "missed": missed,
        "reply_categories": replies_meta.get("by_category_all_time") or [],
        "crosscheck": crosscheck,
        "ev_copy_count": len(copies),
    }
    json.dump(data, open(f"{OUT}/{client}.json", "w"), indent=1)
    return (f"{client}: months={len(monthly)} batches={len(batches)} "
            f"email_camps={len(eb['campaigns'])} missed={len(missed)} "
            f"deals_pos_total={sum(pos_by_m.values())} ev_missing={ev_missing}")


for c in (sys.argv[1:] or CLIENTS):
    try:
        print(build(c))
    except Exception as e:
        print(f"{c}: FAILED {e}")
