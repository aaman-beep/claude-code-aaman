#!/usr/bin/env python3
"""Index page: one row per client — link + health verdict. Usage: gen_index.py urls.json"""
import json, os, sys, html

SP = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(SP, "data")
urls = json.load(open(sys.argv[1]))

CSS = """
:root { --paper:#F4F5F7; --card:#FFF; --ink:#171A20; --ink-2:#3D4453; --muted:#6B7280;
  --line:#E1E4EA; --line-2:#EFF1F4; --accent:#B5771A; --accent-soft:#FBF0DC;
  --good:#1B7A4B; --good-soft:#E3F2EA; --bad:#B8413A; --bad-soft:#FAE7E5;
  --serif:"Iowan Old Style","Palatino Linotype",Palatino,Georgia,serif;
  --sans:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif; }
@media (prefers-color-scheme:dark) { :root { --paper:#0F1116; --card:#171A21; --ink:#E7E9ED;
  --ink-2:#B6BCC7; --muted:#818997; --line:#272C36; --line-2:#1E222A; --accent:#E0A84C;
  --accent-soft:#2E2617; --good:#4FBF85; --good-soft:#15291F; --bad:#E2726A; --bad-soft:#341C1A; } }
:root[data-theme="dark"] { --paper:#0F1116; --card:#171A21; --ink:#E7E9ED; --ink-2:#B6BCC7;
  --muted:#818997; --line:#272C36; --line-2:#1E222A; --accent:#E0A84C; --accent-soft:#2E2617;
  --good:#4FBF85; --good-soft:#15291F; --bad:#E2726A; --bad-soft:#341C1A; }
:root[data-theme="light"] { --paper:#F4F5F7; --card:#FFF; --ink:#171A20; --ink-2:#3D4453;
  --muted:#6B7280; --line:#E1E4EA; --line-2:#EFF1F4; --accent:#B5771A; --accent-soft:#FBF0DC;
  --good:#1B7A4B; --good-soft:#E3F2EA; --bad:#B8413A; --bad-soft:#FAE7E5; }
* { box-sizing:border-box; }
body { margin:0; background:var(--paper); color:var(--ink); font-family:var(--sans); line-height:1.55; }
.wrap { max-width:880px; margin:0 auto; padding:0 24px 80px; }
header { padding:52px 0 26px; border-bottom:1px solid var(--line); margin-bottom:26px; }
.eyebrow { font-size:11px; letter-spacing:.14em; text-transform:uppercase; color:var(--accent);
  font-weight:650; margin:0 0 12px; }
h1 { font-family:var(--serif); font-size:clamp(28px,4.2vw,40px); line-height:1.12; margin:0 0 12px; font-weight:600; }
.lede { color:var(--ink-2); margin:0; font-size:15.5px; max-width:64ch; }
a.card { display:block; background:var(--card); border:1px solid var(--line); border-radius:7px;
  padding:18px 20px; margin-bottom:10px; text-decoration:none; color:var(--ink); }
a.card:hover { border-color:var(--accent); }
.cname { font-family:var(--serif); font-size:20px; font-weight:600; }
.verdict { color:var(--ink-2); font-size:13.5px; margin-top:5px; }
.chips { display:flex; flex-wrap:wrap; gap:6px; margin-top:9px; }
.pill { display:inline-block; font-size:10.5px; font-weight:750; letter-spacing:.04em;
  border-radius:4px; padding:2px 8px; }
.pill.hit { color:var(--good); background:var(--good-soft); }
.pill.miss { color:var(--bad); background:var(--bad-soft); }
.pill.na { color:var(--muted); background:var(--line-2); }
footer { margin-top:36px; padding-top:18px; border-top:1px solid var(--line); font-size:13px; color:var(--muted); }
"""

cards = []
for client, url in urls.items():
    d = json.load(open(f"{DATA}/{client}.json"))
    months = [m for m in d["monthly"] if m["pos_hit"] is not None]
    hp = sum(1 for m in months if m["pos_hit"]); hb = sum(1 for m in months if m["book_hit"])
    burners = sum(1 for b in d["sms_batches"] if b.get("burner"))
    chips = []
    if months:
        chips.append(f'<span class="pill {"hit" if hp==len(months) else "miss" if hp==0 else "na"}">positives {hp}/{len(months)} mo</span>')
        chips.append(f'<span class="pill {"hit" if hb==len(months) else "miss" if hb==0 else "na"}">booked {hb}/{len(months)} mo</span>')
        chips.append(f'<span class="pill {"miss" if d["missed"] else "hit"}">{len(d["missed"])} unconverted replies</span>')
    else:
        chips.append('<span class="pill na">no KPI data — not in Evergreen</span>')
    if d["sms_batches"]:
        chips.append(f'<span class="pill na">{len(d["sms_batches"])} SMS copy units{f" · {burners} burners" if burners else ""}</span>')
    ecamps = [c for c in d["email_campaigns"] if (c.get("sent") or 0) > 0]
    if ecamps:
        chips.append(f'<span class="pill na">{len(ecamps)} email campaigns</span>')
    saved = sum(1 for x in d["crosscheck"] if x["in_evergreen"])
    if d["crosscheck"]:
        chips.append(f'<span class="pill {"miss" if saved < len(d["crosscheck"])//2 else "na"}">{saved}/{len(d["crosscheck"])} copies in Evergreen</span>')
    cards.append(f'''<a class="card" href="{url}">
      <div class="cname">{html.escape(d["label"])}</div>
      <div class="chips">{"".join(chips)}</div></a>''')

page = f"""<title>Client troubleshooting — index</title>
<style>{CSS}</style>
<div class="wrap">
<header>
  <p class="eyebrow">Scaletopia · outbound troubleshooting · 2026-07-13</p>
  <h1>Seven clients, one page each</h1>
  <p class="lede">Each dashboard answers the same four questions: which campaigns ran each month,
  which months hit the positive-reply and booked KPIs, every piece of copy that ever went out
  (SMS from the GHL send log, email from EmailBison with spintax rendered plain), and every
  positive reply that never became a meeting.</p>
</header>
{''.join(cards)}
<footer>Built from GoHighLevel send logs · EmailBison API · Evergreen knowledge API (live Airtable).
Dashboards are private until you share them.</footer>
</div>
"""
open(f"{SP}/pages/index-troubleshoot.html", "w").write(page)
print("wrote pages/index-troubleshoot.html")
