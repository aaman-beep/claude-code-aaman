#!/usr/bin/env python3
"""Build a contact-level register of every categorised cold-SMS reply in a month.

WHY THIS EXISTS
  Evergreen answers "how many positive replies did we get" but nothing in the repo
  answers "who were they, and what did the conversation actually say". JULY-AUTOPSY.md
  has the aggregates; number-split.csv has 150 contacts but only the ones caught by the
  number-rotation bug, and carries no thread text. Before you can diagnose why 50-odd
  positive replies produced 8 meetings, you need to READ them.

WHERE THE DATA COMES FROM (and why it takes two sources, not one)
  /api/clients/{slug}/deals?channel=sms   — rich but INCOMPLETE. Only replies that got an
      Airtable opportunity. Carries linkedin / website / email / phone / stage /
      meeting_booked_at, and a full untruncated `conversation`. NB the `contact` field is
      null on every record — the person's name lives in `opportunity`.
  /api/clients/{slug}/contacts?category=X — complete but THIN. Every categorised reply,
      including the ones that never became a deal (35 of them in July 2026). Carries the
      name and title but no linkedin/phone/website, and `conversation_snippet` is
      truncated ~1.2k chars — it cuts off before the person's actual reply in 4 of 10.

  Taking either one alone gets you a wrong answer: deals-only silently drops 35 real
  replies (4 of them Power Requests), contacts-only loses LinkedIn and half the threads.
  So: union the two, then repair every thread from the raw GHL message log, which is the
  only source with real timestamps and human-vs-automated attribution.

USAGE
  python3 tools/july_pr_register.py                              # scaletopia, July 2026
  python3 tools/july_pr_register.py --client kynship --month 2026-06
  python3 tools/july_pr_register.py --no-ghl                     # Evergreen only, fast
  python3 tools/july_pr_register.py --since 2026-03-01           # narrower GHL pull

Credentials resolve from ~/.claude.json via the same MCP servers ghl_mine.py uses.
Evergreen needs no auth but DOES need a non-Python User-Agent (its host WAFs urllib).
"""
import argparse, csv, datetime as dt, json, os, re, sys, urllib.parse, urllib.request
from collections import defaultdict, Counter, OrderedDict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ghl_mine as gm                      # creds_from_mcp, get_messages, get_contacts, ROOT, REGISTRY
from ghl_number_split_scan import EV_SLUG, norm as norm_phone

EVERGREEN = "https://knowledgebase-production-f52e.up.railway.app"

# Every category Evergreen will hand back. Ordered as we want to READ them: the ones that
# cost us a meeting first, the ones that were never going anywhere last.
CATEGORIES = ["Power Request", "Positive", "More Info Request", "Email Me Request",
              "Objection Handling", "Maybe", "Referral Request", "Future Request",
              "Custom Response", "Neutral", "Not Interested", "Threat"]

# Hard nos. Fetched so the denominator is honest, but kept OUT of the register — they are
# not positive replies under any definition and there are enough of them (167 in July 2026)
# to bury the 80-odd replies you actually need to read. Counted in the reconciliation.
EXCLUDE = {"Not Interested", "Threat"}

# In the register but visually separated: nobody would call these a positive reply either,
# they're just close enough to the line that dropping them silently would hide a judgement.
TAIL = {"Neutral", "(uncategorised)"}

# Stages Airtable leaves OUT of the positive-reply KPI. Reproducing that rule here is what
# makes this register reconcile to the number the client already has in their reporting —
# for Go Fish, July 2026: 76 SMS deals - 23 "Maybe" - 1 Disqualified = the 52 they quote.
# Note "Maybe" is stored WITH literal double quotes in the data; both forms must be caught.
NOT_POSITIVE_STAGES = {"Disqualified", '"Maybe"', "Maybe"}


def counted_positive(r):
    """Does this reply count toward the positive-reply KPI?

    Deal rows follow Airtable exactly, on stage. Rows that never became a deal have no
    stage at all, so the category is the only signal available — they are flagged
    separately in the UI rather than being quietly folded into the headline number."""
    if r["booked"]:
        return True                    # a booked meeting is positive whatever else is set
    if r["source"] == "contact_only":
        return r["category"] not in (TAIL | {"Maybe"})
    return r["stage"] not in NOT_POSITIVE_STAGES

# High/Medium/Low. This mapping is currently written down NOWHERE — it lives implicitly in
# the prose of clients/_rollup/*-weekly-scorecard.md, which counts positives as High+Medium
# only. Encoding it here makes the KPI reproducible instead of a judgement call per week.
TIER = {"Power Request": "High", "Meeting Booked": "High", "Positive": "Medium",
        "More Info Request": "Medium", "Email Me Request": "Medium",
        "Objection Handling": "Medium", "Maybe": "Medium", "Custom Response": "Medium",
        "Future Request": "Low", "Referral Request": "Low", "Neutral": "Low",
        "Not Interested": "Low", "Threat": "Low", "(uncategorised)": "Low"}

# Evergreen renders threads as one flat string: "Outbound - July 7th at 10:56 am, X said: …"
MSG_RX = re.compile(
    r"(Outbound|Inbound)\s*[-–]\s*([A-Z][a-z]+\s+\d{1,2}(?:st|nd|rd|th)?)\s+at\s+"
    r"(\d{1,2}:\d{2}\s*[apAP]\.?[mM]\.?)\s*,\s*(.*?)\s*said:\s*", re.S)


def nkey(s):
    """Normalise a company or person name to a join key."""
    return re.sub(r"[^a-z0-9]", "", (s or "").lower())


def ndom(u):
    """A website URL down to its bare domain, so builtbyviv.com matches
    https://www.builtbyviv.com/about."""
    u = re.sub(r"^https?://", "", (u or "").strip().lower())
    return re.sub(r"^www\.", "", u).split("/")[0].split("#")[0].split("?")[0]


def load_overrides(path):
    """Human curation, kept as data rather than constants in this file.

    A strategist reading the register disqualifies leads that the CRM still counts —
    out-of-ICP companies, replies mis-tagged as positive. Recording that in a CSV means
    next month's curation is an edit, the REASON survives, and the same bad-fit leads
    don't quietly reappear. Matches on website domain or on phone, because plenty of
    rows have no website at all."""
    if not os.path.exists(path):
        return {}
    out = {}
    for row in csv.DictReader(open(path)):
        m = (row.get("match") or "").strip()
        if not m or m.startswith("#"):
            continue
        key = norm_phone(m) if re.fullmatch(r"[\d\-\+\(\) ]{7,}", m) else ndom(m)
        out[key] = {"verdict": (row.get("verdict") or "exclude").strip(),
                    "reason": (row.get("reason") or "").strip()}
    return out


def apply_overrides(r, ov):
    """Website first, then phone — a row can be targeted by either."""
    for key in (ndom(r.get("website")), norm_phone(r.get("phone"))):
        if key and key in ov:
            return ov[key]
    return None


def month_of(s):
    return (s or "")[:7]


def make_window(month, start, end):
    """Either a calendar month or an explicit date range.

    A follow-up list doesn't respect month boundaries — 'who's still open right now' spans
    whatever period is still live, so the range form exists for that."""
    if start or end:
        lo, hi = start or "0000-01-01", end or "9999-12-31"
        return (lambda s: bool(s) and lo <= s[:10] <= hi), f"{lo}_to_{hi}", f"{lo} → {hi}"
    return (lambda s: month_of(s) == month), month, month


# ---------------------------------------------------------------- evergreen
def ev_get(path, query=None):
    url = f"{EVERGREEN}{path}" + ("?" + urllib.parse.urlencode(query) if query else "")
    r = urllib.request.Request(url, headers={"Accept": "application/json",
                                             "User-Agent": "curl/8.7.1"})
    with urllib.request.urlopen(r, timeout=120) as resp:
        return json.load(resp)


def nn(v):
    """Evergreen serialises a missing field as real JSON null on some clients and as the
    literal STRING "None" on others — the two sit side by side inside one payload (Chamber
    Media: 68 nulls and 68 "None"s on meeting_booked_at). `bool("None")` is True, so left
    alone the string form marks unbooked deals as booked and drops them out of every
    follow-up list. Normalise once, at the door."""
    return None if (v is None or (isinstance(v, str) and v.strip() in ("None", "nan", ""))) else v


def fetch_deals(slug, channel="sms"):
    """Every deal on this channel, all time — we filter by month ourselves because the endpoint has no
    date window, and because a July reply can sit on a deal created in June (Justin Hollis)
    or even last September (Brenna B)."""
    q = {"limit": 3000} if channel == "all" else {"channel": channel, "limit": 3000}
    deals = ev_get(f"/api/clients/{slug}/deals", q).get("deals", [])
    return [{k: nn(v) for k, v in d.items()} for d in deals]


def fetch_contact_threads(slug):
    """One call per category — the endpoint requires it. Returns every categorised reply,
    deal or no deal."""
    out = []
    for cat in CATEGORIES:
        try:
            d = ev_get(f"/api/clients/{slug}/contacts", {"category": cat, "limit": 2000})
        except Exception as e:
            print(f"    (category '{cat}' unavailable: {str(e)[:60]})")
            continue
        for t in d.get("threads", []):
            t["_category"] = cat
            out.append(t)
    # the same person can be returned under two categories; keep one
    seen, uniq = set(), []
    for t in out:
        if t.get("id") in seen:
            continue
        seen.add(t.get("id"))
        uniq.append(t)
    return uniq


# ---------------------------------------------------------------- thread parsing
MONTHS = {m: i for i, m in enumerate(
    ["january", "february", "march", "april", "may", "june", "july", "august",
     "september", "october", "november", "december"], 1)}
WHEN_RX = re.compile(r"([A-Za-z]+)\s+(\d{1,2})\w*\s+at\s+(\d{1,2}):(\d{2})\s*([apAP])")


def _md_hm(when):
    """'August 17th at 10:07 am' -> (8, 17, 10, 7). None if it doesn't parse."""
    m = WHEN_RX.search(when or "")
    if not m or m.group(1).lower() not in MONTHS:
        return None
    h = int(m.group(3)) % 12 + (12 if m.group(5).lower() == "p" else 0)
    return MONTHS[m.group(1).lower()], int(m.group(2)), h, int(m.group(4))


def _stamp_thread(msgs, anchor):
    """Put a YEAR back on Evergreen's timestamps.

    Evergreen prints "August 17th at 10:07 am" and never says which year. Over a one-week
    pull you can assume the obvious one; over an all-time pull that silently mangles every
    December-January thread, and any measurement of response TIME is then fiction.

    The row's created_at gives us an anchor. Messages are already chronological, so: pin
    the LAST message to whichever candidate year sits closest to the anchor, then walk
    backwards, dropping a year each time the date stops going down. Anything that won't
    parse keeps iso=None and must be excluded from timing, not guessed at."""
    parsed = [_md_hm(m["when"]) for m in msgs]
    if not any(parsed):
        return
    try:
        a = dt.datetime.fromisoformat((anchor or "").replace("Z", "+00:00")).replace(tzinfo=None)
    except (ValueError, AttributeError):
        return

    last = next((i for i in range(len(parsed) - 1, -1, -1) if parsed[i]), None)
    mo, day, h, mi = parsed[last]
    year = min((a.year - 1, a.year, a.year + 1),
               key=lambda y: abs((_safe(y, mo, day, h, mi) or a) - a))

    prev = None
    for i in range(last, -1, -1):
        if not parsed[i]:
            continue
        mo, day, h, mi = parsed[i]
        if prev and (mo, day, h, mi) > prev:
            year -= 1                      # walking back and the date went UP: crossed New Year
        d = _safe(year, mo, day, h, mi)
        if d:
            msgs[i]["iso"] = d.isoformat() + "Z"
        prev = (mo, day, h, mi)


def _safe(y, mo, day, h, mi):
    try:
        return dt.datetime(y, mo, day, h, mi)
    except ValueError:
        return None                        # Feb 30 and friends


def parse_ev_thread(text, anchor=None):
    """Evergreen's flat thread string -> ordered messages, chronological. A blank sender on
    an outbound is how a human rep reply shows up (automated sends carry the client name).
    Pass `anchor` (the row's created_at) to get real timestamps back on them."""
    msgs, hits = [], list(MSG_RX.finditer(text or ""))
    for i, m in enumerate(hits):
        end = hits[i + 1].start() if i + 1 < len(hits) else len(text)
        body = re.sub(r"\s+", " ", text[m.end():end]).strip()
        if not body:
            continue
        sender = (m.group(4) or "").strip()
        msgs.append({"dir": m.group(1).lower(), "when": f"{m.group(2)} at {m.group(3)}",
                     "iso": None, "body": body, "sender": sender,
                     # inbound has no sender question; outbound with no name = a person typed it
                     "automated": bool(sender) if m.group(1) == "Outbound" else False})
    if anchor:
        _stamp_thread(msgs, anchor)
    return msgs


def ghl_thread(msgs):
    """Raw GHL messages for one contact -> ordered messages with real timestamps."""
    out = []
    for m in sorted(msgs, key=lambda x: x.get("dateAdded") or ""):
        body = re.sub(r"\s+", " ", m.get("body") or "").strip()
        if not body:
            continue
        iso = m.get("dateAdded")
        out.append({"dir": m.get("direction"), "iso": iso,
                    "when": fmt_when(iso), "body": body,
                    "sender": "", "automated": m.get("source") == "workflow"})
    return out


def fmt_when(iso):
    try:
        d = dt.datetime.fromisoformat((iso or "").replace("Z", "+00:00"))
        return d.strftime("%b %-d, %Y at %-I:%M %p")
    except Exception:
        return (iso or "")[:16]


def merge_duplicates(rows):
    """One human, one row.

    Airtable can hold two opportunities for the same person (Scaletopia: David Sahly;
    Go Fish: Melissa Austria, Malissa Hayes), and build_rows only ever dedupes contacts
    against deals — never deals against each other, and it joins on company, so a row with
    a blank company (Ed Romero) never matches anything. Phone is the reliable key, and it
    is fully populated by the time GHL has repaired the threads, which is why this runs
    after that and not inside build_rows."""
    groups = OrderedDict()
    for r in rows:
        key = norm_phone(r.get("phone")) or nkey(r.get("contact")) or id(r)
        groups.setdefault(key, []).append(r)

    merged = []
    for key, g in groups.items():
        if len(g) == 1:
            g[0]["merged_from"] = 1
            merged.append(g[0])
            continue
        # richest record wins the base, then the others fill its gaps
        base = max(g, key=lambda r: sum(1 for v in r.values() if v))
        for other in g:
            if other is base:
                continue
            for f, v in other.items():
                if v and not base.get(f):
                    base[f] = v
            # a meeting on EITHER record is a meeting
            if other.get("booked"):
                base["booked"] = True
                base["meeting_booked_at"] = base.get("meeting_booked_at") or other.get("meeting_booked_at")
            # the earliest reply is when they actually came in
            if other.get("created_at") and other["created_at"] < base.get("created_at", "9999"):
                base["created_at"] = other["created_at"]
            # keep the longer thread
            if len(other.get("messages") or []) > len(base.get("messages") or []):
                base["messages"] = other["messages"]
        base["merged_from"] = len(g)
        merged.append(base)
    return merged


def days_silent(msgs, now):
    """How long this conversation has been dead. Turns a roster into a chase list."""
    stamps = [m["iso"] for m in msgs if m.get("iso")]
    if not stamps:
        return None
    try:
        last = dt.datetime.fromisoformat(max(stamps).replace("Z", "+00:00"))
    except Exception:
        return None
    return max(0, (now - last).days)


def warm_tier(r):
    """What to DO about this reply, which is not the same question as how it was tagged."""
    if r.get("verdict") == "exclude":
        return "excluded"
    if r.get("verdict") == "not_warm":
        return "not_warm"
    if r["booked"]:
        return "booked"
    if not r["counted_positive"]:
        return "not_counted"
    if r["category"] == "Future Request":
        return "later"
    return "stalled" if r["we_replied"] else "no_reply_sent"


def derive(msgs):
    """we_replied / response_gap_mins, measured from their FIRST inbound to the first time
    a HUMAN answered. Automated nudges don't count as answering — that distinction is the
    whole point of the JULY-AUTOPSY 'worked reply' metric."""
    first_in = next((i for i, m in enumerate(msgs) if m["dir"] == "inbound"), None)
    if first_in is None:
        return False, None, False
    after = msgs[first_in + 1:]
    human = next((m for m in after if m["dir"] == "outbound" and not m["automated"]), None)
    any_out = next((m for m in after if m["dir"] == "outbound"), None)
    gap = None
    if human and human.get("iso") and msgs[first_in].get("iso"):
        try:
            a = dt.datetime.fromisoformat(msgs[first_in]["iso"].replace("Z", "+00:00"))
            b = dt.datetime.fromisoformat(human["iso"].replace("Z", "+00:00"))
            gap = round((b - a).total_seconds() / 60)
        except Exception:
            pass
    return bool(human), gap, bool(any_out)


def flatten(msgs):
    return "\n".join(f"[{m['dir'].upper()}{' auto' if m['automated'] else ''}] "
                     f"{m['when']}: {m['body']}" for m in msgs)


# ---------------------------------------------------------------- build the union
def build_rows(deals, threads, in_window, channel="sms"):
    """Deal fields win where both exist; contacts fill the gaps. Match on company+date
    first, then fall back to company alone so a reply logged in July against a deal opened
    in June still lands on the richer record."""
    d_month = [d for d in deals if in_window(d.get("created_at"))]
    t_all = [t for t in threads
             if in_window(t.get("created_at"))
             and (channel == "all" or t.get("channel") == channel)]
    t_month = [t for t in t_all if (t.get("lead_category") or t.get("_category")) not in EXCLUDE]
    hard_no = Counter((t.get("lead_category") or t.get("_category")) for t in t_all
                      if (t.get("lead_category") or t.get("_category")) in EXCLUDE)

    by_co_date, by_co = defaultdict(list), defaultdict(list)
    for d in deals:
        if nkey(d.get("company")):
            by_co[nkey(d["company"])].append(d)
            by_co_date[(nkey(d["company"]), (d.get("created_at") or "")[:10])].append(d)

    rows, used = [], set()
    for d in d_month:
        if d.get("positive_reply_category") in EXCLUDE:
            hard_no[d["positive_reply_category"]] += 1
            continue
        rows.append(_row_from_deal(d))
        used.add(id(d))

    matched = 0
    for t in t_month:
        co, day = nkey(t.get("company")), (t.get("created_at") or "")[:10]
        hit = next((d for d in by_co_date.get((co, day), []) if id(d) in used), None) \
            or next((d for d in by_co.get(co, []) if id(d) in used), None)
        if hit:
            # enrich the existing deal row rather than duplicating the person
            r = next(r for r in rows if r["_deal_id"] == hit.get("airtable_deal_id"))
            r["source"] = "both"
            r["contact"] = r["contact"] or t.get("name")
            r["job_title"] = r["job_title"] or t.get("title")
            r["job_function"] = t.get("job_function") or ""
            matched += 1
            continue
        # a deal exists but outside the month — use it, it has the richer fields
        out_of_month = next((d for d in by_co.get(co, []) if id(d) not in used), None)
        if out_of_month and nkey(t.get("company")):
            r = _row_from_deal(out_of_month)
            r["source"] = "both"
            r["created_at"] = t.get("created_at")          # the REPLY is what's in-month
            r["contact"] = r["contact"] or t.get("name")
            r["category"] = t.get("_category") or r["category"]
            r["job_function"] = t.get("job_function") or ""
            used.add(id(out_of_month))
            rows.append(r)
            matched += 1
            continue
        rows.append(_row_from_thread(t))

    return rows, len(d_month), len(t_month), matched, hard_no


def _row_from_deal(d):
    cat = d.get("positive_reply_category") or "(uncategorised)"
    return {
        "_deal_id": d.get("airtable_deal_id"),
        "contact": d.get("contact") or d.get("opportunity") or "",
        "job_title": d.get("job_title") or "", "job_function": "",
        "company": d.get("company") or "", "website": d.get("website") or "",
        "linkedin": d.get("linkedin") or "", "email": d.get("email") or "",
        "phone": d.get("phone") or "", "location": d.get("location") or "",
        "channel": d.get("channel") or "sms",
        "category": cat, "intent_tier": TIER.get(cat, "Low"),
        "stage": (d.get("stage") or "").strip('"'),
        "campaign_name": d.get("campaign_name") or "",
        "copy_variant": d.get("copy_variant") or "",
        "created_at": d.get("created_at") or "",
        "booked": bool(d.get("meeting_booked_at")),
        "meeting_booked_at": d.get("meeting_booked_at") or "",
        "source": "deal", "thread_source": "evergreen_deal", "snippet_chars": 0,
        "messages": parse_ev_thread(d.get("conversation"), d.get("created_at")),
        "notes": d.get("notes") or "", "lost_reason": d.get("lost_reason") or "",
    }


def _row_from_thread(t):
    cat = t.get("lead_category") or t.get("_category") or "(uncategorised)"
    return {
        "_deal_id": None,
        "contact": t.get("name") or "", "job_title": t.get("title") or "",
        "job_function": t.get("job_function") or "",
        "company": t.get("company") or "", "website": "", "linkedin": "", "email": "",
        "phone": "", "location": "",
        "channel": t.get("channel") or "sms",
        "category": cat, "intent_tier": TIER.get(cat, "Low"), "stage": "",
        "campaign_name": t.get("campaign_name") or "",
        "copy_variant": t.get("copy_variant") or "",
        "created_at": t.get("created_at") or "",
        "booked": False, "meeting_booked_at": "",
        "source": "contact_only", "thread_source": "evergreen_partial",
        # the contacts endpoint hard-truncates at 1200 chars. Recording the raw length is
        # the only way to tell "they went quiet" from "we can't see the end of the thread".
        "snippet_chars": len(t.get("conversation_snippet") or ""),
        "messages": parse_ev_thread(t.get("conversation_snippet"), t.get("created_at")),
        "notes": "", "lost_reason": "",
    }


# ---------------------------------------------------------------- ghl repair
def repair_threads(rows, pit, loc, since):
    """Replace Evergreen's truncated/undated thread strings with the real message log.
    Join by phone where we have one (exact), else by name+company via GHL's contact list."""
    print(f"\n  pulling GHL SMS since {since} …")
    msgs = gm.get_messages(pit, loc, since)
    print(f"  messages: {len(msgs):,}")
    if not msgs:
        return 0, len(rows)

    by_contact = defaultdict(list)
    for m in msgs:
        if m.get("contactId") and m.get("direction") in ("inbound", "outbound"):
            by_contact[m["contactId"]].append(m)

    # GHL routinely holds the SAME human under several contact records (re-imported lists,
    # retargeting uploads). Their opener can sit on one record and their reply on another,
    # so every index maps to a SET of contactIds and we merge all of them — picking just one
    # is how a real reply ends up looking like an unanswered thread.
    lead_phone = defaultdict(set)
    for cid, ms in by_contact.items():
        for m in ms:
            p = norm_phone(m.get("to") if m.get("direction") == "outbound" else m.get("from"))
            if p:
                lead_phone[p].add(cid)
                break

    contacts = gm.get_contacts(pit, loc)
    by_name, by_first_co, phone_of = defaultdict(set), defaultdict(set), {}
    for c in contacts:
        cid = c.get("id")
        if cid not in by_contact:
            continue                                    # never texted in-window
        full = nkey(f"{c.get('firstName') or ''}{c.get('lastName') or ''}")
        co = nkey(c.get("companyName"))
        if full:
            by_name[full].add(cid)
        if co and c.get("firstName"):
            by_first_co[(nkey(c["firstName"]), co)].add(cid)
        p = norm_phone(c.get("phone"))
        if p:
            phone_of[cid] = p

    fixed = 0
    for r in rows:
        # an email PR has no SMS thread. Matching it by name would attach whatever cold
        # SMS we happen to have sent the same person months earlier, and the timestamps
        # from that thread would then drive days_silent — silently wrong, not obviously so.
        if r.get("channel", "sms") != "sms":
            continue
        cids = set()
        p = norm_phone(r.get("phone"))
        if p:
            cids |= lead_phone.get(p, set())
        if r.get("contact"):
            parts = r["contact"].split()
            cids |= by_name.get(nkey(r["contact"]), set())
            if parts:
                cids |= by_first_co.get((nkey(parts[0]), nkey(r.get("company"))), set())
        # a name+company match must agree on phone with what we already have, or we risk
        # stapling a different person's thread onto this row
        if p:
            cids = {c for c in cids if phone_of.get(c, p) == p}
        if not cids:
            continue
        merged = list({m["id"]: m for c in cids for m in by_contact[c]}.values())
        t = ghl_thread(merged)
        if not t:
            continue
        r["messages"] = t
        r["thread_source"] = "ghl"
        r["ghl_contacts"] = len(cids)
        r["phone"] = r["phone"] or next(
            (m.get("to") if m.get("direction") == "outbound" else m.get("from")
             for m in merged), "")
        fixed += 1
    return fixed, len(rows) - fixed


# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--client", default="scaletopia", help="key in clients/registry.json")
    ap.add_argument("--month", default="2026-07", help="YYYY-MM")
    ap.add_argument("--from", dest="start", help="YYYY-MM-DD; with --to, overrides --month")
    ap.add_argument("--to", dest="end", help="YYYY-MM-DD")
    ap.add_argument("--channel", default="sms", choices=["sms", "email", "all"],
                    help="email threads have no GHL log, so they keep Evergreen's text")
    ap.add_argument("--since", default="2026-01-01", help="how far back to pull GHL messages "
                                                          "(threads open months before the reply)")
    ap.add_argument("--no-ghl", action="store_true", help="Evergreen only — skip the thread repair")
    ap.add_argument("--out", help="output dir (default: from registry)")
    a = ap.parse_args()

    reg = {k: v for k, v in json.load(open(gm.REGISTRY)).items() if not k.startswith("_")}
    if a.client not in reg:
        sys.exit(f"'{a.client}' not in registry. Known: {', '.join(sorted(reg))}")
    cfg = reg[a.client]
    slug = EV_SLUG.get(a.client, a.client)
    label = cfg.get("label", a.client)

    in_window, wslug, wlabel = make_window(a.month, a.start, a.end)
    print(f"[{label}] {wlabel} — Evergreen slug '{slug}'")
    deals = fetch_deals(slug, a.channel)
    threads = fetch_contact_threads(slug)
    print(f"  evergreen: {len(deals):,} sms deals (all time) · {len(threads):,} categorised threads")

    rows, n_deals, n_threads, matched, hard_no = build_rows(deals, threads, in_window, a.channel)
    print(f"  {wlabel}: {n_deals} deals + {n_threads} categorised threads "
          f"→ {matched} matched → {len(rows)} distinct replies")
    if hard_no:
        print(f"  excluded as hard nos (not in the register): "
              f"{sum(hard_no.values())} — {dict(hard_no)}")

    # A meeting held in July is not the same thing as a July replier who booked: 4 of the
    # month's 8 SMS meetings came from people who replied in earlier months. Both numbers
    # are true; conflating them is how '52 PRs -> 6 meetings' gets argued in circles.
    # Curation applies here too — an out-of-ICP company that booked isn't a meeting we want
    # to keep claiming, so the same override file filters this count.
    ov_early = load_overrides(os.path.normpath(os.path.join(
        gm.ROOT, cfg.get("output", f"clients/{a.client}/output"), os.pardir,
        "reply-overrides.csv")))
    mtg_in_month = [d for d in deals if in_window(d.get("meeting_booked_at"))
                    and (apply_overrides(d, ov_early) or {}).get("verdict") != "exclude"]

    if not a.no_ghl:
        sms = cfg.get("sms") or {}
        try:
            pit = gm.creds_from_mcp(sms["mcp"]) if sms.get("mcp") else None
        except SystemExit:
            pit = None
        if pit and sms.get("locationId"):
            fixed, left = repair_threads(rows, pit, sms["locationId"], a.since)
            print(f"  threads repaired from GHL: {fixed}/{len(rows)}  ({left} kept on Evergreen text)")
        else:
            print("  !! no GHL token/location — threads stay on Evergreen text")

    before = len(rows)
    rows = merge_duplicates(rows)
    if len(rows) < before:
        dupes = [r for r in rows if r.get("merged_from", 1) > 1]
        print(f"  merged {before - len(rows)} duplicate record(s) — one row per person now: "
              + ", ".join(f"{r['contact']} ×{r['merged_from']}" for r in dupes))

    ov = ov_early
    if ov:
        print(f"  loaded {len(ov)} curation override(s) from reply-overrides.csv")

    # derived fields, after the thread is final
    now = dt.datetime.now(dt.timezone.utc)
    for r in rows:
        r["we_replied"], r["response_gap_mins"], r["any_outbound_after"] = derive(r["messages"])
        r["n_messages"] = len(r["messages"])
        r["days_silent"] = days_silent(r["messages"], now)
        hit = apply_overrides(r, ov)
        r["verdict"] = hit["verdict"] if hit else ""
        r["override_reason"] = hit["reason"] if hit else ""
        r["excluded"] = r["verdict"] == "exclude"
        r["counted_positive"] = counted_positive(r) and not r["excluded"]
        r["warm_tier"] = warm_tier(r)
        r["is_tail"] = not r["counted_positive"]
    rows.sort(key=lambda r: (r["is_tail"],
                             CATEGORIES.index(r["category"]) if r["category"] in CATEGORIES else 99,
                             r["created_at"]))

    out_dir = a.out or os.path.join(gm.ROOT, cfg.get("output", f"clients/{a.client}/output"))
    os.makedirs(out_dir, exist_ok=True)
    stem = os.path.join(out_dir, f"{wslug}-{a.channel}-prs")

    cols = ["contact", "job_title", "job_function", "company", "website", "linkedin", "email",
            "phone", "location", "channel", "category", "intent_tier", "counted_positive", "warm_tier",
            "days_silent", "stage", "campaign_name", "copy_variant", "created_at", "we_replied",
            "response_gap_mins", "booked", "meeting_booked_at", "excluded", "override_reason",
            "merged_from", "n_messages", "source", "thread_source", "thread"]
    with open(f"{stem}.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow({**r, "thread": flatten(r["messages"])})
    json.dump({"client": label, "month": wlabel,
               "built_at": dt.datetime.now(dt.timezone.utc).isoformat()[:19] + "Z",
               "meetings_in_month": len(mtg_in_month), "rows": rows},
              open(f"{stem}.json", "w"), indent=1)

    # ---- reconciliation, printed so the numbers can be argued with
    live = [r for r in rows if not r["excluded"]]
    core = [r for r in live if r["counted_positive"]]
    ex = [r for r in rows if r["excluded"]]
    print(f"\n  {'category':22} {'n':>4} {'answered':>9} {'booked':>7}")
    print("  " + "-" * 46)
    for cat, n in Counter(r["category"] for r in live).most_common():
        sub = [r for r in live if r["category"] == cat]
        print(f"  {cat:22} {n:>4} {sum(1 for r in sub if r['we_replied']):>9} "
              f"{sum(1 for r in sub if r['booked']):>7}")
    print("  " + "-" * 46)
    if ex:
        print(f"  {len(ex)} row(s) excluded by curation, dropped from every count above:")
        for r in sorted(ex, key=lambda r: r["company"] or ""):
            print(f"      {(r['company'] or r['contact'])[:28]:<29} {r['override_reason']}")

    TIERS = [("no_reply_sent", "never answered — they engaged, nobody replied"),
             ("stalled", "we replied, then it went quiet"),
             ("later", "asked us to check back"),
             ("booked", "booked a meeting"),
             ("not_warm", "mis-tagged, not a real lead"),
             ("not_counted", "not counted as positive")]
    by_tier = Counter(r["warm_tier"] for r in rows)
    warm = sum(by_tier[t] for t in ("no_reply_sent", "stalled", "later"))
    print(f"\n  STILL WARM: {warm}")
    for t, why in TIERS:
        if by_tier[t]:
            sub = [r for r in rows if r["warm_tier"] == t]
            ages = [r["days_silent"] for r in sub if r["days_silent"] is not None]
            med = f" · median {sorted(ages)[len(ages)//2]}d silent" if ages else ""
            print(f"    {by_tier[t]:>3}  {t:<14} {why}{med}")
    gaps = [r["response_gap_mins"] for r in live if r["response_gap_mins"] is not None]
    gaps.sort()
    print(f"  TOTAL {len(rows)} logged ({len(live)} after exclusions) · {len(core)} count as "
          f"positive ({sum(1 for r in core if r['source'] != 'contact_only')} from the CRM, "
          f"{sum(1 for r in core if r['source'] == 'contact_only')} with no deal record) · "
          f"{sum(1 for r in live if r['we_replied'])} answered by a human · "
          f"{sum(1 for r in live if r['booked'])} of these repliers booked")
    print(f"  ({len(mtg_in_month)} SMS meetings were BOOKED in {wlabel} — the balance came "
          f"from people who first replied in earlier months)")
    if gaps:
        print(f"  median human response: {gaps[len(gaps)//2]} min "
              f"(n={len(gaps)}, within the hour: {sum(1 for g in gaps if g <= 60)})")
    print(f"  sources: {dict(Counter(r['source'] for r in live))} · "
          f"threads: {dict(Counter(r['thread_source'] for r in live))}")
    missing = [r for r in rows if not r["contact"] or not r["messages"]]
    if missing:
        print(f"  !! {len(missing)} rows missing a name or a thread")
    print(f"\n  wrote {stem}.csv + {stem}.json")


if __name__ == "__main__":
    main()
