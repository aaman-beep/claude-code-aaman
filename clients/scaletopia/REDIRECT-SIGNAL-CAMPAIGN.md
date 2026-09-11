# Redirect-signal campaign — run sheet + strategy

**STRAWMAN — redline me.** Started 2026-08-06. Scaletopia's own outbound.
Strategy rationale in full: `~/.claude/plans/below-so-we-have-parsed-hearth.md`.

---

## The play in five lines

1. We can detect agencies that run cold email by counting domains that 301-redirect into their main domain. ~1–2k qualified.
2. The signal proves they **run** outbound, not that it **works** — and we can't tell which from the data.
3. So we don't split the list. We ask a question both scenarios can answer and let **the reply do the segmenting**.
4. One angle, anchored on *they already run cold outreach*. The test is **mechanism on vs off** against the Chamber result — with a competing candidate axis, **signal-stated vs signal-implied**, in `output/2026-08-06-redirect-signal-email-drafts.md`. Only one reads cleanly at this list size.
5. Email reads the axis cheaply. SMS books the meetings. Risk reversal lives in the follow-up, never the opener.

---

## A · Locked inputs — fill BEFORE any copy

- **Client / offer:** Scaletopia — managed cold outbound (email + SMS) for marketing agencies. Named offer: **30-day pay-on-results pilot**.
- **Segment / persona:** Founder / owner / head of growth at a **25–500** person marketing agency, typically owner-grown through direct outbound sales, that already runs its own cold email — proven by a stack of redirect domains pointing at their site.
- **Offer archetype:** `Agency/outbound`
- **Lead lever: Curious** (+ Helpful on the CTA). The diagnostic question is the open loop, and the soft "can I show you" ask is the Helpful posture. `levers.md`: high-sophistication buyers need Curious + specificity, and this is the most sophisticated audience we've ever mailed. FOMO is off — we have no rival to name and no credible scarcity now that capped-intake is out, and `levers.md` says don't manufacture either.
- **Mechanism — OMIT.** Kernel says omit for `Agency/outbound` and lead on the ICP signal. Here it's stronger than usual: **we found them with the exact method we'd run for them**, so the signal *demonstrates* the mechanism instead of claiming it. Also matches the `email-playbook` standing lesson — the granular/throughput mechanism got 0 replies on email; abstract won.
- **Case study:** Chamber Media · retainers closed from outbound — **number pending the lock below** · **capped intake is OUT**, we're not talking about it · literal mechanism: signal-based / AI-timed outbound, **which must not be said in this campaign** (see the objection finding below) · **tier A** (strawman — named brand, exact same niche, but not a household name) · native unit **Y** (retainers is how an agency owner counts wins).
- **Relevance plan:** redirect-domain count per company, from our own detector. **Rung 3** — a checkable fact about their current behaviour, the highest rung we have. Floor check passes comfortably.
- **Which bar is short** — ⚠ **margin note, don't fix the sheet mid-run.** Neither of the two standard bars is the short one here. "This is real" stands on Chamber + retainers + timeframe. "This is for me" stands on the redirect count. The actual objection from this audience is a third thing: **"we already do this ourselves — why you?"** Both arms have to answer that, and the two-bar model doesn't have a slot for it. Worth adding to `FUNDAMENTALS.md` after the run if it holds up.
- **Closest logged winners:** **W6** (FOMO via capacity reframe + Clay specificity) · **W13** (carried by ICP-signal specificity, not the named method) · **the July 13–17 winner**, which is *not in winners.csv* — see gap below.

### Gaps flagged, not papered over

| # | Gap | Why it matters |
|---|---|---|
| 1 | **We can see they send email; we cannot see whether it works, or whether they also run SMS.** | Anything about their current state stays a question, never an assertion. The diagnostic CTA does this by design — but if anyone rewrites it into a statement it becomes an overclaim and fails QA Q2. |
| 2 | **The July winner was never promoted into `winners.csv`.** | Our best-evidenced agency copy isn't in the file every skill QAs against. Should be added as W-next before drafting. |
| 3 | **Pay-on-results is unconfirmed.** Flagged ⚠ in the July InMail draft, still open. | It ships in the P.S. of both draft versions. Don't put a fourth campaign behind an unverified claim aimed at people who check. |
| 4 | **The list isn't in the repo.** | Everything downstream is blocked on it, including the `{{domainCount}}` merge var both drafts depend on. |
| 5 | **"Ian Johnson, head of sales at Chamber Media"** appears in Aaman's manual draft but in no record we hold. | Our Chamber contacts are Blake Wheeler / Stefan and Taylor Neuffer. Naming a real person at a client is checkable. Cut from both drafts pending confirmation. |

### The research layer (Evergreen, 16 discovery calls, 221 pains)

Full write-up in the plan. The four findings that bind on copy:

- **Burned-and-tried dominates.** Clusters of 10+9+7+6 — *"three email agencies… all failed pitifully"*, *"$9,000 a month… one viable lead over three months"*. The copy's centre of gravity sits there.
- ⚠ **"AI-timed" / "signal-based" is a burnt phrase with this exact audience.** *"burnt heavily with signals data"* · *"that data lives and lasts maybe two weeks"* · *"I need new blood in the system, not efficiencies"* — Richard Dresser, Go Fish. It sits in 29,294 sends of our live copy. **Do not use it here.**
- **The short bar is answered by bandwidth, not skill.** The objection is *"we already do this ourselves — why you?"* and the answer in their own words is that nobody there owns it: *"We just don't have someone to do it, frankly."* Don't argue we're better at outbound than they are.
- **The promise ceiling is low.** *"If you could get us two to three decent calls a week, that's enough."* Don't overpromise volume to people three agencies have already overpromised.

⚠ Confidence caveat: every record is `needs_more` and `client_count: 1` — Scaletopia is the only client in the "Marketing agencies" niche, so none of it is cross-client validated.

---

## The Chamber Media numbers — audit and lock

Counted across every SMS we've sent (`output/sms-copy-history.csv`). **Thirteen distinct claims.**

| Sends | Claim |
|---:|---|
| 29,294 | close **14 retainers in 5 months** with AI-timed outreach |
| 3,593 | sign **22 clients in 7 months** using ai timed outreach |
| 2,142 | close **12 retainers in 5 months** using AI-timed outbound |
| 3,901 | sign **14 retainers (74k mrr) in 5 months** with AI-timed text outreach |
| 2,681 | sign **18 retainers in 8 months** from outbound, **capped client intake** |
| 830 | book **84 meetings in 5 months** — AG1, Volcom, Feastables |
| 726 | **14 retainers closed in 6 months** |
| 466 | sign **4 clients in 2 months** via cold SMS |
| 78 | book **84 proposal calls in 5 months** — AG1, Volcom, Feastables |

**The good news:** most of the drift reconciles as a single timeline — 14 retainers by month 5 → 18 by month 8. Those two don't contradict each other.

**The hard contradictions**, which do not reconcile and must be killed:
- 12 vs 14 retainers at month 5
- 14 retainers at 5 months vs at 6 months
- "22 clients in 7 months" vs "18 retainers in 8 months" (unless clients ≠ retainers, and if so we should stop using both words)
- "84 meetings" vs "84 proposal calls" — same number, two different things
- "74k mrr" appears on only some renders of the same 14-retainer claim
- **"Since January"** in the 2026-08-06 manual draft is a *seventh* timeframe — Jan→Aug is seven months, not five

**Recommended lock: "18 retainers in 8 months from outbound."** Latest snapshot, doesn't contradict the 14-in-5 history, and it's the version attached to the week that booked 5 meetings. Capped intake is dropped per Aaman.

The current drafts use **"14 retainers (74K MRR)"** because that's what the manual draft carried — this is unresolved and one of the two has to go. Partner count also needs one number: we say 26, 32 and 84 agencies.

---

## Pre-send checklist

- [ ] Pick the test axis: **mechanism on/off** vs **signal-stated/implied** (drafts for both in `output/2026-08-06-redirect-signal-email-drafts.md`) — only one reads at ~1,500/arm
- [ ] Confirm or cut "Ian Johnson, head of sales at Chamber Media" — in no record we hold
- [ ] Confirm "AI-timed" / "signal-based" stays out of every asset in this campaign
- [ ] MX-present + name-similarity filter over the full list; hand-check 50 for SEO-redirect false positives; report survival rate
- [ ] Suppress: current/past clients · every company in `POST /api/prospects/lookup` · Chamber, Velox and parents · competitor outbound shops · sub-20 headcount
- [ ] Lock the Chamber numbers above; confirm pay-on-results and capped-intake are real
- [ ] Promote the July winner into `winners.csv`
- [ ] Kill spintax on Scaletopia sends; retire the "I know your inbox is full of agencies" opener
- [ ] Name the owner of reply handling during send hours — **this is the highest-leverage item on the page and it is a staffing decision, not a copy one**
- [ ] Route around the number-split bug before the SMS layer (`output/number-split.csv`, 151 threads affected)

---

## Standing rules for this campaign

- Every live reply answered **inside the hour, in the channel it arrived in.** July: 33 human texts → 5 meetings, all booked 12 min to 1.3 hrs after first reply.
- **Never hand a hot thread to email.** "could I drop you an email w more info?" went **0 for 11**. Banned in copy and in reply handling. If they ask for email, send it *and keep texting*.
- Risk reversal goes in T2 or the P.S. As a standalone opener it pulled 1.13% reply across 3,721 prospects.
- Pay-per-qualified-show stays a call concession, and "qualified" gets defined before it's offered.
- Read arms on **reply rate**, not bookings — at ~1,500/arm there aren't enough positives to read booking rate. SMS gives the meeting read.

---

## What I need from you

1. **The list** — detector output with the redirect counts per company. Everything is blocked on this.
2. **Is pay-on-results genuinely on the table**, and what's the pilot price floor? Marc Levesque walked at $3–4k.
3. **Who owns reply handling** during this send?
4. **Angle B framing** — comfortable telling the "replies die downstream" story as a law we measured across accounts, or keep it vaguer?
5. **How many more companies can the detector produce?** If the angle reads, the detector is the asset, not this list.
