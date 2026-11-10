#!/usr/bin/env python3
"""Pull one day of Scaletopia's own outbound (SMS + email) and every reply since.

Usage:
  python3 daily_pull.py                     # yesterday (previous weekday, US/Pacific)
  python3 daily_pull.py 2026-10-23          # a send day
  python3 daily_pull.py 2026-10-23 --through 2026-10-25   # replies counted to this day (default: today)
  python3 daily_pull.py ... --out DIR       # where to save raw json + report.json (default: /tmp/scaletopia-daily)

Prints a plain-text digest: sends by campaign (first-text template), every human reply with
name/company/title/ICP signal/what we sent after, STOP counts, email sends and non-auto replies,
and Evergreen's view. The judging (warm or not) is done by Claude from this output, not here.

Credentials come from ~/.claude.json MCP entries (ghl-scaletopia, ghl-scaletopia-legacy,
emailbison-scaletopia) and EVERGREEN_API_KEY in the repo .env. Nothing is printed.
"""
import argparse, collections, datetime as dt, json, os, re, sys, time, urllib.parse, urllib.request
from concurrent.futures import ThreadPoolExecutor

def _find_repo():
    """Repo root: the clone this skill sits in, else the current folder, else ~/ICP-development."""
    here = os.path.abspath(__file__)
    for _ in range(6):
        here = os.path.dirname(here)
        if os.path.exists(os.path.join(here, ".git")):
            return here
    if os.path.exists(".git"):
        return os.getcwd()
    return os.path.expanduser("~/ICP-development")
REPO = _find_repo()
API = "https://services.leadconnectorhq.com"
LOCS = {"ghl-scaletopia-legacy": "UqMcuYNiET94KiGWH5Ec",   # A2P local numbers (619 etc.)
        "ghl-scaletopia": "TYVYHj7lX8bamHkOKz4s"}          # toll-free, shared with Velox before Aug 3
EVERGREEN = "https://knowledgebase-production-f52e.up.railway.app"
from zoneinfo import ZoneInfo
LA = ZoneInfo("America/Los_Angeles")  # send-day boundaries follow US Pacific, DST handled

def _load_cfg():
    """MCP server entries from ~/.claude.json: user scope first, then any project/local scope."""
    raw = json.load(open(os.path.expanduser("~/.claude.json")))
    cfg = dict(raw.get("mcpServers", {}))
    for proj in raw.get("projects", {}).values():
        for k, v in (proj.get("mcpServers") or {}).items():
            cfg.setdefault(k, v)
    need = ["ghl-scaletopia-legacy", "ghl-scaletopia", "emailbison-scaletopia"]
    missing = [k for k in need if k not in cfg]
    if missing:
        sys.exit(f"Missing MCP servers {missing}. Run: bash tools/setup_scaletopia_stats.sh <keys file>")
    return cfg
CFG = _load_cfg()
def ghl_token(srv):
    return CFG[srv]["headers"]["Authorization"].split(" ", 1)[1]

def http(url, headers, method="GET", body=None, tries=5):
    for t in range(tries):
        try:
            req = urllib.request.Request(url, data=json.dumps(body).encode() if body else None,
                                         method=method, headers=headers)
            with urllib.request.urlopen(req, timeout=90) as r:
                return json.load(r)
        except Exception as e:
            err = e
            time.sleep(4 * (t + 1))
    raise err

# ---------------- GHL ----------------
def day_bounds(d):
    f = "%Y-%m-%dT%H:%M:%S.000Z"
    s = dt.datetime.combine(d, dt.time(), LA).astimezone(dt.timezone.utc)
    e = dt.datetime.combine(d + dt.timedelta(days=1), dt.time(), LA).astimezone(dt.timezone.utc)
    return s.strftime(f), e.strftime(f)

CACHE = "/tmp/scaletopia-daily/ghl_cache"

def export_day(srv, d, today):
    """Export one PT day. GHL sometimes returns an empty or short day under load, so
    compare against its own `total` and retry until they match. Finished days are cached."""
    cf = f"{CACHE}/{srv}_{d}.json"
    if d < today - dt.timedelta(days=1) and os.path.exists(cf):
        got = json.load(open(cf)); return got, len(got)
    s, e = day_bounds(d)
    # Empty is normal on weekends and early today, so only a past weekday gets the full
    # 5 tries when it comes back empty (toll-free too: on Oct 28 it glitched to 0 of 4).
    expect_sends = d.weekday() < 5 and d <= today
    H = {"Authorization": "Bearer " + ghl_token(srv), "Version": "2021-04-15",
         "Accept": "application/json", "User-Agent": "scaletopia-daily/1.0"}
    best, total = {}, None
    for attempt in range(5):
        got, cur = {}, None
        while True:
            q = dict(locationId=LOCS[srv], channel="SMS", limit=1000, sortBy="createdAt",
                     sortOrder="desc", startDate=s, endDate=e)
            if cur: q["cursor"] = cur
            r = http(API + "/conversations/messages/export?" + urllib.parse.urlencode(q), H)
            total = r.get("total", total)
            for m in r.get("messages", []): got[m["id"]] = m
            cur = r.get("nextCursor")
            if not cur: break
        if len(got) > len(best): best = got
        # The glitch can also answer total=0 for a busy day, so an empty day is
        # only believed after every retry comes back empty.
        if best and total is not None and len(best) >= total: break
        if not best and not expect_sends and attempt >= 1: break
        time.sleep(4 if expect_sends else 2)
    out = list(best.values())
    if d < today and total is not None and len(out) >= total and (out or d.weekday() > 4):
        os.makedirs(CACHE, exist_ok=True); json.dump(out, open(cf, "w"))
    return out, total

def contact(srv, cid):
    H = {"Authorization": "Bearer " + ghl_token(srv), "Version": "2021-07-28",
         "Accept": "application/json", "User-Agent": "scaletopia-daily/1.0"}
    try:
        return http(f"{API}/contacts/{cid}", H, tries=2).get("contact", {})
    except Exception:
        return {}

def evergreen_deals():
    key = next((l.split("=", 1)[1].strip().strip('"') for l in open(f"{REPO}/.env") if l.startswith("EVERGREEN_API_KEY=")), "")
    GH = {"Authorization": "Bearer " + key, "User-Agent": "curl/8.7.1"}
    D = http(f"{EVERGREEN}/api/clients/scaletopia/deals?limit=5000", GH)
    return D.get("deals", D)

T = lambda s: dt.datetime.fromisoformat(s.replace("Z", "+00:00"))
STOP = re.compile(r"^\s*(stop\w*|unsubscribe|remove( me)?|end|quit|cancel|stop2end)[\s.!]*$", re.I)
AUTO_SMS = ("thank you for texting", "thanks for reaching out to", "currently out", "will respond shortly",
            "this number is no longer in", "auto-reply", "autoreply")

def template_key(body):
    """Name a first text by its skeleton: drop the greeting + first name and the company slot."""
    b = (body or "").replace("\xa0", " ")
    b = re.sub(r"^(hi|hey|hello|happy \w+|how's it going|morning|evening)\s+[^,]{0,30},\s*", "", b, flags=re.I)
    b = re.sub(r"been looking at [^,]*,", "been looking at {co},", b, flags=re.I)
    return b[:70]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("date", nargs="?")
    ap.add_argument("--through")
    ap.add_argument("--out", default="/tmp/scaletopia-daily")
    a = ap.parse_args()
    today = dt.datetime.now(LA).date()
    if a.date:
        day = dt.date.fromisoformat(a.date)
    else:
        day = today - dt.timedelta(days=1)
        while day.weekday() > 4: day -= dt.timedelta(days=1)
    through = dt.date.fromisoformat(a.through) if a.through else today
    os.makedirs(a.out, exist_ok=True)

    # 1) GHL: the send day plus every day through `through` (for replies), both accounts
    days = [day + dt.timedelta(days=i) for i in range((through - day).days + 1)]
    lookback = [day - dt.timedelta(days=i) for i in range(1, 5)]  # to place replies to earlier sends
    msgs, totals = {}, {}
    # Evergreen and EmailBison don't depend on GHL, so start them now
    side = ThreadPoolExecutor(4)
    ev_f = side.submit(evergreen_deals)
    # one worker per account: parallel hits on the same account cause the short-day glitch
    def pull(srv): return [(d, export_day(srv, d, today)) for d in days + lookback]
    with ThreadPoolExecutor(len(LOCS)) as ex:
        for srv, res in zip(LOCS, ex.map(pull, LOCS)):
            for d, (got, tot) in res:
                totals[(srv, d.isoformat())] = (len(got), tot)
                for m in got: m["_srv"] = srv; msgs[m["id"]] = m
    M = sorted(msgs.values(), key=lambda m: m["dateAdded"])
    json.dump(M, open(f"{a.out}/ghl_{day}.json", "w"))
    ptday = lambda m: T(m["dateAdded"]).astimezone(LA).date()

    # 2) Batches = workflow texts to one contact within 5 minutes (text 1 + text 2)
    out = [m for m in M if m["direction"] == "outbound" and m.get("source") == "workflow"]
    byc = collections.defaultdict(list)
    for m in out: byc[m["contactId"]].append(m)
    batches = []  # (contactId, day, key, [msgs])
    for cid, ms in byc.items():
        i = 0
        while i < len(ms):
            j = i
            while j + 1 < len(ms) and (T(ms[j + 1]["dateAdded"]) - T(ms[j]["dateAdded"])).total_seconds() <= 300:
                j += 1
            batches.append((cid, ptday(ms[i]), template_key(ms[i]["body"]), ms[i:j + 1]))
            i = j + 1
    sendday = [b for b in batches if b[1] == day]
    camp = collections.defaultdict(lambda: {"people": set(), "texts": 0, "failed": 0, "blank": 0, "from": collections.Counter(), "text2": collections.Counter()})
    for cid, d, k, ms in sendday:
        c = camp[k]; c["people"].add(cid); c["texts"] += len(ms)
        c["failed"] += sum(m.get("status") in ("failed", "undelivered") for m in ms)
        c["blank"] += bool(re.search(r"looking at\s*,|\s,\s*had an idea", ms[0]["body"] or ""))
        c["from"][ms[0].get("from") or "?"] += 1
        if len(ms) > 1: c["text2"][re.sub(r"go after .*? - could", "go after {signal} - could", (ms[1]["body"] or "").replace("\n", " "))[:90]] += 1
    print(f"=== SCALETOPIA DAILY · send day {day} (PT) · replies through {through} ===\n")
    print("GHL day totals (ours / GHL total):", {f"{s.split('-')[-1]} {d}": v for (s, d), v in totals.items() if d >= day.isoformat()})
    print("\n## SMS sends by first-text template")
    tot_p = tot_t = 0
    for k, c in sorted(camp.items(), key=lambda kv: -len(kv[1]["people"])):
        p = len(c["people"]); tot_p += p; tot_t += c["texts"]
        if p < 3: continue
        print(f"- {p} people · {c['texts']} texts · failed {c['failed']/max(c['texts'],1):.1%} · blank company {c['blank']} · from {dict(c['from'])}")
        print(f"    text1: {k!r}")
        for t2, n in c["text2"].most_common(2): print(f"    text2 ({n}): {t2!r}")
    small = [k for k, c in camp.items() if len(c["people"]) < 3]
    print(f"TOTAL {tot_p} people · {tot_t} texts (+{len(small)} one-off templates, e.g. no-show/reschedule texts)")

    # 3) Replies from the send day through `through`
    start = dt.datetime.fromisoformat(day_bounds(day)[0].replace("Z", "+00:00"))
    inb = [m for m in M if m["direction"] == "inbound" and T(m["dateAdded"]) >= start]
    rbyc = collections.defaultdict(list)
    for m in inb: rbyc[m["contactId"]].append(m)
    cohort_of = {}
    for cid, d, k, ms in batches: cohort_of.setdefault(cid, []).append((d, k))
    print("\n## Replies (human ones listed; STOPs and auto-replies counted)")
    counts = collections.Counter(); rows = []
    human = [(cid, ms) for cid, ms in rbyc.items() if not all(STOP.match(m["body"] or "") for m in ms)]
    with ThreadPoolExecutor(10) as ex:
        people = dict(zip([c for c, _ in human], ex.map(lambda x: contact(x[1][0]["_srv"], x[0]), human)))
    for cid, ms in rbyc.items():
        coh = [c for c in cohort_of.get(cid, []) if c[0] <= ptday(ms[0])]
        coh = coh[-1] if coh else ("older", "?")
        bodies = [m["body"] or "" for m in ms]
        kind = "stop" if all(STOP.match(b) for b in bodies) else "auto" if any(x in " ".join(bodies).lower() for x in AUTO_SMS) else "human"
        label = f"{coh[0]} · {coh[1][:40]}"
        counts[(label, kind)] += 1
        if kind != "human": continue
        c = people.get(cid) or contact(ms[0]["_srv"], cid)
        cf = [v.get("value") for v in c.get("customFields", []) if isinstance(v.get("value"), str)]
        after = [m for m in M if m["contactId"] == cid and m["direction"] == "outbound" and m.get("source") != "workflow" and m["dateAdded"] > ms[0]["dateAdded"]]
        last = after[-1]["body"][:110].replace("\n", " ") if after else "NO REPLY FROM US"
        sig = [m["body"] for m in M if m["contactId"] == cid and m["direction"] == "outbound" and "go after" in (m["body"] or "")]
        rows.append(dict(cohort=label, name=f"{c.get('firstName','')} {c.get('lastName','')}".strip(), company=c.get("companyName"),
                         email=c.get("email"), phone=c.get("phone"), fields=[x for x in cf if len(x) < 70][:4],
                         replies=" || ".join(b.replace("\n", " ") for b in bodies), ours_after=last,
                         signal=re.sub(r".*go after (.*?) - could.*", r"\1", sig[-1].replace("\n", " ")) if sig else None))
    for r in sorted(rows, key=lambda r: r["cohort"]):
        print(f"\n[{r['cohort']}] {r['name']} | {r['company']} | {r['fields']} | {r['email']} {r['phone']}")
        if r["signal"]: print(f"   signal sent: {r['signal']}")
        print(f"   THEY: {r['replies'][:400]}")
        print(f"   US AFTER: {r['ours_after']}")
    print("\nReply counts by cohort:")
    for (lab, kind), n in sorted(counts.items()): print(f"   {lab} · {kind}: {n}")

    # 4) Email (EmailBison)
    h = CFG["emailbison-scaletopia"]["headers"]
    EB = h["Instance-URL"].rstrip("/"); auth = h["Authorization"] if h["Authorization"].startswith("Bearer") else "Bearer " + h["Authorization"]
    EH = {"Authorization": auth, "Content-Type": "application/json", "Accept": "application/json", "User-Agent": "curl/8.7.1"}
    eb = lambda p, m="GET", b=None: http(EB + p, EH, m, b)
    print("\n## Email")
    w = eb(f"/api/workspaces/v1.1/stats?start_date={day}&end_date={day}"); w = w.get("data", w)
    print(f"Workspace {day}: sent {w.get('emails_sent')} · leads {w.get('total_leads_contacted')} · replies {w.get('unique_replies_per_contact')} · bounced {w.get('bounced')}")
    camps, p = [], 1
    while True:
        r = eb(f"/api/campaigns?page={p}"); camps += r["data"]
        if p >= r["meta"]["last_page"]: break
        p += 1
    AUTO_EM = ("out of office", "out of the office", "ooo", "on leave", "away", "pto", "no longer with", "delivery status",
               "address not found", "currently out", "maternity", "paternity", "parental leave", "ticket number", "not monitored", "moving email")
    recent = str(day - dt.timedelta(days=3))
    camps = [c for c in camps if c.get("status") in ("active", "paused", "launching") or (c.get("updated_at") or "")[:10] >= recent]
    def cstats(c):
        try:
            s = eb(f"/api/campaigns/{c['id']}/stats", "POST", {"start_date": str(day), "end_date": str(day)}); return s.get("data", s)
        except Exception:
            return {}
    with ThreadPoolExecutor(8) as ex: allstats = list(ex.map(cstats, camps))
    for c, s in zip(camps, allstats):
        if not s.get("emails_sent"): continue
        left = (c.get("total_leads") or 0) - (c.get("total_leads_contacted") or 0)
        print(f"- {c['id']} {c['name'][:70]} [{c['status']}] sent {s.get('emails_sent')} · replies {s.get('unique_replies_per_contact')} · leads left {left}")
        rep = eb(f"/api/campaigns/{c['id']}/replies").get("data", [])
        for x in rep:
            d = (x.get("date_received") or "")[:10]
            body = (x.get("text_body") or "").replace("\n", " ")
            if d < str(day) or d > str(through) or "scaletopia" in (x.get("from_email_address") or "") or any(k in body.lower()[:300] for k in AUTO_EM):
                continue
            if x.get("from_email_address", "").split("@")[-1].endswith((".co",)) and "Scaletopia" in body[:200]:
                continue  # our own inbox replying in thread
            print(f"     {d} {x.get('from_email_address')}: {body[:300]}")

    # 5) Evergreen (cross-check only: its sends are understated, /period lags a day)
    D = ev_f.result()
    print("\n## Evergreen deals created or booked since the send day")
    for x in sorted(D, key=lambda x: x.get("created_at") or ""):
        if (x.get("created_at") or "")[:10] >= str(day) or (x.get("meeting_booked_at") or "")[:10] >= str(day):
            print(f"- {x['created_at'][:10]} {x.get('channel')} {x['stage']} booked:{(x.get('meeting_booked_at') or '')[:10]} {x['opportunity']} | {x.get('company')} | {(x.get('campaign_name') or '')[:45]}")
    json.dump(dict(day=str(day), through=str(through), rows=rows), open(f"{a.out}/report_{day}.json", "w"), default=str)

if __name__ == "__main__":
    main()
