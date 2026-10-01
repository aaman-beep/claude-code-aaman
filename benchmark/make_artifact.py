"""Render all saved run results into one self-contained HTML trace artifact.

  python benchmark/make_artifact.py            # writes benchmark/trace-artifact.html

Reads cases.json + results/*.json + graders.py. Shows, per case: INPUT, the full PATH (every
skill fired + every Evergreen call, in order), the OUTPUT, and the score. This is the artifact
Aaman opens to see input -> path -> output for the whole phase-1 set.

The file is written as artifact page-content (title + style + body markup, no html/head/body
wrapper) so it can be published directly with the Artifact tool, or opened locally.
"""
import glob
import html
import json
import os

import graders

HERE = os.path.dirname(os.path.abspath(__file__))


def esc(x):
    return html.escape(str(x if x is not None else ""))


def score_pill(score):
    m = {1: ("pass", "1"), 0: ("fail", "0"), "void": ("void", "void"), "needs_human": ("human", "judge")}
    cls, label = m.get(score, ("human", str(score)))
    return f'<span class="pill {cls}">{label}</span>'


def trace_html(trace):
    rows = []
    for step in sorted(trace, key=lambda s: s.get("seq", 0)):
        kind = step.get("kind", "")
        rows.append(
            f'<li class="step {esc(kind)}">'
            f'<span class="k">{esc(kind)}</span>'
            f'<span class="n">{esc(step.get("name",""))}</span>'
            f'<span class="rs">{esc(step.get("result_summary",""))}</span>'
            f'</li>'
        )
    return '<ol class="trace">' + "".join(rows) + "</ol>"


def variants_html(variants):
    if not variants:
        return ""
    out = ['<div class="variants">']
    for i, v in enumerate(variants):
        if not (v.get("t1") or v.get("t2")):
            continue
        meta = []
        for key in ("rung", "enrichment", "winner_ref", "loser_ref", "mechanism"):
            if v.get(key):
                meta.append(f'<span class="vm"><b>{esc(key)}</b> {esc(v[key])}</span>')
        out.append(
            '<div class="variant">'
            + (f'<pre class="t">T1  {esc(v.get("t1",""))}</pre>' if v.get("t1") else "")
            + (f'<pre class="t">T2  {esc(v.get("t2",""))}</pre>' if v.get("t2") else "")
            + ('<div class="meta">' + "".join(meta) + "</div>" if meta else "")
            + "</div>"
        )
    out.append("</div>")
    return "".join(out)


CAT_ORDER = {"mechanism": 0, "copy": 1, "benchmark": 2, "routing": 3, "strategy": 4}


def build():
    cases = graders.load_cases()
    files = sorted(glob.glob(os.path.join(HERE, "results", "*.json"))
                   + glob.glob(os.path.join(HERE, "results-native", "*.json")))
    runs = {}
    for f in files:
        r = json.load(open(f))
        runs[r["case_id"]] = r
    report = graders.grade_all(list(runs.values())) if runs else {"results": [], "scorecard": {}}
    graded = {r["case_id"]: r for r in report["results"]}
    sc = report["scorecard"]

    # order by category (mechanism, copy, benchmark, routing, strategy) then id
    order = sorted(cases.values(), key=lambda c: (CAT_ORDER.get(c["category"], 9), c["id"]))

    cards = []
    for c in order:
        cid = c["id"]
        run = runs.get(cid)
        g = graded.get(cid)
        ran = run is not None
        score = g["score"] if g else None
        fired = (g["pipeline_fired"] if g else None)
        open_attr = " open" if (ran and score in (0, "void")) else ""
        head = (
            f'<summary>'
            f'<span class="cid">{esc(cid)}</span>'
            f'<span class="cat {esc(c["category"])}">{esc(c["category"])}</span>'
            f'<span class="gt">{esc(c["grade_type"])}</span>'
            + (score_pill(score) if ran else '<span class="pill notrun">not run</span>')
            + (f'<span class="pill fired-{ "yes" if fired else "no" }">pipeline {"fired" if fired else "void"}</span>' if ran else "")
            + f'</summary>'
        )
        body = ['<div class="body">']
        body.append(f'<div class="field"><label>Input</label><p>{esc(c["input"])}</p></div>')
        body.append(f'<div class="field"><label>Right (ground truth)</label><p>{esc(c.get("right",""))}</p></div>')
        body.append(f'<div class="field"><label>Pass rule</label><p class="rule">{esc(c.get("pass_rule",""))}</p></div>')
        if ran:
            if run.get("output", {}).get("text"):
                body.append(f'<div class="field"><label>Output</label><p>{esc(run["output"]["text"])}</p></div>')
            body.append(variants_html(run.get("output", {}).get("variants", [])))
            if run.get("trace"):
                body.append(f'<div class="field"><label>Path (skills + Evergreen, in order)</label>{trace_html(run["trace"])}</div>')
            if run.get("notes"):
                body.append(f'<div class="field"><label>Notes</label><p class="notes">{esc(run["notes"])}</p></div>')
            if g and g.get("reason"):
                body.append(f'<div class="field"><label>Grader</label><p class="rule">{esc(g["reason"])}</p></div>')
        else:
            body.append('<p class="norun">Not run yet. Generate the prompt with <code>make_prompt.py '
                        + esc(cid) + '</code>, run it in a fresh playbook session, save to results/'
                        + esc(cid) + '.json.</p>')
        body.append("</div>")
        cards.append(f'<details class="case"{open_attr}>{head}{"".join(body)}</details>')

    tile_list = []
    for cat in ("mechanism", "copy", "benchmark", "routing", "strategy"):
        if cat in sc:
            tile_list.append(f'<div class="tile"><div class="tv">{esc(sc[cat])}</div><div class="tl">{cat}</div></div>')
    tile_list.append(f'<div class="tile"><div class="tv">{len(runs)} / {len(cases)}</div><div class="tl">cases run</div></div>')
    tiles = "".join(tile_list)

    html_doc = TEMPLATE.replace("{{TILES}}", tiles).replace("{{CARDS}}", "".join(cards))
    out = os.path.join(HERE, "trace-artifact.html")
    with open(out, "w") as f:
        f.write(html_doc)
    print(f"wrote {out}  ({len(runs)}/{len(cases)} cases)")


TEMPLATE = """<title>Benchmark Trace</title>
<style>
  /* Layout: sticky scorecard header, then a vertical list of expandable case cards.
     Palette: cool off-white ground, ink text, indigo accent for skills, teal for Evergreen,
     semantic green/red/amber for pass/fail/void. Mono for copy + trace content. */
  :root{
    --bg:#f4f5f8; --panel:#ffffff; --edge:#e2e6ee; --ink:#131722; --muted:#5c6575;
    --accent:#4655d6; --ever:#0f8f88; --pass:#1a8f4c; --fail:#c2372e; --void:#b26a00; --human:#6b46c1;
    --mono:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
    --sans:system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
  }
  @media (prefers-color-scheme:dark){:root:not([data-theme="light"]){
    --bg:#0f131a; --panel:#161b24; --edge:#252c38; --ink:#e6e9f0; --muted:#98a2b3;
    --accent:#8b95f0; --ever:#3fc9c0; --pass:#48c07a; --fail:#f0857c; --void:#e0a247; --human:#b79df0; color-scheme:dark;
  }}
  :root[data-theme="dark"]{
    --bg:#0f131a; --panel:#161b24; --edge:#252c38; --ink:#e6e9f0; --muted:#98a2b3;
    --accent:#8b95f0; --ever:#3fc9c0; --pass:#48c07a; --fail:#f0857c; --void:#e0a247; --human:#b79df0; color-scheme:dark;
  }
  body{background:var(--bg);color:var(--ink);font-family:var(--sans);line-height:1.5}
  .wrap{max-width:900px;margin:0 auto;padding-inline:16px;padding-block:0 40px}
  header{position:sticky;top:env(safe-area-inset-top,0px);background:var(--bg);z-index:5;
    padding-block:18px 12px;border-bottom:1px solid var(--edge);margin-bottom:16px}
  h1{margin:0 0 3px;font-size:19px;letter-spacing:-.01em;text-wrap:balance}
  .sub{margin:0 0 14px;color:var(--muted);font-size:12.5px}
  .tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(132px,1fr));gap:10px}
  .tile{background:var(--panel);border:1px solid var(--edge);border-radius:12px;padding:12px 14px}
  .tv{font-size:20px;font-weight:700;font-variant-numeric:tabular-nums;letter-spacing:-.02em}
  .tl{font-size:10.5px;text-transform:uppercase;letter-spacing:.07em;color:var(--muted);margin-top:2px}
  .case{background:var(--panel);border:1px solid var(--edge);border-radius:12px;margin-bottom:10px;overflow:hidden}
  summary{list-style:none;cursor:pointer;display:flex;align-items:center;gap:9px;flex-wrap:wrap;
    padding:12px 14px;font-size:13px}
  summary::-webkit-details-marker{display:none}
  .cid{font-family:var(--mono);font-weight:700;font-size:12.5px}
  .cat{font-size:10.5px;text-transform:uppercase;letter-spacing:.06em;padding:2px 7px;border-radius:999px;border:1px solid var(--edge);color:var(--muted)}
  .cat.mechanism{color:var(--accent);border-color:color-mix(in srgb,var(--accent) 40%,var(--edge))}
  .cat.copy{color:var(--ever);border-color:color-mix(in srgb,var(--ever) 40%,var(--edge))}
  .cat.benchmark{color:var(--void);border-color:color-mix(in srgb,var(--void) 40%,var(--edge))}
  .cat.routing{color:var(--human);border-color:color-mix(in srgb,var(--human) 40%,var(--edge))}
  .cat.strategy{color:var(--fail);border-color:color-mix(in srgb,var(--fail) 40%,var(--edge))}
  .tl{text-transform:capitalize}
  .gt{font-size:10.5px;color:var(--muted);letter-spacing:.04em}
  .pill{margin-left:auto;font-size:10.5px;font-weight:700;padding:3px 9px;border-radius:999px;text-transform:uppercase;letter-spacing:.04em}
  .pill+.pill{margin-left:6px}
  .pass{background:color-mix(in srgb,var(--pass) 16%,transparent);color:var(--pass)}
  .fail{background:color-mix(in srgb,var(--fail) 16%,transparent);color:var(--fail)}
  .void{background:color-mix(in srgb,var(--void) 18%,transparent);color:var(--void)}
  .human{background:color-mix(in srgb,var(--human) 16%,transparent);color:var(--human)}
  .notrun{background:var(--edge);color:var(--muted)}
  .fired-yes{background:color-mix(in srgb,var(--pass) 12%,transparent);color:var(--pass);margin-left:6px}
  .fired-no{background:color-mix(in srgb,var(--void) 16%,transparent);color:var(--void);margin-left:6px}
  .body{padding:2px 14px 15px;border-top:1px solid var(--edge)}
  .field{margin-top:13px;min-width:0}
  label{display:block;font-size:10.5px;text-transform:uppercase;letter-spacing:.07em;color:var(--muted);margin-bottom:4px}
  .field p{margin:0;font-size:13px}
  .rule,.notes{color:var(--muted);font-size:12.5px}
  .variant{border:1px solid var(--edge);border-radius:9px;padding:9px;margin-top:8px;background:var(--bg)}
  pre.t{font-family:var(--mono);font-size:12px;margin:0 0 5px;white-space:pre-wrap;word-break:break-word}
  .meta{display:flex;flex-wrap:wrap;gap:5px;margin-top:4px}
  .vm{font-size:10.5px;color:var(--muted);background:var(--panel);border:1px solid var(--edge);border-radius:6px;padding:2px 7px}
  .vm b{color:var(--ink);font-weight:600}
  ol.trace{list-style:none;margin:0;padding:0;counter-reset:s}
  .step{counter-increment:s;display:grid;grid-template-columns:auto auto 1fr;gap:8px;align-items:baseline;
    padding:6px 0;border-top:1px dashed var(--edge);font-size:12px;min-width:0}
  .step:first-child{border-top:none}
  .step::before{content:counter(s);font-family:var(--mono);font-size:10px;color:var(--muted);
    align-self:start;grid-column:1}
  .step .k{font-size:9.5px;text-transform:uppercase;letter-spacing:.05em;padding:1px 6px;border-radius:5px;font-weight:700}
  .step.skill .k{background:color-mix(in srgb,var(--accent) 16%,transparent);color:var(--accent)}
  .step.evergreen .k{background:color-mix(in srgb,var(--ever) 16%,transparent);color:var(--ever)}
  .step .n{font-family:var(--mono);font-size:11.5px;word-break:break-word}
  .step .rs{color:var(--muted);min-width:0;word-break:break-word}
  .norun{color:var(--muted);font-size:12.5px}
  code{font-family:var(--mono);font-size:11.5px;background:var(--bg);padding:1px 5px;border-radius:5px;border:1px solid var(--edge)}
</style>
<div class="wrap">
  <header>
    <h1>Benchmark Trace</h1>
    <p class="sub">Phase 1 &middot; mechanism + copy &middot; each case run through the playbook (writer) with Evergreen as the data provider. Path = every skill fired and every Evergreen call, in order.</p>
    <div class="tiles">{{TILES}}</div>
  </header>
  {{CARDS}}
</div>
"""


if __name__ == "__main__":
    build()
