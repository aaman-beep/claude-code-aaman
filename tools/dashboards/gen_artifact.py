#!/usr/bin/env python3
"""Render each client's merged dataset into a troubleshooting-dashboard HTML page.

Same visual system as the approved Digital Resource artifact (tokens, serif tiles,
mono copy rows) extended with: monthly KPI scoreboard, email sequence copy
(spintax + rendered plain email), missed positive replies, Evergreen cross-check.
"""
import json, os, sys, html

SP = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(SP, "data")
OUT = os.path.join(SP, "pages")
os.makedirs(OUT, exist_ok=True)

CLIENTS = ["gofish", "leadgenix", "strike-tax", "growth-lab", "redo", "kynship"]

CSS = """
:root {
  --paper:#F4F5F7; --card:#FFF; --ink:#171A20; --ink-2:#3D4453; --muted:#6B7280;
  --line:#E1E4EA; --line-2:#EFF1F4;
  --accent:#B5771A; --accent-soft:#FBF0DC;
  --good:#1B7A4B; --good-soft:#E3F2EA; --bad:#B8413A; --bad-soft:#FAE7E5;
  --serif:"Iowan Old Style","Palatino Linotype",Palatino,Georgia,serif;
  --sans:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;
  --mono:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
}
@media (prefers-color-scheme:dark) { :root {
  --paper:#0F1116; --card:#171A21; --ink:#E7E9ED; --ink-2:#B6BCC7; --muted:#818997;
  --line:#272C36; --line-2:#1E222A; --accent:#E0A84C; --accent-soft:#2E2617;
  --good:#4FBF85; --good-soft:#15291F; --bad:#E2726A; --bad-soft:#341C1A; } }
:root[data-theme="dark"] {
  --paper:#0F1116; --card:#171A21; --ink:#E7E9ED; --ink-2:#B6BCC7; --muted:#818997;
  --line:#272C36; --line-2:#1E222A; --accent:#E0A84C; --accent-soft:#2E2617;
  --good:#4FBF85; --good-soft:#15291F; --bad:#E2726A; --bad-soft:#341C1A; }
:root[data-theme="light"] {
  --paper:#F4F5F7; --card:#FFF; --ink:#171A20; --ink-2:#3D4453; --muted:#6B7280;
  --line:#E1E4EA; --line-2:#EFF1F4; --accent:#B5771A; --accent-soft:#FBF0DC;
  --good:#1B7A4B; --good-soft:#E3F2EA; --bad:#B8413A; --bad-soft:#FAE7E5; }

* { box-sizing:border-box; }
body { margin:0; background:var(--paper); color:var(--ink); font-family:var(--sans);
  line-height:1.55; -webkit-font-smoothing:antialiased; }
.wrap { max-width:1080px; margin:0 auto; padding:0 24px 96px; }
header { padding:52px 0 24px; border-bottom:1px solid var(--line); }
.eyebrow { font-size:11px; letter-spacing:.14em; text-transform:uppercase; color:var(--accent);
  font-weight:650; margin:0 0 12px; }
h1 { font-family:var(--serif); font-size:clamp(28px,4.2vw,42px); line-height:1.12; margin:0 0 12px;
  font-weight:600; letter-spacing:-.01em; text-wrap:balance; }
.lede { max-width:70ch; color:var(--ink-2); margin:0; font-size:15.5px; }
.lede b { color:var(--ink); font-weight:600; }
h2 { font-family:var(--serif); font-size:24px; font-weight:600; margin:0 0 4px; letter-spacing:-.005em; }
.sub { color:var(--muted); font-size:13.5px; margin:0 0 18px; max-width:75ch; }
section { padding-top:44px; }
.tiles { display:grid; grid-template-columns:repeat(auto-fit,minmax(138px,1fr)); gap:1px;
  background:var(--line); border:1px solid var(--line); border-radius:7px; overflow:hidden; margin-top:26px; }
.tile { background:var(--card); padding:14px 17px; }
.tile .k { font-size:11px; letter-spacing:.08em; text-transform:uppercase; color:var(--muted); font-weight:600; }
.tile .v { font-family:var(--serif); font-size:26px; font-weight:600; margin-top:3px; font-variant-numeric:tabular-nums; }
.tile .v small { font-size:14px; color:var(--muted); font-family:var(--sans); }
.note { margin-top:22px; padding:13px 16px; background:var(--accent-soft); border-left:3px solid var(--accent);
  border-radius:0 7px 7px 0; font-size:14px; color:var(--ink-2); }
.note b { color:var(--ink); }
.nav { position:sticky; top:0; z-index:5; background:var(--paper); display:flex; gap:7px; flex-wrap:wrap;
  padding:12px 0; border-bottom:1px solid var(--line); }
.nav a { font-size:12.5px; font-weight:600; color:var(--ink-2); text-decoration:none;
  border:1px solid var(--line); background:var(--card); border-radius:20px; padding:4px 13px; }
.nav a:hover { color:var(--accent); border-color:var(--accent); }

table.score { width:100%; border-collapse:collapse; background:var(--card); border:1px solid var(--line);
  border-radius:7px; overflow:hidden; font-size:13.5px; }
.scroll { overflow-x:auto; border-radius:7px; }
table.score th { text-align:left; font-size:10.5px; letter-spacing:.07em; text-transform:uppercase;
  color:var(--muted); font-weight:700; padding:10px 12px; border-bottom:1px solid var(--line); background:var(--card); }
table.score td { padding:10px 12px; border-bottom:1px solid var(--line-2); vertical-align:top;
  font-variant-numeric:tabular-nums; background:var(--card); }
table.score tr:last-child td { border-bottom:none; }
td.mon { font-family:var(--serif); font-weight:600; white-space:nowrap; }
.pill { display:inline-block; font-size:10.5px; font-weight:750; letter-spacing:.04em; border-radius:4px;
  padding:2px 8px; }
.pill.hit { color:var(--good); background:var(--good-soft); }
.pill.miss { color:var(--bad); background:var(--bad-soft); }
.pill.na { color:var(--muted); background:var(--line-2); }
.camplist { color:var(--muted); font-size:12px; max-width:420px; }
.camplist span { display:block; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }

.bar { display:flex; flex-wrap:wrap; gap:9px; align-items:center; margin:18px 0 16px; }
select { appearance:none; background:var(--card); color:var(--ink); border:1px solid var(--line);
  border-radius:7px; padding:7px 30px 7px 11px; font:inherit; font-size:13px; cursor:pointer;
  background-image:linear-gradient(45deg,transparent 50%,var(--muted) 50%),linear-gradient(135deg,var(--muted) 50%,transparent 50%);
  background-position:calc(100% - 16px) 14px,calc(100% - 11px) 14px; background-size:5px 5px; background-repeat:no-repeat; }
select:focus-visible, .nav a:focus-visible, button:focus-visible, details summary:focus-visible {
  outline:2px solid var(--accent); outline-offset:1px; }
.hint { font-size:13px; color:var(--muted); margin-left:auto; }

.row { background:var(--card); border:1px solid var(--line); border-radius:7px; padding:16px 18px;
  margin-bottom:9px; display:grid; gap:14px; grid-template-columns:32px 1fr 218px; align-items:start; }
@media (max-width:840px) { .row { grid-template-columns:26px 1fr; } .metrics { grid-column:2; } }
.rank { font-family:var(--serif); font-size:19px; color:var(--muted); font-variant-numeric:tabular-nums; }
.txt { display:grid; grid-template-columns:26px 1fr; gap:9px; align-items:start; }
.txt + .txt { margin-top:9px; padding-top:9px; border-top:1px dashed var(--line); }
.leg { font-size:10px; font-weight:800; letter-spacing:.06em; color:var(--muted); padding-top:3px; }
.copy { font-family:var(--mono); font-size:13.5px; line-height:1.6; white-space:pre-wrap; word-break:break-word; }
.slot { color:var(--accent); background:var(--accent-soft); border-radius:3px; padding:0 3px; font-weight:600; }
.chars { font-size:11px; color:var(--muted); font-variant-numeric:tabular-nums; margin-top:3px; }
.meta { margin-top:11px; font-size:12px; color:var(--muted); display:flex; flex-wrap:wrap; gap:5px 8px; }
.tag { background:var(--line-2); border-radius:20px; padding:2px 9px; color:var(--ink-2); font-weight:500; }
.tag.rt { background:var(--accent-soft); color:var(--accent); font-weight:650; }
.metrics { display:flex; flex-direction:column; gap:9px; }
.m { display:grid; grid-template-columns:56px 1fr 50px; gap:8px; align-items:center; }
.m .lbl { color:var(--muted); font-weight:700; font-size:10px; letter-spacing:.05em; text-transform:uppercase; }
.track { height:6px; background:var(--line-2); border-radius:20px; overflow:hidden; }
.fill { height:100%; border-radius:20px; }
.fill.good { background:var(--good); } .fill.bad { background:var(--bad); }
.num { font-variant-numeric:tabular-nums; font-weight:650; text-align:right; font-size:12.5px; }
.num.good { color:var(--good); } .num.bad { color:var(--bad); }
.vol { font-size:12px; color:var(--muted); font-variant-numeric:tabular-nums; padding-top:4px;
  border-top:1px solid var(--line-2); }
.warn { display:inline-block; font-size:10.5px; font-weight:700; color:var(--bad); background:var(--bad-soft);
  border-radius:4px; padding:2px 7px; }

.ecamp { background:var(--card); border:1px solid var(--line); border-radius:7px; margin-bottom:10px; }
.ecamp > .head { padding:14px 18px; display:flex; flex-wrap:wrap; gap:6px 14px; align-items:baseline;
  border-bottom:1px solid var(--line-2); }
.ecamp .nm { font-weight:650; font-size:14.5px; }
.ecamp .st { font-size:10.5px; font-weight:750; letter-spacing:.05em; text-transform:uppercase;
  border-radius:4px; padding:2px 8px; background:var(--line-2); color:var(--ink-2); }
.ecamp .st.active { background:var(--good-soft); color:var(--good); }
.ecamp .st.paused, .ecamp .st.stopped { background:var(--accent-soft); color:var(--accent); }
.ecamp .estats { font-size:12.5px; color:var(--muted); font-variant-numeric:tabular-nums; margin-left:auto; }
.estep { padding:13px 18px; border-bottom:1px solid var(--line-2); }
.estep:last-child { border-bottom:none; }
.estep .shead { display:flex; gap:10px; align-items:baseline; flex-wrap:wrap; margin-bottom:7px; }
.estep .sn { font-size:10.5px; font-weight:800; letter-spacing:.06em; color:var(--muted); text-transform:uppercase; }
.estep .sstat { margin-left:auto; font-size:12px; color:var(--muted); font-variant-numeric:tabular-nums; }
.estep .sstat b { color:var(--good); }
.estep .subj { font-weight:650; font-size:13.5px; font-family:var(--mono); }
.estep .body { font-family:var(--mono); font-size:13px; line-height:1.6; white-space:pre-wrap;
  word-break:break-word; color:var(--ink-2); }
details.raw { margin-top:8px; }
details.raw summary { cursor:pointer; font-size:11.5px; color:var(--accent); font-weight:650; }
details.raw .body { margin-top:7px; padding:10px 12px; background:var(--line-2); border-radius:6px; font-size:12px; }

.miss { background:var(--card); border:1px solid var(--line); border-radius:7px; padding:13px 16px; margin-bottom:8px; }
.miss .top { display:flex; flex-wrap:wrap; gap:5px 10px; align-items:baseline; }
.miss .who { font-weight:650; font-size:14px; }
.miss .jt { color:var(--muted); font-size:12.5px; }
.miss .when { margin-left:auto; color:var(--muted); font-size:12px; font-variant-numeric:tabular-nums; }
.miss details { margin-top:7px; }
.miss summary { cursor:pointer; font-size:12px; color:var(--accent); font-weight:650; }
.miss .conv { margin-top:7px; font-family:var(--mono); font-size:12px; line-height:1.6; white-space:pre-wrap;
  word-break:break-word; color:var(--ink-2); background:var(--line-2); border-radius:6px; padding:10px 12px; }
.miss .ct { display:flex; flex-wrap:wrap; gap:5px 8px; margin-top:7px; font-size:12px; color:var(--muted); }

footer { margin-top:48px; padding-top:20px; border-top:1px solid var(--line); font-size:13px; color:var(--muted); }
.empty { padding:22px; border:1px dashed var(--line); border-radius:7px; color:var(--muted); font-size:14px;
  background:var(--card); }
"""

JS = r"""
const D = window.DATA;
const esc = s => (s||'').replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const slots = s => esc(s).replace(/\{\{([^}]*)\}\}/g,'<span class="slot">{{$1}}</span>')
                         .replace(/\{([A-Z_][A-Z_0-9]*)\}/g,'<span class="slot">{$1}</span>');
const pct = n => (n==null?'—':n.toFixed(2)+'%');
const fmt = n => (n==null?'—':n.toLocaleString('en-US'));

/* ---- monthly scoreboard ---- */
(function(){
  const el = document.getElementById('scorebody');
  if (!el) return;
  el.innerHTML = D.monthly.slice().reverse().map(m => {
    const pos = m.pos_hit==null ? '<span class="pill na">no target</span>'
      : `<span class="pill ${m.pos_hit?'hit':'miss'}">${m.pos_hit?'HIT':'MISS'}</span>`;
    const bk = m.book_hit==null ? '<span class="pill na">no target</span>'
      : `<span class="pill ${m.book_hit?'hit':'miss'}">${m.book_hit?'HIT':'MISS'}</span>`;
    const camps = m.campaigns.length
      ? `<div class="camplist">${m.campaigns.map(c=>`<span title="${esc(c)}">${esc(c)}</span>`).join('')}</div>`
      : '<span class="camplist">—</span>';
    const erep = m.email_sent ? ` <small style="color:var(--muted)">${m.email_replies} rep</small>` : '';
    return `<tr><td class="mon">${m.month}</td><td>${camps}</td>
      <td>${m.sms_sent_est?fmt(m.sms_sent_est):'—'}</td>
      <td>${m.email_sent?fmt(m.email_sent)+erep:'—'}</td>
      <td>${m.positives}${m.maybes?` <small style="color:var(--muted)">+${m.maybes} maybe</small>`:''} / ${m.pos_target??'—'} ${pos}</td>
      <td>${m.booked} / ${m.book_target??'—'} ${bk}</td></tr>`;
  }).join('');
})();

/* ---- SMS explorer (same behavior as the Digital Resource artifact) ---- */
(function(){
  const list = document.getElementById('smslist');
  if (!list || !D.sms_batches.length) return;
  const sel = id => document.getElementById(id);
  const camps = [...new Set(D.sms_batches.map(b=>b.campaign))].sort();
  sel('camp').innerHTML = '<option value="">All campaigns</option>' +
    camps.map(c=>`<option value="${esc(c)}">${esc(c.replace(/^[^-]*- /,''))}</option>`).join('');
  function render(){
    const send = sel('send').value, camp = sel('camp').value,
          sort = sel('sort').value, min = +sel('min').value;
    let rows = D.sms_batches.filter(b => b.prospects >= min &&
      (!send || b.send === send) && (!camp || b.campaign === camp));
    rows.sort((a,b) => sort==='prospects' ? b.prospects-a.prospects
      : sort==='optout_pct' ? b.optout_pct-a.optout_pct : b.reply_pct-a.reply_pct);
    sel('hint').textContent = rows.length + ' of ' + D.sms_batches.length + ' copy units';
    list.innerHTML = rows.map((b,i) => {
      const w = v => Math.min(v/6*100,100);
      return `<div class="row"><div class="rank">${i+1}</div>
      <div><div class="txt"><div class="leg">T1</div><div><div class="copy">${slots(b.T1)}</div>
        <div class="chars">${b.char_T1} chars</div></div></div>
      ${b.T2?`<div class="txt"><div class="leg">T2</div><div><div class="copy">${slots(b.T2)}</div>
        <div class="chars">${b.char_T2} chars</div></div></div>`:''}
      <div class="meta"><span class="tag${b.send==='retarget'?' rt':''}">${b.send}</span>
        <span class="tag">${esc(b.campaign.replace(/^[^-]*- /,''))}</span>
        <span class="tag">${b.first_sent} → ${b.last_sent}</span>
        ${b.burner?'<span class="warn">list burner — opt-outs ≥ replies</span>':''}</div></div>
      <div class="metrics">
        <div class="m"><span class="lbl">Reply</span><div class="track"><div class="fill good" style="width:${w(b.reply_pct)}%"></div></div><span class="num good">${pct(b.reply_pct)}</span></div>
        <div class="m"><span class="lbl">Opt-out</span><div class="track"><div class="fill bad" style="width:${w(b.optout_pct)}%"></div></div><span class="num bad">${pct(b.optout_pct)}</span></div>
        <div class="vol">${fmt(b.prospects)} prospects · ${b.replies} replies · ${b.optouts} opt-outs · ${b.delivered_pct}% delivered</div>
      </div></div>`;
    }).join('') || '<div class="empty">Nothing matches these filters.</div>';
  }
  ['send','camp','sort','min'].forEach(id => sel(id).addEventListener('change', render));
  render();
})();

/* ---- email campaigns ---- */
(function(){
  const el = document.getElementById('emaillist');
  if (!el) return;
  const camps = D.email_campaigns.filter(c => (c.steps||[]).length || (c.sent||0) > 0);
  if (!camps.length) { el.innerHTML = '<div class="empty">No email campaigns with copy or sends.</div>'; return; }
  camps.sort((a,b) => (b.sent||0)-(a.sent||0));
  el.innerHTML = camps.map(c => {
    const rr = c.sent ? (100*(c.replies||0)/c.sent).toFixed(2)+'%' : '—';
    const intr = c.interested ? ` · <b>${c.interested} interested</b>` : '';
    const steps = (c.steps||[]).map((s,i) => {
      const srr = s.sent ? (100*(s.replies||0)/s.sent).toFixed(1)+'%' : null;
      const sstat = s.sent ? `<span class="sstat">${fmt(s.sent)} sent · ${s.replies||0} replies${srr?` (${srr})`:''}${s.interested?` · <b>${s.interested} interested</b>`:''}${s.bounced?` · ${s.bounced} bounced`:''}</span>` : '<span class="sstat">no sends</span>';
      return `
      <div class="estep"><div class="shead"><span class="sn">Step ${s.order||i+1}${s.variant?' · variant B':''}${s.wait_in_days?` · wait ${s.wait_in_days}d`:''}</span>
        <span class="subj">${slots(s.subject_plain)}</span>${sstat}</div>
      <div class="body">${slots(s.body_plain)}</div>
      <details class="raw"><summary>show raw spintax</summary><div class="body">${slots(s.subject_raw)}\n\n${slots((s.body_raw_html||'').replace(/<[^>]+>/g,' '))}</div></details></div>`;
    }).join('');
    return `<div class="ecamp"><div class="head"><span class="nm">${esc(c.name)}</span>
      <span class="st ${esc(c.status)}">${esc(c.status)}</span>
      <span class="estats">${fmt(c.sent)} sent · ${fmt(c.replies)} replies (${rr})${intr} · ${fmt(c.bounced)} bounced · ${fmt(c.leads)} leads</span></div>
      ${steps || '<div class="estep"><span class="sn">No sequence copy saved</span></div>'}</div>`;
  }).join('');
})();

/* ---- missed positive replies ---- */
(function(){
  const el = document.getElementById('misslist');
  if (!el) return;
  if (!D.missed.length) { el.innerHTML = '<div class="empty">' + (D.ev_missing
    ? 'Not available — this client isn\'t loaded in Evergreen yet.' : 'No unconverted positive replies. Clean pipeline.') + '</div>'; return; }
  const cat = c => c ? `<span class="tag">${esc(c)}</span>` : '';
  el.innerHTML = D.missed.map(m => `<div class="miss">
    <div class="top"><span class="who">${esc(m.company||m.contact||'Unknown')}</span>
      <span class="jt">${esc(m.job_title||'')}</span><span class="when">${m.created_at}</span></div>
    <div class="ct"><span class="pill ${m.stage==='No Show'?'miss':'na'}">${esc(m.stage)}</span>
      ${cat(m.category)}${m.channel?`<span class="tag">${esc(m.channel)}</span>`:''}
      ${m.variant?`<span class="tag">variant ${esc(m.variant)}</span>`:''}
      ${m.phone?`<span class="tag">${esc(m.phone)}</span>`:''}${m.email?`<span class="tag">${esc(m.email)}</span>`:''}</div>
    ${m.conversation?`<details><summary>conversation</summary><div class="conv">${esc(m.conversation)}</div></details>`:''}
  </div>`).join('');
})();

/* ---- evergreen cross-check ---- */
(function(){
  const el = document.getElementById('xbody');
  if (!el) return;
  if (D.ev_missing) { document.getElementById('xwrap').innerHTML =
    '<div class="empty">This client isn\'t loaded in Evergreen yet — no copies to cross-check. Onboard it via the ingestion agents first.</div>'; return; }
  if (!D.crosscheck.length) { document.getElementById('xwrap').innerHTML =
    '<div class="empty">No mined SMS batches to cross-check yet.</div>'; return; }
  el.innerHTML = D.crosscheck.map(x => `<tr>
    <td class="copy" style="font-size:12px">${slots(x.t1_preview)}…</td>
    <td>${x.in_evergreen?'<span class="pill hit">IN EVERGREEN</span>':'<span class="pill miss">NOT SAVED</span>'}</td>
    <td>${x.ev_status?`<span class="tag">${esc(x.ev_status)}</span>`:'—'}</td>
    <td>${x.ev_lever?esc(x.ev_lever):'—'}</td></tr>`).join('');
})();
"""


def tile(k, v):
    return f'<div class="tile"><div class="k">{k}</div><div class="v">{v}</div></div>'


def gen(client):
    d = json.load(open(f"{DATA}/{client}.json"))
    label = d["label"]
    b = d["sms_batches"]
    texts = sum(x["prospects"] * x.get("texts_in_batch", 2) for x in b)
    prospects = sum(x["prospects"] for x in b if x["send"] == "initial")
    replies = sum(x["replies"] for x in b)
    rr = f"{100*replies/max(prospects,1):.1f}%" if b else "—"
    ecamps = [c for c in d["email_campaigns"] if (c.get("sent") or 0) > 0 or c.get("steps")]
    esent = sum(c.get("sent") or 0 for c in ecamps)
    ereplies = sum(c.get("replies") or 0 for c in ecamps)
    kpi = d["kpi"]
    months = d["monthly"]
    hits_pos = sum(1 for m in months if m["pos_hit"])
    hits_book = sum(1 for m in months if m["book_hit"])
    scored = [m for m in months if m["pos_hit"] is not None]

    kpi_line = (f'positives <b>{kpi.get("weeklyPositives","?")}/wk</b> · booked '
                f'<b>{kpi.get("monthlyBooked","?")}/mo</b>') if kpi else "no KPI targets found"
    ev_note = ('<p class="note"><b>Evergreen gap:</b> this client is not loaded in the Evergreen '
               'knowledge system yet (API returns 404) — KPI scoreboard and missed-replies below are '
               'unavailable until it\'s onboarded. Copy history still comes from GHL + EmailBison.</p>'
               if d["ev_missing"] else "")
    sms_missing = ('' if b else '<div class="empty">No mined SMS batches — the GHL pull for this '
                   'client returned nothing or failed; see wrap-up notes.</div>')

    tiles = "".join([
        tile("Months hit positives KPI", f'{hits_pos}<small>/{len(scored)}</small>' if scored else "—"),
        tile("Months hit booked KPI", f'{hits_book}<small>/{len(scored)}</small>' if scored else "—"),
        tile("SMS copy units", f"{len(b)}" if b else "—"),
        tile("SMS reply rate", rr),
        tile("Emails sent", f"{esent:,}" if ecamps else "—"),
        tile("Email replies", f"{ereplies:,}" if ecamps else "—"),
        tile("Missed positive replies", f'{len(d["missed"])}' if not d["ev_missing"] else "—"),
    ])

    return f"""<title>{html.escape(label)} — outbound troubleshooting</title>
<style>{CSS}</style>
<div class="wrap">
<header>
  <p class="eyebrow">{html.escape(label)} · outbound troubleshooting · built {d['built_at']}Z</p>
  <h1>Every campaign, every copy change, every reply we didn't convert</h1>
  <p class="lede">One page per question: the <b>monthly scoreboard</b> (campaigns live + KPI hit/miss
  against {kpi_line}), <b>every SMS variant</b> rebuilt from the GoHighLevel send log,
  <b>every email sequence</b> from EmailBison with the spintax collapsed into the email a prospect
  actually reads, and <b>every positive reply that never became a meeting</b>.</p>
  <div class="tiles">{tiles}</div>
  {ev_note}
</header>
<nav class="nav">
  <a href="#score">Monthly scoreboard</a><a href="#sms">SMS copy</a>
  <a href="#email">Email copy</a><a href="#missed">Missed replies</a><a href="#xcheck">Evergreen check</a>
</nav>

<section id="score">
  <h2>Monthly scoreboard</h2>
  <p class="sub">Positives = deals created that month, counted the way the Airtable KPI counts them
  (excludes Disqualified and “Maybe”; maybes shown separately). Booked = meetings booked
  (incl. no-shows). SMS volume is estimated by spreading each batch over its send window.
  {'' if not d['ev_missing'] else 'Unavailable — not in Evergreen.'}</p>
  <div class="scroll"><table class="score">
    <thead><tr><th>Month</th><th>Campaigns live</th><th>SMS sent (est)</th><th>Emails sent</th>
    <th>Positives / target</th><th>Booked / target</th></tr></thead>
    <tbody id="scorebody"></tbody>
  </table></div>
</section>

<section id="sms">
  <h2>Cold SMS — what actually ran</h2>
  <p class="sub">Rebuilt from the send log (workflows are edited in place, so this is the only record).
  T1+T2 ship ~13s apart and score as one unit. Judge the opt-out bar against the reply bar —
  a reply rate bought with equal opt-outs is a burned list, and those are flagged.</p>
  {sms_missing}
  {'''<div class="bar">
    <select id="send"><option value="">Initial + retarget</option><option value="initial" selected>Initial send</option><option value="retarget">Retarget only</option></select>
    <select id="camp"></select>
    <select id="sort"><option value="reply_pct">Best reply rate</option><option value="optout_pct">Worst opt-out</option><option value="prospects">Most sent</option></select>
    <select id="min"><option value="20">20+ prospects</option><option value="100">100+</option><option value="200">200+</option></select>
    <span class="hint" id="hint"></span></div><div id="smslist"></div>''' if b else ''}
</section>

<section id="email">
  <h2>Cold email — EmailBison sequences</h2>
  <p class="sub">Every campaign and every sequence step, each with <b>its own</b> sent / replies /
  interested — so you can see which email actually performed, not just the campaign total. Where two
  steps share a subject, they're an A/B pair. Copy is the plain email a prospect reads (first spintax
  option, merge tags highlighted); raw spintax is one click away.
  <b>Opens are 0 everywhere on purpose</b> — these campaigns run plain-text with open tracking off,
  so replies and “interested” are the only honest signals.</p>
  <div id="emaillist"></div>
</section>

<section id="missed">
  <h2>Positive replies we never converted</h2>
  <p class="sub">Deals still sitting at Positive Reply / “Maybe” / No Show — people who raised a hand
  and never got to a meeting. Newest first; open the conversation to see where it stalled.
  This is a re-engagement list, not just a report.</p>
  <div id="misslist"></div>
</section>

<section id="xcheck">
  <h2>Evergreen cross-check</h2>
  <p class="sub">Each distinct live SMS copy matched against the copies saved in Evergreen
  ({d['ev_copy_count']} on file for this client). NOT SAVED = the copy ran in the real world but the
  knowledge system doesn't know about it yet — an ingestion gap.</p>
  <div id="xwrap"><div class="scroll"><table class="score">
    <thead><tr><th>Live copy (T1)</th><th>In Evergreen?</th><th>Status</th><th>Lever</th></tr></thead>
    <tbody id="xbody"></tbody></table></div></div>
</section>

<footer>Sources: GoHighLevel conversation export (era-scoped) · EmailBison API · Evergreen
knowledge API (live Airtable mirror) · a reply is a genuine human reply; STOP counts as an opt-out,
not a reply.</footer>
</div>
<script>window.DATA = {json.dumps(d)};</script>
<script>{JS}</script>
"""


for c in (sys.argv[1:] or CLIENTS):
    p = f"{OUT}/{c}-troubleshoot.html"
    open(p, "w").write(gen(c))
    print(p, f"{os.path.getsize(p)//1024}KB")
