#!/usr/bin/env python3
"""Render the unbooked-reply pack as one self-contained, filterable HTML page.

Reads {out}/{window}-unbooked-replies.json (written by week_reply_pack.py) and writes
{out}/{window}-unbooked-replies.html. Same single-file pattern as july_pr_page.py:
one TEMPLATE string, __DATA__ replaced with the payload, no build step, no CDN.

USAGE
  python3 tools/week_reply_page.py --window 2026-08-24_to_2026-08-28
"""
import argparse, json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ghl_mine as gm

TEMPLATE = r"""<title>__TITLE__</title>
<style>
:root{--paper:#F4F5F7;--card:#FFF;--ink:#171A20;--ink-2:#3D4453;--muted:#6B7280;
--line:#E1E4EA;--line-2:#EFF1F4;--accent:#B5771A;--accent-soft:#FBF0DC;
--good:#1B7A4B;--good-soft:#E3F2EA;--bad:#B8413A;--bad-soft:#FAE7E5;
--warn:#8A6410;--warn-soft:#FBF0DC;--in-soft:#EAF1FB;--in-line:#2B5FA8;
--serif:"Iowan Old Style","Palatino Linotype",Palatino,Georgia,serif;
--sans:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;
--mono:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){
--paper:#0F1116;--card:#171A21;--ink:#E7E9ED;--ink-2:#B6BCC7;--muted:#818997;
--line:#272C36;--line-2:#1E222A;--accent:#E0A84C;--accent-soft:#2E2617;
--good:#4FBF85;--good-soft:#15291F;--bad:#E2726A;--bad-soft:#341C1A;
--warn:#E0A84C;--warn-soft:#2E2617;--in-soft:#16202E;--in-line:#5D93DA;}}
:root[data-theme="dark"]{--paper:#0F1116;--card:#171A21;--ink:#E7E9ED;--ink-2:#B6BCC7;
--muted:#818997;--line:#272C36;--line-2:#1E222A;--accent:#E0A84C;--accent-soft:#2E2617;
--good:#4FBF85;--good-soft:#15291F;--bad:#E2726A;--bad-soft:#341C1A;
--warn:#E0A84C;--warn-soft:#2E2617;--in-soft:#16202E;--in-line:#5D93DA;}
*{box-sizing:border-box;}
body{margin:0;background:var(--paper);color:var(--ink);font-family:var(--sans);
line-height:1.55;-webkit-font-smoothing:antialiased;}
.wrap{max-width:1120px;margin:0 auto;padding:0 22px 110px;}
header{padding:46px 0 22px;border-bottom:1px solid var(--line);}
.eyebrow{font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--accent);
font-weight:650;margin:0 0 10px;}
h1{font-family:var(--serif);font-size:clamp(27px,4vw,40px);line-height:1.12;margin:0 0 12px;
font-weight:600;letter-spacing:-.01em;text-wrap:balance;}
.lede{max-width:74ch;color:var(--ink-2);margin:0 0 14px;font-size:15.5px;}
.lede b{color:var(--ink);font-weight:650;}
.note{max-width:78ch;color:var(--muted);font-size:12.5px;margin:8px 0 0;}
.note code{font-family:var(--mono);font-size:11.5px;background:var(--line-2);padding:1px 5px;
border-radius:4px;}
h2{font-family:var(--serif);font-size:23px;margin:44px 0 6px;font-weight:600;}
h2 .of{color:var(--muted);font-family:var(--sans);font-size:13px;font-weight:400;}
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(148px,1fr));gap:12px;
margin:26px 0 8px;}
.tile{background:var(--card);border:1px solid var(--line);border-radius:11px;padding:15px 16px;}
.tile .n{font-family:var(--serif);font-size:31px;line-height:1;font-weight:600;}
.tile .k{font-size:11px;letter-spacing:.07em;text-transform:uppercase;color:var(--muted);
margin-top:7px;}
.tile.bad .n{color:var(--bad);} .tile.warn .n{color:var(--accent);}
.tablewrap{overflow-x:auto;margin:14px 0 0;}
table{border-collapse:collapse;width:100%;font-size:13.5px;min-width:620px;}
th,td{padding:8px 11px;border-bottom:1px solid var(--line-2);text-align:left;}
th{font-size:11px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);
font-weight:650;border-bottom:1px solid var(--line);}
td.n,th.n{text-align:right;font-variant-numeric:tabular-nums;}
tr.tot td{font-weight:700;border-top:1px solid var(--line);border-bottom:none;}
.bar{position:sticky;top:0;z-index:20;background:var(--paper);border-bottom:1px solid var(--line);
padding:11px 0;margin:34px 0 0;display:flex;flex-wrap:wrap;gap:8px;align-items:center;}
select,input[type=search]{font-family:var(--sans);font-size:13px;padding:6px 9px;
border:1px solid var(--line);border-radius:7px;background:var(--card);color:var(--ink);}
input[type=search]{min-width:210px;flex:1;}
button.tog{font-family:var(--sans);font-size:12.5px;padding:6px 11px;border:1px solid var(--line);
border-radius:7px;background:var(--card);color:var(--ink-2);cursor:pointer;}
button.tog[aria-pressed=true]{background:var(--accent-soft);border-color:var(--accent);
color:var(--accent);font-weight:650;}
.count{font-size:12.5px;color:var(--muted);margin-left:auto;font-variant-numeric:tabular-nums;}
.card{background:var(--card);border:1px solid var(--line);border-radius:11px;padding:0;
margin:11px 0;overflow:hidden;}
.card.never{border-left:3px solid var(--bad);}
.card.ball{border-left:3px solid var(--accent);}
.head{padding:14px 17px;cursor:pointer;display:block;width:100%;text-align:left;
background:none;border:0;color:inherit;font:inherit;}
.head:hover{background:var(--line-2);}
.head:focus-visible{outline:2px solid var(--accent);outline-offset:-2px;}
button.tog:focus-visible,select:focus-visible,input:focus-visible{outline:2px solid var(--accent);
outline-offset:2px;}
@media (prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important;}}
.who{font-family:var(--serif);font-size:17.5px;font-weight:600;letter-spacing:-.01em;}
.who .co{color:var(--ink-2);font-weight:400;}
.chips{display:flex;flex-wrap:wrap;gap:6px;margin:8px 0 0;align-items:center;}
.chip{font-size:11px;padding:2.5px 8px;border-radius:20px;border:1px solid var(--line);
color:var(--ink-2);background:var(--paper);white-space:nowrap;}
.chip.client{background:var(--accent-soft);border-color:var(--accent);color:var(--accent);
font-weight:650;}
.chip.never{background:var(--bad-soft);border-color:var(--bad);color:var(--bad);font-weight:650;}
.chip.ball{background:var(--accent-soft);border-color:var(--accent);color:var(--accent);
font-weight:650;}
.chip.type{background:var(--line-2);}
.chip.flag{background:var(--warn-soft);border-color:var(--warn);color:var(--warn);}
.meta{font-size:12.5px;color:var(--muted);margin:7px 0 0;}
.quote{margin:10px 0 0;padding:9px 12px;background:var(--in-soft);
border-left:2px solid var(--in-line);border-radius:0 7px 7px 0;font-size:13.5px;
color:var(--ink);display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;
overflow:hidden;}
.body{display:none;padding:0 17px 16px;border-top:1px solid var(--line-2);}
.card.open .body{display:block;}
.routes{font-family:var(--mono);font-size:12px;margin:13px 0 0;color:var(--ink-2);
word-break:break-word;}
.routes a{color:var(--accent);text-decoration:none;} .routes a:hover{text-decoration:underline;}
.routes .drv{color:var(--muted);font-style:italic;}
.warnrow{font-size:12.5px;color:var(--warn);background:var(--warn-soft);border-radius:7px;
padding:7px 11px;margin:11px 0 0;}
.thread{margin:14px 0 0;}
.msg{font-size:13.5px;margin:0 0 8px;padding:9px 12px;border-radius:8px;line-height:1.5;
white-space:pre-wrap;word-break:break-word;}
.msg.in{background:var(--in-soft);border-left:2px solid var(--in-line);}
.msg.out{background:var(--line-2);border-left:2px solid var(--line);}
.msg .w{display:block;font-size:11px;letter-spacing:.05em;text-transform:uppercase;
color:var(--muted);margin:0 0 4px;font-weight:650;}
.msg.in .w{color:var(--in-line);}
.empty{color:var(--muted);font-style:italic;padding:34px 0;text-align:center;}
.legend{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:5px 22px;
font-size:12.5px;color:var(--ink-2);margin:12px 0 0;}
.legend b{color:var(--ink);font-weight:650;}
footer{margin:56px 0 0;padding:18px 0 0;border-top:1px solid var(--line);font-size:12px;
color:var(--muted);}
@media print{.bar{display:none;} .card .body{display:block!important;}}
</style>

<div class="wrap">
<header>
  <p class="eyebrow">Weekly inbox review</p>
  <h1>__H1__</h1>
  <p class="lede" id="lede"></p>
  <p class="note" id="caveats"></p>
</header>

<div class="tiles" id="tiles"></div>

<h2>By client</h2>
<div class="tablewrap"><table id="bytable"></table></div>

<h2>What is not in here</h2>
<p class="note" id="coverage"></p>

<h2>What the tags mean</h2>
<div class="legend" id="legend"></div>

<div class="bar">
  <select id="f-client"></select>
  <select id="f-type"></select>
  <select id="f-status"></select>
  <select id="f-channel"></select>
  <input type="search" id="f-q" placeholder="search name, company, campaign, thread…">
  <button class="tog" id="f-flag" aria-pressed="false">mis-tagged only</button>
  <button class="tog" id="f-exp" aria-pressed="false">expand all</button>
  <span class="count" id="count"></span>
</div>

<div id="list"></div>

<footer id="foot"></footer>
</div>

<script>
const D = __DATA__;
const esc = s => (s==null?"":String(s)).replace(/[&<>"]/g, c =>
  ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const rows = D.rows, R = D.reconciliation, L = D.labels;

// ---- header numbers
const n = rows.length,
      never = rows.filter(r=>r.status==="never answered").length,
      ball  = rows.filter(r=>r.status==="ball with us").length,
      mis   = rows.filter(r=>r.mistagged===true).length,
      nosee = rows.filter(r=>r.status==="reply not in the record").length,
      clients = new Set(rows.map(r=>r.client_slug)).size,
      booked  = Object.values(R).reduce((a,v)=>a+v.booked,0),
      inwin   = Object.values(R).reduce((a,v)=>a+v.in_window,0);

document.getElementById("lede").innerHTML =
  `<b>${n} replies came in between ${esc(D.window)} and never became a meeting</b>, across `+
  `${clients} clients. <b>${never}</b> of them nobody answered at all, and on <b>${ball}</b> `+
  `more the lead wrote last and we never came back — so the ball is with us on `+
  `<b>${never+ball}</b> of ${n}. For scale: ${inwin} replies landed in the window in total `+
  `and ${booked} of those booked.` +
  (nosee ? ` A further <b>${nosee}</b> were tagged as replies but Evergreen returned no `+
           `inbound message for them — they are in the list, marked, and are not counted `+
           `as unanswered.` : "");

const E = D.enrichment || {};
document.getElementById("caveats").innerHTML =
  `Built ${esc(D.built_at)}. Threads and outcomes come from Evergreen — every client `+
  `Evergreen holds, live or past. Hard nos (<code>Not Interested</code>, <code>Threat</code>) `+
  `are excluded; every other tag is here. `+
  (E.matched ? `Contact details are joined in from the Airtable <i>Master Inbox &amp; CRM</i> `+
    `Contacts table, because Evergreen carries them only for replies that became an `+
    `opportunity — <b>${E.matched} of ${rows.length} rows matched, ${E.unmatched} did not, `+
    `and ${E.routes_recovered} had no email or phone at all until that join</b>. ` : "")+
  `<b>No source in the stack holds a company LinkedIn URL</b>, so that link is a LinkedIn `+
  `company <i>search</i> built from the company name and labelled as derived. `+
  `Rebuild: <code>python3 tools/week_reply_pack.py --from ${esc((D.window_slug||"").split("_to_")[0])} `+
  `--to ${esc((D.window_slug||"").split("_to_")[1])}</code>, then `+
  `<code>week_reply_enrich.py</code>, then <code>week_reply_page.py</code>.`;

const tile = (v,k,cls="") => `<div class="tile ${cls}"><div class="n">${v}</div><div class="k">${k}</div></div>`;
document.getElementById("tiles").innerHTML =
  tile(n,"unbooked replies") + tile(never,"never answered","bad") +
  tile(ball,"they wrote last","warn") + tile(mis,"mis-tagged","warn") +
  tile(clients,"clients");

// ---- by-client table
const slugs = Object.keys(R).filter(s => R[s].in_window > 0)
  .sort((a,b)=> cnt(b)-cnt(a) || a.localeCompare(b));
function cnt(s){ return rows.filter(r=>r.client_slug===s).length; }
function sub(s,f){ return rows.filter(r=>r.client_slug===s&&f(r)).length; }
let t = `<thead><tr><th>client</th><th class="n">replies in window</th>`+
        `<th class="n">booked</th><th class="n">unbooked</th><th class="n">never answered</th>`+
        `<th class="n">ball with us</th></tr></thead><tbody>`;
for (const s of slugs) t += `<tr><td>${esc(L[s]||s)}</td><td class="n">${R[s].in_window}</td>`+
  `<td class="n">${R[s].booked}</td><td class="n">${cnt(s)}</td>`+
  `<td class="n">${sub(s,r=>r.status==="never answered")}</td>`+
  `<td class="n">${sub(s,r=>r.status==="ball with us")}</td></tr>`;
t += `<tr class="tot"><td>total</td><td class="n">${inwin}</td><td class="n">${booked}</td>`+
     `<td class="n">${n}</td><td class="n">${never}</td><td class="n">${ball}</td></tr></tbody>`;
document.getElementById("bytable").innerHTML = t;

const C = D.coverage || {};
const dead = Object.entries(C.dead_end_tags_evergreen_cannot_return || {});
const nie  = Object.entries(C.not_in_evergreen || {});
document.getElementById("coverage").innerHTML =
  `<b>Hard nos and dead ends are excluded by design.</b> Airtable tagged `+
  dead.map(([k,v])=>`${v} <code>${esc(k)}</code>`).join(", ") +
  ` in the same window; none are here, but the counts are worth knowing — `+
  `${(C.dead_end_tags_evergreen_cannot_return||{})["Wrong Number"]||0} wrong numbers in one `+
  `week is a list-quality number, not an inbox number. <code>Not Interested</code> and `+
  `<code>Threat</code> are excluded on the same grounds.<br>`+
  `<b>Strike Tax is not loaded into Evergreen</b> — it also had no reply categorised in `+
  `Airtable this week, so nothing is being hidden by that. ` +
  (nie.length ? `<b>${nie.map(([k,v])=>esc(k)+" ("+v+")").join(", ")}</b> `+
     `${nie.length===1?"works":"work"} out of Airtable with no Evergreen slug, so `+
     `${nie.length===1?"that reply is":"those replies are"} not in the list below.` : "");

document.getElementById("legend").innerHTML = D.categories
  .filter(c => rows.some(r=>r.category===c))
  .map(c => `<div><b>${esc(c)}</b> — ${esc(D.gloss[c]||"")}</div>`).join("");

// ---- filters
function fill(id, vals, all){
  const el = document.getElementById(id);
  el.innerHTML = `<option value="">${all}</option>` +
    vals.map(v=>`<option value="${esc(v)}">${esc(v)}</option>`).join("");
  el.onchange = render;
}
fill("f-client", slugs.map(s=>L[s]||s), "every client");
fill("f-type", D.categories.filter(c=>rows.some(r=>r.category===c)), "every request type");
fill("f-status", ["never answered","ball with us","we spoke last",
                  "reply not in the record"], "any status");
fill("f-channel", [...new Set(rows.map(r=>r.channel).filter(Boolean))].sort(), "sms + email");
document.getElementById("f-q").oninput = render;
for (const id of ["f-flag","f-exp"]) {
  const b = document.getElementById(id);
  b.onclick = () => { b.setAttribute("aria-pressed", b.getAttribute("aria-pressed")!=="true"); render(); };
}

const routes = r => {
  const b = [];
  if (r.email)   b.push(`<a href="mailto:${esc(r.email)}">${esc(r.email)}</a>`);
  if (r.phone)   b.push(`<a href="sms:${esc(r.phone)}">${esc(r.phone)}</a>`);
  if (r.linkedin)b.push(`<a href="${esc(r.linkedin)}" target="_blank" rel="noopener">LinkedIn profile</a>`);
  if (r.website) b.push(`<a href="${esc(r.website)}" target="_blank" rel="noopener">${esc(r.website.replace(/^https?:\/\//,""))}</a>`);
  if (r.company_linkedin_search)
    b.push(`<a href="${esc(r.company_linkedin_search)}" target="_blank" rel="noopener">company on LinkedIn</a> <span class="drv">(derived search)</span>`);
  const head = b.length ? b.join(" &middot; ") : `<span class="drv">no contact route on any record</span>`;
  const how = r.enriched_by
    ? `<span class="drv">details joined from Airtable on ${esc(r.enriched_by)}</span>` : "";
  return `<div class="routes">${head}${how?"<br>"+how:""}</div>`;
};

const thread = r => !r.messages.length
  ? `<div class="warnrow">Evergreen returned no thread text for this reply. It was tagged, so the reply happened — we just cannot see it.</div>`
  : `<div class="thread">` + r.messages.map(m =>
      `<div class="msg ${m.dir==="inbound"?"in":"out"}"><span class="w">`+
      `${m.dir==="inbound" ? esc(m.sender||"them") : "us"+(m.automated?" &middot; automated":"")}`+
      ` &middot; ${esc(m.when)}</span>${esc(m.body)}</div>`).join("") + `</div>`;

function card(r, i){
  const cls = r.status==="never answered" ? "never" : r.status==="ball with us" ? "ball" : "";
  const showStatus = r.status!=="we spoke last";
  const chips = [`<span class="chip client">${esc(L[r.client_slug]||r.client_slug)}</span>`,
    `<span class="chip type">${esc(r.category)}</span>`,
    showStatus ? `<span class="chip ${cls||"flag"}">${esc(r.status)}</span>` : "",
    `<span class="chip">${esc(r.channel||"?")}</span>`,
    r.mistagged===true ? `<span class="chip flag">tagged ${esc(r.category)}, reads as ${esc(r.intent)}</span>` : "",
    r.thread_truncated ? `<span class="chip flag">thread cut at 1200 chars</span>` : "",
  ].filter(Boolean).join("");
  const meta = [r.job_title, r.stage ? "stage "+r.stage : "no deal record",
    "replied " + (r.created_at||"").slice(0,10),
    r.days_since_reply!=null ? r.days_since_reply+"d ago" : "",
    r.speed_mins!=null ? "answered in "+Math.round(r.speed_mins)+" min" : "",
    r.followups ? r.followups+" follow-up"+(r.followups>1?"s":"") : ""].filter(Boolean).join(" · ");
  return `<div class="card ${cls}" data-i="${i}">
    <button class="head" type="button" aria-expanded="false"
      onclick="const c=this.parentNode;c.classList.toggle('open');
               this.setAttribute('aria-expanded',c.classList.contains('open'));">
      <div class="who">${esc(r.contact||"(no name on record)")}${r.company?` <span class="co">— ${esc(r.company)}</span>`:""}</div>
      <div class="chips">${chips}</div>
      <div class="meta">${esc(meta)}${r.campaign_name?` · <i>${esc(r.campaign_name)}</i>`:""}</div>
      ${r.their_reply?`<div class="quote">${esc(r.their_reply)}</div>`:""}
    </button>
    <div class="body">${routes(r)}${thread(r)}</div></div>`;
}

function render(){
  const c = document.getElementById("f-client").value,
        ty= document.getElementById("f-type").value,
        st= document.getElementById("f-status").value,
        ch= document.getElementById("f-channel").value,
        q = document.getElementById("f-q").value.trim().toLowerCase(),
        fl= document.getElementById("f-flag").getAttribute("aria-pressed")==="true",
        ex= document.getElementById("f-exp").getAttribute("aria-pressed")==="true";
  const hay = r => [r.contact,r.company,r.job_title,r.campaign_name,r.their_reply,
                    r.our_answer,r.opener].join(" ").toLowerCase();
  const out = rows.filter(r =>
    (!c || (L[r.client_slug]||r.client_slug)===c) && (!ty||r.category===ty) &&
    (!st||r.status===st) && (!ch||r.channel===ch) && (!fl||r.mistagged===true) &&
    (!q || hay(r).includes(q)));
  document.getElementById("count").textContent =
    `${out.length} of ${n} shown · ${out.filter(r=>r.status==="never answered").length} never answered`;
  const box = document.getElementById("list");
  if (!out.length){ box.innerHTML = `<p class="empty">Nothing matches those filters.</p>`; return; }
  let html = "", last = null;
  for (const s of slugs){
    const mine = out.filter(r=>r.client_slug===s);
    if (!mine.length) continue;
    html += `<h2>${esc(L[s]||s)} <span class="of">${mine.length} unbooked of ${R[s].in_window} replies</span></h2>`;
    html += mine.map(card).join("");
  }
  box.innerHTML = html;
  box.querySelectorAll(".card").forEach(e=>{
    if (ex) e.classList.add("open");
    e.querySelector(".head").setAttribute("aria-expanded", String(ex));
  });
}
render();

document.getElementById("foot").innerHTML =
  `${esc(D.window)} · built ${esc(D.built_at)} · source: Evergreen `+
  `<code>/deals</code> + <code>/contacts</code>, unioned and de-duplicated · `+
  `CSV of the same rows sits next to this file.`;
</script>
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--window", default="2026-08-24_to_2026-08-28")
    ap.add_argument("--out", default=os.path.join(gm.ROOT, "clients/_rollup/output"))
    a = ap.parse_args()

    src = os.path.join(a.out, f"{a.window}-unbooked-replies.json")
    d = json.load(open(src))
    mons = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
            "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    lo, hi = d["window_slug"].split("_to_")
    pretty = (f"{mons[int(lo[5:7]) - 1]} {int(lo[8:10])}\u2013{int(hi[8:10])}"
              if lo[:7] == hi[:7]
              else f"{mons[int(lo[5:7]) - 1]} {int(lo[8:10])}\u2013"
                   f"{mons[int(hi[5:7]) - 1]} {int(hi[8:10])}")
    html = (TEMPLATE.replace("__DATA__", json.dumps(d))
                    .replace("__TITLE__", f"Unbooked Replies, {pretty}")
                    .replace("__H1__", f"Every reply from {pretty} that never became a meeting"))
    dst = os.path.join(a.out, f"{a.window}-unbooked-replies.html")
    open(dst, "w").write(html)
    print(f"  {len(d['rows'])} rows -> {dst}")


if __name__ == "__main__":
    main()
