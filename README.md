# GTM Playground — How This Repo Works

This is the operating system for our outbound/GTM work: research a client's market from real buyer evidence, develop the proof and mechanism, write the copy, learn from what actually shipped.

**New machine? Start with [SETUP.md](SETUP.md)** — it gets you cloned, connected and running in ~20 minutes.

---

## The current system (July 2026) — start here

The pipeline now runs as **auto-loading Claude Code skills** in [.claude/skills/](.claude/skills/). You don't open prompt files — you open Claude Code in this folder and describe what you want in plain English; the right skill fires on its own.

The SMS workflow, in order:

| Step | Skill | What it does |
|---|---|---|
| 1 | `sms-brief` | Layer A market-research brief for a client + segment + persona (sales calls → master sheet → web, every claim traced) |
| 2 | `case-study-developer` | Turns a chosen case study into menus of proof framings + mechanism reframings |
| 3 | `mechanism-wordsmith` | Reframes a literal mechanism into sticky, SMS-ready lines |
| 4 | `sms-draft` | Assembles ship-ready T1/T2 SMS variants and QAs them against the Voice Profile |
| — | `sms-performance` | Mines GoHighLevel for what a client's copy ACTUALLY did (replies, opt-outs, variants) |
| — | `evergreen-stats` | Numbers only from the Evergreen API: sent, PRs, positives, booked, conversion, which variant won, reports, benchmarks, churn |
| — | `evergreen-research` | Evidence in and out: pains, buyer lingo, tiered proof, winners/losers with why-it-worked, client voice/positioning, objections, saved guidelines |
| — | `evergreen-data` | Reference only — the full Evergreen endpoint catalogue behind the two above |
| — | `call-corpus-search` | Searches the sales-call corpus for a pain/objection/theme |

Supporting pieces:

- [sms-playbook/](sms-playbook/) — `winners.csv` / `losers.csv` + the playbook. Drafting QAs against these.
- [clients/registry.json](clients/registry.json) — maps each client to its channels (GHL locationId, EmailBison/GHL MCP server names). No secrets — keys live in `~/.claude.json`.
- [tools/ghl_mine.py](tools/ghl_mine.py) / [tools/sms_report.py](tools/sms_report.py) — the GHL send-log miners behind `sms-performance`.
- [clients/](clients/) — per-client workspaces (`source/` inputs, `output/` deliverables).

The **Evergreen system** (Hilal's Supabase knowledge graph: all clients' calls, campaigns, copies, deals) is the data backbone — reached through `evergreen-stats` (numbers) and `evergreen-research` (evidence). `evergreen-data` is the full endpoint reference behind them.

---

## Legacy pipeline (pre-June 2026) — kept for reference

Everything below this line describes the ORIGINAL prompt-file pipeline (`skills/`, `rules/`, `sops/`, `frameworks/`, `sheet/`). The files still exist and still work — parts (the rules/QA thinking, the corpus tools, the Sandler references) fed directly into the current skills — but for SMS work, **use the current system above**. Kept for cold-email templates (`frameworks/`), the ingest pipeline (`sheet/`), and historical context.

A complete diagram of the legacy system lives at [GTM_SYSTEM_FLOW.md](GTM_SYSTEM_FLOW.md) — open in a Mermaid-aware viewer (VSCode preview, GitHub, Obsidian).

---

## The folders in plain English

| Folder | What lives here | Who reads it |
|---|---|---|
| [skills/](skills/) | **Legacy prompts**. The old manually-loaded step files. Superseded by `.claude/skills/` for SMS work. | Historical reference |
| [.claude/skills/](.claude/skills/) | **Auto-firing Claude Code skills — the current system.** `sms-brief`, `case-study-developer`, `mechanism-wordsmith`, `sms-draft`, `sms-performance`, `evergreen-stats`, `evergreen-research`, `evergreen-data`, `call-corpus-search`. | Claude Code auto-loads on intent match |
| [tools/](tools/) | Python CLIs: Fireflies fetcher, chunker, embedder, 5 corpus-search CLIs, Slack/Fathom helpers. | Skills shell out to these; you can run them by hand too. |
| [sheet/](sheet/) | The Supabase ingest pipeline (`fetch_all.py`, `build_final.py`, `upload_supabase.py`) + SQL migrations. | Run once per new client to load their calls into the corpus. |
| [sops/](sops/) | **Standard Operating Procedures**. How-to guides for the human operator — step-by-step checklists. | Humans + the AI reads them as reference |
| [frameworks/](frameworks/) | **Templates and proven formulas** (SMS structures, email swipe files, value-prop formulas). | Skills pull from these when writing copy |
| [rules/](rules/) | **Guardrails**. Things we always do / never do. Style, tone, anti-patterns. | Every skill reads these before producing output |
| [clients/](clients/) | **Per-client workspaces**. Each client has an `output/` folder where the pipeline writes its results, starting with `00_brainstorm.md`. | Read by downstream steps; final deliverable |
| [winning-sms/](winning-sms/) | Library of SMS messages that actually got replies. Copy skills cross-reference this. | SMS writing skill |

---

## The full pipeline — one picture

```
                ┌──────────────────────────────────┐
                │   CLIENT ONBOARDING INPUTS       │
                │   • onboarding form              │
                │   • sales-call transcripts       │
                │   • case studies / excel         │
                │   • website URL                  │
                └──────────────┬───────────────────┘
                               │
                               ▼
╔════════════════════════════════════════════════════════════════════╗
║  PHASE 0 — INGEST CALLS INTO THE SUPABASE CORPUS (one-time/client) ║
║                       (folder: tools/ + sheet/)                    ║
╚════════════════════════════════════════════════════════════════════╝
  fireflies URLs → tools/fireflies.py → markdown
                 → sheet/fetch_all.py → transcripts/*.md
                 → sheet/build_final.py → rec_enriched.csv (categorised)
                 → sheet/upload_supabase.py → client_calls table
                 → tools/chunk_calls.py → call_chunks (10–15 chunks/call)
                 → tools/embed_chunks.py → 6 Gemini vectors per chunk

  RESULT: every call sliced + embedded for retrieval. Skip if already done.
                               │
                               ▼
╔════════════════════════════════════════════════════════════════════╗
║      PHASE 0.5 — CLIENT BRAINSTORM (one consolidated KG view)      ║
║                  (skill: skills/00_client_brainstorm.md)           ║
╚════════════════════════════════════════════════════════════════════╝
  Reads: clients/<client>/* + clients/*/output/*.md + memory/*
  Runs:  ≥6 cross-client corpus searches (pain_point, angle, label,
         summary, text) — see tools/search_chunks_*.py
  Writes: clients/<client>/output/00_brainstorm.md
          → client snapshot
          → cross-client matches (verbatim quotes + what worked for
            those prior clients downstream)
          → recurring patterns
          → initial hypotheses
          → gaps for downstream skills

  RESULT: ONE FILE that every later skill reads as primary input.
          Phases 1–5 do NOT re-query Supabase. The corpus is consulted
          once here, distilled, and reused.
                               │
                               ▼
╔════════════════════════════════════════════════════════════════════╗
║                 PHASE 1 — DEEP RESEARCH PIPELINE                   ║
║              (folder: skills/ICP-skills-deepsearch-engine/)        ║
╚════════════════════════════════════════════════════════════════════╝

┌──────────────────────────────────────────────────────────────────────┐
│ STEP 1 ─► 01_context_and_data_source.md
│          ← map TAM, ICP, VoC sources
│          INPUT:  brainstorm + client website + ICP + persona
│          OUTPUT: clients/<client>/output/01_context_and_data_source.md
│          NOTE: MANDATORY corpus pass before web search
└────────────────────────────────────┬─────────────────────────────────┘
                                     ▼
┌──────────────────────────────────────────────────────────────────────┐
│ STEP 2 ─► 02_pain_points_and_consequences.md
│          ← mine real pains from VoC, rank 1–10, cascade consequences
│          INPUT:  brainstorm + Step 1 output
└────────────────────────────────────┬─────────────────────────────────┘
                                     ▼
┌──────────────────────────────────────────────────────────────────────┐
│ STEP 3 ─► 03_outcomes_and_whys.md
│          ← dream outcomes + 5 whys (emotional driver)
│          INPUT:  brainstorm + Step 2 output
└────────────────────────────────────┬─────────────────────────────────┘
                                     ▼
┌──────────────────────────────────────────────────────────────────────┐
│ STEP 4 ─► 04_current_solutions.md
│          ← what they've tried, what's blocking, what's pressuring
│          INPUT:  brainstorm + Steps 1–3
└────────────────────────────────────┬─────────────────────────────────┘
                                     ▼
┌──────────────────────────────────────────────────────────────────────┐
│ STEP 5 ─► 05_objections_and_triggers.md
│          ← predicted objections + "why now" trigger events
│          INPUT:  brainstorm + Steps 1–4
└────────────────────────────────────┬─────────────────────────────────┘
                                     ▼
╔════════════════════════════════════════════════════════════════════╗
║              PHASE 2 — STRATEGY + COMPILE THE GTM SHEET            ║
╚════════════════════════════════════════════════════════════════════╝

┌──────────────────────────────────────────────────────────────────────┐
│ STEP 6 ─► skills/ICP-skills/Market Deep-Dive & Variable Balancing.md
│          ← pressure-test research against current market reality
│          INPUT:  brainstorm + Steps 1–5
└────────────────────────────────────┬─────────────────────────────────┘
                                     ▼
┌──────────────────────────────────────────────────────────────────────┐
│ STEP 7 ─► skills/ICP-skills/GTM Hypothesis Generation & Trigger Mapping.md
│          ← produce 3+ campaign hypotheses (MDX)
└────────────────────────────────────┬─────────────────────────────────┘
                                     ▼
┌──────────────────────────────────────────────────────────────────────┐
│ STEP 8 ─► skills/ICP-skills-deepsearch-engine/gtm-sheet-compiler.md
│          ← synthesise into 3–5 scalable segments (NO new research)
│          INPUT:  brainstorm + Steps 1–7 + onboarding form + case studies
│          OUTPUT: clients/<client>/output/01_gtm_strategy.md
└────────────────────────────────────┬─────────────────────────────────┘
                                     ▼
                ➜ 3–5 segments, each with persona, triggers, offer angle
                                     │
                                     ▼
╔════════════════════════════════════════════════════════════════════╗
║                       PHASE 3 — COPYWRITING                        ║
╚════════════════════════════════════════════════════════════════════╝

┌──────────────────────────────────────────────────────────────────────┐
│ STEP 9 ─► skills/copies/sms-skills.md
│          ← write SMS copy (Pain + Mechanism + Outcome)
│          ALSO READS:
│            • sops/sms_guidelines.md
│            • sops/unique_mechanism_sop.md
│            • frameworks/sms_frameworks.md
│            • winning-sms/
│            • rules/copy_and_prompt_guidelines.md
│            • rules/anti_patterns_and_mistakes.md
│            • skills/sandler-sales-rules.md
│          INPUT:  brainstorm + GTM sheet + Steps 1–5
│          OUTPUT: clients/<client>/output/06_sms_copy_drafts.md
└────────────────────────────────────┬─────────────────────────────────┘
                                     ▼
┌──────────────────────────────────────────────────────────────────────┐
│ STEP 10 ─► QA PASS (no skill, just checklists)
│           READS: rules/copy-iterator.md + sops/qa_checklists.md
│           OUTPUT: clients/<client>/output/07_sms_copy_improved.md
└──────────────────────────────────────────────────────────────────────┘

╔════════════════════════════════════════════════════════════════════╗
║              LATERAL — fires anywhere in phases 1–3                ║
╚════════════════════════════════════════════════════════════════════╝
  .claude/skills/call-corpus-search/SKILL.md
  ├── tools/search_chunks_by_text.py        ← verbatim quotes
  ├── tools/search_chunks_by_summary.py     ← theme matches
  ├── tools/search_chunks_by_label.py       ← bucket (pain/objection/etc)
  ├── tools/search_chunks_by_pain_point.py  ← KG hop on parent pain
  └── tools/search_chunks_by_angle.py       ← KG hop on parent angle

  Cross-client by default. Used heavily in Phase 0.5; phases 1–5 only
  hit it if they discover a NEW probe that the brainstorm missed.
```

Everything the AI reads at a given step is listed inside the skill file's `<rules>` block. The graph above is the short version — the long version is [GTM_SYSTEM_FLOW.md](GTM_SYSTEM_FLOW.md).

---

## Two corpus-integration tiers (READ THIS)

The Supabase call corpus is the knowledge graph. It's wired into skills at two levels of mandate:

| Tier | Skills | Behaviour |
|---|---|---|
| **Mandatory corpus pass before web search** | `00_client_brainstorm.md`, `Pre-Research & Case Study Extraction.md`, DRP Skill 01 (Context) | Must run cross-client corpus queries before any web call. Web is a supplement. Every claim tagged `[CORPUS …]` / `[TRANSCRIPT]` / `[WEB …]`. |
| **Optional corpus supplement** | DRP 02–05, Market Deep-Dive, GTM Hypothesis, GTM Sheet, SMS, GTM Sheet Compiler | Brainstorm is primary input. Hit corpus directly only if you discover a new probe mid-task. |

The full protocol (which CLI to pick for which question, how to cite, when to scope to one client) lives in [skills/_corpus_first_protocol.md](skills/_corpus_first_protocol.md).

---

## Step-by-step — what each step actually does

### Phase 0 — Ingest (one-time per client)

Fetch transcripts, categorise, push to Supabase, chunk, embed. See [GTM_SYSTEM_FLOW.md](GTM_SYSTEM_FLOW.md) Phase 0 for exact commands.

### Phase 0.5 — Brainstorm (NEW)

**Skill 0 — Client Brainstorm** — [skills/00_client_brainstorm.md](skills/00_client_brainstorm.md)
- Reads `clients/<client>/*` + every other client's `output/*.md` + memory.
- Runs ≥6 cross-client corpus searches.
- Writes `clients/<client>/output/00_brainstorm.md`.
- This file becomes the **primary input for every Phase 1–3 skill.**

### Phase 1 — Deep Research (the 5 chained skills)

Each is a self-contained prompt. You run them **in order**. Each one takes the brainstorm + the previous step's output.

**Step 1 — Context & Data Sources** — [skills/ICP-skills-deepsearch-engine/01_context_and_data_source.md](skills/ICP-skills-deepsearch-engine/01_context_and_data_source.md)
- Maps the client's business, TAM, ICP, persona, and the exact Reddit subs / LinkedIn groups / G2 sections / Slack communities where the persona actually talks.
- Mandatory corpus pass before web.

**Step 2 — Pain Points & Consequences** — [skills/ICP-skills-deepsearch-engine/02_pain_points_and_consequences.md](skills/ICP-skills-deepsearch-engine/02_pain_points_and_consequences.md)
- Pulls verbatim pain quotes (from corpus + web), ranks 1–10, cascades consequences at 30/90/365 days.

**Step 3 — Dream Outcomes & Whys** — [skills/ICP-skills-deepsearch-engine/03_outcomes_and_whys.md](skills/ICP-skills-deepsearch-engine/03_outcomes_and_whys.md)
- For each pain, finds the outcome the persona actually wants in their words, then runs 5 Whys.

**Step 4 — Current Solutions & Blockers** — [skills/ICP-skills-deepsearch-engine/04_current_solutions.md](skills/ICP-skills-deepsearch-engine/04_current_solutions.md)
- What the ICP is currently doing, what they've tried and failed, what's blocking them, what's pressuring them now.

**Step 5 — Objections & Triggers** — [skills/ICP-skills-deepsearch-engine/05_objections_and_triggers.md](skills/ICP-skills-deepsearch-engine/05_objections_and_triggers.md)
- Predicts objections + surfaces trigger events (funding, hiring, tech changes) that make this quarter the right moment.

### Phase 2 — Strategy + GTM Sheet

**Step 6 — Market Deep-Dive & Variable Balancing** — [skills/ICP-skills/Market Deep-Dive & Variable Balancing.md](skills/ICP-skills/Market%20Deep-Dive%20%26%20Variable%20Balancing.md)
- Pressure-tests the research against current market realities to find high-urgency markets.

**Step 7 — GTM Hypothesis Generation** — [skills/ICP-skills/GTM Hypothesis Generation & Trigger Mapping.md](skills/ICP-skills/GTM%20Hypothesis%20Generation%20%26%20Trigger%20Mapping.md)
- Produces 3+ campaign hypotheses (MDX format).

**Step 8 — Compile the GTM Sheet** — [skills/ICP-skills-deepsearch-engine/gtm-sheet-compiler.md](skills/ICP-skills-deepsearch-engine/gtm-sheet-compiler.md)
- **No new research.** Synthesises Phase 0.5 + Phase 1 + Phase 2 plus onboarding form and case studies into 3–5 scalable segments the data team runs in Apollo/Clay.
- Reads:
  - All prior outputs
  - Onboarding form + case studies CSV
  - [sops/gtm_data_sheet_sop.md](sops/gtm_data_sheet_sop.md)
  - [sops/unique_mechanism_sop.md](sops/unique_mechanism_sop.md)

> **Alternative shorter path** — [skills/ICP-skills/](skills/ICP-skills/) also contains an older 4-step compilation (`Pre-Research & Case Study Extraction` → `Market Deep-Dive` → `GTM Hypothesis Generation` → `GTM-sheet`). Use it when the client is simple or research budget is tight. The 5-skill deepsearch engine is the default.

### Phase 3 — Copywriting

**Step 9 — Write the SMS** — [skills/copies/sms-skills.md](skills/copies/sms-skills.md)
- Writes SMS copy that sounds like one business owner texting another (Pain + Mechanism + Outcome).
- Reads: brainstorm, GTM sheet, all 5 DRP outputs, plus:
  - [sops/sms_guidelines.md](sops/sms_guidelines.md)
  - [sops/unique_mechanism_sop.md](sops/unique_mechanism_sop.md)
  - [frameworks/sms_frameworks.md](frameworks/sms_frameworks.md)
  - [winning-sms/](winning-sms/)
  - [rules/copy_and_prompt_guidelines.md](rules/copy_and_prompt_guidelines.md)
  - [rules/anti_patterns_and_mistakes.md](rules/anti_patterns_and_mistakes.md)
  - [skills/sandler-sales-rules.md](skills/sandler-sales-rules.md) + [skills/sandler-49-rules-quickref.md](skills/sandler-49-rules-quickref.md)

For cold email, the parallel template library is [frameworks/email_templates.md](frameworks/email_templates.md) and the value-prop formulas are [frameworks/value_prop_frameworks.md](frameworks/value_prop_frameworks.md).

**Step 10 — QA / iterate**
- [rules/copy-iterator.md](rules/copy-iterator.md) — the quick "does this sound human?" pass.
- [sops/qa_checklists.md](sops/qa_checklists.md) — the pre-ship checklist (relevance, lingo, flow, CTA, unique mechanism visible, pattern interrupt present).
- Enforced by: [rules/anti_patterns_and_mistakes.md](rules/anti_patterns_and_mistakes.md)

---

## The rules files — read these first, always

Every skill reads the `rules/` folder before producing anything. If you are tweaking a skill or writing copy by hand, start here:

- [rules/core_principles.md](rules/core_principles.md) — the 5 ICP principles + market research principles. The *why* behind the whole pipeline.
- [rules/copy_and_prompt_guidelines.md](rules/copy_and_prompt_guidelines.md) — the 80/20 prompting template + pyramid of persuasion.
- [rules/anti_patterns_and_mistakes.md](rules/anti_patterns_and_mistakes.md) — the "never do this" list.
- [rules/copy-iterator.md](rules/copy-iterator.md) — the human-voice QA checklist.

---

## How a new client moves through the repo

```
clients/<new-client>/
  ├── onboardingform.txt             ← raw input
  ├── transcripts/                   ← raw input (sales calls — also pushed to Supabase in Phase 0)
  ├── excel/                         ← raw input (case studies)
  └── output/
      ├── 00_brainstorm.md                ← Skill 0 (NEW — runs first)
      ├── 01_context_and_data_source.md   ← DRP Step 1
      ├── 02_pain_points_and_consequences.md
      ├── 03_outcomes_and_whys.md
      ├── 04_current_solutions.md
      ├── 05_objections_and_triggers.md
      ├── 01_gtm_strategy.md              ← GTM sheet compiler
      ├── 06_sms_copy_drafts.md
      └── 07_sms_copy_improved.md         ← FINAL after QA
```

When a new client lands:
1. Create `clients/<new-client>/` with onboarding form, transcripts, case studies (any format).
2. **Phase 0** — push their calls into Supabase (run the ingest pipeline in [tools/](tools/) + [sheet/](sheet/)).
3. **Phase 0.5** — run [skills/00_client_brainstorm.md](skills/00_client_brainstorm.md) to produce `00_brainstorm.md`.
4. **Phase 1** — run DRP Steps 1 → 5 in order.
5. **Phase 2** — run Strategy steps + GTM Sheet compiler.
6. **Phase 3** — write copy (Step 9) → QA (Step 10) → ship.

---

## One-liner cheat sheet

| I want to… | Open this file |
|---|---|
| See the whole system as a graph | [GTM_SYSTEM_FLOW.md](GTM_SYSTEM_FLOW.md) |
| Understand the whole philosophy | [rules/core_principles.md](rules/core_principles.md) |
| Push a client's calls into the corpus | [sheet/fetch_all.py](sheet/fetch_all.py) → [sheet/upload_supabase.py](sheet/upload_supabase.py) → [tools/chunk_calls.py](tools/chunk_calls.py) → [tools/embed_chunks.py](tools/embed_chunks.py) |
| Brainstorm a new client (ALWAYS RUN FIRST) | [skills/00_client_brainstorm.md](skills/00_client_brainstorm.md) |
| Search the corpus by hand | [skills/_corpus_first_protocol.md](skills/_corpus_first_protocol.md) |
| Kick off deep research | [skills/ICP-skills-deepsearch-engine/01_context_and_data_source.md](skills/ICP-skills-deepsearch-engine/01_context_and_data_source.md) |
| Compile a finished GTM segment sheet | [skills/ICP-skills-deepsearch-engine/gtm-sheet-compiler.md](skills/ICP-skills-deepsearch-engine/gtm-sheet-compiler.md) |
| Write SMS | [skills/copies/sms-skills.md](skills/copies/sms-skills.md) |
| Write cold email | [frameworks/email_templates.md](frameworks/email_templates.md) + [frameworks/value_prop_frameworks.md](frameworks/value_prop_frameworks.md) |
| QA copy before shipping | [sops/qa_checklists.md](sops/qa_checklists.md) + [rules/copy-iterator.md](rules/copy-iterator.md) |
| Build a unique mechanism | [sops/unique_mechanism_sop.md](sops/unique_mechanism_sop.md) |
| Pressure-test copy against Sandler | [skills/sandler-sales-rules.md](skills/sandler-sales-rules.md) |
