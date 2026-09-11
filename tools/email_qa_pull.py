#!/usr/bin/env python3
"""Pull every client's live email campaign copy + performance from Evergreen.

Evergreen only — no EmailBison / GHL / Airtable MCP calls. The running copy is
reconstructed by Evergreen from the outbound messages inside reply threads
(/report), then joined by campaign name to the live Airtable status (/stats).

Output: clients/_rollup/output/email-qa-corpus.json
  { pulled_at, in_scope, coverage: [...], campaigns: [{client, campaign, status,
      sent, positives, power_requests, booked, power_rate_pct, vs_client_avg,
      t1, t2, variant, reconstructed_at}] }

USAGE: python3 tools/email_qa_pull.py [--status PROCESSING,PAUSED,COMPLETED]
"""
import argparse, datetime as dt, json, os, re, sys, time, urllib.request
from concurrent.futures import ThreadPoolExecutor

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://knowledgebase-production-f52e.up.railway.app"

SLUGS = ["acceler8", "big_leap", "chamber_media", "digital_resource", "go_fish",
         "growth_lab", "kynship", "leadgenix", "redo", "scaletopia", "seedx",
         "wise_digital"]


def get(path, tries=3):
    for a in range(tries):
        try:
            r = urllib.request.Request(BASE + path, headers={
                "Accept": "application/json", "User-Agent": "curl/8.7.1"})
            with urllib.request.urlopen(r, timeout=180) as resp:
                return json.loads(resp.read().decode())
        except Exception as e:
            if a == tries - 1:
                print(f"  !! {path}: {str(e)[:120]}", flush=True)
                return None
            time.sleep(2 * (a + 1))


def norm(name):
    """Campaign names differ by whitespace/case between the two endpoints."""
    return re.sub(r"\s+", " ", (name or "")).strip().lower()


def pull(slug):
    return slug, get(f"/api/clients/{slug}/report"), get(f"/api/clients/{slug}/stats")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--status", default="PROCESSING,PAUSED,COMPLETED",
                    help="comma-separated Airtable statuses to keep")
    args = ap.parse_args()
    keep = {s.strip().upper() for s in args.status.split(",") if s.strip()}

    with ThreadPoolExecutor(max_workers=12) as ex:
        pulled = list(ex.map(pull, SLUGS))

    rows, coverage = [], []
    for slug, report, stats in pulled:
        if not report or not stats:
            coverage.append({"client": slug, "error": "fetch failed"})
            continue

        # live Airtable status, keyed by normalised campaign name
        status_by_name = {norm(c.get("name")): (c.get("status") or "").upper()
                          for c in (stats.get("campaigns") or [])
                          if (c.get("type") or "") == "EmailBison"}

        email = [c for c in (report.get("campaigns") or []) if c.get("channel") == "email"]
        with_copy = [c for c in email if (c.get("live_copy") or {}).get("t1")]

        unmatched = in_scope = 0
        for c in with_copy:
            status = status_by_name.get(norm(c.get("name")))
            if status is None:
                unmatched += 1
                continue
            if status not in keep:
                continue
            in_scope += 1
            lc = c["live_copy"]
            rows.append({
                "client": slug,
                "campaign": c.get("name"),
                "status": status,
                "sent": c.get("sent"),
                "positives": c.get("positives"),
                "power_requests": c.get("power_requests"),
                "booked": c.get("booked"),
                "power_rate_pct": c.get("power_rate_pct"),
                "vs_client_avg": c.get("vs_client_avg"),
                "variant": lc.get("variant"),
                "t1": lc.get("t1"),
                "t2": lc.get("t2"),
                "reconstructed_at": lc.get("reconstructed_at"),
            })

        coverage.append({"client": slug, "email_campaigns": len(email),
                         "with_copy": len(with_copy), "in_scope": in_scope,
                         "dropped_no_status_match": unmatched})

    out = {"pulled_at": dt.datetime.now(dt.timezone.utc).isoformat(),
           "statuses_kept": sorted(keep), "in_scope": len(rows),
           "coverage": coverage, "campaigns": rows}

    dest = os.path.join(ROOT, "clients", "_rollup", "output", "email-qa-corpus.json")
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, "w") as f:
        json.dump(out, f, indent=1)

    print(f"{'client':18} {'email':>6} {'copy':>6} {'scope':>6} {'unmatched':>10}")
    for c in coverage:
        if "error" in c:
            print(f"{c['client']:18} {c['error']}")
            continue
        print(f"{c['client']:18} {c['email_campaigns']:6} {c['with_copy']:6} "
              f"{c['in_scope']:6} {c['dropped_no_status_match']:10}")
    by_status = {}
    for r in rows:
        by_status[r["status"]] = by_status.get(r["status"], 0) + 1
    print(f"\nIN SCOPE: {len(rows)} campaigns  {by_status}")
    print(f"-> {dest}")


if __name__ == "__main__":
    main()
