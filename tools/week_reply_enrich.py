#!/usr/bin/env python3
"""Fill in the contact details Evergreen doesn't carry, from the Airtable Contacts table.

WHY THIS EXISTS
  Evergreen's /deals rows carry email, phone, website and LinkedIn. Its /contacts rows —
  which is where most replies live, because most replies never become an opportunity —
  carry only name, title, company and a thread snippet. On the 2026-08-24 week that was
  66 of 82 unbooked replies with no way to contact the person at all.

  Airtable's "Master Inbox & CRM" Contacts table (tblw9gbzYD6LJV092 in appgezzL6Uqr0xgBa)
  is the record the inbox manager actually works from, and it holds all of it — email,
  phone, LinkedIn profile, website, title, city, country — for every lead, opportunity
  or not. This joins the two.

  Airtable has no API key on this machine, so the dump is taken through the Airtable MCP
  and handed to this script as a file:

    list_records_for_table(baseId="appgezzL6Uqr0xgBa", tableId="tblw9gbzYD6LJV092",
      fieldIds=["First name","Last name","Company Name","Title","email",
                "Phone Number Formatted","LinkedIn profile","Website","City","Country",
                "Client Name","Lead Categorisation"],
      filters={"operator":"and","operands":[{"operator":"isWithin",
        "operands":["fldHgcF6tiXvoRmGv",{"mode":"pastNumberOfDays","numberOfDays":6,
                                        "timeZone":"America/New_York"}]}]},
      pageSize=1000)

  fldHgcF6tiXvoRmGv is "Category Last Modified" — the week's replies are exactly the
  contacts the inbox manager re-categorised this week, so that filter is the right window.

MATCHING
  name+company first, then full name alone, then company alone — and only ever when the
  candidate is UNIQUE. An ambiguous match is left blank rather than guessed at, and every
  row records which rule matched it in `enriched_by` so a wrong join is findable later.

USAGE
  python3 tools/week_reply_enrich.py --window 2026-08-24_to_2026-08-28 \
      --airtable /path/to/airtable-contacts-week.json
"""
import argparse, csv, json, os, re, sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ghl_mine as gm
import week_reply_pack as pack

F = {"first": "fldALQg5UVX5RlqYT", "last": "fldT62W4F2eVqVOgM",
     "company": "fldWiHT3g7Ju32Jl2", "title": "fldrlmFac7RA9S3jQ",
     "email": "fldkym5iXtlCu4qMX", "phone": "fldblME5RoiNYMCYl",
     "linkedin": "fldaTQo5x95PLqSfM", "website": "fldksdHRO13jzvLac",
     "city": "fldf0E2mnWreRokVC", "country": "fldQ3lM9VtQAFnZeC",
     "client": "fldPYiFnIUpAXBsgK", "category": "fldAel2jWMpR63UVj"}

# Airtable stores these as singleSelect objects; everything else is a bare string.
def val(cell):
    if isinstance(cell, dict):
        return cell.get("name", "")
    if isinstance(cell, list):
        return ", ".join(val(x) for x in cell)
    return cell or ""


def nkey(s):
    return re.sub(r"[^a-z0-9]", "", (s or "").lower())


# Company suffixes carry no identity — "Herbal One Inc" and "Herbal One" are one company.
SUFFIX = re.compile(r"\b(inc|llc|ltd|limited|co|corp|corporation|company|group|holdings|"
                    r"plc|gmbh|pty|pvt|sa|srl|bv|ab|as|nv)\b\.?", re.I)


def ckey(s):
    return nkey(SUFFIX.sub("", s or ""))


def load_airtable(path):
    recs = json.load(open(path))["records"]
    out = []
    for r in recs:
        c = r.get("cellValuesByFieldId", {})
        name = f"{val(c.get(F['first']))} {val(c.get(F['last']))}".strip()
        out.append({
            "rec": r["id"], "name": name, "company": val(c.get(F["company"])),
            "title": val(c.get(F["title"])), "email": val(c.get(F["email"])),
            "phone": val(c.get(F["phone"])), "linkedin": val(c.get(F["linkedin"])),
            "website": val(c.get(F["website"])), "city": val(c.get(F["city"])),
            "country": val(c.get(F["country"])), "client": val(c.get(F["client"])),
            "category": val(c.get(F["category"])),
        })
    return out


def index(recs):
    by_nc, by_n, by_c = defaultdict(list), defaultdict(list), defaultdict(list)
    for a in recs:
        n, c = nkey(a["name"]), ckey(a["company"])
        if n and c:
            by_nc[(n, c)].append(a)
        if n:
            by_n[n].append(a)
        if c:
            by_c[c].append(a)
    return by_nc, by_n, by_c


def match(r, by_nc, by_n, by_c):
    """Returns (record, rule) or (None, reason). Unique matches only — an ambiguous
    company like 'Marketing' must never silently attach the wrong person's phone."""
    n, c = nkey(r.get("contact")), ckey(r.get("company"))
    for key, bucket, rule in (((n, c), by_nc, "name+company"), (n, by_n, "name"),
                              (c, by_c, "company")):
        if not key or (isinstance(key, tuple) and not all(key)):
            continue
        hits = bucket.get(key, [])
        if len(hits) == 1:
            return hits[0], rule
        if len(hits) > 1:
            # same person recorded twice with identical details is not ambiguity
            uniq = {(h["email"], h["phone"], h["linkedin"]) for h in hits}
            if len(uniq) == 1:
                return hits[0], rule + " (dup rows, identical details)"
    return None, "no unique match"


# Only ever ADD. An Evergreen deal row's own email/phone came from the same Airtable
# record and is the more trustworthy of the two; overwriting it would be churn.
FILL = ["email", "phone", "linkedin", "website", "title", "city", "country"]
DEST = {"title": "job_title"}


# Airtable tags replies with categories Evergreen's /contacts endpoint will not return.
# They are all dead ends, so they stay out of the pack — but they are COUNTED here, because
# "87 wrong numbers in a week" is a list-quality signal and silently dropping it would read
# as though the week were clean.
UNRETURNABLE = ["Wrong Number", "Retired", "Disqualified", "AI Automated", "AI Error"]
IN_SCOPE = set(pack.CATEGORIES)


def coverage(recs, d):
    """Cross-check the Evergreen-built pack against what Airtable says the inbox manager
    actually touched. Catches two specific failures: a client who works out of Airtable but
    has no Evergreen slug, and a whole category Evergreen cannot hand back."""
    from collections import Counter
    seen = {(d["labels"].get(s) or s).lower() for s in d["reconciliation"]}
    by_client, by_cat, missing = Counter(), Counter(), Counter()
    for a in recs:
        cl, cat = a["client"], a["category"]
        if cat in IN_SCOPE:
            by_client[cl] += 1
            if cl and cl.lower() not in seen and not any(
                    cl.lower().startswith(s.split()[0]) for s in seen if s):
                missing[cl] += 1
        elif cat in UNRETURNABLE:
            by_cat[cat] += 1
    return {"airtable_in_scope_by_client": dict(by_client.most_common()),
            "not_in_evergreen": dict(missing.most_common()),
            "dead_end_tags_evergreen_cannot_return": dict(by_cat.most_common())}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--window", default="2026-08-24_to_2026-08-28")
    ap.add_argument("--airtable", required=True)
    ap.add_argument("--out", default=os.path.join(gm.ROOT, "clients/_rollup/output"))
    a = ap.parse_args()

    src = os.path.join(a.out, f"{a.window}-unbooked-replies.json")
    d = json.load(open(src))
    recs = load_airtable(a.airtable)
    by_nc, by_n, by_c = index(recs)
    print(f"airtable: {len(recs)} contacts · pack: {len(d['rows'])} rows")

    stats = defaultdict(int)
    for r in d["rows"]:
        before = bool(r.get("email") or r.get("phone"))
        hit, rule = match(r, by_nc, by_n, by_c)
        r["enriched_by"] = rule if hit else ""
        if not hit:
            stats["unmatched"] += 1
            continue
        stats[rule] += 1
        for k in FILL:
            dest = DEST.get(k, k)
            if not r.get(dest) and hit.get(k):
                r[dest] = hit[k]
                stats["field:" + dest] += 1
        if not r.get("location") and (hit["city"] or hit["country"]):
            r["location"] = ", ".join(x for x in (hit["city"], hit["country"]) if x)
        if not r.get("company_linkedin_search"):
            r["company_linkedin_search"] = pack.linkedin_company_search(r.get("company"))
        if not before and (r.get("email") or r.get("phone")):
            stats["route recovered"] += 1

    d["enrichment"] = {"source": "Airtable Master Inbox & CRM / Contacts",
                       "airtable_records": len(recs), "matched": len(d["rows"]) - stats["unmatched"],
                       "unmatched": stats["unmatched"],
                       "routes_recovered": stats["route recovered"]}
    d["coverage"] = coverage(recs, d)
    json.dump(d, open(src, "w"), indent=1)

    label_of = d["labels"]
    with open(os.path.join(a.out, f"{a.window}-unbooked-replies.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=pack.CSV_COLS + ["enriched_by"])
        w.writeheader()
        for r in d["rows"]:
            row = pack.csv_row(r, label_of.get(r["client_slug"], r["client_slug"]))
            row["enriched_by"] = r.get("enriched_by", "")
            w.writerow(row)

    n = len(d["rows"])
    for k in sorted(stats):
        print(f"  {k:26} {stats[k]}")
    for k in ("email", "phone", "website", "linkedin", "job_title"):
        print(f"  now have {k:10} {sum(1 for r in d['rows'] if r.get(k)):>3}/{n}")
    print(f"  no route at all: {sum(1 for r in d['rows'] if not r.get('email') and not r.get('phone'))}/{n}")
    print(f"  -> {src}")


if __name__ == "__main__":
    main()
