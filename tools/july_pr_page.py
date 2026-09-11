#!/usr/bin/env python3
"""Render the monthly SMS reply register (from july_pr_register.py) as a readable page.

The register JSON is a reading surface, not a report: ~100 conversations somebody has to
get through before anyone can argue about why they didn't convert. So the page is built to
be scanned and filtered, with every thread one click from the row that summarises it.

TWO AUDIENCES
  --audience internal  (default)  campaign + copy-variant filters, our own ops metrics.
  --audience client               for sending to the client's exec team: the operational
                                  chrome comes off, the headline reconciles to the
                                  positive-reply number already in their reporting, and
                                  every row leads with who the person is and what they asked
                                  for. Nothing is removed from the data — only from the view.

USAGE
  python3 tools/july_pr_page.py --client gofish --audience client
  python3 tools/july_pr_page.py --client scaletopia --month 2026-07
"""
import argparse, html, json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ghl_mine as gm
from july_pr_register import CATEGORIES, TAIL

# What the category actually means, in the words you'd use out loud.
BLURB = {
    "Power Request": "Asked for the call, the price, or the next step outright.",
    "Positive": "Replied warmly without a specific ask.",
    "More Info Request": "Wanted to understand the offer before committing to anything.",
    "Email Me Request": "Asked us to take it to email rather than answer over text.",
    "Objection Handling": "Engaged, but led with a reason it wouldn't work.",
    "Maybe": "Warm but non-committal — no clear ask either way.",
    "Referral Request": "Not them, but pointed us at someone else.",
    "Future Request": "Interested, on a later timeline.",
    "Custom Response": "Didn't fit any of the standard buckets.",
    "Neutral": "Replied, but with no intent signal in either direction.",
    "(uncategorised)": "No reply category was set on the record.",
}

# The chase list, ordered by what you'd do first. "Never answered" leads because it is the
# only tier where the reason it stalled is entirely on our side of the conversation.
WARM_TIERS = ["no_reply_sent", "stalled", "later"]
TIER_COPY = {
    "no_reply_sent": ["Never answered",
                      "They replied — some handed over an email address — and nobody on our side ever wrote back."],
    "stalled": ["Answered, then went quiet",
                "We did reply. The conversation died anyway, so these need a different angle rather than a faster one."],
    "later": ["Asked us to check back",
              "Warm, but they named a timeline. Worth a diarised nudge, not a chase."],
}


def esc(s):
    return html.escape(str(s or ""))


def month_label(m):
    y, mo = m.split("-")
    names = ["", "January", "February", "March", "April", "May", "June",
             "July", "August", "September", "October", "November", "December"]
    return f"{names[int(mo)]} {y}"


def build(d, out_path, audience, label):
    rows = d["rows"]
    live = [r for r in rows if not r.get("excluded")]
    excluded = [r for r in rows if r.get("excluded")]
    core = [r for r in live if r["counted_positive"]]
    crm = [r for r in core if r["source"] != "contact_only"]
    extra = [r for r in core if r["source"] == "contact_only"]
    answered = [r for r in live if r["we_replied"]]
    gaps = sorted(r["response_gap_mins"] for r in answered if r["response_gap_mins"] is not None)
    booked = [r for r in live if r["booked"]]
    warm = [r for r in live if r.get("warm_tier") in WARM_TIERS]

    # A category only sinks below the line if EVERY reply in it fell outside the positive
    # count. Go Fish's July has an uncategorised row that booked a meeting — sorting that
    # section by its label alone would file a booked meeting under "didn't count".
    cats = {r["category"] for r in live}
    all_tail = {c: all(r["is_tail"] for r in live if r["category"] == c) for c in cats}
    order = sorted(cats, key=lambda c: (all_tail[c],
                                        CATEGORIES.index(c) if c in CATEGORIES else 99))

    # strip the client's own name off the front of every campaign — it's on every row and
    # tells the reader nothing
    pref = re.compile(r"^" + re.escape(label) + r"\s*[-–]\s*", re.I)
    campaigns = sorted({r["campaign_name"] for r in rows})
    variants = sorted({r["copy_variant"] for r in rows if r["copy_variant"]})

    payload = {
        "rows": rows, "order": order, "all_tail": all_tail, "blurb": BLURB,
        "simple": audience == "client", "tiers": WARM_TIERS, "tier_copy": TIER_COPY,
        "campaigns": campaigns, "variants": variants, "prefix": pref.pattern,
        "client": d["client"], "month": d["month"], "built_at": d["built_at"],
        "stats": {"n": len(live), "logged": len(rows), "excluded": len(excluded),
                  "core": len(core), "crm": len(crm), "extra": len(extra),
                  "warm": len(warm), "answered": len(answered), "booked": len(booked),
                  # duplicate CRM records folded away, so the page can explain why its
                  # positive-reply figure sits below the one in the client's own reporting
                  "dupes": sum(r.get("merged_from", 1) - 1 for r in crm),
                  "meetings": d.get("meetings_in_month", len(booked)),
                  "median": gaps[len(gaps) // 2] if gaps else None,
                  "within_hr": sum(1 for g in gaps if g <= 60), "gaps_n": len(gaps)},
    }

    doc = (TEMPLATE
           .replace("__DATA__", json.dumps(payload))
           .replace("__MONTH__", esc(month_label(d["month"])))
           .replace("__CLIENT__", esc(d["client"]))
           .replace("__BUILT__", esc(d["built_at"][:10])))
    open(out_path, "w").write(doc)
    return payload["stats"]


TEMPLATE = r"""<title>__CLIENT__ — cold SMS replies, __MONTH__</title>
<style>
:root{
  --paper:#F6F7F9; --surface:#FFFFFF; --sunk:#EDEFF3;
  --ink:#14161C; --ink-2:#4A5060; --ink-3:#767D8E;
  --rule:#DEE2E9; --rule-2:#C8CEDA;
  --accent:#2D4ECC; --good:#17795E; --good-soft:#E2F1EC;
  --bad:#C0472B; --bad-soft:#FBE9E4; --gold:#A97400; --gold-soft:#FAF0DA;
  --sans:ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
  --mono:ui-monospace,SFMono-Regular,"SF Mono",Menlo,Consolas,monospace;
}
@media (prefers-color-scheme:dark){:root{
  --paper:#101218; --surface:#171A22; --sunk:#1D212B;
  --ink:#E9EBF0; --ink-2:#A3AAB9; --ink-3:#767E90;
  --rule:#272C38; --rule-2:#39404F;
  --accent:#8098F5; --good:#5FC49F; --good-soft:#123027;
  --bad:#F0876A; --bad-soft:#38201A; --gold:#DFAE4A; --gold-soft:#332812;
}}
:root[data-theme="dark"]{
  --paper:#101218; --surface:#171A22; --sunk:#1D212B;
  --ink:#E9EBF0; --ink-2:#A3AAB9; --ink-3:#767E90;
  --rule:#272C38; --rule-2:#39404F;
  --accent:#8098F5; --good:#5FC49F; --good-soft:#123027;
  --bad:#F0876A; --bad-soft:#38201A; --gold:#DFAE4A; --gold-soft:#332812;
}
:root[data-theme="light"]{
  --paper:#F6F7F9; --surface:#FFFFFF; --sunk:#EDEFF3;
  --ink:#14161C; --ink-2:#4A5060; --ink-3:#767D8E;
  --rule:#DEE2E9; --rule-2:#C8CEDA;
  --accent:#2D4ECC; --good:#17795E; --good-soft:#E2F1EC;
  --bad:#C0472B; --bad-soft:#FBE9E4; --gold:#A97400; --gold-soft:#FAF0DA;
}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);font-family:var(--sans);
     font-size:15px;line-height:1.55;-webkit-font-smoothing:antialiased}
.wrap{max-width:1060px;margin:0 auto;padding:0 22px}

header.top{border-bottom:1px solid var(--rule);background:var(--surface)}
.mast{display:flex;flex-wrap:wrap;align-items:baseline;gap:8px 16px;padding:30px 0 4px}
h1{font-size:27px;font-weight:640;letter-spacing:-.022em;margin:0;text-wrap:balance}
.sub{font-family:var(--mono);font-size:11.5px;letter-spacing:.06em;text-transform:uppercase;color:var(--ink-3)}
.lede{color:var(--ink-2);max-width:64ch;margin:6px 0 22px;font-size:15px}

.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(172px,1fr));gap:1px;
       background:var(--rule);border:1px solid var(--rule);border-radius:9px;
       overflow:hidden;margin-bottom:28px}
.stat{background:var(--surface);padding:15px 16px}
.stat .v{font-family:var(--mono);font-size:27px;font-weight:600;letter-spacing:-.025em;
         font-variant-numeric:tabular-nums;line-height:1.05}
.stat .k{font-size:12.5px;font-weight:600;margin-top:4px}
.stat .d{font-size:11.5px;color:var(--ink-3);line-height:1.45;margin-top:3px}
.stat.-good .v{color:var(--good)} .stat.-gold .v{color:var(--gold)} .stat.-bad .v{color:var(--bad)}
.stat.-warm{background:var(--accent);color:#fff}
.stat.-warm .k{color:#fff} .stat.-warm .d{color:rgba(255,255,255,.8)}

.filters{position:sticky;top:0;z-index:20;background:var(--surface);
         border-bottom:1px solid var(--rule);padding:11px 0}
.frow{display:flex;flex-wrap:wrap;gap:8px;align-items:center}
.frow + .frow{margin-top:8px}
.chip{font:inherit;font-size:12.5px;padding:5px 11px;border-radius:999px;cursor:pointer;
      border:1px solid var(--rule-2);background:transparent;color:var(--ink-2);
      display:inline-flex;align-items:center;gap:6px;transition:.13s}
.chip:hover{border-color:var(--accent);color:var(--ink)}
.chip[aria-pressed="true"]{background:var(--accent);border-color:var(--accent);color:#fff}
.chip[aria-pressed="true"] .ct{color:rgba(255,255,255,.78)}
.chip .ct{font-family:var(--mono);font-size:11px;color:var(--ink-3);font-variant-numeric:tabular-nums}
select,input[type=search]{font:inherit;font-size:13px;padding:6px 9px;border-radius:6px;
      border:1px solid var(--rule-2);background:var(--surface);color:var(--ink);max-width:100%}
input[type=search]{min-width:210px;flex:1}
:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
.count{font-family:var(--mono);font-size:12px;color:var(--ink-3);margin-left:auto;
       font-variant-numeric:tabular-nums;white-space:nowrap}
.linkish{background:none;border:none;font:inherit;font-size:12.5px;color:var(--accent);
         cursor:pointer;padding:5px 2px;text-decoration:underline;text-underline-offset:2px}

section{margin:36px 0 0}
.shead{display:flex;align-items:baseline;gap:11px;flex-wrap:wrap;
       padding-bottom:7px;border-bottom:2px solid var(--ink)}
.shead h2{font-size:18px;font-weight:640;letter-spacing:-.015em;margin:0}
.shead .n{font-family:var(--mono);font-size:12px;color:var(--ink-3);font-variant-numeric:tabular-nums}
.shead .why{font-size:13.5px;color:var(--ink-2);margin-left:auto;text-align:right}
section.-tail .shead{border-bottom-color:var(--rule-2)}
section.-tail .shead h2{color:var(--ink-2)}
.tailnote{font-size:13.5px;color:var(--ink-3);margin:26px 0 -10px;padding-top:22px;
          border-top:1px dashed var(--rule-2);max-width:70ch}

/* the chase list — the reason most people open this page */
.warmwrap{margin:34px 0 0;padding:20px 22px 6px;border:1px solid var(--accent);
          border-radius:12px;background:var(--surface)}
.warmwrap > h2{margin:0;font-size:19px;font-weight:660;letter-spacing:-.018em}
.warmwrap > p.k{margin:5px 0 4px;color:var(--ink-2);font-size:14px;max-width:66ch}
.tier{margin-top:22px}
.tier > h3{margin:0;font-size:15px;font-weight:640;letter-spacing:-.01em;
           display:flex;align-items:baseline;gap:9px;flex-wrap:wrap}
.tier > h3 .n{font-family:var(--mono);font-size:11.5px;color:#fff;background:var(--accent);
              padding:2px 7px;border-radius:999px;font-variant-numeric:tabular-nums}
.tier > p{margin:3px 0 2px;font-size:13px;color:var(--ink-3);max-width:70ch}
.said{grid-column:1/-1;font-size:12.5px;color:var(--ink-2);padding:2px 0 0;
      overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.said b{font-family:var(--mono);font-size:10px;letter-spacing:.05em;text-transform:uppercase;
        color:var(--ink-3);font-weight:600;margin-right:6px}
.cold{font-family:var(--mono);font-size:11px;padding:3px 7px;border-radius:4px;font-weight:600;
      background:var(--sunk);color:var(--ink-3);white-space:nowrap}
.cold.-hot{background:var(--bad-soft);color:var(--bad)}

.exwrap{margin-top:44px;border:1px dashed var(--rule-2);border-radius:12px;padding:4px 20px 8px}
.exwrap > summary{cursor:pointer;font-size:14.5px;font-weight:600;padding:13px 0;list-style:none}
.exwrap > summary::-webkit-details-marker{display:none}
.exwrap > summary::before{content:"▸ ";color:var(--ink-3)}
.exwrap[open] > summary::before{content:"▾ "}
.exwrap > p{font-size:13px;color:var(--ink-3);max-width:70ch;margin:0 0 10px}
.exrow{display:flex;flex-wrap:wrap;gap:4px 14px;align-items:baseline;
       padding:9px 0;border-top:1px solid var(--rule)}
.exrow .c{font-weight:600;font-size:14px} .exrow .p{font-size:12.5px;color:var(--ink-3)}
.exrow .r{font-size:12.5px;color:var(--bad);margin-left:auto;text-align:right}

details.rec{border-bottom:1px solid var(--rule)}
details.rec > summary{list-style:none;cursor:pointer;display:grid;
   grid-template-columns:1.5fr 1fr auto auto;gap:6px 16px;align-items:center;
   padding:12px 4px;transition:background .12s}
details.rec > summary::-webkit-details-marker{display:none}
details.rec > summary:hover,details.rec[open] > summary{background:var(--sunk)}
.who{min-width:0}
.who .nm{font-weight:600;font-size:15px;letter-spacing:-.01em}
.who .ti{font-size:12.5px;color:var(--ink-3);overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.co{min-width:0;font-size:13.5px}
.co a{color:var(--accent);text-decoration:none}
.co a:hover{text-decoration:underline}
.co .meta{font-family:var(--mono);font-size:11px;color:var(--ink-3);
          overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.state{display:flex;gap:6px;align-items:center;justify-content:flex-end;flex-wrap:wrap}
.tag{font-family:var(--mono);font-size:10.5px;letter-spacing:.04em;text-transform:uppercase;
     padding:3px 7px;border-radius:4px;white-space:nowrap;font-weight:600}
.tag.-ans{background:var(--good-soft);color:var(--good)}
.tag.-no{background:var(--bad-soft);color:var(--bad)}
.tag.-book{background:var(--gold-soft);color:var(--gold)}
.tag.-mute{background:var(--sunk);color:var(--ink-3)}
.when{font-family:var(--mono);font-size:11.5px;color:var(--ink-3);text-align:right;
      font-variant-numeric:tabular-nums;white-space:nowrap}
.li{display:inline-block;width:15px;height:15px;border-radius:3px;background:var(--accent);
    color:#fff;font-size:10px;font-weight:700;text-align:center;line-height:15px;
    text-decoration:none;vertical-align:-2px;margin-left:6px}

.thread{padding:16px 4px 24px;display:flex;flex-direction:column;gap:9px}
.bub{max-width:min(74%,530px);padding:9px 13px;border-radius:14px;font-size:14px;line-height:1.5}
.bub .st{display:block;font-family:var(--mono);font-size:10.5px;letter-spacing:.03em;
         opacity:.72;margin-bottom:4px;font-variant-numeric:tabular-nums}
.bub.out{align-self:flex-end;background:var(--accent);color:#fff;border-bottom-right-radius:4px}
.bub.out.auto{background:var(--sunk);color:var(--ink-2);border:1px dashed var(--rule-2)}
.bub.in{align-self:flex-start;background:var(--surface);border:1px solid var(--rule-2);
        border-bottom-left-radius:4px}
.gapline{align-self:center;font-family:var(--mono);font-size:11px;color:var(--ink-3);letter-spacing:.04em}
.factbar{display:flex;flex-wrap:wrap;gap:8px 20px;padding:12px 14px;margin-bottom:4px;
         background:var(--sunk);border-radius:8px;font-size:13px}
.factbar div{min-width:0}
.factbar b{font-weight:600;color:var(--ink-3);font-size:10.5px;text-transform:uppercase;
           letter-spacing:.05em;display:block;font-family:var(--mono)}
.factbar span{word-break:break-word}
.factbar a{color:var(--accent)}
.warn{font-size:12.5px;color:var(--bad);background:var(--bad-soft);padding:8px 12px;
      border-radius:7px;margin-bottom:4px}

footer{margin:60px 0 44px;padding-top:20px;border-top:1px solid var(--rule);
       font-size:13px;color:var(--ink-3);max-width:72ch}
footer p{margin:0 0 9px}
.empty{padding:46px 4px;color:var(--ink-3);font-size:14px}
@media (max-width:760px){
  details.rec > summary{grid-template-columns:1fr auto;gap:5px 10px}
  .co{grid-column:1/-1;order:3} .when{order:4;grid-column:1/-1;text-align:left}
  .bub{max-width:88%}
  .shead .why{margin-left:0;text-align:left;flex-basis:100%}
}
@media (prefers-reduced-motion:reduce){*{transition:none!important;animation:none!important}}
</style>

<header class="top">
  <div class="wrap">
    <div class="mast">
      <h1>Cold SMS replies — __MONTH__</h1>
      <span class="sub">__CLIENT__ · built __BUILT__</span>
    </div>
    <p class="lede" id="lede"></p>
    <div class="stats" id="stats"></div>
  </div>
</header>

<div class="filters">
  <div class="wrap">
    <div class="frow" id="catbar"></div>
    <div class="frow" id="controls"></div>
  </div>
</div>

<main class="wrap" id="main"></main>
<footer class="wrap" id="foot"></footer>

<script>
const D = __DATA__;
const S = D.stats, R = D.rows, SIMPLE = D.simple;
const PRE = new RegExp(D.prefix, "i");
const esc = s => String(s??"").replace(/[&<>"']/g, c =>
  ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
const pct = (a,b) => b ? Math.round(100*a/b) + "%" : "—";
const day = s => (s||"").slice(0,10);
const gapTxt = g => g==null ? "" : g < 60 ? g+" min" :
  g < 1440 ? (g/60).toFixed(1).replace(/\.0$/,"")+" hr" : Math.round(g/1440)+" days";
const camp = c => c.replace(PRE,"");

document.getElementById("lede").textContent = SIMPLE
  ? "Every person who replied to our cold text outreach this month, what they asked for, and the full conversation with each of them. Hard nos are left out."
  : "Every categorised reply to our cold SMS this month, with the whole conversation attached. Hard nos are excluded. Nothing here is analysis — it's the record you read before making one.";

/* ---------- summary ---------- */
const tiles = SIMPLE ? [
  [S.crm, "positive replies", S.dupes
    ? "Distinct people. Reporting shows " + (S.crm + S.dupes) + " — " + S.dupes
      + (S.dupes === 1 ? " person was" : " people were") + " logged twice in the CRM."
    : "The figure in your monthly reporting.", ""],
  [S.meetings, "meetings booked", "Meetings that took place this month.", "-gold"],
  [S.warm, "still warm", "Replied, never converted, and not yet written off.", "-warm"],
  [S.answered + " · " + pct(S.answered,S.n), "conversations we replied to", "A person replied, not an automated follow-up.", S.answered/S.n < .6 ? "-bad" : "-good"],
  [S.median==null?"—":S.median+" min", "typical reply speed", S.within_hr + " of " + S.gaps_n + " answered inside the hour.", ""],
] : [
  [S.warm, "still warm", "Replied, never converted, not written off. The list below.", "-warm"],
  [S.core, "count as positive", S.crm + " from the CRM, " + S.extra + " with no deal record"
    + (S.excluded ? ", after removing " + S.excluded + " out-of-ICP" : "") + ".", ""],
  [S.n, "replies in scope", S.logged + " logged" + (S.excluded ? ", " + S.excluded + " excluded by hand" : "") + ". Hard nos already out.", ""],
  [S.answered + " · " + pct(S.answered,S.n), "a human answered", "The rest got an automated nudge or nothing at all.", S.answered/S.n < .6 ? "-bad" : "-good"],
  [S.booked, "of these repliers booked", S.meetings + " meetings were booked in the month overall.", "-gold"],
];
document.getElementById("stats").innerHTML = tiles.map(([v,k,d,c]) =>
  `<div class="stat ${c}"><div class="v">${esc(v)}</div><div class="k">${esc(k)}</div>
   <div class="d">${esc(d)}</div></div>`).join("");

/* ---------- filters ---------- */
const st = {cats:new Set(), camp:"", vari:"", ans:"", book:"", q:""};
const LIVE_ALL = R.filter(r => !r.excluded);          // excluded rows never reach the filters
const catbar = document.getElementById("catbar");
catbar.innerHTML = D.order.map(c =>
  `<button class="chip" data-cat="${esc(c)}" aria-pressed="false">${esc(c)}<span class="ct">${
    LIVE_ALL.filter(r=>r.category===c).length}</span></button>`).join("");
catbar.onclick = e => {
  const b = e.target.closest(".chip"); if(!b) return;
  st.cats.has(b.dataset.cat) ? st.cats.delete(b.dataset.cat) : st.cats.add(b.dataset.cat);
  b.setAttribute("aria-pressed", st.cats.has(b.dataset.cat));
  render();
};

const ctrl = document.getElementById("controls");
const sels = [];
if(!SIMPLE && D.campaigns.length > 1) sels.push(`<select id="camp"><option value="">All campaigns</option>` +
  D.campaigns.map(c => `<option value="${esc(c)}">${esc(camp(c))} (${LIVE_ALL.filter(r=>r.campaign_name===c).length})</option>`).join("") + `</select>`);
if(!SIMPLE && D.variants.length > 1) sels.push(`<select id="var"><option value="">All variants</option>` +
  D.variants.map(v => `<option value="${esc(v)}">Variant ${esc(v)} (${LIVE_ALL.filter(r=>r.copy_variant===v).length})</option>`).join("") + `</select>`);
ctrl.innerHTML = sels.join("") + `
  <select id="ans"><option value="">Replied to or not</option>
    <option value="y">We replied</option><option value="n">No reply sent</option></select>
  <select id="book"><option value="">Booked or not</option>
    <option value="y">Booked a meeting</option><option value="n">No meeting</option></select>
  <input type="search" id="q" placeholder="Search name, company, or message text…">
  <button class="linkish" id="toggle">Expand all</button>
  <button class="linkish" id="reset">Reset</button>
  <span class="count" id="count"></span>`;

const $ = id => document.getElementById(id);
if($("camp")) $("camp").onchange = e => {st.camp = e.target.value; render()};
if($("var"))  $("var").onchange  = e => {st.vari = e.target.value; render()};
$("ans").onchange  = e => {st.ans  = e.target.value; render()};
$("book").onchange = e => {st.book = e.target.value; render()};
let t; $("q").oninput = e => {
  clearTimeout(t); t = setTimeout(() => {st.q = e.target.value.toLowerCase().trim(); render()}, 140);
};
$("reset").onclick = () => {
  st.cats.clear(); st.camp = st.vari = st.ans = st.book = st.q = "";
  catbar.querySelectorAll(".chip").forEach(b => b.setAttribute("aria-pressed","false"));
  ["camp","var","ans","book","q"].forEach(id => {if($(id)) $(id).value = ""});
  render();
};
let openAll = false;
$("toggle").onclick = e => {
  openAll = !openAll;
  document.querySelectorAll("details.rec").forEach(d => d.open = openAll);
  e.target.textContent = openAll ? "Collapse all" : "Expand all";
};

function keep(r){
  if(st.cats.size && !st.cats.has(r.category)) return false;
  if(st.camp && r.campaign_name !== st.camp) return false;
  if(st.vari && r.copy_variant !== st.vari) return false;
  if(st.ans === "y" && !r.we_replied) return false;
  if(st.ans === "n" && r.we_replied) return false;
  if(st.book === "y" && !r.booked) return false;
  if(st.book === "n" && r.booked) return false;
  if(st.q && !(r.contact+" "+r.company+" "+r.job_title+" "+
      r.messages.map(m=>m.body).join(" ")).toLowerCase().includes(st.q)) return false;
  return true;
}

/* ---------- render ---------- */
function bubbles(r){
  let out = "", firstIn = r.messages.findIndex(m => m.dir === "inbound"), shown = false;
  r.messages.forEach((m,i) => {
    if(!shown && firstIn > -1 && i > firstIn && r.response_gap_mins != null
       && m.dir === "outbound" && !m.automated){
      out += `<div class="gapline">↓ ${esc(gapTxt(r.response_gap_mins))} later</div>`; shown = true;
    }
    const cls = m.dir === "inbound" ? "in" : (m.automated ? "out auto" : "out");
    const lbl = m.dir === "inbound" ? esc(r.contact||"Them")
              : (m.automated ? "Us · automated" : "Us · typed");
    out += `<div class="bub ${cls}"><span class="st">${lbl} · ${esc(m.when)}</span>${esc(m.body)}</div>`;
  });
  return out;
}

/* what they last said, so a row is judgeable without opening it */
function lastSaid(r){
  const ins = r.messages.filter(m => m.dir === "inbound");
  if(!ins.length) return "";
  return `<div class="said"><b>last said</b>${esc(ins[ins.length-1].body.slice(0,190))}</div>`;
}

function card(r, opts){
  opts = opts || {};
  const tags = [];
  if(r.booked) tags.push(`<span class="tag -book">booked${r.stage&&r.stage!=="Meeting Booked"?" · "+esc(r.stage.toLowerCase()):""}</span>`);
  if(r.we_replied) tags.push(`<span class="tag -ans">replied in ${esc(gapTxt(r.response_gap_mins))}</span>`);
  else tags.push(`<span class="tag -no">no reply sent</span>`);
  if(!SIMPLE && r.stage && r.stage !== "Positive Reply" && !r.booked)
    tags.push(`<span class="tag -mute">${esc(r.stage)}</span>`);

  const site = r.website
    ? `<a href="${esc(r.website)}" target="_blank" rel="noopener">${esc(r.company||r.website)}</a>`
    : esc(r.company || "—");
  const li = r.linkedin
    ? `<a class="li" href="${esc(r.linkedin)}" target="_blank" rel="noopener" title="LinkedIn profile">in</a>` : "";

  const facts = (SIMPLE ? [
    ["Company", site], ["Role", esc(r.job_title||"—")],
    ["What they asked for", esc(r.category)],
    ["Email", r.email ? `<a href="mailto:${esc(r.email)}">${esc(r.email)}</a>` : "not on record"],
    ["Phone", esc(r.phone||"—")],
    ["LinkedIn", r.linkedin ? `<a href="${esc(r.linkedin)}" target="_blank" rel="noopener">profile</a>` : "not on record"],
    ["Based", esc(r.location||"—")], ["Replied", esc(day(r.created_at))],
  ] : [
    ["Campaign", esc(camp(r.campaign_name))], ["Variant", esc(r.copy_variant||"—")],
    ["Category", esc(r.category)+" · "+esc(r.intent_tier)+" intent"],
    ["Counted positive", r.counted_positive ? "yes" : "no"],
    ["Phone", esc(r.phone||"—")],
    ["Email", r.email ? `<a href="mailto:${esc(r.email)}">${esc(r.email)}</a>` : "—"],
    ["LinkedIn", r.linkedin ? `<a href="${esc(r.linkedin)}" target="_blank" rel="noopener">profile</a>` : "not on record"],
    ["Location", esc(r.location||"—")], ["Logged", esc(day(r.created_at))],
  ]).map(([k,v]) => `<div><b>${k}</b><span>${v}</span></div>`).join("");

  const warn = r.messages.some(m => m.dir === "inbound") ? "" :
    `<div class="warn">No inbound text on record for this conversation — the reply that got it
      categorised came in through another channel, or was logged by hand.</div>`;

  const meta = SIMPLE ? esc(r.location||"") : esc(camp(r.campaign_name).split(" | ")[0]);

  // in the chase list, "how long since anyone touched this" beats the logged date
  const when = opts.chase && r.days_silent != null
    ? `<span class="cold ${r.days_silent >= 21 ? "-hot" : ""}">${r.days_silent}d silent</span>`
    : esc(day(r.created_at));

  return `<details class="rec">
    <summary>
      <div class="who"><div class="nm">${esc(r.contact||"—")}${li}</div>
        <div class="ti">${esc(r.job_title||"")}</div></div>
      <div class="co"><div>${site}</div><div class="meta">${meta}</div></div>
      <div class="state">${tags.join("")}</div>
      <div class="when">${when}</div>
      ${opts.chase ? lastSaid(r) : ""}
    </summary>
    <div class="thread"><div class="factbar">${facts}</div>${warn}${bubbles(r)}</div>
  </details>`;
}

/* ---------- the chase list ---------- */
function warmBlock(vis){
  const warm = vis.filter(r => D.tiers.includes(r.warm_tier));
  if(!warm.length) return "";
  let out = `<div class="warmwrap"><h2>Still warm — ${warm.length}</h2>
    <p class="k">Replied, never booked, and not written off. Ordered by how long they've been
      sitting untouched.</p>`;
  D.tiers.forEach(t => {
    const sub = warm.filter(r => r.warm_tier === t)
      .sort((a,b) => (b.days_silent??0) - (a.days_silent??0));
    if(!sub.length) return;
    const [title, why] = D.tier_copy[t];
    out += `<div class="tier"><h3>${esc(title)}<span class="n">${sub.length}</span></h3>
      <p>${esc(why)}</p>${sub.map(r => card(r, {chase:true})).join("")}</div>`;
  });
  return out + `</div>`;
}

/* ---------- what was cut, and why ---------- */
function excludedBlock(){
  const ex = R.filter(r => r.excluded);
  if(!ex.length) return "";
  return `<details class="exwrap"><summary>Excluded by hand — ${ex.length}</summary>
    <p>Judged out of ICP on review and removed from every figure on this page. Kept here so
      the call is visible, and so the same companies don't get worked again next month.</p>
    ${ex.sort((a,b) => (a.company||"").localeCompare(b.company||"")).map(r => `
      <div class="exrow"><span class="c">${esc(r.company||r.contact||"—")}</span>
        <span class="p">${esc(r.contact||"")}${r.website?" · "+esc(r.website.replace(/^https?:\/\/(www\.)?/,"")):""}</span>
        <span class="r">${esc(r.override_reason||"out of ICP")}</span></div>`).join("")}
  </details>`;
}

function render(){
  const LIVE = R.filter(r => !r.excluded);
  const vis = LIVE.filter(keep);
  $("count").textContent = vis.length === LIVE.length ? `${LIVE.length} replies` : `${vis.length} of ${LIVE.length}`;
  const main = $("main");
  if(!vis.length){ main.innerHTML = `<p class="empty">Nothing matches those filters.</p>` + excludedBlock(); return; }

  let html = warmBlock(vis), tailOpened = false;
  D.order.forEach(cat => {
    const sub = vis.filter(r => r.category === cat);
    if(!sub.length) return;
    if(D.all_tail[cat] && !tailOpened){
      tailOpened = true;
      html += `<p class="tailnote">${SIMPLE
        ? "Below the line: replies that don't count toward the positive-reply figure — warm but non-committal, or no clear signal either way. They're here so you can see exactly what was and wasn't counted."
        : "Below the line: replies nobody would count as positive. They're here so the filtering is visible rather than assumed."}</p>`;
    }
    html += `<section class="${D.all_tail[cat]?"-tail":""}">
      <div class="shead"><h2>${esc(cat)}</h2>
        <span class="n">${sub.length} · ${sub.filter(r=>r.we_replied).length} replied to</span>
        <span class="why">${esc(D.blurb[cat]||"")}</span></div>
      ${sub.map(r => card(r)).join("")}</section>`;
  });
  main.innerHTML = html + excludedBlock();
  if(openAll) main.querySelectorAll("details.rec").forEach(d => d.open = true);
}
render();

/* ---------- footer ---------- */
$("foot").innerHTML = SIMPLE ? `
  <p><b>What's counted.</b> The positive-reply figure follows the same rule as your monthly
    reporting: every reply logged against a record, excluding the non-committal "Maybe" ones
    and anyone disqualified. A handful of genuine replies never made it onto a record at all —
    those are shown here too, but kept out of that figure so it stays comparable.</p>
  ${S.dupes ? `<p><b>Why this reads ${S.crm} and not ${S.crm+S.dupes}.</b> ${S.dupes}
    ${S.dupes===1?"person holds two records":"people hold two records each"} in the CRM, so
    ${S.dupes===1?"they are":"they were"} counted twice in the monthly figure. This page lists
    one row per person. Same conversations, no one dropped.</p>` : ""}
  <p><b>Reading a conversation.</b> Our texts are on the right, theirs on the left. Messages
    sent automatically by the campaign are shown dashed; solid ones were typed by a person.</p>
  <p><b>Meetings.</b> Meetings booked counts what took place this month, including from people
    who first replied earlier. That's why it can differ from the number of this month's
    repliers who went on to book.</p>` : `
  <p><b>How this was built.</b> Replies and their categories come from Evergreen — the
    <code>deals</code> and <code>contacts</code> endpoints unioned, because neither is complete
    on its own. Every conversation was then rebuilt from the raw GoHighLevel SMS log, the only
    source with real timestamps and with automated sends distinguishable from a human typing.</p>
  <p><b>Two numbers that get confused.</b> Repliers-who-booked counts people who first replied
    this month and went on to book. Meetings-booked counts meetings held this month, including
    from people who replied earlier. Both are true; they are not the same number.</p>
  <p><b>Answered</b> means a human on our side sent something after their reply. Automated
    follow-ups don't count and are shown dashed in the thread.</p>`;
</script>
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--client", default="scaletopia")
    ap.add_argument("--month", default="2026-07")
    ap.add_argument("--audience", choices=["internal", "client"], default="internal")
    a = ap.parse_args()

    reg = json.load(open(gm.REGISTRY))
    cfg = reg[a.client]
    out_dir = os.path.join(gm.ROOT, cfg.get("output", f"clients/{a.client}/output"))
    src = os.path.join(out_dir, f"{a.month}-sms-prs.json")
    if not os.path.exists(src):
        sys.exit(f"{src} not found — run tools/july_pr_register.py --client {a.client} first.")

    d = json.load(open(src))
    suffix = "-client" if a.audience == "client" else ""
    dst = os.path.join(out_dir, f"{a.month}-sms-prs{suffix}.html")
    st = build(d, dst, a.audience, cfg.get("label", a.client))
    print(f"wrote {dst}  [{a.audience}]")
    print(f"  {st['n']} logged · {st['core']} positive ({st['crm']} CRM + {st['extra']} extra) · "
          f"{st['answered']} answered · {st['meetings']} meetings · median {st['median']} min")


if __name__ == "__main__":
    main()
