---
name: call-corpus-search
description: Search a client's sales/strategy call corpus in Supabase for transcript chunks that match a specific pain point, ideal outcome, objection, or theme. Use this whenever the user is doing GTM/positioning/copy work for a specific client (e.g. "for kynship I'm targeting X pain point — find me anything similar in our call corpus", "what have prospects said about Y for client Z", "pull objections about pricing across kynship's calls"). The skill calls the existing tools/search_chunks_by_*.py scripts which hit the call_chunks table.
---

# Call Corpus Search

The `client_calls` + `call_chunks` tables in Supabase contain every prospect/strategy call we've imported, sliced into ~10–15 topic-coherent chunks each, with three embedding columns (verbatim text, one-line gist, label) so the right retrieval mode can be picked per question.

## Evergreen — the shared knowledge API (check it first)

Scaletopia's knowledge lives in **Evergreen**, the one API every skill in this playbook shares.
It is the research/data **provider** — it serves evidence and numbers; it does **not** write copy
(that's this skill's job, and your proven copy stays yours). Your local `call_chunks` search still works. Evergreen holds the same calls PLUS every categorized reply thread across ALL clients — use it to widen a search beyond one client's local corpus.

- **Base URL:** `https://knowledgebase-production-f52e.up.railway.app`
- **Auth (required):** send header `Authorization: Bearer $EVERGREEN_API_KEY` on every call — the key
  lives in this playbook's `.env` (gitignored). No header -> **401**.
- **Discover the API yourself:** `GET /api/docs` is the live index of every endpoint with its params
  and descriptions; `GET /api/openapi` is the full machine schema. Unsure which endpoint/field exists?
  Read `/api/docs` first — never guess a path or bulk-pull GHL/Airtable for what Evergreen already has.
- **Focused entry points:** `evergreen-research` (pull/save findings) · `evergreen-stats` (numbers) ·
  `evergreen-data` (full field-level catalogue).

**What THIS skill pulls from Evergreen:**
- `POST /api/search {"type":"deals","query":"..."}` — semantic search over real **reply
  conversations** (e.g. "price objection handled then meeting booked").
- `POST /api/search {"type":"contacts","query":"..."}` and
  `GET /api/clients/{slug}/contacts?category=Not%20Interested` — categorized reply threads incl. negatives.
- `POST /api/search {"type":"calls","query":"..."}` — ingested call chunks (exact buyer phrasing) across
  clients, not just the local table.

## When to use this skill

Use it the moment a GTM-style request mentions BOTH a client and an angle/pain/outcome/objection — anything that sounds like *"find me what real prospects said about ___ for ___"*. Examples:

- "I'm doing kynship copy for the 'high CAC' pain point — find similar moments in their calls."
- "What objections did kynship prospects raise about agency pricing?"
- "Show me ideal-outcome quotes from kynship calls about creative volume."
- "Are prospects across kynship calls talking about forecasting?"

Skip it for: code questions, generic claude.md tasks, anything not tied to a real client.

## Schema cheat-sheet

`client_calls`: one row per call. Useful columns: `id`, `client`, `company`, `call_date`, `category`, `specialty`, `pain_point`, `transcript_md`, `chunked`, `embedded`.

`call_chunks`: one row per topic chunk. Columns:
- `call_id` → FK to `client_calls.id`
- `client` (denormalised, filter on this)
- `start_time`, `end_time`, `speakers[]`
- `text` (verbatim dialogue), `summary` (one-line gist), `label`
- `label` ∈ {`pain`, `ideal_outcome`, `current_solution`, `tried_failed`, `belief`, `objection`, `context`}
- `embedding`, `summary_embedding`, `label_embedding` (vector(1536), Gemini)

## How to search — pick the right tool

Three CLIs in `tools/`. All return JSON.

**Client scoping — DEFAULT IS CROSS-CLIENT:**
- **ALWAYS omit `--client` by default.** Search across the WHOLE corpus (every client we have). Pain points, objections, and ideal-outcome language travel across verticals — a "high CAC" complaint from a kynship prospect is usually echoed verbatim by prospects in other clients' books. The strategist needs that cross-pollination signal.
- Only add `--client <name>` if the user **explicitly** says "only kynship calls" / "just for client X" / "scope to <client>". If they say "for kynship I'm working on…" that is just *which client they're writing for*, NOT a request to limit search — still go cross-client.
- After running cross-client, when displaying results group hits by `client` + `company` so the strategist can see which other client books echo the pattern.

| Tool | Use when… | Example |
|---|---|---|
| `search_chunks_by_text.py "<query>"` | Want **verbatim quotes** / actual phrasing of prospects | `python3 tools/search_chunks_by_text.py "burned by previous agency"` |
| `search_chunks_by_summary.py "<query>"` | Want **theme/concept matches**, scanning many calls | `python3 tools/search_chunks_by_summary.py "channel diversification anxiety"` |
| `search_chunks_by_label.py <label> [query]` | Want **every chunk of one type** (all pains, all objections), optionally ranked. Searches against `label_text` (label \| pain_point \| summary) so it's strategic-bag-of-words match. | `python3 tools/search_chunks_by_label.py pain "high CAC" --top 20` |
| `search_chunks_by_pain_point.py "<query>"` | Want every chunk from any call whose **strategic pain point** matched (KG hop). Pulls all chunks — even action-items / pricing — from calls that were ABOUT that pain. | `python3 tools/search_chunks_by_pain_point.py "high CAC"` |
| `search_chunks_by_angle.py "<query>"` | Want every chunk from any call **pitched on that angle** (e.g. "cut CAC by 50%", "creative volume"). | `python3 tools/search_chunks_by_angle.py "cut CAC by 50%"` |

Common flags: `--top N` (default 10), `--label <bucket>` to constrain text/summary search to a label, `--all` (label tool only) to dump every chunk in that bucket without ranking.

## Working pattern

1. **Hear a request like "for kynship I want pain points about X."**
2. **Pick the right tool:**
   - Need actual words → `search_chunks_by_text.py`
   - Need concept matches across calls → `search_chunks_by_summary.py`
   - Want a specific bucket of all chunks → `search_chunks_by_label.py <label>`
3. **Run with `--client <client>` and an appropriate `--top`** (10–25 for first pass).
4. **Read the JSON output** — each hit has `company`, `call_date`, `label`, `summary`, `text`, `similarity`. The `similarity` is cosine; >0.55 is meaningfully related, >0.7 is strong.
5. **Synthesise back to the user**: cluster results by company/theme, surface the verbatim quote if they're writing copy, surface the gist + count if they're sizing up a pattern.

## Practical tips

- If summary search returns shallow results, fall back to text search with the same query — they hit different signals.
- Combine: use `search_chunks_by_label.py pain "high CAC" --top 30` to scope to pain chunks and rank by relevance.
- For broad sweeps, `--top 25` then group hits by `company` to see which calls cluster on the theme.
- Don't dump raw JSON to the user — translate it into a brief: 3–6 verbatim quotes with attribution + a one-line synthesis at the top.
- Check `client_calls.transcript_status` is `ok` and `embedded=true` before assuming corpus completeness for a client. If the user adds new calls, run `tools/chunk_calls.py --client <name>` then `tools/embed_chunks.py --client <name>` to bring them in.

## Adding a new client

The same tooling works for any client — just insert their calls into `client_calls` with the new `client` value, run the chunker + embedder, and pass `--client <name>` to the search tools.
