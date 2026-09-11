# What happens after a positive reply — 2,339 threads, all clients, all time

**Strawman. Redline it.** Built from Evergreen only, 13 clients, Oct 2025 → Aug 2026.
Data: [2026-08-26-reply-handling-audit.json](2026-08-26-reply-handling-audit.json) ·
rebuild with `python3 tools/reply_handling_audit.py`

**Population.** 2,339 threads across Power Request (1,265), More Info Request (686),
Email Me Request (388). SMS 1,963 · email 376. Three "stop texting me" complaints filtered
out of Email Me Request as you asked.

**Every booked-rate below is computed on 1,635 deal rows only** — the contacts endpoint
moves a reply into the "Meeting Booked" bucket the moment it converts, so asking it whether
speed predicts booking is asking a population with no bookings in it. Baseline for the rate
population: **37.2% booked.** 345 rows had no readable thread text and are excluded from
everything except volume.

---

## Verdicts on your four hypotheses

| | your hypothesis | verdict | the number |
|---|---|---|---|
| **H1** | reply copy is salesy / AI / uninformative | **supported — but it's a brand-new problem** | stock template: 0% of replies for 10 months, **38% in August** |
| **H2** | not enough follow-ups | **can't be tested this way** — the metric runs backwards | 0 follow-ups books at 42%, 3+ books at 14% |
| **H3** | speed, target 5 min | **half right — the cliff is 1 hour, not 5 minutes** | under 1h 43% · over 1h 28% · under 5min 46% vs 5–60min 43% |
| **H4** | coverage, "comes later" | **this is the biggest single number in the audit** | 477 positive replies never got a human answer |

---

## H3 — Speed. Your instinct is right, your target is wrong.

SMS, minutes from their reply to our first human answer:

| | n | booked | rate |
|---|---:|---:|---:|
| under 5 min | 98 | 45 | **46%** |
| 5–10 min | 214 | 97 | 45% |
| 10–30 min | 398 | 168 | 42% |
| 30–60 min | 165 | 68 | 41% |
| 1–4 h | 141 | 35 | **25%** |
| 4–24 h | 123 | 40 | 33% |
| over 24 h | 104 | 27 | 26% |

Collapse it and the shape is unmistakable: **under an hour books at 43%, over an hour at
28%.** That's a 15-point cliff and it's worth real money.

But **5 minutes is not where the cliff is.** Under-5-min (46%) versus 5–60 min (43%) is
three points on n=98 — noise. Going from a one-hour SLA to a five-minute one buys you
almost nothing; going from four hours to one hour buys you fifteen points. A five-minute
target costs a great deal to staff and the data does not pay for it.

**Suggested target: answer inside the hour, every time.** Then spend what you saved on H4.

Email is too thin to call (n=198, one single thread under 5 minutes). Don't set an email SLA
off this.

---

## H1 — The copy. Real, and it started this month.

The stock sentence I flagged last week —

> *"Awesome. If you have got a few minutes [time] or maybe next week, I'd be happy to hop on
> a quick call and discuss what we can do for [Company]."*

— books at **26% against a 39% baseline** on SMS. So it is worse. But here is the finding
that matters:

| month | answered SMS threads | using the stock template |
|---|---:|---:|
| Oct 2025 – Jun 2026 | 582 | **0** |
| Jul 2026 | 245 | 1 |
| **Aug 2026** | **101** | **38 (38%)** |

**It did not exist before August.** Something changed this month and it is now on more than
a third of all SMS replies, across eight clients at once — Chamber 8, Growth Lab 7, Go Fish
6, Scaletopia 6, Wise 5, Acceler8 4, Leadgenix 4, Kynship 2. Eight clients don't
independently invent the same sentence in the same month. That's one shared automation, one
shared macro, or one person's snippet, rolled out around the start of August.

**Finding out what changed on ~1 Aug is the highest-value thing in this document.** It's
reversible, it's recent, and there are ten months of better-performing replies to roll back to.

Other copy markers, all answered threads (baseline 38%):

| marker | n | booked |
|---|---:|---:|
| "got a few minutes" | 98 | **21%** |
| "hop on a quick call" | 35 | 26% |
| answered a different question than they asked | 65 | **18%** |
| opens "Awesome / Perfect / Sounds good" | 640 | 38% — neutral, ignore it |

**"Answered the wrong question" is the one to fix beyond the template.** 65 threads where
they asked to be shown something and got a meeting request with nothing attached. 18% vs
38%. That one is judgement, not a macro.

### A correction to what I told you last week

I said *"never ask for the email in order to book"* on the strength of three threads.
Across all time that is **wrong**: 66 threads where we asked for their email book at
**59%** — well above the 38% baseline. It's used mostly by Leadgenix (29) and Chamber (17)
and it works for them. Sue Graham going cold after that ask was one bad thread, not a pattern.
Drop that recommendation.

---

## H2 — Follow-ups. My first read was wrong. It's quality, not count.

I measured how MANY follow-ups went out and never looked at what they said. Aaman's
correction: a 3rd follow-up is usually automated, so a low booking rate at 3+ may be
measuring automation, not cadence — and nothing in a count tells you whether any of them
were worth sending. He's right, and reading them settles it.

**The best month and the worst month send a structurally different follow-up.**

May 2026 (SMS, 64% booked) — the follow-up **takes the action**:

> "Perfect. I've booked us in for Friday at 10:30am MT with our director Ian, and sent an
> invite to chris@risehealthaz.com — talk soon." → **booked**
> "Sure. To avoid back and forth, I'll put in a placeholder for next Tuesday around 11:30am
> ET with our director Ian, and send the invite to valerie@…" → **booked**

August 2026 (SMS, 25% booked) — the follow-up **asks for the action**:

> "Sure, let me know both of your availability and I'll send a calendar invite." → no
> "If you have got a few minutes tomorrow 12:30 pm or maybe Thursday 1:30 pm pst…" → no

And where August still books, it's the May move, unchanged:

> "I've just booked us in for Monday at 11 am MDT with our director Spencer, and sent an
> invite to david@zingbars.com." → **booked** (Acceler8)

**The rule isn't "follow up more." It's: book it and say you've booked it.** Put a
placeholder in, name the time, name the person, say the invite is sent. Requesting
availability is the losing move at both ends of the year.

This also explains the "asks for their email" result (59% booked). It was never about the
email — the email ask is *part of* the booking move: *"What's the best email — I'll send a
placeholder for Tuesday afternoon just to get something on the books, easier to move than
to find."* Asking for an email in order to book works. Asking for an email **instead of**
booking is what killed Sue Graham.

Count still can't be tested here — it's downstream of the outcome — but it no longer
matters, because count was the wrong question.

The one clean count-based signal: **29 threads got the identical follow-up sent twice,
verbatim. 2 booked (7%).**

## H4 — Coverage. You deprioritised this and it's the biggest number here.

Positive replies that **never received a human answer**:

- **SMS: 318 of 1,620 — 20%**
- **Email: 159 of 374 — 43%**
- **477 people said yes and heard nothing back.**

For scale: the entire stock-template problem is 45 threads all-time. This is 477. No copy
change reaches a thread nobody opened.

Worst offenders — and the concentration is the useful part:

| client | unanswered | of readable | |
|---|---:|---:|---|
| seedx | 18 | 27 | **67%** |
| redo | 25 | 62 | **40%** |
| scaletopia | 178 | 556 | **32%** |
| big_leap | 10 | 37 | 27% |
| kynship | 23 | 97 | 24% |
| chamber_media | 103 | 543 | 19% |
| leadgenix | 60 | 340 | 18% |
| growth_lab | 6 | 53 | 11% |

**Scaletopia is your own book and it's third-worst at 32% — 178 replies.** Email at 43%
unanswered across the board suggests nobody owns the email inbox the way someone owns SMS.

---

## The category tags are ~20% wrong

340 of 1,675 classifiable threads carry a tag that doesn't match what the person actually
wrote. This inflates every headline count and it's why "power requests" felt overstated to you.

| tag | mis-tagged | most common truth |
|---|---|---|
| Power Request | 143 / 912 (16%) | channel_switch 84 — "email me your pitch" is not a call ask |
| More Info Request | 129 / 422 (**31%**) | **objection 40**, soft_yes 31, call_ask 26 |
| Email Me Request | 68 / 341 (20%) | soft_yes 16, info_ask 13, objection 10 |

**More Info Request is the worst bucket — nearly a third wrong, and the largest single error
is objections filed as info requests.** Which is exactly the case you remembered:

> **Big Leap · ViewCrew Home Services · 22 Jul 2026 · tagged More Info Request**
> *"We do 10M a year can you scale above that??"*

That's a capability objection from a qualified buyer, and filing it as "more info" means
nobody ever answered the actual question. Same shape found at Scaletopia (13 Aug, an Email
Me Request that's really an objection about scripts and references).

---

## Opener → what comes back

| opener CTA | n | booked | ≤3-word replies |
|---|---:|---:|---:|
| soft ("lmk if it's worth exploring") | 153 | **61%** | 25% |
| direct time ask ("free this week?") | 42 | 48% | 24% |
| permission ("could I show you how?") | 746 | 35% | 28% |
| other question | 521 | 32% | 34% |

Softest ask wins by a distance, and the permission ask — which is on 746 threads, our most-used
opener — is second from bottom. This is worth a proper test rather than a rewrite off n=153,
but it points the opposite way to the tightening instinct.

---

## What I'd do, in order

1. **Find out what changed around 1 August.** Eight clients started sending the same reply
   in the same month after ten months of not doing so. Whatever shipped, roll it back.
2. **Set the reply SLA at one hour, not five minutes.** 15 points of booking rate sit at the
   one-hour line; nothing measurable sits at five minutes.
3. **Put someone on the email inbox.** 43% of email positives get no answer at all.
4. **Split More Info Request** — a third of it is objections nobody answered.
5. **Leave the follow-up cadence alone** until there's a real test. The only clean rule is
   *don't send the same nudge twice.*
6. **Drop my "never ask for the email" advice from last week.** It books at 59%.

Not covered: Strike Tax and Taktical (in Airtable, not loaded in Evergreen); NextLeft has
no replies yet.
