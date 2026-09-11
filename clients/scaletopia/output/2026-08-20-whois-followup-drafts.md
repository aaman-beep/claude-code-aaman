# WHOis campaign — follow-up (step 2) drafts

**STRAWMAN — redline me.** 2026-08-20. Campaigns **1040** (Google) / **1041** (Outlook).
Config: `order: 2`, `thread_reply: true`, subject `Re: {same step-1 subject}`, `wait_in_days: 3`.

---

## 1 · Where 1040 actually stands

| | |
|---|---|
| Leads / sent | 584 / 573 |
| Replies | **9 → 1.57%** |
| Bounced | 17 (3.0%) |
| Sequence steps | **1. There is no follow-up at all.** |

1.57% is above the Scaletopia account average (1.1%) and level with the best campaigns ever run
(863 Ecom @ 1.5%, 920 BD @ 1.5%). Your read is right — it's working. Sister campaign 1041
(Outlook) has the identical step 1 and **0 replies on 270 sends**, so the read is Google-only so far.

Repliers so far: Common Thread Co, Echidna, Jordan Digital Marketing, Heart & Soul Mktg —
i.e. real agencies in the ICP, not noise.

**Note on "second follow-up":** there is currently *nothing* in slot 2, so this doc writes
**step 2** (the first follow-up). Step 3 (breakup) is sketched at the bottom.

---

## 2 · The follow-up you were trying to remember

Two different things, and they're often conflated:

**A · `Scaletopia - OOO Follow Up` (campaign 377) — 26 replies / 193 sends = 13.5%.**
Highest-replying asset in the account by ~9×. Full copy, verbatim:

> Hey {FIRST_NAME}, you mentioned on your email you'll be back into the office today - just
> reaching back out to see if my email resonated at all or just not a priority at the moment?

One sentence. No proof, no P.S., no spintax, no pitch. ⚠️ It's a `reply_followup` that only fires
on people who already sent an out-of-office auto-reply — a *warm, triggered* audience, so 13.5% is
not comparable to a cold send. **The transferable lesson is the shape, not the rate.**

**B · BD Campaign step 2 (campaigns 899 @ 1.67%, 920 @ 1.5%, 903).** The best cold follow-up
structure we've shipped, and the one already carrying the pilot line:
concede → differentiate → one concrete example for their company → two-way question → pilot in the P.S.

⚠️ **Do not lift B verbatim.** Two of its lines are on this campaign's banned list (§5).

---

## 3 · The drafts

All three: ≤80 words, exactly one question mark, no exclamations, no em dashes, ≤2 lines per
paragraph, **no spintax**. Signature is appended by the sending profile.

### V1 · Bandwidth — *recommended*

Answers the objection step 1 provokes ("we already do this ourselves, why you?") with the answer
this audience gave us in their own words: nobody there owns it. Doesn't argue we're better at
outbound than they are. **66 words.**

```
{{firstName}}, agencies sending from that many domains usually aren't stuck on the copy.
It's that nobody there owns it full time.

Chamber Media were already running their own email when we started. We ran alongside their team instead of replacing them.

Want me to show you how we split it?

P.S. It runs as a 30-day pilot, so you're testing us before you commit to anything.
```

### V2 · Reply handling

Carries the one insight step 1 couldn't, and it's a fact we own rather than a claim. **75 words.**

```
{{firstName}}, one thing we watch closely: the meetings we booked last month all came off a reply we answered inside the hour.

None came from the ones we got to the next day.

Chamber Media didn't change their copy or their list. They changed who sat on the inbox.

Is that the gap at {{companyName}}, or is yours covered?

P.S. It runs as a 30-day pilot, so you're testing us before you commit to anything.
```

⚠️ The inside-the-hour number is from **July SMS** (33 human replies → 5 meetings, all booked
12 min–1.3 hrs after first reply). Claiming it on an email campaign is a channel stretch. Also
Q4 on the run sheet — "tell the replies-die-downstream story as a measured law, or keep it
vaguer?" — is still unanswered by you. Ship V2 only if you're happy with both.

### V3 · Plain ask — the OOO shape ported to cold

Near-zero pitch, mirrors the 13.5% winner's structure. Lowest risk, lowest information. **53 words.**

```
{{firstName}}, following up on the below.

Did the redirect thing land at all, or is outbound just not the priority right now?

Either answer is useful. If it's the second one, I'll leave you be.

P.S. Whenever it does come up, we run a 30-day pilot so you can test us before committing.
```

---

## 4 · The pilot line — pick one, they are three different promises

Step 1 on 1040/1041 **does not mention the pilot at all.** These are the options:

| wording | status |
|---|---|
| "a 30-day pilot, so you're testing us before you commit to anything" | ✅ **shipped** in 899/920/903 P.S. Safe. Used above. |
| "a 30-day pilot, free" | ⚠️ never shipped. Is it actually free, or just no-commitment? |
| "a 30-day pilot where you only pay on results" | ⚠️ blocker #5 on the run sheet, **still unconfirmed** since 2026-08-06 |

You said "free pilot" — that's the second row, and it's a stronger claim than anything we've sent.
Drafts default to the shipped wording. Swap the P.S. to
`P.S. First 30 days run as a free pilot, so you can see it work before you pay for it.`
once you confirm it's true.

---

## 5 · Banned in this campaign (all three drafts are clean)

1. **"signal-based" / "AI-timed" / "the moment your prospect shows a signal"** — burnt phrase with
   this exact audience (*"burnt heavily with signals data"* — Richard Dresser, Go Fish). It is the
   core line of the BD step-2 winner, which is why B can't be lifted as-is.
2. **"I'm sure you get a lot of these" / "your inbox is full of agencies"** — EMAIL-QA retired it;
   six clients run it simultaneously. Also the opener of the BD step-2 winner.
3. **A new Chamber number.** Step 1 already ships *"112 qualified shows in the past 6 months"* — an
   **11th** distinct Chamber claim, and one that appears nowhere in the number audit. The follow-up
   deliberately carries a *different kind* of proof (how we worked, who owned the inbox) rather
   than a different figure. Do not add one.
4. **Spintax.** Step 1 is heavily spun; EMAIL-QA found spintax shipping broken sentences on
   Scaletopia at scale. These drafts are flat text on purpose.
5. **A bulleted 3-point list** — the most recognisable AI-email silhouette in our corpus ([35]/[36]).

---

## 6 · Step 3, if you want it

The BD breakup (899 step 3) is reusable, minus the bullets and minus the stale
"going into Q3" / "after the holidays" timing. Say the word and I'll draft it to the same rules.

---

## 7 · One thing worth more than the copy

573 sends → 9 replies → the run sheet's highest-leverage open item is still
**who owns reply handling during send hours** (unanswered since 2026-08-06). July: every meeting
came from a reply answered in 12 min–1.3 hrs. And *"could I drop you an email"* went **0 for 11** —
if a WHOis reply comes in, keep it in the thread.
