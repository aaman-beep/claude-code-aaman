#!/usr/bin/env python3
"""Quick answers to the side questions that come up after the daily stats.

Usage (from the repo root):
  python3 .claude/skills/scaletopia-daily-stats/scripts/side_checks.py rehit 2026-11-09 [--days 45]
      Were the people texted on that day already texted before? Split by first-text copy and number.
  python3 .claude/skills/scaletopia-daily-stats/scripts/side_checks.py email 2026-11-02 [2026-11-08]
      Emails sent, replies and bounces for a day or a date range (EmailBison workspace).
  python3 .claude/skills/scaletopia-daily-stats/scripts/side_checks.py inboxes
      Every sending inbox in EmailBison, grouped by tag: how many, connected, daily limit, sent, bounced, replied.

Uses the same keys as daily_pull.py. Prints no keys.
"""
import collections, datetime as dt, importlib.util, json, os, sys, urllib.request

spec = importlib.util.spec_from_file_location("dp", os.path.join(os.path.dirname(__file__), "daily_pull.py"))
dp = importlib.util.module_from_spec(spec); spec.loader.exec_module(dp)


def first_text_key(body):
    b = body or ""
    if "had an idea" not in b:
        return None
    if "helped Redo" in b: return "Redo 'helped' (old tech copy)"
    if "Chamber" in b: return "Chamber"
    if "qualified de" in b: return "Redo demos"
    if "qualified ca" in b: return "Redo calls"
    return b.split("had an idea.")[-1][:45].strip()


def rehit(day, days_back=45):
    d = dt.date.fromisoformat(day); today = dt.datetime.now(dp.LA).date()
    groups = collections.defaultdict(set); frm = collections.defaultdict(collections.Counter)
    for srv in dp.LOCS:
        msgs, _ = dp.export_day(srv, d, today)
        for m in msgs:
            if m.get("direction") != "outbound": continue
            k = first_text_key(m.get("body"))
            if k: groups[k].add(m["contactId"]); frm[k][m.get("from")] += 1
    prev = collections.defaultdict(set)
    for i in range(1, days_back + 1):
        pd = d - dt.timedelta(days=i)
        for srv in dp.LOCS:
            msgs, _ = dp.export_day(srv, pd, today)
            for m in msgs:
                if m.get("direction") == "outbound": prev[m["contactId"]].add(str(pd))
    print(f"People texted a first text on {day}, checked against the previous {days_back} days:\n")
    for k, s in sorted(groups.items(), key=lambda x: -len(x[1])):
        hit = [c for c in s if prev.get(c)]
        last = collections.Counter(max(prev[c]) for c in hit).most_common(3)
        nums = ", ".join(f"{n} ({c})" for n, c in frm[k].most_common(3))
        print(f"- {k}: {len(s)} people from {nums}. Texted before: {len(hit)}. Most recent earlier text: {last}")
    allc = [c for s in groups.values() for c in s]
    dup = [c for c, n in collections.Counter(allc).items() if n > 1]
    print(f"\nPeople who got two different first texts on {day}: {len(dup)}")


def bison():
    h = dp.CFG["emailbison-scaletopia"]["headers"]
    base = h["Instance-URL"].rstrip("/")
    auth = h["Authorization"] if h["Authorization"].startswith("Bearer") else "Bearer " + h["Authorization"]
    H = {"Authorization": auth, "Accept": "application/json", "User-Agent": "curl/8.7.1"}
    return lambda path: json.load(urllib.request.urlopen(urllib.request.Request(base + path, headers=H), timeout=90))


def email(start, end=None):
    get = bison(); end = end or start
    j = get(f"/api/workspaces/v1.1/stats?start_date={start}&end_date={end}")["data"]
    keep = ["emails_sent", "total_leads_contacted", "unique_replies_per_contact", "bounced", "interested"]
    print(f"Email {start} to {end}: " + ", ".join(f"{k} {j.get(k)}" for k in keep))
    print("(interested is always 0, nobody tags replies. Read the replies.)")


def inboxes():
    get = bison(); rows, p = [], 1
    while True:
        j = get(f"/api/sender-emails?per_page=100&page={p}")
        rows += j["data"]
        if p >= j.get("meta", {}).get("last_page", 1): break
        p += 1
    g = collections.defaultdict(collections.Counter)
    for s in rows:
        tags = sorted(t["name"] for t in s["tags"] if t["name"] not in ("Google",))
        c = g[" + ".join(tags) or "(no tag)"]
        c["inboxes"] += 1
        c["connected"] += s["status"] == "Connected"
        c["daily limit"] += s["daily_limit"] if s["status"] == "Connected" else 0
        c["sent"] += s["emails_sent_count"] or 0
        c["bounced"] += s["bounced_count"] or 0
        c["replied"] += s["unique_replied_count"] or 0
    print(f"{len(rows)} inboxes in EmailBison\n")
    for k, c in sorted(g.items(), key=lambda x: -x[1]["inboxes"]):
        print(f"- {k}: " + ", ".join(f"{n} {c[n]}" for n in ["inboxes", "connected", "daily limit", "sent", "bounced", "replied"]))


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a: sys.exit(__doc__)
    if a[0] == "rehit": rehit(a[1], int(a[a.index("--days") + 1]) if "--days" in a else 45)
    elif a[0] == "email": email(a[1], a[2] if len(a) > 2 else None)
    elif a[0] == "inboxes": inboxes()
    else: sys.exit(__doc__)
