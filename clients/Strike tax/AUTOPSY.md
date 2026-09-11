# Strike Tax — Red Zone Autopsy (STRAWMAN — redline me)

**Date:** 2026-07-17 · **Client:** Strike Tax Advisory (buyer: Jonathan Cardella, Ventive LLC) · **Status:** terminated ~2026-07-07
**Question:** (1) what actually went wrong, ranked by contribution to churn; (2) where were the earlier warning signs we could have caught.
**Scope note:** findings + detection read only. No prevention checklist and no protocol edits in this pass — you wanted to see the autopsy first. Numbers are from the on-disk send logs (SMS to 2026-07-13, email to 2026-07-13), your funnel dashboard, and one live GHL conversation pull. Anything I couldn't verify is labelled.

---

## TL;DR (the one-paragraph verdict)
Strike was **not a healthy account we broke by scaling — it was a chronically under-optimized engine carried by one good quarter (Jan–Apr), and the upsell removed the mask.** The same four diseases were already present in the $3,500 era (see §1i): 68% of pre-upsell SMS volume was burner copy, the templates were frozen every month except one, email reply rate decayed monotonically to 0.18%, and the first three months closed zero. We then **upsold to $8,200/mo for 15–20 appointments as it was still sliding** — no closed-won since April, and our own [COPY-AUDIT.md](COPY-AUDIT.md) (June 30) had just flagged the copy as frozen and leaking credibility. We then **scaled the wrong things**: SMS volume ramped (June 17k prospects vs ~14k promised) but **56% of all SMS ran on burner copy** (opt-outs ≥ replies) and the scale-up months ran just **3 frozen templates**; meanwhile **email — the channel that converted positives at 89% — never scaled at all** (June 8.9k vs ~20k promised, flat-to-down the whole engagement). Cost per booked meeting **tripled** ($622 → $2,050) and cost per win went to **infinite** in the exact window the client paid 2.3× more. The warning signs were on the table months early (the April CSAT literally asked us to *"confirm feedback implemented"*; the two lowest CSAT scores were Volume and Strategy — the exact axes that blew up) and we sold *more* instead of *fixing*. **Root cause: we scaled a known-broken engine and raised the client's expectations at the same time.**

---

## 1. Reconciled data pack

### 1a. The funnel is trustworthy (three sources agree)
| Source | Meetings | Shows | Wins |
|---|---|---|---|
| Your sales dashboard | 53 booked | 31 | 6 |
| Jon's termination email | "50 meetings" | 31 | 6 |
| Campaign snapshot (Evergreen-style) | 52 | — | — |

Agreement within **3 meetings**; **shows (31) match exactly**. Treat the funnel as sound. Full funnel: 53 booked → 31 shows (58%) → 15 next-stage → 11 proposals → **6 won (11.3% close)**.

### 1b. The trend — it declined, then we scaled it
| Month | Booked | Shows | Wins | Price era |
|---|---|---|---|---|
| Oct 25 | 8 | 5 | 0 | $3,500 |
| Nov 25 | 3 | 2 | 0 | $3,500 |
| Dec 25 | 4 | 2 | 0 | $3,500 |
| **Jan 26** | **11** | 6 | **2** | $3,500 |
| Feb 26 | 4 | 3 | **2** | $3,500 |
| Mar 26 | 2 | 2 | **1** | $3,500 |
| Apr 26 | 8 | 4 | **1** | $3,500 |
| May 26 | 5 | 3 | 0 | $3,500 |
| **Jun 26** | 5 | 4 | 0 | **$8,200 upsell** |
| **Jul 26** | 3 | 0 | 0 | **$8,200 upsell** |

**All 6 wins landed Jan–Apr. Zero wins in May, June, July.** The upsell month (June) and the month after produced 5 and 3 meetings — *below* the pre-upsell average — and no closes.

### 1c. ROI by era (⚠ price/dates are placeholders — you confirm)
| | Era A (Oct–May, $3,500) | Era B (Jun–Jul, $8,200 upsell) |
|---|---|---|
| Est. spend | ~$28,000 (8 mo) | ~$16,400 (2 mo) + any upfront |
| Booked / Shows / Wins | 45 / 27 / 6 | 8 / 4 / **0** |
| **Cost per booked** | **$622** | **$2,050** (3.3×) |
| **Cost per win** | **$4,667** | **∞ (0 wins)** |

Est. total ~$44k to Scaletopia for 6 wins (your stated LTV $30–40k — roughly consistent). *We don't have Strike's revenue-per-win (MRR never entered), so this is cost-to-outcome on our fee, not the client's ROI — but Jon computed his own ROI as negative and the direction is unambiguous.*

### 1d. Channel volume: promise vs delivery (the ramp)
| Channel | Promised/mo (your ramp plan) | Actual June | Verdict |
|---|---|---|---|
| SMS | ~14,000 | 17,030 prospects | **Delivered (117%)** |
| Email | ~20,000 | **8,903** | **Missed (45%)** — flat/down vs the 9–11k it ran all engagement |

Email monthly sent never moved off ~9–11k the entire year and *dropped* during the ramp (Apr 9.0k, May 9.5k, Jun 8.9k, Jul 2.3k). **Jon's #1 termination line — "email sends are the same as before the increase" — is literally true in the data.** Email reply rate also *declined* over time (0.5–0.6% early → 0.18% in May).

### 1e. SMS quality — we scaled burner copy
- **56% of all SMS volume (47,915 of 86,166 prospects) ran on "burner" batches** where opt-outs ≥ replies.
- Template variety **cratered at scale-up**: March ran 22 distinct structural templates; **April–July ran 3 each** while volume peaked. May = 10,950 prospects on 3 templates, **98% of it burner**.
- The single workhorse template (40,782 prospects — *"Erika…your dev team's salaries…likely qualify…SecureCircle $668k"*) was itself a **net-burner** (1.20% reply / 1.15% opt-out). The best-performing openers (up to 1.57% reply / **0.22% opt-out**) got a fraction of the volume.

### 1f. Lever & proof concentration (confirms COPY-AUDIT, quantified)
- Only **4 of 13 levers** carried real volume: likely-qualify (56%), retroactive/back-years (75%), deadline-FOMO (52%), success-fee (49%). Levers 5/6/8/11 = **0%**.
- The **"already claimed?" branch** the audit called the unlock ran on **2% of SMS volume**.
- **CrowdStrike / SecureCircle = 46% of all SMS volume.** Jon explicitly asked to diversify names; it didn't happen.

### 1g. Targeting drift (vertical mix + ICP size)
| Vertical | SMS volume share | SMS reply% | SMS opt% | Where wins came from |
|---|---|---|---|---|
| **SaaS/Software** | **46%** | 1.22% | 1.19% (≈burner) | few |
| Unknown/untagged | 26% | 0.82% (worst) | 1.02% | — |
| **Machinery/Mfg** | 22% | **1.39% (best)** | **0.84% (best)** | **most wins (industrial)** |

We put **the most SMS volume into SaaS (worst engagement) and less than half of that into Machinery (best engagement, and where the actual wins were** — Professional Coating, Faytech, Blackrock Automation, Uplink Robotics, Omega ATC). Email shows the same tilt (SaaS 40%, Cyber 20% at 0.12% reply — near-zero return). **A live GHL pull corroborates ICP violations at the contact level**: of 25 recent "prospect-replied-last" SMS threads, ~40% were **wrong-number / not-the-person / "remove me,"** and the list contained **enterprise names far outside the ≤$31M ICP** (Akamai, Essity/Playtex, FactSet). The list was not hard-filtered to the ICP the [GTM-STRATEGY.md](GTM-STRATEGY.md) specified, and phone-data quality was poor.

### 1h. Positive-reply leakage
Email **27 positive → 24 booked (89%)** vs SMS **87 positive → 28 booked (32%)** — ~59 SMS positives never became meetings. Cause is **mixed**, not one thing: SMS "positive" is a looser signal (lower intent) **and** there's a large unworked inbox (2,009 prospect-spoke-last threads) with at least one genuine booking attempt left hanging (Nova-Tech, *"9am works better"* — prospect spoke last, unread). Magnitude is solid; exact cause split needs the conversation review.

### 1i. The $3,500 era was not clean — it was masked
The pre-upsell period looked fine only because a Jan–Apr win cluster hid a chronically under-optimized engine. Auditing Oct–May on its own:
| Symptom | $3,500 era (Oct–May) | $8,200 era (Jun–Jul) |
|---|---|---|
| SMS volume on **burner** copy | **68%** | 31% |
| Months running frozen (≤3) templates | 5 of 8 (only March tested, then abandoned) | both |
| Email reply rate | **decayed 0.57% → 0.18%** every month | — |
| Win output | **Oct–Dec = 15 booked, 0 wins**; 6 of 8 months had 0–1 win | 0 |
| Booking trend | **Jan 11 → Feb 4 → Mar 2** (collapsing) | 5 → 3 |
| Client sentiment | **April CSAT: Volume 6, Strategy 6, confidence-to-replace 5** — lukewarm *before* we proposed scaling | — |

**Read:** burner copy, frozen templates, decaying email and off-ICP targeting were all present from month one — the upsell didn't create them, it amplified them. The deeper failure isn't the June decision; it's that **we never audited a mediocre-and-declining account at any of the obvious trigger points** (the Oct–Dec 0-win drought, the March booking collapse, the April CSAT). We ran it on autopilot until it churned.

---

## 2. Findings, ranked by contribution to churn
Each = claim · evidence · confidence.

**① We upsold into a declining account and scaled a known-broken engine. [HIGH]**
The June upsell to $8,200 for 15–20 appts came *after* wins had already stopped (none since April) and *after* our own COPY-AUDIT flagged frozen/leaking copy. We raised the price and the promise without first fixing copy, data, or email infra. Result: cost/meeting tripled, zero wins in the paid-more window. This is the meta-error that made everything below fatal instead of merely mediocre.

**② Email — the high-intent channel — never scaled; it dropped. [HIGH, hard data]**
Promised ~20k/mo, delivered 8.9k in June and 2.3k in July, flat-to-down all year. Email converted positives at **89%** yet got no ramp and declining reply rates. This is the single most defensible, client-verifiable failure and his stated #1 reason.

**③ SMS scaled onto burner copy. [HIGH]**
56% of SMS volume ran opt-out ≥ reply; scale-up months ran 3 frozen templates at 77–98% burner volume; the 40k-prospect workhorse was a net-burner while winning openers sat unused. This is "SMS response rates too low," root-caused.

**④ Targeting drifted off ICP — vertical *and* size. [MED-HIGH]**
Most volume into the worst-engaging vertical (SaaS) and away from the one that actually won (Machinery); ~40% wrong-numbers and enterprise names in the funnel. Bad-fit list + bad phone data = wasted spend and opt-outs.

**⑤ We didn't act on our own audit. [MED-HIGH]**
COPY-AUDIT (June 30) prescribed break-the-template, add the "already claimed?" branch, fix credibility leaks, diversify proof. Post-June reality: 3 templates, branch at 2%, CrowdStrike still 46%, only 2 new (Accounting) email campaigns. **The window we were paid the most is the window we changed the least.** Directly echoes the April CSAT ask: *"confirm feedback implemented."*

**⑥ Positive-reply leakage + unworked SMS inbox. [MED]**
32% SMS positive→booked vs 89% email; ~59 SMS positives lost; real booking attempts sitting unworked. Partly intent, partly follow-up execution.

**⑦ Open deliverable + trust debt. [MED, relationship]**
Termination conditions waiving the underperformance credit on **getting "our data"** — an unmet deliverable at the exit. Trust was pre-eroded before kickoff: the contract was sent with the **wrong/un-edited version three separate times**, each caught by Jon — which is exactly why he audited us so hard at the end.

### What wasn't ours / what went right (non-bias check)
- **Service was genuinely good:** CSAT scored Response-time **9**, Proactive-comms **8**. Jon liked working with us and even referred us (Ryan Tabloff).
- **Hard motion, real wins:** R&D tax-credit cold outbound is a complex, technical sale; 6 wins in 10 months isn't nothing.
- **External headwind:** the **July 6 OBBBA deadline** was the entire FOMO spine — it expired mid-campaign, gutting July urgency.
- **Client-side conversion limits:** Jon was his **only salesperson** ("I'm our only sales guy"), had a bad sales hire quit (Eric), and gave us **few call recordings until late** — so the show→won leak and the copy's thin voice-of-customer were partly client-side, not fully ours.

---

## 3. Detection timeline — the signals we had, and the data underneath
| When | Signal we saw | What the data already showed underneath | Actioned? |
|---|---|---|---|
| **Pre-kickoff (2025)** | Contract sent wrong 3× (Jon caught each) | n/a — process sloppiness | Primed him to distrust our execution |
| **Oct 25 →** | Launch | SMS 91% burner month 1; email 0.57% reply | Not flagged as a copy/data problem |
| **Apr 1 26** | **CSAT: Volume 6, Strategy 6 (both lowest); Confidence-to-replace 5; ask = "confirm feedback implemented or push back"** | Wins already thinning (Apr last win); SMS 77% burner; email reply at 0.25% | **No — this is the biggest missed signal** |
| **Apr–May 26** | Quiet — account still "fine" | SMS frozen to 3 templates at 77–98% burner; email reply hits 0.18%; **May 0 wins** | No copy reset |
| **~Jun 26** | Jon asks for more volume → **we upsell to $8,200 / 15–20** | No win since April; COPY-AUDIT says copy is frozen/leaking; email can't hit 20k | We sold *more* instead of *fixing* |
| **Late Jun–Jul** | Jon DMs: "8 days no lead," "sends down 15%," "volume only double… not on track" | July: email collapses to 2.3k, 3 booked, **0 shows** | Acknowledged late (Khizar), not pre-empted |
| **~Jul 7** | Termination | 0 wins in the $8,200 era; email never ramped | — |

**The pattern:** every leading indicator (the April CSAT axes, the "confirm feedback" ask, the frozen-burner copy, the flat email) was visible **60–90 days before** termination. The account didn't fail suddenly — it was **audited into failure** by a client who'd been telling us, politely, since April.

---

## 4. What the data can't tell us (open items) + what I need from you
1. **Exact era dates + any upfront charged.** When did $3,500→$8,200 take effect, and was there an upfront on the upsell? (Firms up §1c.)
2. **Funnel source rows.** Are the pasted dashboard figures the source of truth, or can I get the underlying per-deal rows? (Lets me tie meetings to campaigns/verticals directly.)
3. **The late sales-call recordings** ("millions to work with"). Drop transcripts into `clients/Strike tax/source/` and the leakage + objection read gets far sharper (right now there are **zero** Tier-1 calls on file).
4. **Positive-reply cause split.** To move ⑥ from "mixed/indicative" to a quantified rate, I'd review the ~59 unconverted SMS positives' conversations (or onboard Strike to Evergreen for the categorized version).
5. **Your spot-validation** on findings ①–③ — do these match what you lived?

---

## Appendix — method & reconciliation notes
- **SMS:** `output/batches.json` (227 curated batches) + `output/sms-copy-history.csv` (12,159 rows); burner = opt-outs ≥ replies; template variety measured on structurally-normalized T1 (name/number/team-noun stripped) because per-prospect AI first-lines make raw T1 look falsely unique.
- **Email:** `output/emailbison.json` (39 campaigns); monthly from `campaign.monthly`; opens are 0 (tracking off) so reply/interested are the honest signals.
- **Funnel:** your dashboard artifact (Strike is **not** in Evergreen, so no deal-level pull was possible without onboarding).
- **Live pull:** one GHL `search-conversation` (25 recent inbound-last SMS threads) — a deliberately **non-random** slice (biased to unworked/negative), used for qualitative color only, not rates.
- **Residual discrepancy:** meeting counts 50/52/53 across sources (≤3, immaterial); SMS "sent" 92k (dashboard) vs 86k prospects (batches) vs 104k (full log) differ by counting method (texts vs unique contacts vs all rows) — noted, not smoothed.
