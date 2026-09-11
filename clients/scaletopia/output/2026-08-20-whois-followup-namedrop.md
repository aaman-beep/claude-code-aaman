# WHOis follow-up (step 2) — namedrop direction

**STRAWMAN — redline me.** 2026-08-20. Campaigns **1040** (Google) / **1041** (Outlook).
Config: `order: 2`, `thread_reply: true`, subject `Re: {step-1 subject}`, `wait_in_days: 3`. **No spintax.**

Supersedes the bandwidth/reply-handling angles in
[2026-08-20-whois-followup-drafts.md](2026-08-20-whois-followup-drafts.md) — those stay on the shelf.

---

## Your line, in English

What you dictated:

> "we're working with probably the only outbound company that works with the most agencies"

That's two different claims fused together, and they cancel each other out — *only* means nobody else
does it, *the most* means plenty do and we lead. Pick one:

| claim | reads as | needs |
|---|---|---|
| **"we work with more agencies than anyone else"** ← recommended | a leaderboard position | a number you'll stand behind |
| "we're the only outbound shop that specialises in agencies" | a category of one | falsifiable in about ten seconds |

Drafts use the first.

---

## Namedrop list — verified

**"Perana" is Pirawna.** ✅ And you're already sending that exact set live in reply handling:

> *"we've worked with Pirawna, Bad marketing, Evolved commerce etc. So we're extremely familiar with Amazon agencies"*
> *"we've worked with half of the amazon agencies out there haha - Pirawna, Hyperzon, BAD marketing etc."*

| name | status |
|---|---|
| **Go Fish Digital** | ✅ client (`registry.json`) — strongest name for this list, genuinely known in SEO/digital |
| **Digital Resource** | ✅ client (`registry.json`) |
| **Pirawna** | ✅ sent live by you in reply handling |
| **BAD Marketing** | ✅ sent live by you in reply handling |
| Hyperzon, Evolved Commerce, Firecracker PR | ✅ also sent live — bench, if you want to swap |
| Chamber Media, Kynship, LeadGenix, Growth Lab, Big Leap, Redo, WISE Digital | ✅ clients, unused here |
| **Purple** | ❌ **cut it.** Not a client. Every `Purple*` in the repo is a **prospect** — Purple Cow, Purplepatch, Purplez, all from the retargeting campaign |
| NextLeft | ❌ also a prospect (John McKusick, meeting booked Aug 5). Don't add it |

⚠️ **The count still isn't locked.** Sent copy carries **32 agencies** (76 sends), 27, and 17;
the live WHOis step 1 says **26**. Step 1 and step 2 land in the same thread, so if step 2 says 32
the reader sees the number move inside one conversation. **Make step 2 match step 1, or fix both.**

⚠️ Pirawna and BAD Marketing are Amazon agencies; Go Fish and Digital Resource are SEO/digital.
For this list (agencies running their own cold email) **Go Fish Digital carries the most weight** —
keep it first.

---

## The drafts

All four: ≤80 words, exactly one question mark, no exclamations, no em dashes, ≤2 lines per
paragraph. Signature appended by the sending profile.

### D1 · closest to your dictation — *recommended*

**72 words.** Straight through, "But" opener on the turn, no number to contradict step 1.

```
{{firstName}}, I'm assuming you get way too many of these, or you've already got outbound covered.

Either way just tell me and I'll stop bothering you.

But we're probably the only outbound shop working with this many agencies - Go Fish Digital, BAD Marketing, Pirawna, Digital Resource.

Want me to just share what's working right now?

P.S. We run a 30-day pilot so you can test us before you commit to anything.
```

### D2 · the claim made concrete

**72 words.** Puts the number in. Only ship if step 1 also says 32.

```
{{firstName}}, I'm assuming you get way too many of these, or you've already got outbound covered.

Either way, say the word and I'll leave you alone.

We run outbound for 32 agencies, which is more than anyone else I know of - Go Fish Digital, BAD Marketing, Pirawna, Digital Resource.

Want the two-minute version of what's working right now?

P.S. There's a 30-day pilot, so you test us before committing to anything.
```

### D3 · namedrop leads the turn

**70 words.** The names land before the claim, so the claim reads as the summary rather than the pitch.

```
{{firstName}}, assuming you get way too many of these, or outbound's already handled.

Either way, tell me and I'll drop off.

If not - Go Fish Digital, BAD Marketing, Pirawna and Digital Resource all run their outbound through us. More agencies than anyone else I've come across.

Want me to send over what's working right now?

P.S. It runs as a 30-day pilot, so you're testing us before you commit.
```

### D4 · flattest

**71 words.** Least salesy verb on the CTA.

```
{{firstName}}, I'm assuming you get way too many of these, or outbound's already covered.

Either way just say so and I won't bother you again.

If it's the first one, we're the outbound shop that works with the most agencies. Go Fish Digital, BAD Marketing, Pirawna, Digital Resource.

Can I just show you what's working right now?

P.S. Runs as a 30-day pilot, so you test us before committing to anything.
```

---

## On the opener — your instinct is backed, and I was over-cautious

I flagged *"I'm assuming you get way too many of these"* as retired. That flag was about **cold
openers** — six clients run a version of it as a first touch, so it stopped interrupting anything.

**In slot 2 it's a different move, and it's the best cold follow-up we've ever shipped.** BD step 2
(campaign 899, **1.67%**, the highest cold reply rate in the account) opens with that exact line.
It works there because the reader has already ignored one email, so conceding it is accurate rather
than performative — and it's the one place our corpus scores a genuine "costs you the sale" out,
which EMAIL-QA found is the criterion we fail 63% of the time. **Keep it.**

The one thing I'd still hold from BD step 2 is the line *after* it — *"we text and email at scale the
moment your prospect shows a signal"* — which is the burnt signal-based phrasing
(*"burnt heavily with signals data"*, Richard Dresser). The namedrop replaces it cleanly. All four
drafts are clean of it.

---

## Pilot wording — still three different promises

You said "free pilot." The drafts default to the **shipped** wording from 899/920/903, which is
no-commitment, not free:

- ✅ shipped: *"a 30-day pilot so you can test us before you commit to anything"*
- ⚠️ never sent: *"a 30-day **free** pilot"*
- ⚠️ unconfirmed since Aug 6 (run-sheet blocker #5): *"you only pay on results"*

Swap in `P.S. First 30 days run as a free pilot, so you see it work before you pay for it.`
the moment you confirm that's actually the offer.

---

## Before this goes live

- [ ] Cut **Purple** — it's a prospect, not a client
- [ ] Pick one agency count and make step 1 and step 2 agree (**26** or **32**)
- [ ] Confirm Go Fish Digital / Digital Resource are contractually fine to name in cold outbound
      (Pirawna and BAD Marketing you've already sent, so those are settled)
- [ ] Decide "free" vs "no-commitment" on the pilot P.S.
- [ ] Still the highest-leverage open item: **who owns reply handling during send hours**
