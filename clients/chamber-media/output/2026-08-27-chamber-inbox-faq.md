# Chamber Media inbox FAQ — every question a prospect actually asked

**Strawman for the inbox manager. Redline it.** Source: Evergreen, `chamber_media`, deals ∪
categorised contacts, **1 Jan – 27 Aug 2026**. Rebuild with `tools/reply_handling_audit.py`.

**The corpus.** 1,387 reply threads after dedupe (863 deals + 995 contact threads unioned) —
**1,140 SMS, 247 email**. A further 690 "Not Interested" and 20 "Threat" threads sit outside
this and are not counted. Of those 1,387, **515 inbound messages carry a real question or
objection**; 289 of them fall into the eleven repeating shapes below.

Every quote is verbatim. Answers marked ✅ are lifted from threads that went on to book.

---

## The scoreboard — ranked by how often it's asked

| what they ask | n | sms / email | we answered | later booked |
|---|---:|---|---:|---:|
| **How did you get my number?** | **96** | 96 / 0 | **28%** | 7% |
| What does it cost / what's the comp model? | 60 | 48 / 12 | 67% | 12% |
| Show me the work / send examples | 42 | 33 / 9 | 86% | 14% |
| Who is this / what is Chamber? | 40 | 33 / 7 | **40%** | 15% |
| Where are you based / what timezone? | 14 | 11 / 3 | 86% | **50%** |
| Wrong person / I've moved on | 13 | 13 / 0 | **31%** | 15% |
| What exactly do you do? | 10 | 8 / 2 | 90% | 10% |
| We already have this / tried it, poor results | 5 | 3 / 2 | 80% | 20% |
| I didn't get your email | 5 | 5 / 0 | 80% | **0%** |
| Is this AI? | 2 | 1 / 1 | 50% | 50% |
| Are you joining? I'm on the call | 2 | 1 / 1 | **0%** | 100% |

**Read the "we answered" column first.** Three of the top four most-asked questions go
unanswered more than half the time. That's ~110 people who asked Chamber a direct question
and got silence.

**One thing that is NOT broken:** only **1 of 153** answered questions got an automated nudge
instead of a real reply. Whatever else is wrong, the inbox isn't answering people with
"did my text go through btw" — don't spend time there.

---

## 1. "How did you get my number?" — 96 asks, the single biggest hole

Nearly one in five questions in the entire corpus. **SMS only — it never comes up on email.**
We answer 27 of 96. Phrasings:

> "How'd you get this number?" · "Where did you get this number?" · "How did you find me?" ·
> "How did you track me down?" · "Will you please tell me how you got my information?" ·
> "Hello... This is my personal cell phone number. Can I ask how you acquired it?" ·
> "Text me what your idea is. Also, how did you get my number?"

**What separates the answers that booked from the ones that didn't: naming why *they*
specifically came up, instead of explaining the mechanism.**

**✅ These booked:**

> "Found you through some research into brands doing interesting work in beauty
> manufacturing — saw your background in brand partnerships and thought the approach might
> fit what you're building at Ayo."

> "Fair. Angglz came up while researching standout DTC brands in the sleep/comfort space.
> Reached out direct from my founder shortlist rather than just emailing."

**⚠️ This one is a coin flip** — it appears on booked *and* dead threads, because it answers
the mechanism and nothing else:

> "Got it from a public database that we use for outreach, nothing shady. Happy to continue
> over email if you prefer."

**✍️ Template:**

> Fair question. [Brand] came up while I was researching [specific category — sleep/comfort
> DTC, beauty manufacturing, health & nutrition]. You were on my shortlist rather than a
> list I bought, so I reached out direct instead of emailing. Happy to move to email if
> that's easier.

**Note what this really is.** 96 people asking where the number came from is a list-and-opener
signal as much as an inbox one — nobody asks that when the opener has clearly done its
homework. Worth logging as a copy test, not just an inbox script.

---

## 2. "What does it cost?" — 60 asks

> "How much does it cost?" · "What's your comp model?" · "How do you work financially Wise?"
> · "I'm assuming this will cost me $0?" · "We don't have a lot of money right now. How can
> we make this cost efficient?" · "I'm worried it will be out of our price range" · "Not sure
> we have the budget for campaigns you're looking to run"

**✅ The number that appears in the answers that booked is $2.5k/mo, framed as a test rather
than a retainer:**

> "We work with brands at all stages, not just Fortune 500. The starting point is $2.5k/mo to
> test a few directions and you only scale when the math works."

> "Appreciate the heads up Adam — that's actually a fair concern. We usually start around
> $2.5k/mo testing a few angles, then scale once the math works. Same play we ran with Team
> Keto ($1m to $4m in 12 months) and Nature's Eats."

**✅ On the business model specifically:**

> "We charge a flat monthly fee for creative production and ad management. We build the video
> creative, run it on YouTube and Meta, and optimize based on what's actually performing."

**❌ Don't dodge into a meeting request.** One prospect wrote a long, honest note about
being a small brand worried about price and got *"Perfect. I'll send a calendar invite over
for Friday at 1pm PST, drop your best email"* back. It didn't book. **Answer the number
first, then propose the time.**

**✍️ Template:**

> Starts around $2.5k/mo — that's to test 2-3 angles, not a big commitment. We don't
> recommend scaling past that until the creative is proving itself. Flat monthly fee covering
> production and ad management. [Proof point matched to their size.]

---

## 3. "Send me examples / show me the work" — 42 asks

> "Can you send a link to your website or portfolio of your work?" · "Can you send over 2-3
> examples of campaigns you're referencing?" · "Would you mind sharing example of your work
> for TL?" · "Can you provide me with any of Transparent's social accounts so I can
> evaluate?" · "Do you have a website and case study I can review?"

Answered 86% of the time — the best-served question we have — but it only converts at 14%.

**✅ The two that booked were short, and offered to tailor rather than dumping:**

> "Sure, www.chamber.media. Happy to share an overview highlighting results relevant to
> Novara's growth stage if it's worth exploring sometime this week or next."

**✅ And the best one answered the question hiding behind the question** — a UK prospect
asking for examples was really asking whether Chamber could produce in the UK:

> "Hi Dinuk, yes — we do. We've worked with brands outside the US and can handle production
> in the UK as well. Stefan on our team is actually based there, so timing/logistics tend to
> be pretty smooth."

**⚠️ The elaborate version underperformed.** A three-link, three-case-study reply tailored to
Pura Vida (Team Keto, Nature's Eats, with YouTube links) did *not* book. Small numbers, so
don't over-read it — but it's evidence against the instinct that more links is better.

**✍️ Template:** one link, one line on what you'd tailor, one time.

---

## 4. "Who is this / what is Chamber?" — 40 asks, and an identity problem underneath

> "Who is this?" · "Who is this ? lol" · "Is this a company?" · "What is chamber?" · "Is this
> the chamber?" · "Remind me how I know you Courtney and what is Chamber?" · "Can you tell me
> who are you?" · "I am Interested but what is your last name?" · "Are you on LinkedIn?"

**✅ Answer that booked:**

> "Yes, this is Chamber Media. We work with health & nutrition brands on performance video
> creative — that's how we helped Transparent Labs scale from ~$2M to $26M/yr."

**The identity problem is worth its own line.** The copy signs as Claire, Courtney, Ian and
Bri, and prospects are catching it:

> *"Also is this an AI? If yes I'd love to know what setup you are using. **I couldn't find a
> Claire associated with chamber media on LinkedIn**"*
>
> *"**Ian???!!! I have you saved as Courtney for some reason.** You must be a nice person too"*

**✅ The reply to the first one was straight, and it booked:**

> "Yeah we use a mix of manual + AI for outreach. Claire used to be on our team and we kept
> her name as our outreach alias."

**Honesty converted here.** Whether to keep running aliases that don't resolve on LinkedIn is
a decision above the inbox — but while they're running, the inbox manager needs that line
ready, because it works better than deflecting.

**✅ Have Ian's real LinkedIn to hand:**

> "Here's Ian Johnson's LinkedIn — he leads sales & partnerships at Chamber and would be the
> one walking you through ideas."

---

## 5. "Where are you based / what timezone?" — the highest-converting question in the inbox

Only 14 asks, but **50% of them booked** — roughly four times the rate of anything else.

> "Hi — where are you located?" · "Which time zone are you in?" · "What time zone are we
> speaking? I'm in CET" · "I'll be traveling this week. Where are you based? I'm in Finland"

**This isn't really a question, it's a diary check.** Somebody asking your timezone is
already picturing the call. Treat it as a booking signal, answer in one line, and book.

**✅ Verbatim, all three booked:**

> "Those are PST, but happy to work around whatever timezone you're in."

> "Perfect — I'm US-based but Wednesday or Thursday next week works great on my end. EET is
> totally fine. Let's lock in Wednesday at 5 PM EET (that's 9 AM MST / 11 AM EST for me).
> I'll send over a calendar invite to confirm."

**Rule: any timezone or location question gets an answer and a specific slot in the same
message.**

---

## 6. "I'm not with them anymore" — 13 asks, we answer 4

> "Hello Courtney, **I am not with Nutrabolt anymore. I started my own company called
> Peakform Nutrition. Could you send me some details on what you are re[ferring to]**"

That is a warm inbound from a founder at a brand-new company, and it's in the pile with the
nine others we never replied to. **A "wrong person" message that names where they went now is
a fresh lead, not a bounce.** Route it, don't close it.

---

## 7. "I didn't get your email" — 5 asks, 0 booked

> "I didn't receive anything from you. To which email address did you send it?" · "Email?" ·
> "I don't have any emails about this — only texts."

Every one of these died. The SMS→email handoff is dropping messages, and by the time the
prospect is chasing *us* for something we said we sent, the thread is already damaged.
Worth checking whether the sends are actually landing before writing a script for it.

---

## 8. "Are you joining? I'm on the call"

Two people sat on a booked call waiting for us. **Neither got a reply.** Small numbers, but
the cost per instance is a booked meeting plus the relationship. Whoever runs the inbox needs
eyes on the calendar, or these need routing to Ian directly.

---

## Quick-reference card

| they ask | one-line answer | full |
|---|---|---|
| How'd you get my number? | Name why *their brand* came up, not the database | §1 |
| What's it cost? | From $2.5k/mo to test 2-3 angles, flat fee, scale when the math works | §2 |
| What's the comp model? | Flat monthly for creative production + ad management | §2 |
| Send examples | One link + "happy to tailor an overview to [their] growth stage" | §3 |
| Who is this / what is Chamber? | Chamber Media, performance video creative, Transparent Labs $2M→$26M | §4 |
| Is this AI? / can't find you on LinkedIn | Straight answer — mix of manual and AI, Claire is an outreach alias | §4 |
| Where are you based / timezone? | Answer + a specific slot in the same message. Highest-converting question we get | §5 |
| I've left that company | Ask what they're building now. It's a new lead | §6 |
| Didn't get your email | Resend in-thread, don't ask them to check spam | §7 |

---

## Three things this data says that aren't inbox scripts

1. **96 people asked where their number came from.** No script fixes that — it's what the
   opener and the list are producing. Log it as a copy test.
2. **The aliases are being caught.** "I couldn't find a Claire associated with Chamber Media
   on LinkedIn" is a prospect doing diligence and failing to verify us. The honest answer
   works; the question is whether we want to keep needing it.
3. **Answer rate is the lever, not answer quality.** The scripts in here matter less than the
   fact that ~110 direct questions got no reply at all. Fixing coverage is worth more than
   perfecting any single template.
