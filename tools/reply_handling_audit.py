#!/usr/bin/env python3
"""What happens AFTER someone replies positively — measured across every client, all time.

WHY THIS EXISTS
  open_pr_rollup.py answers "who is still open this week". It found one pattern in 36
  threads: the same stock sentence answering every positive reply. 36 threads over five
  days is an anecdote. This runs the same read over ~1,400 threads, all clients, all time,
  SMS and email kept apart, and turns four standing beliefs into numbers:

    H1  the reply copy is the problem — uninformative, salesy, or AI-sounding
    H2  we don't follow up enough
    H3  we're too slow (target: 5 minutes)
    H4  we miss replies entirely (acknowledged, deprioritised)

THE METHOD POINT THAT MAKES OR BREAKS IT
  Rates are computed on DEALS ONLY. The contacts endpoint re-categorises a reply the moment
  it books — it moves to the "Meeting Booked" bucket — so /contacts?category=Power Request
  is, by construction, almost entirely the ones that did NOT convert. Ask it whether speed
  predicts booking and it will tell you no, because there are no bookings in it. /deals
  keeps positive_reply_category all the way through to Meeting Booked / Show / Won, so it
  is the only population where both outcomes exist side by side.

  Contacts rows are still pulled: they carry the replies that never became an opportunity
  at all, which is H4 and nothing else. They are counted in volume and coverage, never in
  a booked-rate.

USAGE
  python3 tools/reply_handling_audit.py                        # all clients, all time
  python3 tools/reply_handling_audit.py --from 2026-08-17 --to 2026-08-21
  python3 tools/reply_handling_audit.py --client scaletopia
"""
import argparse, datetime as dt, json, os, re, sys
from collections import Counter, defaultdict, OrderedDict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ghl_mine as gm
import july_pr_register as reg
import open_pr_rollup as roll

# In the order Aaman wants them read: the strongest ask first.
CATEGORIES = ["Power Request", "More Info Request", "Email Me Request"]

# Email Me Request covers two opposite things. "Sure, send me an email" is a lead. "Stop
# texting me, email instead" is a complaint wearing the same tag. Only the first is in scope.
OPTOUT_RX = re.compile(
    r"stop text|stop messag|take me off|remove me|unsubscribe|do ?n'?t text|"
    r"quit text|no more text|opt.?out|leave me alone|lose my number", re.I)

# ---------------------------------------------------------------- classifiers
# Order matters: the first bucket that matches wins, hardest signal first.
INTENT_RULES = [
    ("optout_hostile", r"stop text|take me off|remove me|unsubscribe|do ?n'?t (text|contact)|"
                       r"leave me alone|fuck|piss off|harass"),
    # a merge-var that never rendered, or a shop's own autoresponder answering our text
    ("auto_responder", r"\{\{|\}\}|thank you for (asking|contacting|reaching)|"
                       r"finish your purchase|was in your cart|our team will get back|"
                       r"out of (the )?office|automatic reply"),
    ("wrong_person",   r"wrong (number|person|guy|contact)|i'?m not (a|the|with)\b|"
                       r"no longer (with|at)|i'?m retired|you have the wrong|"
                       r"not the right person|i have no influence"),
    ("referral",       r"(talk|speak|reach out|reach) (to|with)\b|forward (this|it) to|"
                       r"cc'?ing|copying (in|him|her)|best person|you'?ll want to (talk|speak|ask)|"
                       r"(email|contact) (my|our) (colleague|partner|boss|owner|cmo|ceo|team)"),
    ("objection",      r"how much|what.{0,10}cost|\bprice|pricing|budget|expensive|"
                       r"already\b.{0,25}(have|got|work|use|doing|implemented|in place)|"
                       r"(have|got|use|doing).{0,25}\balready\b|in.?house|we'?re (at|doing) \$?\d|"
                       r"can you scale|what makes you|why should|(two|2) firms|no promises"),
    ("channel_switch", r"stick to email|email me|send.{0,15}(an )?email|via email|by email|"
                       r"email is better|prefer email|my email is|[\w.]+@\w+\.\w"),
    # includes them proposing a time, or sending their own booking link — the strongest asks
    ("call_ask",       r"\bcall\b|meeting|schedule|book|calendar|zoom|chat|conversation|"
                       r"^\W*(mon|tues|wednes|thurs|fri|satur|sun)day\b|"
                       r"let'?s (discuss|talk|connect)|\btalk(ing)?\b|set (up|it up)|"
                       r"hop on|jump on|free (this|next) week|available|"
                       r"calendly|cal\.com|savvycal|hubspot\.com/meetings|"
                       r"(monday|tuesday|wednesday|thursday|friday)\s*(work|ok|good)|"
                       r"pick a (date|time)|after (jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)"),
    # a question back is a request for information, even when it isn't phrased as one
    ("info_ask",       r"send (it|me|over|them|us)|share|show me|more info|details|deck|"
                       r"case stud|take a look|tell me more|learn more|examples?|"
                       r"\bwhat (is|are|do|does|was|area|kind)|what'?s\b|\bwhich\b|"
                       r"how (do|does|would|did|much time)|explain|elaborate|\bwhere\b|who (are|is) "),
    ("soft_yes",       r"^\W*(sure|yes|yeah|yep|ok|okay|sounds (good|perfect|great)|"
                       r"interested|i'?m interested|great|i do\b|absolutely|please)\b|"
                       r"i'?m open|i'?ll bite|happy to (hear|take a look)|worth it|"
                       r"do ?n'?t mind|sign me up|you have my attention|^\W*always\b"),
]
INTENT_RX = [(k, re.compile(v, re.I)) for k, v in INTENT_RULES]

# Which CRM tags each intent is a reasonable match for. Anything outside = mis-tagged.
TAG_OK = {
    "call_ask":       {"Power Request"},
    "soft_yes":       {"Power Request"},
    "info_ask":       {"More Info Request", "Power Request"},
    "channel_switch": {"Email Me Request", "More Info Request"},
    "objection":      {"Objection Handling"},
    "referral":       {"Referral Request"},
    "wrong_person":   set(),
    "optout_hostile": set(),
    "no_reply":       set(),
    "no_thread":      None,          # unreadable: never counts for or against a tag
    "auto_responder": set(),
    "other":          {"Power Request", "More Info Request", "Email Me Request"},
}

OPENER_RX = [
    ("permission", re.compile(r"could i (show|walk)|can i (show|walk)|mind if i|"
                              r"worth (exploring|a look)|would it be worth|ok if i", re.I)),
    ("time_ask",   re.compile(r"free (this|next) week|any chance you'?re free|"
                              r"do you have (time|\d)|what time|how does .{0,20}look|"
                              r"are you (free|around)|\b\d{1,2}\s?(am|pm)\b", re.I)),
    ("soft",       re.compile(r"lmk|let me know|thoughts\?|open to|interested\?", re.I)),
]

# The sentence found answering everything, and its parts.
STOCK_RX = re.compile(r"awesome.{0,45}got a few minutes.{0,90}(hop on|happy to)", re.I | re.S)
MARKERS = OrderedDict([
    ("got a few minutes",      re.compile(r"got a few minutes", re.I)),
    ("hop on a (quick) call",  re.compile(r"hop on a (quick )?call", re.I)),
    ("what we can do for X",   re.compile(r"what we can do for", re.I)),
    ("opens Awesome/Perfect",  re.compile(r"^\s*(awesome|perfect|sounds good|great)\b", re.I)),
    ("asks for their email",   re.compile(r"(drop|send|share|whats?|what'?s).{0,25}best email|"
                                          r"drop your.{0,15}email", re.I)),
])
LINK_RX = re.compile(r"https?://|\bwww\.", re.I)
TIME_RX = re.compile(r"\b\d{1,2}([:.]\d{2})?\s?(am|pm)\b|"
                     r"\b(mon|tues|wednes|thurs|fri)day\b|\btomorrow\b", re.I)


def classify_intent(body):
    if not body:
        return "no_reply"       # thread exists, nothing inbound in it
    for k, rx in INTENT_RX:
        if rx.search(body):
            return k
    return "other"


def classify_opener(body):
    for k, rx in OPENER_RX:
        if rx.search(body or ""):
            return k
    return "no_ask" if "?" not in (body or "") else "other_question"


def shape(body):
    """Strip the variable bits so two mail-merges of the same sentence collapse together."""
    b = (body or "").lower()
    b = re.sub(r"https?://\S+", " URL ", b)
    b = re.sub(r"\b\d{1,2}([:.]\d{2})?\s?(am|pm)\b", " TIME ", b)
    b = re.sub(r"\b(mon|tues|wednes|thurs|fri|satur|sun)day\b", " DAY ", b)
    b = re.sub(r"[^a-z ]", " ", b)
    return " ".join(b.split())


def trigrams(s):
    w = s.split()
    return {tuple(w[i:i + 3]) for i in range(max(0, len(w) - 2))}


# ---------------------------------------------------------------- fetch
def fetch_cats(slug, cats):
    """Only the categories in scope — fetch_contact_threads pulls all twelve, which is
    120 wasted calls across thirteen clients."""
    out = []
    for cat in cats:
        try:
            d = reg.ev_get(f"/api/clients/{slug}/contacts", {"category": cat, "limit": 3000})
        except Exception as e:
            print(f"    ({slug}/{cat} unavailable: {str(e)[:50]})")
            continue
        for t in d.get("threads", []):
            t["_category"] = cat
            out.append(t)
    seen, uniq = set(), []
    for t in out:
        if t.get("id") in seen:
            continue
        seen.add(t["id"])
        uniq.append(t)
    return uniq


def mins_between(a, b):
    try:
        x = dt.datetime.fromisoformat(a.replace("Z", ""))
        y = dt.datetime.fromisoformat(b.replace("Z", ""))
    except (ValueError, AttributeError):
        return None
    d = (y - x).total_seconds() / 60
    return d if d >= 0 else None


SPEED_BUCKETS = [(5, "<5 min"), (10, "5-10 min"), (30, "10-30 min"), (60, "30-60 min"),
                 (240, "1-4 h"), (1440, "4-24 h"), (float("inf"), ">24 h")]


def speed_bucket(m):
    if m is None:
        return None
    for hi, label in SPEED_BUCKETS:
        if m < hi:
            return label


def analyse(r):
    """Everything measured about one thread. Pure function of r['messages']."""
    ms = r["messages"]
    fi = next((i for i, m in enumerate(ms) if m["dir"] == "inbound"), None)
    r["their_reply"] = ms[fi]["body"] if fi is not None else ""
    # A deal whose `conversation` came back empty is UNREADABLE, not unanswered. It was
    # tagged a positive reply, so the reply happened — we just can't see it. Folding these
    # into "never answered" would invent a coverage crisis and drag every denominator.
    r["no_thread"] = not ms
    r["intent"] = "no_thread" if not ms else classify_intent(r["their_reply"])
    r["reply_words"] = len(re.findall(r"\w+", r["their_reply"]))
    r["opener"] = ms[fi - 1]["body"] if (fi not in (None, 0)) else ""
    r["opener_cta"] = classify_opener(r["opener"]) if r["opener"] else None

    after = ms[fi + 1:] if fi is not None else []
    ours = next((m for m in after if m["dir"] == "outbound" and not m["automated"]), None)
    r["our_answer"] = ours["body"] if ours else ""
    r["answered"] = bool(ours)
    r["speed_mins"] = mins_between(ms[fi]["iso"], ours["iso"]) if (ours and fi is not None) else None
    r["speed_bucket"] = speed_bucket(r["speed_mins"])

    # follow-ups = human outbounds after their LAST inbound
    li = next((i for i in range(len(ms) - 1, -1, -1) if ms[i]["dir"] == "inbound"), None)
    tail = [m for m in ms[li + 1:] if m["dir"] == "outbound" and not m["automated"]] if li is not None else []
    r["followups"] = len(tail)
    bodies = [shape(m["body"]) for m in tail]
    r["repeat_followups"] = len(bodies) - len(set(bodies))
    r["they_wrote_last"] = bool(ms) and ms[-1]["dir"] == "inbound"

    a = r["our_answer"]
    r["answer_shape"] = shape(a)
    r["is_stock"] = bool(STOCK_RX.search(a))
    r["markers"] = [k for k, rx in MARKERS.items() if rx.search(a)]
    r["answer_words"] = len(re.findall(r"\w+", a))
    r["answer_has_link"] = bool(LINK_RX.search(a))
    r["answer_has_time"] = bool(TIME_RX.search(a))
    # they asked to be SHOWN something and got a meeting ask with nothing attached
    r["answer_mismatch"] = bool(a) and r["intent"] == "info_ask" and not r["answer_has_link"] \
        and bool(re.search(r"call|meeting|minutes|chat", a, re.I))
    ok = TAG_OK.get(r["intent"], set())
    r["mistagged"] = None if ok is None else (r["category"] not in ok)
    return r


def collect(slug, in_window, cats):
    deals = reg.fetch_deals(slug, "all")
    threads = fetch_cats(slug, cats)
    rows, *_ = reg.build_rows(deals, threads, in_window, channel="all")
    rows = roll.dedupe(rows)
    out = []
    for r in rows:
        if r["category"] not in cats:
            continue
        r["client_slug"] = slug
        r["booked"] = bool(r["booked"]) or (r.get("stage") or "") in roll.BOOKED_STAGES
        # only a readable deal row can enter a rate: deals carry the booked/unbooked split,
        # and a row with no thread text can't be scored on speed, copy or follow-ups
        r["has_outcome"] = r["source"] in ("deal", "both") and bool(r["messages"])
        r.pop("_deal_id", None)
        out.append(analyse(r))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--from", dest="start")
    ap.add_argument("--to", dest="end")
    ap.add_argument("--client")
    ap.add_argument("--out", default=os.path.join(gm.ROOT, "clients/_rollup/output"))
    ap.add_argument("--stem", default="reply-handling-audit")
    a = ap.parse_args()

    if a.start or a.end:
        in_window, wslug, wlabel = reg.make_window(None, a.start, a.end)
    else:
        in_window, wslug, wlabel = (lambda s: bool(s)), "all-time", "all time"

    slugs = [a.client] if a.client else roll.active_slugs()
    print(f"reply-handling audit — {wlabel} — {len(slugs)} client(s)")
    rows = []
    for slug in slugs:
        try:
            got = collect(slug, in_window, CATEGORIES)
        except Exception as e:
            print(f"  {slug:18s} FAILED: {str(e)[:70]}")
            continue
        rows += got
        print(f"  {slug:18s} {len(got):>4} threads")

    # Email Me Request: keep the leads, drop the complaints, say how many
    dropped = [r for r in rows if r["category"] == "Email Me Request"
               and (OPTOUT_RX.search(r["their_reply"] or "") or r["intent"] == "optout_hostile")]
    rows = [r for r in rows if r not in dropped]

    os.makedirs(a.out, exist_ok=True)
    stem = os.path.join(a.out, f"{dt.date.today()}-{a.stem}")
    json.dump({"window": wlabel, "built_at": dt.datetime.now(dt.timezone.utc).isoformat()[:19] + "Z",
               "categories": CATEGORIES, "emr_dropped": len(dropped), "rows": rows},
              open(f"{stem}.json", "w"), indent=1)
    print(f"\n  {len(rows)} threads kept · {len(dropped)} Email-Me complaints filtered out")
    print(f"  with an outcome (deals): {sum(1 for r in rows if r['has_outcome'])}")
    print(f"  -> {stem}.json")


if __name__ == "__main__":
    main()
