#!/usr/bin/env python3
"""Flag (never silently drop) opted-out people in a PR register before it becomes a call sheet.

The register + followup_sheet pipeline has no opt-out check: someone who replied
"yes send info" in July and later texted STOP still lands on the sheet. That is TCPA
exposure, so this pass marks them loudly and leaves the judgement to the rep.

Two independent signals, both from GHL (Evergreen can't answer this — it excludes hard
opt-outs, so its reply data is a floor):
  1. contact.dnd / dndSettings on the GHL contact record
  2. a STOP-shaped inbound in the thread we already pulled (ghl_mine.STOP_RX)

Also optionally drops a campaign cohort (--exclude-campaign) — e.g. a conference push
that shouldn't be re-texted as if it were cold outbound.

Writes the enriched register back in place, adding per row:
  opted_out (bool) · optout_reason (str) · optout_evidence (str, the quoted STOP text)

Usage:
  python tools/followup_optout_flag.py --client wise-digital \
      --window 2026-03-01_to_2026-08-12 --exclude-campaign engage
"""
import argparse, json, os, sys, urllib.parse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ghl_mine as gm

DND_KEYS = ("dnd",)


def ghl_contacts_by_phone(pit, loc, phones):
    """Look each phone up in GHL. Returns {normalised_phone: contact}."""
    out = {}
    for i, ph in enumerate(sorted(phones), 1):
        if not ph:
            continue
        q = urllib.parse.quote(ph)
        d = gm.req(pit, "/contacts/", "2021-07-28",
                   query={"locationId": loc, "query": ph, "limit": 5}) or {}
        for c in d.get("contacts", []):
            for field in ("phone", "phoneLabel"):
                v = c.get(field)
                if v and gm_norm(v) == gm_norm(ph):
                    out[gm_norm(ph)] = c
        if i % 25 == 0:
            print(f"    …{i}/{len(phones)} looked up", flush=True)
    return out


def gm_norm(p):
    return "".join(ch for ch in str(p or "") if ch.isdigit())[-10:]


def stop_hit(row):
    """First STOP-shaped inbound in the thread, if any."""
    for m in row.get("messages") or []:
        if (m.get("dir") or "").lower() != "inbound":
            continue
        body = (m.get("body") or "").strip()
        if gm.STOP_RX.match(body):
            return body[:160]
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--client", required=True, help="key in clients/registry.json")
    ap.add_argument("--window", required=True, help="e.g. 2026-03-01_to_2026-08-12")
    ap.add_argument("--channel", default="sms", choices=["sms", "email", "all"])
    ap.add_argument("--exclude-campaign", action="append", default=[],
                    help="substring; rows whose campaign matches are marked excluded "
                         "(repeatable)")
    a = ap.parse_args()

    reg = {k: v for k, v in json.load(open(gm.REGISTRY)).items() if not k.startswith("_")}
    if a.client not in reg:
        sys.exit(f"'{a.client}' not in registry. Known: {', '.join(sorted(reg))}")
    cfg = reg[a.client]
    out_dir = os.path.join(gm.ROOT, cfg.get("output", f"clients/{a.client}/output"))
    path = os.path.join(out_dir, f"{a.window}-{a.channel}-prs.json")
    if not os.path.exists(path):
        sys.exit(f"{path} not found — run july_pr_register.py for that window first.")

    doc = json.load(open(path))
    rows = doc["rows"]
    print(f"[{cfg.get('label', a.client)}] {len(rows)} rows in {os.path.basename(path)}")

    # --- campaign cohort exclusion (e.g. a conference push) ---
    n_camp = 0
    for r in rows:
        camp = (r.get("campaign_name") or "").lower()
        for pat in a.exclude_campaign:
            if pat.lower() in camp:
                r["excluded"] = True
                r["override_reason"] = (r.get("override_reason") or
                                        f"excluded cohort: campaign matches '{pat}'")
                n_camp += 1
                break
    if a.exclude_campaign:
        print(f"  excluded {n_camp} row(s) by campaign: {a.exclude_campaign}")

    # --- STOP scan on threads we already have (free, no API call) ---
    for r in rows:
        r.setdefault("opted_out", False)
        r.setdefault("optout_reason", "")
        r.setdefault("optout_evidence", "")
        hit = stop_hit(r)
        if hit:
            r["opted_out"] = True
            r["optout_reason"] = "replied STOP"
            r["optout_evidence"] = hit
    n_stop = sum(1 for r in rows if r["opted_out"])
    print(f"  STOP-shaped inbound found in thread: {n_stop}")

    # --- DND lookup in GHL for everyone still live on the sheet ---
    sms = cfg.get("sms") or {}
    pit = gm.creds_from_mcp(sms["mcp"]) if sms.get("mcp") else None
    loc = sms.get("locationId")
    if not (pit and loc):
        print("  !! no GHL connector for this client — DND check skipped", file=sys.stderr)
    else:
        live = [r for r in rows if not r.get("excluded")]
        phones = {r.get("phone") for r in live if r.get("phone")}
        print(f"  looking up {len(phones)} phone(s) in GHL for DND…")
        found = ghl_contacts_by_phone(pit, loc, phones)
        n_dnd = 0
        for r in live:
            c = found.get(gm_norm(r.get("phone")))
            if not c:
                continue
            if any(c.get(k) for k in DND_KEYS):
                r["opted_out"] = True
                r["optout_reason"] = ("DND + replied STOP" if r["optout_reason"]
                                      else "DND flag set in GHL")
                n_dnd += 1
        print(f"  DND flagged in GHL: {n_dnd}  (matched {len(found)}/{len(phones)} phones)")

    total = sum(1 for r in rows if r["opted_out"] and not r.get("excluded"))
    doc["optout_flagged"] = total
    doc["optout_policy"] = "flag, do not drop — rep decides"
    json.dump(doc, open(path, "w"), indent=1)
    print(f"\n  {total} live row(s) flagged as opted out — surfaced, NOT removed")
    print(f"  wrote {path}")


if __name__ == "__main__":
    main()
