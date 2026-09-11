# NextLeft — GTM Strategy (segments · ICP · offer)

> ⚠️ **SUPERSEDED on the vertical calls — written before the John McKusick discovery call (2026-08-13).**
> Read [`output/2026-08-13-NextLeft-ICP-segments.md`](output/2026-08-13-NextLeft-ICP-segments.md) instead for the live segments.
> What the call changed: **credit unions are OUT** (agreed live — market too small for outbound), **multi-location / PE-backed home services is IN** and is John's stated strength, and **B2B is back on** as Segment 2 on the strength of ShipCalm's 1,500%+ SQL lift (which isn't on the `/our-work/` page — it's on `/b2b-seo-agency/`).
> Still valid below: the proof-density map, the marketer-not-owner persona call, the GEO-has-no-proof finding, and the Big Leap / Wise Digital / Go Fish per-send benchmarks.

**Status: STRAWMAN — redline me.**
**Prospect:** NextLeft (nextleft.com) — B Corp SEO / content / GEO agency, San Diego + Raleigh
**Stage:** Meeting Booked. John McKusick (CEO, Founder), first touch 2026-07-17, last 2026-08-05, via *Scaletopia — Marketing Agencies (Ecom focused) | 11-500E | NA | Retargeting* [source: `POST /api/prospects/lookup`]
**Date:** 2026-08-13
**Archetype:** SEO/GEO/organic (per `GTM-RUN-PROTOCOL.md` kernel)

**Sources this is built on**
- Tier 2 — NextLeft's own case studies: `/our-work/`, `/island-federal-case-study/`, `/hfsfcu-case-study/`, `/our-work/fiskars-marketing/`, `/our-work/gilmour-marketing/`, `/our-work/monkey-sports-marketing/`, `/our-work/shipcalm-marketing/`, `/services/`
- Tier 2 — our own outbound results for SEO-offer agencies: Evergreen `GET /api/clients/{big_leap,wise_digital,go_fish}` campaigns + `/deals`
- Tier 2 — Evergreen `POST /api/search` on `offers`, `copies` (winners), `pains`
- **GAP — Tier 1:** no discovery call with NextLeft ingested. Everything about *their* economics (retainer size, close rate, capacity, which verticals they actually want) is inferred from public material. Closing source: the McKusick call transcript → `POST /api/agents/transcript`.

---

## 1. The strategy in one line

NextLeft's proof is denominated in **marketer units** (keywords, monthly traffic value), so we sell to **in-house marketing leaders who are measured in those same units** — starting with consumer brands that sell through retail *and* their own site, where NextLeft owns household names (Fiskars, Hallmark, Gilmour) and the only revenue number they have.

---

## 2. Named-proof density map

Everything NextLeft publicly claims, sorted by whether the number is in a unit a buyer *feels*.

| Vertical | Named clients | Headline proof | Buyer-native unit? |
|---|---|---|---|
| **Consumer brands (retail + DTC)** | Fiskars, Hallmark, Gilmour, Reima, MonkeySports, PaperMart | Fiskars **revenue +300%**, 77,800 kw, $108k/mo · Gilmour $137k/mo, 5× referring domains, *"greatest ROI our team has seen"* · MonkeySports 68,000 kw, $137k/mo · PaperMart 95,900 kw, $613k/mo | **YES — Fiskars is the only revenue number on the whole site** |
| **Credit unions / financial** | Island Federal, HFS FCU | Island: organic traffic **+70%**, top-1-3 keywords **500 → 1,400**, monthly visits 20k → 34k, $82,100/mo · HFS: page-1 kw **+61%**, new users to **loan pages +46.3%**, Maps views +276%, CPC −76% | Partial — "new users to loan pages" is the closest thing to pipeline |
| **B2B SaaS / tech** | Widen, Midigator | Widen **1,100%** organic traffic · Midigator **587% monthly increase in SEO leads** | YES (Midigator) — but see §3 Wave 3 |
| **3PL / fulfillment** | ShipCalm | 400 → **6,000+** monthly visitors (1500%), *"best return on our marketing dollars"* | Weak (traffic) |
| **Higher ed** | GMercyU | 85,500 kw, **$1.3M/mo** | No |
| **Moving / relocation** | United Van Lines | 3,500 kw, **$1.4M/mo** | No |
| **Nonprofit** | Helen Woodward, SD Coastkeeper | 17,300 kw, $61,600/mo | No |
| **Local services** | eLocal | 90,900 kw, $202,844 | No |
| **GEO / AI search** | *(none)* | Marketed hard — *"Win at AI search"* — **zero case studies, zero numbers** | **No proof at all** |

### The two findings that drive everything

**(a) NextLeft's proof cabinet is stocked for marketers, not owners.** Their currency is keywords and monthly traffic value. Every single client quote on the site comes from an in-house marketing person — *Senior Digital Marketing Manager* (Fiskars), *Director of E-Commerce & Digital Marketing* (MonkeySports), *Marketing Manager* (Island Federal), *Marketing Coordinator* (HFS FCU). Not one owner, not one CEO.

That is decisive. "$613,000/mo in traffic value" is fluent to a Director of Ecom who reports that metric upward, and **mute** to an owner-operator who thinks in jobs and revenue. So the Wise Digital / Growth Lab / Leadgenix playbook — owner persona, local, result in their native unit — **does not transfer here**. NextLeft doesn't have the ammo for it.

**(b) They market GEO and can't prove it.** Same position Go Fish was in [source: `gofish-geo-offer` memory]. Treat GEO as the *why-now hook*, never the offer. Our data agrees: Go Fish's GEO-led email burned ~3,400 sends for 1 booked meeting.

---

## 3. Vertical prioritization

Cross-referenced against what SEO-offer agencies actually get in our outbound (positive replies per send — never raw reply rate [source: `rank-campaigns-by-positive-per-send` memory]):

| Our comparable | Segment | Sends | Pos/send | Booked |
|---|---|---|---|---|
| Wise Digital | Accounting/CPA (SMS) | 832 | **2.04%** | 6 |
| Big Leap | Home Services (SMS) | 3,181 | 0.97% | 3 |
| Big Leap | Food & Bev DTC (SMS) | 1,222 | 0.90% | 2 |
| **Big Leap** | **B2B SaaS (SMS + email)** | **~15,000** | **0.07–0.33%** | **0** |
| Go Fish | GEO High Consideration (email) | ~3,400 | 0.06% | 1 |

### WAVE 1 — Consumer brands that sell through retail *and* their own site
**Why:** six named brands, two of them household names, and the only revenue proof they own. Our own data has a directly analogous winner (below). The persona is literally the person who gives NextLeft their testimonials.

**The mechanism to lead with** — mined from the case-study set, not invented: Fiskars, Gilmour, Hallmark, Reima and MonkeySports are all brands sitting in retail *and* running their own store. Search has to pull both channels.

This is not a guess. Big Leap's highest-intent SMS winner is this exact framing:

> *"…I helped Spoonful of Comfort add $924k additional revenue in under 12 months by capturing {{niche}} market search demand that supported both their DTC and retail/Amazon pull-through."*
> **why_it_worked:** *"The mechanism names a structural problem almost no SEO pitch acknowledges — a DTC brand sitting in retail needs search to pull through BOTH channels. That specificity is what separates it from a generic ranking claim."* [source: Evergreen `POST /api/search {type:"copies", status:"winner"}`]

NextLeft can say the same thing and back it with Fiskars instead of a mid-market brand.

### WAVE 1B — Credit unions *(small parallel test, run alongside not after)*
**Why:** two named clients, a dedicated `/credit-union-seo/` page already built, and a tight, fully-enumerable universe (~4,600 US credit unions) where everyone knows everyone — the same known-name authority dynamic that carried Wise Digital's Dark Horse CPAs copy to 2.04%.

**The signal that makes this wave worth running:** Island Federal's *starting problem* was a **Fiserv-built website that limited customization and SEO**. That's a scrapeable, verifiable, universe-wide signal — every credit union on Fiserv / Jack Henry / Symitar has the identical constraint. It's a relevance rung-2/3 hook, not a guess.

**Caveat (MED confidence):** we have zero outbound history in financial services, and credit union procurement runs through committees. Run it at low volume to learn, don't bet the launch on it.

### WAVE 2 — 3PL / ecommerce fulfillment, then higher education
3PL: one strong named client (ShipCalm) with an ROI quote, and it's adjacent to Wave 1's buyer (the brands' fulfillment partners). Higher ed: $1.3M/mo is a huge number but the sales cycle is brutal and it's a single case study. Hold both until Wave 1 has data.

### WAVE 3 — **Do not run B2B SaaS**
This is the most important "don't" in the doc, because NextLeft's site will pull us straight toward it — they have a `/b2b-seo-agency/` page, a `/services/seo/saas/` page, Widen at 1,100%, and Midigator at 587% SEO leads. It looks like their best proof.

**Big Leap ran this exact offer at this exact segment and got zero meetings off ~15,000 sends.** [source: Evergreen `GET /api/clients/big_leap` campaigns]. B2B SaaS marketing leaders are the single most agency-saturated inbox in existence. Save Widen and Midigator as *proof-stacking* namedrops inside another wave, not as a segment.

---

## 4. The targeting thesis

> We're targeting **in-house digital/ecommerce marketing leaders at consumer brands with both retail distribution and an owned store**, because they carry a revenue number they don't fully control (retail sell-through) and a channel they're personally scored on (organic), which makes them feel the pain of *search demand leaking to retailers and marketplaces instead of pulling both channels* — a problem NextLeft has a household-name proof for and almost no competing agency frames at all.

**Why the persona is the marketer and not the founder:**
1. Every NextLeft testimonial is from one — the proof is pre-tuned to their language.
2. Traffic value and keyword counts are the metrics they report upward. That's the number that makes them look good in their next QBR.
3. An owner would ask "what's this in revenue?" and NextLeft has exactly one answer (Fiskars) instead of a cabinet full.

**Pre-empt these before they're raised** [source: Evergreen `POST /api/search {type:"pains"}`]:
- *"We've worked with x number of agencies that all swear they can get us results and none of them actually do."*
- *"We know SEO is important but have lost trust in agencies due to bad experiences."*
- *"AI is destroying top-of-funnel strategies"* / *"don't even know how to see if they are ranking or getting traffic through ChatGPT, Google AI Overviews."* ← this is the GEO wedge, used as a *why-now*, not a promise.

**Lever + mechanism call (per `GTM-RUN-PROTOCOL.md` kernel):** SEO/GEO archetype defaults to Helpful/Curious with mechanism OMITTED — the case study carries it (confirmed by the Velox winners: *"SEO offer where the 'mechanism' is just the ranking"*). **Override that here for Wave 1.** Big Leap's evidence shows the retail-pull-through mechanism is what separates this from a generic ranking claim. GENERATE the mechanism for Wave 1; OMIT for Wave 1B where Island Federal + the Fiserv observation carry it.

---

## 5. GTM Data Sheet (build spec)

**Mechanism, simplified (jargon-free):** *Search demand for your category gets captured by retailers and marketplaces instead of you — we make organic pull revenue through both your store and your retail channel.*
**Core formula:** *"We took Fiskars to 300% revenue growth by capturing category search demand that pulled through both their own store and their retail channel."*

| # | Segment / Niche | Job Titles | Company Size | Notes / Exclusions | Offer / Angle | Signal 1 (why now) | Signal 2 |
|---|---|---|---|---|---|---|---|
| **1** | Consumer brands, retail + owned ecom (outdoor/garden/tools, sporting goods, kids apparel, houseware, gifting) | Director of Ecommerce · Head of Ecommerce · Sr. Digital Marketing Manager · Director of Digital Marketing · VP Marketing · Head of Growth | 50–1,000 employees | **Exclude:** marketplace-only sellers (no owned site) · pure-play DTC with no retail distribution (mechanism doesn't apply) · agencies · sub-$5M brands · enterprise with in-house SEO teams. **Do NOT pull:** CEO/Founder — the proof is in marketer units, not owner units | Fiskars 300% revenue / 77,800 keywords — capturing category search demand that pulls through both the store and retail | Product stocked at a named national retailer **and** running an owned Shopify/Magento/BigCommerce store | Site replatform or migration in last 12 mo · OR posted/lost an in-house SEO or ecom role in last 6 mo |
| **1B** | US credit unions | Marketing Manager · Marketing Director · VP of Marketing · CMO · Marketing Coordinator | $200M–$3B assets, 3–20 branches | **Exclude:** <$100M assets (no budget) · top-50 CUs (in-house teams) · single-branch. Banks = separate test, don't mix | Island Federal: top-3 rankings 500 → 1,400, organic +70%, $82,100/mo — and HFS drove **+46.3% new users to loan pages** | **Website built on Fiserv / Jack Henry / Symitar** (the exact constraint Island Federal started with) | Multi-branch with unclaimed or unoptimized Google Business Profiles · OR ranking below a peer CU for "[city] auto loan" / "[city] home loan" |
| **2** | 3PL / ecommerce fulfillment | VP Marketing · Head of Demand Gen · Director of Marketing | 50–500 employees | Hold until Wave 1 has data. Exclude freight brokers | ShipCalm 400 → 6,000+ monthly visitors | — | — |
| **3** | **B2B SaaS — DO NOT RUN** | — | — | Big Leap: ~15,000 sends, 0 meetings. Use Widen/Midigator as namedrops inside other waves only | — | — | — |

### Clay build (Wave 1)

- **Step 0 — Seed.** Storeleads / BuiltWith: Shopify + Magento + BigCommerce brands, 50–1,000 employees, US/CA.
- **Step 1 — Retail-footprint check (the qualifier).** Enrich for presence at a named national retailer (Target, Walmart, Home Depot, Dick's, REI, specialty chains) via retailer site search or brand-site "where to buy" / store-locator page. **No retail footprint = drop.** This one filter is what makes the mechanism true for the recipient.
- **Step 2 — Organic baseline.** Pull current keyword count + estimated traffic value so the copy can carry a real, specific number about *them*, not a generic claim.
- **Step 3 — Category head term.** Identify the head term for their category and who currently outranks them — if it's a retailer or Amazon rather than a brand, that IS the pitch, stated back to them.
- **Step 4 — Trigger.** Replatform/migration detection + job-post scan for in-house SEO/ecom roles (posted = they're investing; recently removed = they gave up on hiring).
- **Step 5 — Contact.** Title-match to the Step-1 list above; exclude founder/CEO seniority.

### Clay build (Wave 1B)

- **Step 0 — Seed.** NCUA public credit union list, filter to $200M–$3B in assets. Fully enumerable — no discovery needed.
- **Step 1 — Platform detect.** BuiltWith / HTML fingerprint for Fiserv, Jack Henry, Symitar, Alkami. **This is the qualifier and the relevance hook in one.**
- **Step 2 — GBP audit.** Count branches vs. claimed/optimized Google Business Profiles. The gap is the observation.
- **Step 3 — Loan-term rank check.** "[city] auto loan", "[city] home equity" — who outranks them locally.
- **Step 4 — Contact.** Marketing titles; CUs are small so seniority ranges from Coordinator to CMO — pull the whole marketing department.

---

## 6. Hard dependencies / caveats

1. **No Tier 1 call.** Everything about NextLeft's own economics is inferred from public material. The McKusick call must be ingested before we write a line of copy.
2. **We don't know which verticals NextLeft actually wants.** They may be actively trying to *exit* credit unions, or higher ed may be their most profitable book. Ask before committing the waves.
3. **The Fiskars revenue number is a client quote, not a NextLeft claim** — "Revenue increased by 300%" is from the Senior Digital Marketing Manager at Fiskars Brands. Confirm we're cleared to use it in cold outreach and that the relationship is current.
4. **Case-study currency.** ShipCalm's numbers are dated 2019–2020. Verify which engagements are still live before namedropping.
5. **GEO has zero proof.** If NextLeft wants a GEO-led offer, it needs the Go Fish treatment — namedrops (name-only), FOMO, and a free scorecard as the value-give, because there are no stats to lead with [source: `gofish-geo-offer` memory].
6. **Channel.** Every comparable in §3 is SMS-led; email underperformed for all three SEO agencies. But the Wave 1 persona is a corporate marketing director, not an owner with a cell phone on the website — **mobile-number coverage on this ICP is an open risk** and needs a data-team feasibility check before we commit to SMS.

---

## 7. Open decisions for you

1. **Wave 1 = consumer brands, or lead with credit unions instead?** I've argued consumer brands (bigger universe, household-name proof, only revenue number, matches our Big Leap evidence) with credit unions as a small parallel test. Credit unions are the sharper *niche* play if you want tighter positioning over volume.
2. **Confirm the persona call** — marketing leader, not founder/CEO. This is the biggest departure from how we run Wise Digital / Growth Lab / Leadgenix, and it's driven entirely by NextLeft having no owner-unit proof.
3. **Do we run the retail-pull-through mechanism, or omit and let Fiskars carry it?** I'm recommending GENERATE against the archetype default, on Big Leap's evidence.
4. **SMS or email for Wave 1?** Depends on #6 above — needs a mobile-coverage check on corporate marketing titles.
5. **Confirm B2B SaaS stays off the table** despite it looking like their strongest proof.

**Next once you confirm:** ingest the McKusick call → `sms-brief` (Layer A on the chosen wave) → `case-study-developer` (Fiskars: frame 300% revenue vs. 77,800 keywords; mechanism variants on retail pull-through) → `sms-draft`.
