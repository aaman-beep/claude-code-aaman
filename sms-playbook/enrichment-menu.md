# Enrichment Menu — which enrichment, which move, when

> The Clay enrichments we run across clients, turned into a decision table: for each one, **which
> relevance rung it buys** (per `relevance-engine.md`), **which lever/offer it powers**, **how to
> weave it at human altitude**, and **when NOT to use it.** This is the supply chain for relevance
> — `relevance-engine.md` says *climb as high as the data allows*; this says *what data you have
> and what it's good for.*
>
> Names vary per client (Clay calls the same thing `{{niche}}`, `SubNiche`, `subniche`…) — the
> canonical `{{slot}}` is what matters, not the label. Keep it general: the examples below span
> offers; the client's real values come from Layer A + Clay at runtime, never hardcoded.

---

## The table

| Enrichment `{{slot}}` | What it is | Rung | Powers (lever / offer) | Weave it like (human altitude) | Don't |
|---|---|---|---|---|---|
| `{{first_name}}`, `{{company}}` | name + company | core | every text | baseline merge — gives uniqueness, not relevance | rely on it *as* the relevance |
| `{{product_category}}` | their main category | 1 | any · niche floor | "the {{product_category}} brands winning organic right now" | leave so broad it fits anyone |
| `{{subniche}}` | sharper sub-category | 1 | any · sharper than category | "in {{subniche}}, the buyer searches before they buy" | use when you only know the broad niche |
| `{{niche}}` | their space (shorthand) | 1 | any | "how {{company}} could do this in {{niche}}" | use it *alone* in T2 (that's rung 0) |
| `{{main_product}}` | hero product beyond the category | 1 | DTC / ecom | "the people searching for {{main_product}} dupes" | name a product you haven't verified |
| `{{top_service}}` / `{{speciality}}` / `{{main_expertise}}` | their core service / case-type | 1 | local · services · law | "more {{main_expertise}} cases, the same way" (W14) | use a service they don't lead with |
| `{{saas_type}}` / `{{what_they_build}}` | software category / what they make | 1–2 | SaaS · R&D | "for a {{saas_type}} team, the play is…" | guess the category — verify |
| `{{ideal_segment}}` | the vertical *they* sell to | 1–2 | agency · B2B | "to land more {{ideal_segment}} accounts" | confuse it with *their own* niche |
| `{{city}}` | their location / service area | 2 | local | "do something similar for you in {{city}}" (W10) | use for a non-local offer |
| `{{directory}}` | a directory they're listed on | 2 | discovery disarmer / Helpful | "found {{company}} on {{directory}}…" (W6) | claim a directory unless it's true |
| `{{competitor_1/2/3}}` | a named rival | 2 | **FOMO** | "{{competitor_1}} is already ranking for this — you're not in it yet" | **fabricate** — Clay-given or flagged "verify before sending" only |
| `{{dream_client}}` | a real account they sell to / want | 2–3 | authority · aspiration · FOMO | "the kind of brand that lands {{dream_client}}" | name a client you can't source |
| `{{relevant_search_term}}` | what their buyer types into Google/ChatGPT | 2–3 | **Curious · SEO bridge** | the bridge engine — "the {{relevant_search_term}} searches going to retailers" | use a term they already rank #1 for |
| `{{dream_icp}}` / `{{ideal_persona}}` | who *they* target | 3 | **Timely · Helpful** | "I'd go after {{dream_icp}} for you" (W13 shape) | use as generic flattery |
| `{{ICP_signal}}` | the Clay signal that proves we know exactly who they are | 3 | **Timely · highest leverage** | "{{ICP_signal}}" — e.g. "just hired a first CMO, no agency yet" (W13) | state a scraped/nerdy metric — keep it human-altitude |
| `{{relevance}}` / `{{reason_1/2}}` | a specific true observation / why-fit | 3 | any · why-them/why-now | "saw you head up sales", "saw your work with {case}" (W6) | leave generic ("saw your company") — that's rung 0 |

---

## How to decide (read this, don't guess)

> Source real values for the slots instead of leaving "verify before sending": `{{competitor}}` /
> `{{ICP_signal}}` / `{{dream_client}}` can come from **Evergreen** — `POST /api/prospects/lookup` and
> reply-thread search (`{"type":"deals"|"contacts"}`), plus mined `pains` for the pain-grounded weaves.
> See FUNDAMENTALS → "Reaching Evergreen".

1. **Start from the offer archetype** (match the case study to the closest tagged winner(s) — pull them
   from **Evergreen** `POST /api/search {"type":"copies","status":"winner"}` + `{"type":"offers"}`; that's
   the live router, with `winners.csv` as the seed and `offer-matrix.md` on hold). The archetype suggests
   the lead lever, and the lever points at the enrichments below.
2. **Lever → enrichment shortlist:**
   - **FOMO** → `competitor_1/2/3`, `dream_client`, or their own uncaptured result (a
     `relevant_search_term` they're ceding).
   - **Curious / SEO** → `relevant_search_term` (+ the **bridge move** if the case is in a
     different world), `main_product`.
   - **Timely** → `ICP_signal` / `dream_icp` / `reason_1/2` — a real trigger only.
   - **Helpful** → `directory` (discovery opener), `city` + `top_service` (local match), or any
     value-give grounded in their `subniche`.
   - **Unique** → relevance rides on the mechanism; use the niche slots (rung 1) to ground it.
3. **Climb the ladder** (`relevance-engine.md` §1): take the highest-rung enrichment you actually
   have for this segment and build the bridge around it. Leave per-prospect vars as Clay slots.
4. **Floor check:** if the only enrichment in play is `{{niche}}`/`{{company}}` and the case isn't
   S-tier, you're at rung 0 — find one more enrichment or the variant doesn't ship
   (`relevance-engine.md` §4).

---

## The two ways every enrichment goes wrong

- **Fabrication** — naming a `{{competitor}}`, `{{dream_client}}`, or `{{relevant_search_term}}`
  you can't source. Use a slot + "verify before sending," never an invented value.
- **Nerdy altitude** — a true-but-robotic signal ("saw your traffic was 87.2k", "you have 3,412
  SKUs"). Re-say it the way a human would notice it, or drop it. Specific ≠ relevant if it reads
  scraped.
