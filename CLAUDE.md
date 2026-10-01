# Scaletopia GTM playbook — router (read first, every session)

This repo writes cold-outreach copy. The skills here are the recipe (writer/reasoner). Evergreen
is the data provider. The skills do NOT self-activate from a bare prompt, so this file is the
router that forces them to. The failure this prevents is real (2026-09-25 YS Digital, 2026-09-21
DTCo): a strategist asked for copy, the model pulled some data and wrote plain copy, and the whole
QA/benchmark/winner-referenced pipeline never ran.

## The hard rule (not optional)

If the request is to **write or draft SMS copy, make variants, run a campaign, pick a case study,
or develop a mechanism/angle** — for any client — you MUST run it through the **`campaign-director`**
skill. Do not write copy directly, ever, even for a quick one. Invoke `campaign-director` as the
first move and let it drive.

Trigger phrases that MUST route (non-exhaustive): "write cold SMS / copy for {client}", "draft the
SMS", "make variants", "turn this case study into texts", "write copy using {winners}", "develop
the mechanism", "run a campaign for {client}", "look at {X} winners and write copy".

## The mandatory pipeline (campaign-director enforces this order)

Each stage must produce a checked artifact before the next runs:

1. **Evidence** — `sms-brief` + pull Evergreen for this client: `GET /api/clients/{slug}` (context),
   and when the client has calls, `GET /api/clients/{slug}/call-insights` FIRST (terminology,
   objections, angles — before the mechanism stage, not after).
2. **Strategy** — frame (broad vs niche, decided + justified), persona, proof spine, angles. Before any copy.
3. **Mechanism** — auto-chain `case-study-developer` → `mechanism-wordsmith`. Apply the portability gate.
4. **Copy** — `sms-draft`. Size the variant count to the space (not capped at 3–7).
5. **Benchmark** — `POST /api/benchmark-copy` on EVERY draft. KEEP/REWORK/DROP/CAUTION. A draft that leans loser is reworked.
6. **QA** — `sms-draft`'s qa-checklist + voice profile. Unsupported CTA is an auto-fail.
7. **Learning** — save the structured learning back.

## Evergreen (data only — never invent data)

Base `https://knowledgebase-production-f52e.up.railway.app`, header
`Authorization: Bearer $EVERGREEN_API_KEY` (in `.env`). Endpoint index: `GET /api/docs`. Scope every
client search with `client=<slug>`. Evergreen serves evidence, benchmarks, learnings, call-insights;
it does not write copy.

## Binary self-check before you show any copy

- [ ] Did `campaign-director` run (not ad-hoc copywriting)?
- [ ] Did `sms-draft` and the QA gate actually fire?
- [ ] Was every draft benchmarked against winners/losers via `/api/benchmark-copy`?
- [ ] For a client with a call corpus, did call-insights fire before the mechanism stage?

If any box is "no", STOP and route through `campaign-director`. A bare prompt that skips this is the
routing bug, not a copy result.

(See `benchmark/` for the test suite that checks all of the above; `GTM-RUN-PROTOCOL.md` for the run sheet.)
