#!/usr/bin/env python3
"""Pull a client's EmailBison campaigns, stats, and sequence copy.

Credentials come from the emailbison-<client> MCP servers already configured in
~/.claude.json (Authorization + Instance-URL headers) — no secrets in the repo.

Output: clients/<client>/output/emailbison.json
  { pulled_at, campaigns: [{id, name, status, type, leads, sent, opens, replies,
      bounced, completion, created_at, steps: [{order, variant, wait_in_days,
      subject_raw, body_raw_html, subject_plain, body_plain}]}] }

USAGE: python tools/eb_pull.py --client gofish
"""
import argparse, datetime as dt, json, os, sys, time, urllib.request
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from spintax import resolve, strip_html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def creds(client):
    cfg = json.load(open(os.path.expanduser("~/.claude.json")))
    s = cfg.get("mcpServers", {}).get(f"emailbison-{client}")
    if not s:
        sys.exit(f"No MCP server 'emailbison-{client}' in ~/.claude.json")
    h = s.get("headers", {})
    return h["Instance-URL"].rstrip("/"), h["Authorization"]


def get(base, auth, path, tries=3, body=None, method="GET"):
    data = json.dumps(body).encode() if body is not None else None
    for a in range(tries):
        try:
            r = urllib.request.Request(base + path, data=data, method=method, headers={
                "Authorization": auth, "Accept": "application/json",
                "Content-Type": "application/json", "User-Agent": "curl/8.7.1"})
            with urllib.request.urlopen(r, timeout=60) as resp:
                return json.loads(resp.read().decode())
        except Exception as e:
            if a == tries - 1:
                print(f"  !! {path}: {str(e)[:100]}", flush=True)
                return None
            time.sleep(1.5 * (a + 1))


def months_between(start, end):
    y, m = int(start[:4]), int(start[5:7])
    ey, em = int(end[:4]), int(end[5:7])
    out = []
    while (y, m) <= (ey, em):
        last = [31, 29 if y % 4 == 0 and (y % 100 or y % 400 == 0) else 28, 31, 30, 31, 30,
                31, 31, 30, 31, 30, 31][m - 1]
        out.append((f"{y:04d}-{m:02d}", f"{y:04d}-{m:02d}-01", f"{y:04d}-{m:02d}-{last}"))
        m += 1
        if m == 13:
            y, m = y + 1, 1
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--client", required=True)
    ap.add_argument("--out")
    a = ap.parse_args()

    base, auth = creds(a.client)
    reg = json.load(open(os.path.join(ROOT, "clients", "registry.json")))
    cfg = reg.get(a.client, {})
    out_dir = a.out or os.path.join(ROOT, cfg.get("output", f"clients/{a.client}/output"))
    os.makedirs(out_dir, exist_ok=True)

    campaigns, page = [], 1
    while True:
        d = get(base, auth, f"/api/campaigns?page={page}&per_page=50")
        if not d or not d.get("data"):
            break
        campaigns += d["data"]
        meta = d.get("meta", {})
        if page >= (meta.get("last_page") or 1):
            break
        page += 1

    out = []
    for c in campaigns:
        cid = c["id"]
        row = {
            "id": cid, "name": c.get("name"), "status": c.get("status"),
            "type": c.get("type"), "created_at": c.get("created_at"),
            "leads": c.get("total_leads"),
            "leads_contacted": c.get("total_leads_contacted"),
            "sent": c.get("emails_sent"),
            "opens": c.get("unique_opens"),
            "replies": c.get("unique_replies"),
            "bounced": c.get("bounced"),
            "interested": c.get("interested"),
            "unsubscribed": c.get("unsubscribed"),
            "completion": c.get("completion_percentage"),
            "steps": [],
        }
        # per-sequence-step stats (which email COPY actually performed) — POST, not GET
        allstats = get(base, auth, f"/api/campaigns/{cid}/stats", method="POST",
                       body={"start_date": "2024-01-01", "end_date": "2030-12-31"}) or {}
        sd = allstats.get("data") or allstats.get("stats") or {}
        step_stats = {s["sequence_step_id"]: s for s in (sd.get("sequence_step_stats") or [])}

        seq = get(base, auth, f"/api/campaigns/v1.1/{cid}/sequence-steps")
        for s in ((seq or {}).get("data") or {}).get("sequence_steps", []):
            subj, body = s.get("email_subject") or "", s.get("email_body") or ""
            st = step_stats.get(s.get("id"), {})
            row["steps"].append({
                "id": s.get("id"),
                "order": s.get("order"), "variant": s.get("variant"),
                "wait_in_days": s.get("wait_in_days"),
                "thread_reply": s.get("thread_reply"),
                "subject_raw": subj, "body_raw_html": body,
                "subject_plain": resolve(subj),
                "body_plain": strip_html(resolve(body)),
                "sent": st.get("sent"), "replies": st.get("unique_replies"),
                "interested": st.get("interested"), "bounced": st.get("bounced"),
                "unsubscribed": st.get("unsubscribed"),
            })

        # real monthly email volume (the campaign object only carries lifetime totals).
        # One POST per month per campaign — fanned out, or the big accounts take ~30 min.
        row["monthly"] = {}
        created = (c.get("created_at") or "")[:10]
        if created and (row["sent"] or 0) > 0:
            def one_month(win):
                label, s0, s1 = win
                m = get(base, auth, f"/api/campaigns/{cid}/stats", method="POST",
                        body={"start_date": s0, "end_date": s1}) or {}
                md = m.get("data") or m.get("stats") or {}
                sent = int(md.get("emails_sent") or 0)
                if not sent:
                    return None
                return (label, {"sent": sent,
                                "replies": int(md.get("unique_replies_per_contact") or 0),
                                "interested": int(md.get("interested") or 0),
                                "bounced": int(md.get("bounced") or 0)})
            wins = months_between(created, dt.date.today().isoformat())
            with ThreadPoolExecutor(8) as ex:
                for r in ex.map(one_month, wins):
                    if r:
                        row["monthly"][r[0]] = r[1]
        out.append(row)
        print(f"  [{a.client}] {c.get('name','?')[:52]} — {len(row['steps'])} steps, "
              f"{len(row['monthly'])} active months", flush=True)

    path = os.path.join(out_dir, "emailbison.json")
    json.dump({"pulled_at": dt.datetime.now(dt.timezone.utc).isoformat(),
               "client": a.client, "campaigns": out}, open(path, "w"), indent=2)
    print(f"wrote {path} ({len(out)} campaigns)")


if __name__ == "__main__":
    main()
