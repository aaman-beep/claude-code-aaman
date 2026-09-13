# Winners DB — the tagged source of truth

> Every verified winning cold-SMS, tagged. This is the **data backbone**: the pattern library, the
> levers, and sms-draft's scaffolds are all derived from this file. When you add a winner here, the
> whole system gets smarter.
>
> **Winner benchmark:** a "winner" = roughly **≤ 250 sends per positive reply**.
> Performance IS tracked now — **Evergreen** carries every copy's real results (sent, positives, booked,
> positive_rate) via `POST /api/search {"type":"copies"}` and `/variant-performance`. Winners are
> metric-defined there, not reputation-defined. This local file is the original tagged seed; when you
> add a winner, also save it to Evergreen (`POST /api/agents/save-copy`) so the whole system compounds.

---

## How to add a new winner (step-by-step)

You fill the **judgment fields** (the stuff only you know). I fill/verify the **derived fields**
(pattern mechanics + char counts) and flag anything that doesn't fit an existing pattern.

1. **Copy the template block** below.
2. **Paste the raw text** — Text 1 (+ Text 2 if used), verbatim.
3. **Fill the 4 judgment fields:** `offer`, `niche`, `sophistication`, `why_it_worked`.
4. **Pick from the menus** (or leave blank and I'll propose): `lever`, `pattern`, `what_carries`.
5. Hand it to me. I verify the pattern tags, compute char counts, and **flag if it doesn't fit an
   existing pattern — that's the signal to add/adjust a pattern** (this is how the library grows from
   real evidence, not guesses).

### Blank template (copy this per winner)

```
### W## — [short handle, e.g. "Pirawna / Cymbiotika"]
- raw_T1:           "..."
- raw_T2:           "..."            (or "single text")
— JUDGMENT (you fill) —
- offer:            [what we sold, e.g. "Meta ads creative", "SEO/organic", "PR", "SMS outbound"]
- niche:            [who we sent to, e.g. "DTC supplements", "roofing contractors", "SaaS $10M+"]
- sophistication:   [low | mid | high]   (how many similar pitches this buyer has already heard)
- why_it_worked:    [one line — your read on why this landed]
— DERIVED (I fill/verify) —
- lever:            [FOMO | Unique | Curious | Timely | Helpful]
- pattern:          [Contrarian | Belief-break | High-level abstraction | Plain-English | Trigger | Competitor-redirect | (offer-frame = no mechanism pattern)]
- without_X_wrapper:[yes/no — is a "…without [assumed thing]" clause used]
- what_carries:     [mechanism | result | relevance | offer-frame]
- mechanism_line:   "..."            (verbatim, or "omitted")
- connector:        ["using" | "mostly by" | "by" | "mainly by … without" | n/a]
- pattern_interrupt:"..."            (or "skipped — high relevance/credibility lead")
- cta:              "..."
- char_T1 / char_T2:[auto]
```

---

## Quick-reference table (all 13)

| # | Winner | Offer type | Niche | Soph. | Lever | Pattern | Carries | without-X |
|---|---|---|---|---|---|---|---|---|
| 1 | Chamber / Transparent Labs | DTC paid-creative | DTC supplements | mid–high | Unique | Contrarian | mechanism | no |
| 2 | Firecracker / Shield AI | PR / authority | B2B tech/AI (PR) | high | Curious (Helpful posture) | High-level abstraction | mechanism | no |
| 3 | Target Market / Restorify | Timing lead-gen | Local commercial restoration | low | Timely | Trigger | mechanism | no |
| 4 | Leadgenix / Vital Psych | Local SEO | Healthcare/local | low–mid | Helpful | Plain-English | result | no |
| 5 | Stratedia / BP Builders | SEO + expansion | Trade/roofing | low | Helpful | Plain-English | result+relevance | no |
| 6 | Scaletopia / Velox (AgencyVista) | Agency lead-gen | Marketing agencies | high | FOMO (scarcity) | offer-frame | offer-frame | no |
| 7 | Tiger Tracks / Lightyear | Paid-ads optimization | SaaS/AI $10M+ | high | Curious | Belief-break | mechanism | **yes** |
| 8 | Velox / GunBroker | SEO/organic | Restricted ecom | mid | Helpful | Plain-English | result | implied |
| 9 | Velox / Dr Axe | SEO/organic | Health/supplements ecom | mid | Curious | Plain-English + wrapper | result | **yes** |
| 10 | Exchange / Lester Greene | Local SEO | Insurance/prof. services | low | Helpful | Plain-English + wrapper | result | **yes** |
| 11 | Pirawna / Cymbiotika | Amazon ads | DTC/Amazon ecom | mid | Curious | Competitor-redirect | mechanism | no |
| 12 | DMA / Kendall Animal | Guarantee lead-gen | Vet/local healthcare | low | Helpful | offer-frame (risk-reversal) | offer-frame | no |
| 13 | Scaletopia / AthleanX | Outbound/lead-gen | Agencies / B2B | high | FOMO (authority) | High-level abstraction | mechanism | no |

**Pattern coverage:** Plain-English ×4 · High-level abstraction ×2 · offer-frame ×2 · Contrarian,
Belief-break, Trigger, Competitor-redirect ×1 each. **What-carries split:** result ×4, mechanism ×5,
offer-frame ×2, mixed ×2 — note SEO/organic offers (#4,5,8,9,10) almost always carry on **result**,
not a clever mechanism. That's the Big Leap lesson, sitting right in the data.

---

## Per-winner detail

### W1 — Chamber / Transparent Labs
- raw_T1: "Hi [FirstName], it's Courtney from Chamber. I know this is random but I took Transparent Labs from $2m to $26m/yr in under 2 years using humor to make their ads actually entertaining"
- raw_T2: "It's a bit of a weird approach😂 but I think it could work for {company} - lmk if it's worth exploring sometime next week"
- offer: Meta/paid-ads creative (DTC video) · niche: DTC supplements · sophistication: mid–high
- lever: **Unique** · pattern: **Contrarian** · without_X: no · what_carries: **mechanism**
- mechanism_line: "humor to make their ads actually entertaining" · connector: "using"
- pattern_interrupt: "I know this is random but" (+ T2 "bit of a weird approach")
- cta: "lmk if it's worth exploring sometime next week" · char_T1: ~178 · char_T2: ~118
- why_it_worked: dry supplement-ad category → "humor" is the contrarian bite; the weird-approach line disarms. *(confirm/expand)*

### W2 — Firecracker / Shield AI
- raw_T1: "Hi Kjirstin, feel free to ignore if you've got investor meetings lined up for Q1, but I helped Shield AI go from cold outreach to investors chasing them - mostly by making their CEO the go-to voice for AI defense (Forbes picked them up regularly, and they raised $200M off the back of it)."
- raw_T2: "Saw what you're doing with graphene and had a few ideas on how you could get that same kind of attention. Can we chat sometime next week? Happy to walk you through exactly how we did it. - Edward, Firecracker PR"
- offer: PR / authority-building · niche: B2B tech/AI seeking PR+funding · sophistication: high
- lever: **Curious** (Helpful posture) · pattern: **High-level abstraction** (position) · without_X: no · what_carries: **mechanism** (the position, strong case → flies high)
- mechanism_line: "making their CEO the go-to voice for AI defense" · connector: "mostly by"
- pattern_interrupt: "feel free to ignore if…"
- cta: "Can we chat sometime next week? Happy to walk you through exactly how we did it." · char_T1: ~292 · char_T2: ~210
- why_it_worked: strong case lets you skip tactics and name the *position*; permission opener + "graphene" relevance for a sophisticated buyer. *(confirm/expand)*

### W3 — Target Market / Restorify
- raw_T1: "Hi [first_name], it's April from Target Market - bit random but we run ads at the exact moment when commercial properties have water damage"
- raw_T2: "It helped Restorify add $600k in bottom line within 5 months in this way - can I show you how?"
- offer: timing-based paid lead-gen · niche: local commercial restoration · sophistication: low
- lever: **Timely** · pattern: **Trigger** · without_X: no · what_carries: **mechanism** (the timing)
- mechanism_line: "we run ads at the exact moment when commercial properties have water damage" · connector: n/a (verb-led)
- pattern_interrupt: "bit random but"
- cta: "can I show you how?" · char_T1: ~138 · char_T2: ~92
- why_it_worked: the trigger is sketchable + obviously relevant to restoration; result anchors it. *(confirm/expand)*

### W4 — Leadgenix / Vital Psych MD
- raw_T1: "Hey [Name], Taylor over at Leadgenix here. Could [Company] handle 12-15 extra patient bookings a week right now?"
- raw_T2: "Just helped Vital Psych MD in Miami do that by ranking them #1 locally for mental health treatments. They're now seeing 90 leads/month. Had a few ideas for you with [Service] - lmk if you are open to a quick chat sometime tomorrow?"
- offer: local SEO/ranking · niche: healthcare/professional services · sophistication: low–mid
- lever: **Helpful** (capacity hook) · pattern: **Plain-English** · without_X: no · what_carries: **result** (SEO → result, not a clever mechanism)
- mechanism_line: "ranking them #1 locally for mental health treatments" · connector: "by"
- pattern_interrupt: capacity question ("Could [Company] handle X right now?")
- cta: "lmk if you are open to a quick chat sometime tomorrow?" · char_T1: ~110 · char_T2: ~232
- why_it_worked: the capacity question engages differently than a statement; local proof; SEO offer leads with result. *(confirm/expand)*

### W5 — Stratedia / BP Builders
- raw_T1: "Hey {{first_name}}, Steve from Stratedia. Know this is random but if you're mostly doing residential roof replacements, I can help you break into commercial roof installations"
- raw_T2: "Did this for BP Builders in CT - helped them go from 70 to 300 roof replacements/year after I got them ranking #1 for 'roof contractor CT' for both residential and commercial. Quick call where I can share the strategy?"
- offer: SEO/ranking + market-expansion · niche: trade/roofing contractors · sophistication: low
- lever: **Helpful** (expansion path) · pattern: **Plain-English** (+ expansion frame) · without_X: no · what_carries: **result + relevance**
- mechanism_line: "ranking #1 for 'roof contractor CT' for both residential and commercial" · connector: "after I got them"
- pattern_interrupt: "Know this is random but"
- cta: "Quick call where I can share the strategy?" · char_T1: ~172 · char_T2: ~213
- why_it_worked: the residential→commercial expansion is specific + relevant; SEO result carries; plain tactic. *(confirm/expand)*

### W6 — Scaletopia / Velox (AgencyVista)
- raw_T1: "Hi {{firstname}}, found {{company}} on AgencyVista - bit of a weird situation, we helped Velox Media (inc5000 agency) sign 24 {ICP} in 6 months but they're maxed for client capacity"
- raw_T2: "Saw your work with {case study} so thought you could get similar results, interested to see how it works? - Ashley, Scaletopia"
- offer: agency lead-gen / outbound · niche: marketing agencies · sophistication: high
- lever: **FOMO** (scarcity/referral) · pattern: **offer-frame** (no mechanism pattern) · without_X: no · what_carries: **offer-frame**
- mechanism_line: omitted · connector: n/a
- pattern_interrupt: "bit of a weird situation" (+ discovery source "found you on AgencyVista")
- cta: "interested to see how it works?" · char_T1: ~178 · char_T2: ~128
- why_it_worked: scarcity/referral frame ("maxed capacity") + double relevance (found you + saw your work); no mechanism needed. *(confirm/expand)*

### W7 — Tiger Tracks / Lightyear
- raw_T1: "Hi {{first_name}}, it's Cliff over at Tiger Tracks. I used to lead digital ad strategy at Google, and just helped Lightyear add $234K in ARR in 53 days without increasing ad spend - by training target CPA models to focus on actual new customers (not just site visitors or form fills)."
- raw_T2: "Had a few ideas in mind for [company] with [product category] ads - can we chat sometime tomorrow?"
- offer: paid-ads optimization · niche: SaaS/AI $10M+ · sophistication: high
- lever: **Curious** · pattern: **Belief-break** · without_X: **yes** ("without increasing ad spend") · what_carries: **mechanism** (+ credibility lead)
- mechanism_line: "training target CPA models to focus on actual new customers (not just site visitors or form fills)" · connector: "by"
- pattern_interrupt: skipped — uses credibility lead "I used to lead digital ad strategy at Google"
- cta: "can we chat sometime tomorrow?" · char_T1: ~292 · char_T2: ~97
- why_it_worked: belief-break shows insider understanding of their hidden flaw; Google credibility replaces the interrupt; "without increasing ad spend" negates the assumed lever. *(confirm/expand)*

### W8 — Velox / GunBroker
- raw_T1: "Hi {{first_name}}, feel free to ignore if you have cracked online sales without ads but, I helped GunBroker reach #1 on Google for 7 high-intent keywords. They went from $22K to $251K/month in 6 months"
- raw_T2: "Saw {{company}} and had some ideas - can we chat sometime tomorrow? (also done this for Daniel Defense and 4 Patriots.) - Alexis, Velox"
- offer: SEO/organic · niche: restricted/regulated ecom (firearms/outdoor) · sophistication: mid
- lever: **Helpful** (permission) · pattern: **Plain-English** · without_X: implied (in the qualifier "cracked online sales without ads") · what_carries: **result** (+ social-proof stack)
- mechanism_line: "reach #1 on Google for 7 high-intent keywords" · connector: "I helped … reach"
- pattern_interrupt: "feel free to ignore if you have cracked online sales without ads but"
- cta: "can we chat sometime tomorrow?" · char_T1: ~205 · char_T2: ~133
- why_it_worked: permission opener for a skeptical regulated niche + strong $ result + recognizable proof stack (Daniel Defense, 4 Patriots); SEO offer leads with result. *(confirm/expand)*

### W9 — Velox / Dr Axe  ⭐ (the Big Leap template)
- raw_T1: "Hi Tom-Louis, it's Christy over at Velox Media - this might sound random, but hear me out. I helped Dr Axe add $113K in monthly organic revenue in 90 days - mainly by ranking them first on Google for terms like {keyword} - without spending on ads"
- raw_T2: "Can I show you how {company} can do the same?"
- offer: SEO/organic · niche: health/supplements ecom · sophistication: mid
- lever: **Curious** · pattern: **Plain-English + constraint-negation wrapper** · without_X: **yes** ("without spending on ads") · what_carries: **result** (wrapper is the bite)
- mechanism_line: "ranking them first on Google for terms like {keyword}" (plain) + "without spending on ads" · connector: "mainly by … without"
- pattern_interrupt: "this might sound random, but hear me out"
- cta: "Can I show you how {company} can do the same?" · char_T1: ~232 · char_T2: ~46
- why_it_worked: **this is exactly what Big Leap should emulate** — SEO offer where the "mechanism" *is* the result (ranking); the **"without spending on ads" wrapper is the bite**, NOT a forced unique mechanism. *(confirm/expand)*

### W10 — Exchange Media / Lester Greene Insurance
- raw_T1: "Hi {{first_name}}, not sure if you're at capacity, but I helped Lester Greene Insurance hit #1 on Google for commercial insurance in Tullahoma, TN"
- raw_T2: "Took a few months, and now they're writing around 15-20 new commercial policies every month without relying on referral networks or cold calling. I think I could do something similar for you in {{city}}. lmk if we can chat this week? - Gabby, Exchange Media"
- offer: local SEO · niche: insurance/professional services · sophistication: low
- lever: **Helpful** (capacity) · pattern: **Plain-English + constraint-negation wrapper** · without_X: **yes** ("without relying on referral networks or cold calling") · what_carries: **result**
- mechanism_line: "hit #1 on Google for commercial insurance in Tullahoma, TN" · connector: "I helped … hit"
- pattern_interrupt: "not sure if you're at capacity, but"
- cta: "lmk if we can chat this week?" · char_T1: ~140 · char_T2: ~248
- why_it_worked: capacity hook + hyper-local proof + "without referrals or cold calling" negates the two methods this buyer assumes are the only way. *(confirm/expand)*

### W11 — Pirawna / Cymbiotika
- raw_T1: "Hi [Name], it's Nate over at Pirawna. We helped Cymbiotika grow Amazon revenue from $200k to $1.5m/year in 7 months - using targeted ads to redirect competitors' traffic straight to their products"
- raw_T2: "I had a few ideas in mind for [company] - can we chat sometime tomorrow? (Happy to share our full Amazon strategy.)"
- offer: Amazon ads · niche: DTC/Amazon ecom · sophistication: mid
- lever: **Curious** · pattern: **Competitor-redirect** · without_X: no · what_carries: **mechanism** (the redirect is the bite)
- mechanism_line: "redirect competitors' traffic straight to their products" · connector: "using targeted ads to"
- pattern_interrupt: skipped — leans on result + mechanism (could add one)
- cta: "can we chat sometime tomorrow? (Happy to share our full Amazon strategy.)" · char_T1: ~190 · char_T2: ~114
- why_it_worked: competitor-redirect is a sketchable, curious mechanism + strong result + a curiosity-hook offer in parens. *(confirm/expand)*

### W12 — DMA / Kendall Animal Clinic
- raw_T1: "Hey [Name], Brianna over at DMA - not sure if you're looking for more patients right now, but wanted to see if we could partner up? I'm looking for 1-2 vet clinics in [City] to pilot our 30-day program - where we guarantee 10 new patient appointments or you don't pay"
- raw_T2: "Same system that brought Kendall Animal Clinic $591K in under 10 months - lmk if I could give you a ring this week?"
- offer: guarantee lead-gen · niche: vet/local healthcare · sophistication: low
- lever: **Helpful** · pattern: **offer-frame** (risk-reversal/pilot/guarantee) · without_X: no · what_carries: **offer-frame** (+ result)
- mechanism_line: omitted ("same system" — vague, flies on the guarantee + result) · connector: n/a
- pattern_interrupt: "not sure if you're looking for more patients right now, but"
- cta: "lmk if I could give you a ring this week?" · char_T1: ~268 · char_T2: ~112
- why_it_worked: risk-reversal guarantee removes all risk for a low-sophistication local buyer; mechanism omitted because the offer-frame carries. *(confirm/expand)*

### W13 — Scaletopia / AthleanX
- raw_T1: "Hi Joe, it's Ashley from Scaletopia - bit random but we're booking Chamber Media meetings with CMOs at brands like AthleanX (spending $10m/yr on ads) using signal-based outbound"
- raw_T2: "e.g for Acclaim communications I'd run outbound to mid-sized organizations that recently hired a CMO with no agency of record - worth exploring?"
- offer: outbound / lead-gen · niche: agencies / B2B · sophistication: high
- lever: **FOMO** (authority/name-drop) · pattern: **High-level abstraction** (named method) · without_X: no · what_carries: **mechanism** (named method) + proof stack
- mechanism_line: "signal-based outbound" · connector: "using"
- pattern_interrupt: "bit random but"
- cta: "worth exploring?" (+ the "e.g. for [company] I'd…" hyper-relevant bridge) · char_T1: ~178 · char_T2: ~146
- why_it_worked: the named-method abstraction is intriguing + AthleanX name-drop proof + Text 2 shows the signal thesis in action ("recently hired a CMO with no agency of record"). *(confirm/expand)*

---

## Notes for the pattern library (derived next)

- **SEO/organic offers (#4, 5, 8, 9, 10) carry on RESULT, not mechanism.** The "mechanism" is just
  the plain tactic ("ranking #1"); the bite comes from a **constraint-negation wrapper** ("without
  ads / referrals / cold calling") or a **capacity hook**. This is the universality fix encoded in data.
- **offer-frame winners (#6, 12)** use NO mechanism at all — scarcity/referral or guarantee carries.
- **Strong/famous-brand cases (#2, 13)** fly high with a **high-level abstraction** (position / named
  method) instead of tactics.
- **Pattern interrupts get skipped (#7, 11)** only when a credibility lead or strong mechanism replaces them.
