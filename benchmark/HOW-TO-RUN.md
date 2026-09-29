# How to run the benchmark

Runs the 16 phase-1 cases (from `BENCHMARK-CASES.md`) through THIS playbook (so the SMS skills
auto-load) against live Evergreen, capturing the full path of each run.

## Boundary (why it runs here)
- **Evergreen = data/insight provider** (live API, read-only for the run).
- **This playbook = the writer/reasoner** — the SMS recipe, voice, mechanism logic, QA.
The benchmark tests the two together: playbook writes, Evergreen feeds. It never grades Evergreen
on copy quality.

## One-time
- Set `EVERGREEN_API_KEY` in this repo's `.env` (the copywriter key). The run prompt uses it.

## Run one case
1. Generate the prompt:
   ```
   python benchmark/make_prompt.py CP-02
   ```
2. Open a **fresh Claude session in this repo** (so the skills auto-load) and paste it as the
   first message.
3. Claude executes the case through the real pipeline and returns a JSON block — the output,
   the **full trace** (every skill fired + every Evergreen call, in order), `pipeline_fired`,
   and `notes`.
4. Save that JSON to `benchmark/results/CP-02.json`.

Repeat for each case (or `python benchmark/make_prompt.py --all` to pre-generate all 16 prompts
into `benchmark/prompts/`).

## Score
```
python benchmark/score.py
```
Prints the scorecard (PIPELINE-FIRED void count, MECHANISM _/7, COPY _/9), each case's score, and
the phase-2 backlog column. MCQ + the two string CONTAINS cases score automatically; JUDGE and
semantic cases show `needs_human` — Aaman grades those against each case's PASS rule (he is ground
truth on mechanism/copy).

## Read the trace, not just the score
A case that passes for the wrong reason is worse than one that fails. For every failure, walk the
trace back to the earliest stage that made it inevitable — that line is the phase-2 test case.

## Voids are the routing finding
If `pipeline_fired` is "no" (a required skill never ran), the case is **void, not failed**. A high
void count means the fix is routing (skills not firing), not copy. This is the exact 2026-09-25 YS
Digital lesson: the prompt must actually invoke the skills.
