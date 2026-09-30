# RUN ALL (paste this into a fresh Claude session IN THIS REPO)

Paste everything below the line as your first message in a new Claude Code session opened in this
playbook repo (so the SMS skills auto-load) with `EVERGREEN_API_KEY` set in `.env`. It runs the 16
phase-1 cases (mechanism + copy), saves each as JSON, and builds the trace artifact.

If a single session gets too long, run it in two passes: "cases M-01..M-07" then "cases CP-01..CP-09".

---

You are running the phase-1 benchmark for the Scaletopia GTM system, in this playbook repo, against
live Evergreen. Do all 16 cases in `benchmark/cases.json` (7 mechanism, 9 copy). Work one case at a
time, in order.

## Boundary (do not blur)
- **Evergreen is the data/insight provider.** Get ALL data from it (client context, pains, case
  studies, call-insights, winners/losers, benchmark-copy, learnings). Base
  `https://knowledgebase-production-f52e.up.railway.app`, header `Authorization: Bearer
  $EVERGREEN_API_KEY`, index `GET /api/docs`. Scope every client search with `client=<slug>`.
- **This playbook is the writer/reasoner.** The SMS recipe, voice, mechanism logic and QA are the
  skills here. Evergreen does NOT write copy.

## For each case
1. Read the case (INPUT, GRADE TYPE, PASS RULE) from `benchmark/cases.json`.
2. **Fire the real skills** listed in the case's `required_skills` (use `campaign-director` to drive
   Evidence -> Strategy -> Mechanism -> Copy -> Benchmark -> QA). Do not shortcut to plain AI copy.
   If a skill genuinely can't run, say so in the trace rather than faking it.
3. Do the task. For MCQ, state your chosen option token explicitly.
4. Save the result to `benchmark/results/<ID>.json`, matching `benchmark/trace_schema.json` exactly:
   `case_id`, `pipeline_fired` (yes/no), `answer` (MCQ token or null), `output` (text + variants),
   `trace` (ordered list; every skill fired as `kind:"skill"` and every Evergreen call as
   `kind:"evergreen"`, with a one-line `result_summary`), and `notes`.

The trace is the point. It must show what data Evergreen returned and which skill fired, in order.
A case where the skills did not fire is `pipeline_fired: "no"` (it scores void, not failed — that is
the routing finding, not a copy failure).

## When all 16 are saved
Run:
```
python benchmark/score.py          # prints the scorecard: void count, MECHANISM _/7, COPY _/9
python benchmark/make_artifact.py  # writes benchmark/trace-artifact.html
```
Then publish `benchmark/trace-artifact.html` as an artifact (input -> path -> output for every case)
and hand back the link, plus the scorecard, plus for every 0/void the earliest stage that made it
inevitable (the phase-2 backlog).

Ground truth: on mechanism/copy JUDGE cases, Aaman's answer decides; report those as `needs_human`
with your read and the trace so he can grade them fast.
