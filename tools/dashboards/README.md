# Client troubleshooting dashboards

One page per client answering four questions: which campaigns ran each month, which months
hit the positive-reply and booked KPIs, every piece of copy that ever went out, and every
positive reply that never converted.

## Rebuild

```sh
python3 tools/ghl_mine.py --client <client>     # SMS copy history from the GHL send log
python3 tools/eb_pull.py  --client <client>     # EmailBison campaigns + sequence copy (de-spun)
# Evergreen: GET /api/clients/<slug>/{stats,deals,replies,copies} → scratchpad/evergreen/<client>.json
python3 tools/dashboards/build_datasets.py <client>   # merges the three into data/<client>.json
python3 tools/dashboards/gen_artifact.py   <client>   # → pages/<client>-troubleshoot.html
python3 tools/dashboards/gen_index.py urls.json      # → pages/index-troubleshoot.html
```

`build_datasets.py` / `gen_artifact.py` read and write under the scratchpad dir they live next
to; point `DATA`/`OUT` at a repo path if you want the output committed.

## Two things worth knowing

**Positives are counted the way Airtable counts them** — Disqualified *and* "Maybe" excluded.
Verified against the live `This Month` figure for go_fish (27 deals − 9 maybes = 18 positives).
Maybes are shown separately in the scoreboard rather than dropped.

**Evergreen slugs differ from registry keys** — `go_fish`, `growth_lab`, `strike_tax`
(underscores). Strike Tax is in Airtable but not loaded into Evergreen, so it has no KPI or
deals data; the page says so instead of showing zeros.

`clients/registry.json` is the source of truth for locationIds, workflow prefixes, and the
per-client MCP servers that hold the credentials.
