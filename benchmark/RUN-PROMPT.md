# Benchmark run prompt (template)

This is the prompt used to run ONE benchmark case, inside this playbook repo (so the SMS skills
auto-load) against live Evergreen. Fill the `{{...}}` fields from `cases.json`, paste it as the
first message of a fresh Claude session in this repo, and save the JSON it returns to
`benchmark/results/{{CASE_ID}}.json`. Then score with `graders.py` / `score.py`.

The whole point: Claude must **report the full path** — every skill it fired and every Evergreen
call it made, in order — so we can see what actually happened, not just the final copy.

---

You are running a single benchmark case for the Scaletopia GTM system. Execute it end to end,
then report the full path. Follow this exactly.

## Roles (do not blur)
- **Evergreen is the data/insight provider.** Get ALL data from it — client context, pains,
  case studies, call insights, winners/losers, benchmarks, learnings. Do not invent data.
  Base URL `https://knowledgebase-production-f52e.up.railway.app`, header
  `Authorization: Bearer $EVERGREEN_API_KEY`. Endpoint index: `GET /api/docs`. Scope every
  client search with `client=<slug>`. Useful here: `GET /api/clients/{slug}` (context),
  `GET /api/clients/{slug}/call-insights` (whole-call terminology/angles/objections),
  `GET /api/clients/{slug}/calls?q=` (scoped call search), `POST /api/search` (winners/losers,
  pass `status` + `client`), `POST /api/benchmark-copy` (score a draft vs winners/losers),
  `GET /api/clients/{slug}/learnings`.
- **The playbook (this repo) is the writer/reasoner.** The SMS recipe, voice, mechanism logic
  and QA live in the skills here. Evergreen does NOT write copy.

## You MUST fire the real skills (they do not self-activate)
Run the actual pipeline, not plain AI copy. For this case fire, in order, at minimum:
**{{REQUIRED_SKILLS}}** (use `campaign-director` to drive Evidence -> Strategy -> Mechanism ->
Copy -> Benchmark -> QA). If a skill genuinely cannot run, say so in the trace rather than
skipping silently or faking it. An honest "did not fire" is more useful than a pretend run.

## The case
```
ID:         {{CASE_ID}}
CATEGORY:   {{CATEGORY}}
GRADE TYPE: {{GRADE_TYPE}}
INPUT:      {{INPUT}}
PASS RULE:  {{PASS_RULE}}
```
Do the task in INPUT. If GRADE TYPE is MCQ, also state your chosen option explicitly.

## Report — return ONLY this JSON (no prose outside it)
Match `benchmark/trace_schema.json`. Be truthful; the trace matters more than the score.
```json
{
  "case_id": "{{CASE_ID}}",
  "pipeline_fired": "yes | no",
  "answer": "<MCQ option token, e.g. b / omit / authority / do_not_ship; else null>",
  "output": {
    "text": "<the final thing a strategist would see>",
    "variants": [
      {"t1":"","t2":"","rung":"0-3","enrichment":"","winner_ref":"","loser_ref":"","mechanism":""}
    ]
  },
  "trace": [
    {"seq":1,"kind":"skill","name":"sms-brief","input":"...","result_summary":"..."},
    {"seq":2,"kind":"evergreen","name":"GET /api/clients/<slug>/call-insights","input":"...","result_summary":"..."}
  ],
  "notes": "<where you had to inject judgment, anything that felt missing or wrong, why the output is what it is>"
}
```

## Trace rules
- One `trace` entry PER real step, in the order it happened.
- `kind` is `skill` (a playbook skill fired) or `evergreen` (an API call).
- `result_summary` = what came back in one line (counts, verdict, the key fact used).
- `pipeline_fired` = "yes" only if every required skill above actually ran. Otherwise "no"
  (the case will be scored `void`, which is the finding — routing, not copy).
- Never fabricate a step. If Evergreen returned nothing useful, log that.
