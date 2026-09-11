#!/usr/bin/env python3
"""Every Power Request that never became a call, across every client, for one week.

WHY THIS EXISTS
  Evergreen reports Power Requests as a COUNT. A count is not workable: "9 power requests
  at Chamber Media" tells you nothing about who said yes, what they said yes to, or whether
  anybody ever wrote back. The people in that number are the warmest leads the whole system
  produces — they replied to a cold text with "yes let's discuss" — and every week some of
  them go quiet because nobody put them in front of a human.

  july_pr_register.py already answers this for ONE client and ONE category at a time, and
  writes into that client's own output dir. This walks every active client in Evergreen,
  keeps only the open Power Requests, and lands one rollup you can read top to bottom.

WHAT "OPEN" MEANS HERE
  No meeting exists (meeting_booked_at is empty) AND the deal is still parked at stage
  "Positive Reply" — or there is no deal record at all, which is the more common case and
  the more urgent one: nobody in the CRM has so much as opened an opportunity on them.
  Disqualified / Lost / No Show are deliberately NOT here. They also never converted, but
  they're autopsy material; this file is a call list.

  Note the two halves are not equally trustworthy. A row sourced from /deals carries the
  phone, email, LinkedIn and the full thread. A contact_only row carries a name, a company
  and up to 1200 characters of conversation, because that is all the contacts endpoint
  returns. Rows whose thread hit that ceiling are marked, so "they went quiet" is never
  confused with "we cannot see the end of the thread".

USAGE
  python3 tools/open_pr_rollup.py --from 2026-08-17 --to 2026-08-21
  python3 tools/open_pr_rollup.py --from 2026-08-17 --to 2026-08-21 --category "Positive"
  python3 tools/open_pr_rollup.py --from 2026-08-01 --to 2026-08-31 --client scaletopia

Evergreen needs no auth but DOES need a non-Python User-Agent; july_pr_register.ev_get
already handles that. No GHL/EmailBison calls are made — this is Evergreen only.
"""
import argparse, datetime as dt, json, os, sys
from collections import OrderedDict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ghl_mine as gm
import july_pr_register as reg
from ghl_number_split_scan import EV_SLUG, norm as norm_phone

# Stages that mean a meeting exists or once existed. A row in any of these is not open,
# whatever meeting_booked_at says — the two fields disagree often enough that trusting
# either one alone under-reports.
BOOKED_STAGES = {"Meeting Booked", "Show", "No Show", "Proposal Sent", "Next Stage",
                 "Won", "Verbal Agreement", "Post Meeting Lost"}
# Parked, never advanced. This is the whole point of the file.
OPEN_STAGES = {"Positive Reply", ""}
# The contacts endpoint hard-truncates conversation_snippet at this many characters.
SNIPPET_CAP = 1200

EV_TO_REG = {v: k for k, v in EV_SLUG.items()}


def active_slugs():
    """Ask Evergreen who's live rather than hardcoding — clients get added between runs
    (nextleft and acceler8 both post-date the skill's client table)."""
    return [c["slug"] for c in reg.ev_get("/api/clients") if c.get("status") == "active"]


def week_trend(slug, category):
    """The contacts endpoint's own per-week counts, used as an independent denominator.
    If our union disagrees with this, one of the two is wrong and the run should be read
    with suspicion rather than published."""
    try:
        d = reg.ev_get(f"/api/clients/{slug}/contacts", {"category": category, "limit": 1})
    except Exception:
        return {}
    return {w["week"]: w["n"] for w in (d.get("weekly_trend") or [])}


def overrides_for(slug):
    """Curation lives per client, next to that client's output dir. Slugs that aren't in
    the registry (Evergreen-only clients) simply have no curation file yet."""
    key = EV_TO_REG.get(slug, slug)
    try:
        cfg = {k: v for k, v in json.load(open(gm.REGISTRY)).items()
               if not k.startswith("_")}[key]
    except (KeyError, OSError):
        return {}
    return reg.load_overrides(os.path.normpath(os.path.join(
        gm.ROOT, cfg.get("output", f"clients/{key}/output"), os.pardir,
        "reply-overrides.csv")))


def truncated(r):
    """Did Evergreen cut this thread off? Only a contacts-sourced row can be — a row that
    merged with a deal carries that deal's untruncated conversation instead. Measured on
    the raw snippet length, not the parsed bodies, because the parse strips the
    "Outbound - Aug 21 at 9:51 am, X said:" headers and would read short."""
    return r.get("source") == "contact_only" and (r.get("snippet_chars") or 0) >= SNIPPET_CAP


# Names the CRM uses when it has no name. Left in as identities they merge 50 unrelated
# people into one row (Redo carries 50 "John Doe" contacts), and swallow real replies.
PLACEHOLDER_NAMES = {"johndoe", "janedoe", "johnsmith", "unknown", "noname", "test",
                     "na", "none", "nan", "customer", "contact", "lead"}


def _phone_key(r):
    """Only a complete number is an identity. norm_phone hands back whatever digits it
    found, so a junk fragment like "1" would otherwise match everything holding junk."""
    p = norm_phone(r.get("phone"))
    return p if len(p) == 10 else ""


def _name_key(r):
    n = reg.nkey(r.get("contact"))
    return "" if (len(n) < 5 or n in PLACEHOLDER_NAMES) else n


def _co_key(r):
    co = reg.nkey(r.get("company"))
    return (co, (r.get("created_at") or "")[:10]) if co else None


def _co_compatible(a, b):
    """Two rows may only be merged on a shared NAME if their companies don't contradict.
    One side blank is fine — that's the normal deal-vs-contact shape — but two different
    companies means two different people who happen to share a name."""
    ca, cb = reg.nkey(a.get("company")), reg.nkey(b.get("company"))
    return not ca or not cb or ca == cb


def dedupe(rows):
    """One human, one row.

    build_rows joins contacts onto deals by COMPANY, so anyone whose contact record has a
    blank company (Trevor Roberts, Erica Swerdlow) comes back twice, and Airtable's own
    duplicate opportunities (Andre Cvijovic, two deals on Referrizer LLC) come back twice
    again. Left in, they inflate the headline and put the same person on the call list
    twice. reg.merge_duplicates can't fix it here because it keys on phone-or-name and the
    two halves of a duplicate pair have exactly one of those each — the deal brings the
    phone, the contact brings the name.

    So: union rows that share a full phone number, or a company on the same day, or a name
    that their companies don't contradict. Then the richest record wins and the others fill
    its gaps."""
    parent = list(range(len(rows)))

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    def union(i, j):
        a, b = find(i), find(j)
        if a != b:
            parent[b] = a

    buckets = {}
    for i, r in enumerate(rows):
        for k in (("p", _phone_key(r)) if _phone_key(r) else None,
                  ("c",) + _co_key(r) if _co_key(r) else None,
                  ("n", _name_key(r)) if _name_key(r) else None):
            if k:
                buckets.setdefault(k, []).append(i)

    for k, idxs in buckets.items():
        if k[0] == "n":
            # names need the company cross-check; phone and company+day don't
            for x in range(len(idxs)):
                for y in range(x + 1, len(idxs)):
                    if _co_compatible(rows[idxs[x]], rows[idxs[y]]):
                        union(idxs[x], idxs[y])
        else:
            for j in idxs[1:]:
                union(idxs[0], j)

    groups = OrderedDict()
    for i, r in enumerate(rows):
        groups.setdefault(find(i), []).append(r)

    out = []
    for g in groups.values():
        if len(g) == 1:
            g[0]["merged_from"] = 1
            out.append(g[0])
            continue
        base = max(g, key=lambda r: sum(1 for v in r.values() if v))
        for other in g:
            if other is base:
                continue
            for f, v in other.items():
                if v and not base.get(f):
                    base[f] = v
        # a meeting on ANY record is a meeting; the furthest stage wins
        base["booked"] = any(r["booked"] for r in g)
        stages = [r.get("stage") for r in g if r.get("stage")]
        base["stage"] = next((s for s in stages if s in BOOKED_STAGES), stages[0] if stages else "")
        # the fullest thread wins — a /deals conversation is untruncated, a snippet is not
        base["messages"] = max((r["messages"] for r in g),
                               key=lambda ms: sum(len(m["body"]) for m in ms))
        base["source"] = "both" if len({r["source"] for r in g}) > 1 else g[0]["source"]
        # the REPLY date is what we want, and that is the earliest record of it
        dates = [r.get("created_at") for r in g if r.get("created_at")]
        base["created_at"] = min(dates) if dates else ""
        base["merged_from"] = len(g)
        out.append(base)
    return out


def is_open(r):
    return (not r["booked"]
            and (r.get("stage") or "") not in BOOKED_STAGES
            and (r.get("stage") or "") in OPEN_STAGES
            and not r.get("excluded"))


def days_since(created_at, now):
    try:
        d = dt.datetime.fromisoformat((created_at or "").replace("Z", "+00:00"))
    except ValueError:
        return None
    return max(0, (now - d).days)


def collect(slug, in_window, category, now):
    """One client -> (open rows, reconciliation counts). The union of deals and contacts is
    done by build_rows; all we add is the category filter and the open/booked split."""
    deals = reg.fetch_deals(slug, "all")
    threads = reg.fetch_contact_threads(slug)
    rows, n_deals, n_threads, matched, _ = build(deals, threads, in_window)
    before = len(rows)
    rows = dedupe(rows)
    n_merged = before - len(rows)

    ov = overrides_for(slug)
    for r in rows:
        hit = reg.apply_overrides(r, ov)
        r["excluded"] = (hit or {}).get("verdict") == "exclude"
        r["override_reason"] = (hit or {}).get("reason", "")
        r["we_replied"], r["response_gap_mins"], r["any_outbound_after"] = reg.derive(r["messages"])
        r["n_messages"] = len(r["messages"])
        r["days_since_reply"] = days_since(r.get("created_at"), now)
        # Who spoke last is the sharper question for a call list. "we_replied" only asks
        # whether we EVER answered — Sue Graham was answered and still left hanging, and
        # that reads as handled unless you look at the last line of the thread.
        r["ball_in_our_court"] = bool(r["messages"]) and r["messages"][-1]["dir"] == "inbound"
        r["thread_truncated"] = truncated(r)
        r["client_slug"] = slug
        r.pop("_deal_id", None)

    inc = [r for r in rows if r["category"] == category]
    if n_merged:
        print(f"    {slug}: merged {n_merged} duplicate record(s) — one row per person now")
    opn = [r for r in inc if is_open(r)]
    bkd = [r for r in inc if r["booked"] or (r.get("stage") or "") in BOOKED_STAGES]
    other = [r for r in inc if r not in opn and r not in bkd]

    # Work order, worst failure first: nobody answered them at all, then they wrote back
    # and we left it there, then the ones where the last word was ours. Oldest within each.
    opn.sort(key=lambda r: (r["we_replied"], not r["ball_in_our_court"],
                            r.get("created_at") or ""))
    return opn, {"in_window": len(inc), "open": len(opn), "booked": len(bkd),
                 "other": len(other), "deals_in_window": n_deals,
                 "contacts_in_window": n_threads, "matched": matched,
                 "merged_duplicates": n_merged,
                 "never_answered": sum(1 for r in opn if not r["we_replied"]),
                 "ball_in_our_court": sum(1 for r in opn if r["ball_in_our_court"]),
                 "excluded": sum(1 for r in inc if r.get("excluded")),
                 "other_stages": sorted({(r.get("stage") or "(none)") for r in other})}


def build(deals, threads, in_window):
    return reg.build_rows(deals, threads, in_window, channel="all")


# ---------------------------------------------------------------- rendering
def contact_routes(r):
    bits = []
    if r.get("email"):
        bits.append(r["email"])
    if r.get("phone"):
        bits.append(r["phone"])
    if r.get("linkedin"):
        bits.append(r["linkedin"])
    if r.get("website"):
        bits.append(r["website"])
    return " · ".join(bits) or "_no contact route on the record — it never became a deal_"


def render_thread(r):
    if not r["messages"]:
        return "> _(no thread text in Evergreen)_"
    out = []
    for m in r["messages"]:
        who = m["sender"] or ("them" if m["dir"] == "inbound" else "us")
        tag = "IN " if m["dir"] == "inbound" else "OUT"
        out.append(f"> **{tag}** {m['when']} — {who}: {m['body']}")
    return "\n>\n".join(out)


def render(rows_by_client, recon, labels, window_label, category, now, skipped, trend_check):
    total_in = sum(v["in_window"] for v in recon.values())
    total_open = sum(v["open"] for v in recon.values())
    total_never = sum(v["never_answered"] for v in recon.values())

    L = [f"# Open {category}s — {window_label}", ""]
    total_ball = sum(v["ball_in_our_court"] for v in recon.values())
    L.append(f"**{total_open} of {total_in} {category}s never converted to a call.** "
             f"{total_never} were never answered at all, and on {total_ball} more the lead "
             f"wrote last and nobody came back — so the ball is with us on "
             f"{total_never + total_ball} of {total_open}.")
    L.append("")
    L.append(f"Open = no meeting on the record and the deal is still parked at *Positive "
             f"Reply*, or there is no deal record at all. Disqualified / Lost / No Show are "
             f"excluded — they never converted either, but this is a call list, not an "
             f"autopsy. Built {now.strftime('%Y-%m-%d %H:%M')}Z from Evergreen only.")
    if skipped:
        L.append("")
        L.append("Not covered: " + ", ".join(skipped) + ".")
    L.append("")

    L.append("| client | in window | open | booked | other | never answered | ball with us |")
    L.append("|---|---:|---:|---:|---:|---:|---:|")
    for slug in sorted(recon, key=lambda s: -recon[s]["open"]):
        v = recon[slug]
        if not v["in_window"]:
            continue
        L.append(f"| {labels.get(slug, slug)} | {v['in_window']} | {v['open']} | "
                 f"{v['booked']} | {v['other']} | {v['never_answered']} | "
                 f"{v['ball_in_our_court']} |")
    L.append(f"| **total** | **{total_in}** | **{total_open}** | "
             f"**{sum(v['booked'] for v in recon.values())}** | "
             f"**{sum(v['other'] for v in recon.values())}** | **{total_never}** | "
             f"**{sum(v['ball_in_our_court'] for v in recon.values())}** |")
    L.append("")

    short = [t for t in trend_check if t[1] < t[2]]
    over = [t for t in trend_check if t[1] > t[2]]
    if short:
        L.append("> ⚠ **Under the endpoint's own count** — these clients are missing rows and "
                 "the numbers should not be published as-is: "
                 + "; ".join(f"{s}: {a} here vs {b} on the contacts endpoint" for s, a, b in short)
                 + ".")
        L.append("")
    if over:
        L.append("> Above the contacts endpoint on "
                 + ", ".join(f"{s} ({a} vs {b})" for s, a, b in over)
                 + " — those extras exist only as Airtable deals, so the contacts bucket "
                   "never had them. Expected; it is the reason both sources are unioned.")
        L.append("")

    for slug in sorted(rows_by_client, key=lambda s: -len(rows_by_client[s])):
        rows = rows_by_client[slug]
        if not rows:
            continue
        v = recon[slug]
        L.append(f"## {labels.get(slug, slug)} — {v['open']} open of {v['in_window']}")
        L.append("")
        for i, r in enumerate(rows, 1):
            placeholder = reg.nkey(r.get("contact")) in PLACEHOLDER_NAMES
            who = r["contact"] or "(no name on record)"
            co = f" — {r['company']}" if r.get("company") else ""
            L.append(f"### {i}. {who}{co}" + (" ⚠" if placeholder else ""))
            if placeholder:
                # the CRM's stand-in for "we never captured a name". The real one is usually
                # in the sign-off of their own reply — read the thread before writing back.
                L.append(f"*\u26a0 \u201c{who}\u201d is a placeholder, not their name — take it "
                         f"from their sign-off below before you reply.*")
            meta = [r.get("job_title") or "", r.get("channel") or "",
                    f"variant {r['copy_variant']}" if r.get("copy_variant") else "",
                    f"replied {(r.get('created_at') or '')[:10]}",
                    f"{r['days_since_reply']}d ago" if r.get("days_since_reply") is not None else ""]
            L.append(" · ".join(x for x in meta if x))
            if r.get("campaign_name"):
                L.append(f"*{r['campaign_name']}*")
            if not r["we_replied"]:
                status = "**never answered**"
            elif r["ball_in_our_court"]:
                status = "**they wrote last — ball is with us**"
            else:
                status = "we spoke last, no reply since"
            src = "no deal record — never opened as an opportunity" if r["source"] == "contact_only" \
                else f"deal stage `{r.get('stage') or '—'}`"
            L.append(f"{status} · {src}")
            L.append(contact_routes(r))
            if r["thread_truncated"]:
                L.append("")
                L.append("⚠ *thread truncated by Evergreen at 1200 chars — the end of this "
                         "conversation is not visible here.*")
            L.append("")
            L.append(render_thread(r))
            L.append("")
    return "\n".join(L) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--from", dest="start", required=True, help="YYYY-MM-DD")
    ap.add_argument("--to", dest="end", required=True, help="YYYY-MM-DD")
    ap.add_argument("--category", default="Power Request")
    ap.add_argument("--client", help="one Evergreen slug; default is every active client")
    ap.add_argument("--out", default=os.path.join(gm.ROOT, "clients/_rollup/output"))
    a = ap.parse_args()

    in_window, wslug, wlabel = reg.make_window(None, a.start, a.end)
    slugs = [a.client] if a.client else active_slugs()
    labels = {c["slug"]: c["client"] for c in reg.ev_get("/api/clients")}
    now = dt.datetime.now(dt.timezone.utc)

    print(f"{a.category}s, {wlabel} — {len(slugs)} client(s)")
    rows_by_client, recon, trend_check = OrderedDict(), OrderedDict(), []
    for slug in slugs:
        try:
            opn, v = collect(slug, in_window, a.category, now)
        except Exception as e:
            print(f"  {slug:18} FAILED: {str(e)[:80]}")
            continue
        rows_by_client[slug], recon[slug] = opn, v
        # independent denominator: the endpoint's own week bucket, when the window is one week
        # Independent denominator. The contacts endpoint RE-CATEGORISES a reply once it
        # books (it moves to the "Meeting Booked" bucket), so its Power Request count for
        # the week is the count of ones still open — which is exactly what we produce.
        # Under it = we're losing rows and the run should not be published. Over it = rows
        # that only exist on the deals side, which the contacts bucket never had.
        tr = week_trend(slug, a.category)
        if a.start in tr and (dt.date.fromisoformat(a.end) - dt.date.fromisoformat(a.start)).days < 7:
            trend_check.append((slug, v["open"], tr[a.start]))
        print(f"  {slug:18} in-window {v['in_window']:>3}  open {v['open']:>3}  "
              f"booked {v['booked']:>3}  other {v['other']:>3}"
              + (f"  ({', '.join(v['other_stages'])})" if v["other"] else ""))

    os.makedirs(a.out, exist_ok=True)
    cat_slug = a.category.lower().replace(" ", "-")
    stem = os.path.join(a.out, f"{wslug}-open-{cat_slug}s")
    md = render(rows_by_client, recon, labels, wlabel, a.category, now,
                ["Strike Tax (in Airtable, not loaded in Evergreen)"], trend_check)
    open(f"{stem}.md", "w").write(md)
    json.dump({"window": wlabel, "category": a.category,
               "built_at": now.isoformat()[:19] + "Z",
               "reconciliation": recon,
               "rows": [r for rs in rows_by_client.values() for r in rs]},
              open(f"{stem}.json", "w"), indent=1)

    total_open = sum(v["open"] for v in recon.values())
    total_in = sum(v["in_window"] for v in recon.values())
    print(f"\n  {total_open} open of {total_in} {a.category}s in window")
    for slug, mine, theirs in trend_check:
        if mine < theirs:
            print(f"  !! {slug}: {mine} open here vs {theirs} on the contacts endpoint — MISSING ROWS")
        elif mine > theirs:
            print(f"  .. {slug}: {mine} open here vs {theirs} on the contacts endpoint "
                  f"(+{mine - theirs} deals-only)")
    print(f"  -> {stem}.md")
    print(f"  -> {stem}.json")


if __name__ == "__main__":
    main()
