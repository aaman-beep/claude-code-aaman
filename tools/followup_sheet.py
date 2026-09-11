#!/usr/bin/env python3
"""Turn a reply register into a call sheet: the qualified, unconverted leads, ready to work.

WHY THIS IS SEPARATE FROM july_pr_page.py
  The register answers "what happened last month". This answers "who do I contact in the
  next two hours". Different job, so a different page — one row per person, the contact
  route on the row, and the last thing they said in full, because that is what you need in
  front of you when you write the follow-up.

WHAT "QUALIFIED" MEANS HERE
  A reply that (a) counts as positive under the CRM's own rule, (b) never booked, (c)
  wasn't excluded by hand, and (d) has a CRM deal record. That last test is the one that
  matters: replies that never became an opportunity were never qualified by anyone, and in
  Scaletopia's Jul-Aug data they are exactly the thin ones — no company, one-word answers.
  They're carried through to a second list rather than deleted, because "nobody qualified
  this" is not the same claim as "this is not qualified".

USAGE
  python3 tools/followup_sheet.py --client scaletopia --window 2026-07-01_to_2026-08-05
"""
import argparse, html, json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ghl_mine as gm

# Work order: the strongest ask first. Someone who said "yes, here's my email" is a
# different job from someone who asked what it costs.
ASK_ORDER = ["Power Request", "Positive", "More Info Request", "Email Me Request",
             "Objection Handling", "Referral Request", "Custom Response", "Future Request"]

ASK_COPY = {
    "Power Request": ["Said yes", "Agreed to a call or handed over a contact. Pick the time for them."],
    "Positive": ["Warm, no ask", "Replied positively without asking for anything specific."],
    "More Info Request": ["Wants detail", "Asked how it works. Answer the question, then propose a slot."],
    "Email Me Request": ["Asked for email", "Wanted it in writing. Send it, then come back to the thread."],
    "Objection Handling": ["Pushed back", "Engaged but led with a blocker — usually price. Answer it straight."],
    "Referral Request": ["Pointed elsewhere", "Not them. Named someone else to contact."],
    "Custom Response": ["Other", "Didn't fit a standard bucket."],
    "Future Request": ["Later", "Warm but gave a timeline. Diarise rather than chase."],
}


def esc(s):
    return html.escape(str(s or ""))


def qualified(r):
    return (r.get("counted_positive") and not r.get("booked")
            and not r.get("excluded") and r.get("warm_tier") != "not_warm")


def last_inbound(r):
    ins = [m for m in r["messages"] if m["dir"] == "inbound"]
    return ins[-1]["body"] if ins else ""


def last_outbound(r):
    outs = [m for m in r["messages"] if m["dir"] == "outbound" and not m["automated"]]
    return outs[-1]["body"] if outs else ""


def build(d, out_path):
    rows = [r for r in d["rows"] if qualified(r)]
    main = [r for r in rows if r["source"] != "contact_only"]
    thin = [r for r in rows if r["source"] == "contact_only"]

    def prep(r):
        return {**{k: r.get(k) for k in
                   ("contact", "job_title", "company", "website", "linkedin", "email",
                    "phone", "location", "category", "days_silent", "we_replied",
                    "created_at", "campaign_name", "warm_tier", "source",
                    "opted_out", "optout_reason", "optout_evidence")},
                "said": last_inbound(r), "ours": last_outbound(r),
                "n_messages": r.get("n_messages")}

    # Opted-out people are flagged, never silently dropped (see followup_optout_flag.py),
    # so they sort to the TOP of their bucket — the rep must see them before texting.
    order = lambda rs: sorted(rs, key=lambda r: (
        ASK_ORDER.index(r["category"]) if r["category"] in ASK_ORDER else 99,
        not r.get("opted_out"),
        -(r["days_silent"] or 0)))

    n_flag = sum(1 for r in rows if r.get("opted_out"))
    payload = {"main": [prep(r) for r in order(main)],
               "thin": [prep(r) for r in order(thin)],
               "ask_order": ASK_ORDER, "ask_copy": ASK_COPY,
               "optout_flagged": n_flag, "optout_total": len(rows),
               "client": d["client"], "window": d["month"], "built_at": d["built_at"]}

    doc = (TEMPLATE.replace("__DATA__", json.dumps(payload))
           .replace("__CLIENT__", esc(d["client"]))
           .replace("__WINDOW__", esc(pretty_window(d["month"]))))
    open(out_path, "w").write(doc)
    return len(main), len(thin)


def pretty_window(w):
    m = re.match(r"(\d{4})-(\d{2})-(\d{2})_to_(\d{4})-(\d{2})-(\d{2})", w or "")
    if not m:
        return w
    mo = ["", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    a, b = m.groups()[:3], m.groups()[3:]
    return f"{int(a[2])} {mo[int(a[1])]} – {int(b[2])} {mo[int(b[1])]} {b[0]}"


TEMPLATE = r"""<title>__CLIENT__ — follow-up list, __WINDOW__</title>
<style>
:root{
  --paper:#F7F7F5; --surface:#FFFFFF; --sunk:#EFEFEB;
  --ink:#17181A; --ink-2:#4C4E52; --ink-3:#7C7F85;
  --rule:#E0E0DA; --rule-2:#C7C7BF;
  --accent:#1F5C3D; --accent-soft:#E3EFE8;
  --hot:#B33A17; --hot-soft:#FBE8E1; --gold:#96700B;
  --sans:ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
  --mono:ui-monospace,SFMono-Regular,"SF Mono",Menlo,Consolas,monospace;
}
@media (prefers-color-scheme:dark){:root{
  --paper:#0F1110; --surface:#181A19; --sunk:#1F2220;
  --ink:#EAEBE8; --ink-2:#A6A9A4; --ink-3:#787C78;
  --rule:#2A2E2B; --rule-2:#3C413D;
  --accent:#6FC095; --accent-soft:#16281F;
  --hot:#F0906C; --hot-soft:#35201A; --gold:#D6AA4B;
}}
:root[data-theme="dark"]{
  --paper:#0F1110; --surface:#181A19; --sunk:#1F2220;
  --ink:#EAEBE8; --ink-2:#A6A9A4; --ink-3:#787C78;
  --rule:#2A2E2B; --rule-2:#3C413D;
  --accent:#6FC095; --accent-soft:#16281F;
  --hot:#F0906C; --hot-soft:#35201A; --gold:#D6AA4B;
}
:root[data-theme="light"]{
  --paper:#F7F7F5; --surface:#FFFFFF; --sunk:#EFEFEB;
  --ink:#17181A; --ink-2:#4C4E52; --ink-3:#7C7F85;
  --rule:#E0E0DA; --rule-2:#C7C7BF;
  --accent:#1F5C3D; --accent-soft:#E3EFE8;
  --hot:#B33A17; --hot-soft:#FBE8E1; --gold:#96700B;
}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);font-family:var(--sans);
     font-size:15px;line-height:1.5;-webkit-font-smoothing:antialiased}
.wrap{max-width:940px;margin:0 auto;padding:0 20px}

header{padding:32px 0 18px;border-bottom:2px solid var(--ink)}
h1{margin:0;font-size:26px;font-weight:660;letter-spacing:-.022em}
.sub{font-family:var(--mono);font-size:11.5px;letter-spacing:.06em;text-transform:uppercase;
     color:var(--ink-3);margin-top:5px}
.lede{margin:12px 0 0;color:var(--ink-2);max-width:62ch;font-size:14.5px}
.warn{margin:14px 0 0;padding:11px 14px;border:2px solid #b3261e;border-radius:8px;
      background:#fdf0ef;color:#8c1d18;font-size:14px;font-weight:560}
.warn b{font-family:var(--mono);font-size:12.5px;letter-spacing:.04em}
.lead.-out{border-left:4px solid #b3261e;background:#fdf0ef}
.stop{display:inline-block;font-family:var(--mono);font-size:11px;letter-spacing:.06em;
      padding:4px 9px;border-radius:4px;background:#b3261e;color:#fff;font-weight:700;
      margin-bottom:7px}
.stop-why{font-size:13px;color:#8c1d18;margin:0 0 8px}
.bar{display:flex;flex-wrap:wrap;gap:9px;margin-top:16px;align-items:center}
.pill{font-family:var(--mono);font-size:11.5px;padding:5px 10px;border-radius:999px;
      background:var(--sunk);color:var(--ink-2);font-variant-numeric:tabular-nums}
.pill.-n{background:var(--accent);color:var(--surface);font-weight:600}
.tick{margin-left:auto;font-size:12.5px;color:var(--ink-3);font-family:var(--mono)}

.grp{margin-top:34px}
.grp h2{margin:0 0 2px;font-size:17px;font-weight:650;letter-spacing:-.015em;
        display:flex;align-items:baseline;gap:9px}
.grp h2 .c{font-family:var(--mono);font-size:11.5px;background:var(--accent);color:var(--surface);
           padding:2px 8px;border-radius:999px;font-variant-numeric:tabular-nums}
.grp > p{margin:0 0 12px;font-size:13.5px;color:var(--ink-3);max-width:68ch}

.lead{background:var(--surface);border:1px solid var(--rule);border-radius:10px;
      padding:14px 16px;margin-bottom:9px;display:grid;
      grid-template-columns:1fr auto;gap:4px 16px;align-items:start}
.lead.done{opacity:.42}
.lead.done .nm{text-decoration:line-through}
.hd{display:flex;flex-wrap:wrap;align-items:baseline;gap:4px 9px;min-width:0}
.nm{font-weight:650;font-size:16px;letter-spacing:-.01em}
.ti{font-size:13px;color:var(--ink-3)}
.co{font-size:13.5px;color:var(--ink-2);font-weight:500}
.co a{color:var(--accent)}
.age{font-family:var(--mono);font-size:11px;padding:3px 8px;border-radius:999px;
     background:var(--sunk);color:var(--ink-3);white-space:nowrap;font-weight:600}
.age.-hot{background:var(--hot-soft);color:var(--hot)}
.quote{grid-column:1/-1;margin:8px 0 0;padding:9px 13px;background:var(--sunk);
       border-left:3px solid var(--accent);border-radius:0 7px 7px 0;font-size:14px}
.quote b{display:block;font-family:var(--mono);font-size:9.5px;letter-spacing:.08em;
         text-transform:uppercase;color:var(--ink-3);margin-bottom:3px}
.quote.-ours{border-left-color:var(--rule-2);background:transparent;
             border:1px dashed var(--rule-2);border-radius:7px;color:var(--ink-2);font-size:13px}
.routes{grid-column:1/-1;display:flex;flex-wrap:wrap;gap:7px;margin-top:9px;align-items:center}
.route{font-family:var(--mono);font-size:12px;padding:5px 10px;border-radius:6px;
       border:1px solid var(--rule-2);color:var(--ink-2);text-decoration:none;
       display:inline-flex;gap:6px;align-items:center}
.route:hover{border-color:var(--accent);color:var(--accent)}
.route b{font-family:var(--sans);font-size:10px;text-transform:uppercase;letter-spacing:.06em;
         color:var(--ink-3);font-weight:600}
.mark{margin-left:auto;font:inherit;font-size:12px;background:none;cursor:pointer;
      border:1px solid var(--rule-2);border-radius:6px;padding:5px 11px;color:var(--ink-2)}
.mark:hover{border-color:var(--accent);color:var(--accent)}
:focus-visible{outline:2px solid var(--accent);outline-offset:2px}

details.thin{margin:44px 0 0;border:1px dashed var(--rule-2);border-radius:10px;padding:2px 18px 10px}
details.thin > summary{cursor:pointer;font-weight:640;font-size:15px;padding:14px 0;list-style:none}
details.thin > summary::-webkit-details-marker{display:none}
details.thin > summary::before{content:"▸ ";color:var(--ink-3)}
details.thin[open] > summary::before{content:"▾ "}
details.thin > p{font-size:13.5px;color:var(--ink-3);max-width:68ch;margin:0 0 12px}
footer{margin:50px 0 40px;padding-top:16px;border-top:1px solid var(--rule);
       font-size:12.5px;color:var(--ink-3);max-width:70ch}
footer p{margin:0 0 8px}
@media (max-width:680px){
  .lead{grid-template-columns:1fr}
  .age{justify-self:start}
  .mark{margin-left:0}
}
@media print{
  body{background:#fff} .mark,.tick{display:none} .lead{break-inside:avoid;border-color:#bbb}
  details.thin{break-before:page} details.thin[open] > summary::before{content:""}
}
@media (prefers-reduced-motion:reduce){*{transition:none!important}}
</style>

<header><div class="wrap">
  <h1>Follow-up list</h1>
  <div class="sub">__CLIENT__ · cold SMS · __WINDOW__</div>
  <p class="lede">Qualified positive replies that never booked. Ordered by what they asked
    for, then by how long they've been sitting.</p>
  <div id="warn"></div>
  <div class="bar" id="bar"></div>
</div></header>

<main class="wrap" id="main"></main>
<footer class="wrap" id="foot"></footer>

<script>
const D = __DATA__;
const esc = s => String(s??"").replace(/[&<>"']/g, c =>
  ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
const done = new Set();

function routes(r){
  const out = [];
  if(r.phone)    out.push(`<a class="route" href="sms:${esc(r.phone)}"><b>text</b>${esc(r.phone)}</a>`);
  if(r.email)    out.push(`<a class="route" href="mailto:${esc(r.email)}"><b>email</b>${esc(r.email)}</a>`);
  if(r.linkedin) out.push(`<a class="route" href="${esc(r.linkedin)}" target="_blank" rel="noopener"><b>linkedin</b>profile</a>`);
  if(r.website)  out.push(`<a class="route" href="${esc(r.website)}" target="_blank" rel="noopener"><b>site</b>${esc(r.website.replace(/^https?:\/\/(www\.)?/,"").replace(/\/$/,""))}</a>`);
  return out.join("");
}

function lead(r, i, pfx){
  const id = pfx + i;
  const hot = (r.days_silent ?? 0) >= 21;
  const out = !!r.opted_out;
  return `<div class="lead ${out?"-out":""}" id="${id}">
    ${out ? `<div class="stop">⛔ DO NOT TEXT — OPTED OUT</div>
    <p class="stop-why">${esc(r.optout_reason||"opted out")}${
      r.optout_evidence ? ` — they replied: “${esc(r.optout_evidence)}”` : ""}</p>` : ""}
    <div class="hd"><span class="nm">${esc(r.contact||"—")}</span>
      <span class="co">${esc(r.company||"")}</span>
      <span class="ti">${esc(r.job_title||"")}</span></div>
    <span class="age ${hot?"-hot":""}">${r.days_silent==null?"—":r.days_silent+"d silent"}</span>
    ${r.said ? `<div class="quote"><b>they said</b>${esc(r.said)}</div>` : ""}
    ${r.ours ? `<div class="quote -ours"><b>we last sent</b>${esc(r.ours)}</div>` : ""}
    <div class="routes">${routes(r)}
      <button class="mark" data-id="${id}">Mark done</button></div>
  </div>`;
}

function group(list, pfx){
  let out = "";
  D.ask_order.forEach(cat => {
    const sub = list.filter(r => r.category === cat);
    if(!sub.length) return;
    const [title, why] = D.ask_copy[cat] || [cat, ""];
    out += `<div class="grp"><h2>${esc(title)}<span class="c">${sub.length}</span></h2>
      <p>${esc(why)}</p>${sub.map((r,i) => lead(r, i, pfx+cat.replace(/\W/g,""))).join("")}</div>`;
  });
  return out;
}

// Opted-out people are shown, not removed — so the count has to be impossible to miss.
document.getElementById("warn").innerHTML = (D.optout_flagged > 0)
  ? `<p class="warn"><b>⛔ ${D.optout_flagged} of ${D.optout_total} on this sheet have opted
     out or are marked DND in GoHighLevel.</b> They are still listed, pinned to the top of
     their group and outlined in red. Do not text them.</p>` : "";

document.getElementById("bar").innerHTML =
  `<span class="pill -n">${D.main.length} to contact</span>` +
  D.ask_order.filter(c => D.main.some(r => r.category === c))
    .map(c => `<span class="pill">${esc((D.ask_copy[c]||[c])[0])} ${D.main.filter(r=>r.category===c).length}</span>`).join("") +
  `<span class="tick" id="tick"></span>`;

document.getElementById("main").innerHTML = group(D.main, "m") + (D.thin.length ? `
  <details class="thin"><summary>Replied, but never qualified into the CRM — ${D.thin.length}</summary>
    <p>These people replied and were categorised, but no opportunity was ever created for them,
      so nobody worked the thread. That's why they look thin — not because they were judged and
      rejected. Worth a skim before you write them off.</p>
    ${group(D.thin, "t")}</details>` : "");

document.getElementById("foot").innerHTML = `
  <p><b>Who's on this list.</b> Every reply between ${esc(D.window.replace("_to_"," and "))} that
    counts as a positive under the CRM's own rule, never booked a meeting, and wasn't excluded
    by hand as out-of-ICP.</p>
  <p><b>Days silent</b> counts from the last message in the thread either way, so it's how long
    the conversation has actually been dead — not how long since they first replied.</p>
  <p>Built ${esc(D.built_at.slice(0,10))} from the SMS reply register.</p>`;

function tick(){
  const t = document.getElementById("tick");
  t.textContent = done.size ? `${done.size} done · ${D.main.length - done.size} left` : "";
}
document.addEventListener("click", e => {
  const b = e.target.closest(".mark"); if(!b) return;
  const el = document.getElementById(b.dataset.id);
  const on = el.classList.toggle("done");
  on ? done.add(b.dataset.id) : done.delete(b.dataset.id);
  b.textContent = on ? "Undo" : "Mark done";
  tick();
});
</script>
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--client", default="scaletopia")
    ap.add_argument("--window", required=True, help="the register's window, e.g. 2026-07-01_to_2026-08-05")
    ap.add_argument("--channel", default="sms", choices=["sms", "email", "all"])
    a = ap.parse_args()

    cfg = json.load(open(gm.REGISTRY))[a.client]
    out_dir = os.path.join(gm.ROOT, cfg.get("output", f"clients/{a.client}/output"))
    src = os.path.join(out_dir, f"{a.window}-{a.channel}-prs.json")
    if not os.path.exists(src):
        sys.exit(f"{src} not found — run july_pr_register.py for that window first.")

    dst = os.path.join(out_dir, f"{a.window}-{a.channel}-followup.html")
    n_main, n_thin = build(json.load(open(src)), dst)
    print(f"wrote {dst}")
    print(f"  {n_main} qualified to contact · {n_thin} replied but never qualified into the CRM")


if __name__ == "__main__":
    main()
