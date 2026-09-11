# T2 drafts — "playbook" frame

**T1 (fixed):** Hi {{firstName}}, sorry to text out of the blue but we took Dark Horse CPAs from $1.5m to $21m in 5 years by replacing referrals with organic search — *148 chars, 1 segment*

**Status: strawman — redline it.** Every pattern below is lifted from a logged winner in Evergreen, not invented. Sources named per variant.

---

## What the winners actually say

Two winners already use the word, so it isn't a new coinage:

- **acceler8** — *"Happy to walk you through how {{company}} could apply the **same playbook** — and the audit is yours to keep."* → 100% high intent. Sharpest mechanism in its set.
- **chamber_media** — *"Been quietly working through {{niche}} to find 3-4 brands best positioned to run the **same playbook** — {{company}} is one of them."* → the shortest T1 of any winner still worked, because the proof was recognisable.

Three mechanics that separate winners from losers here:

1. **Work already done.** Chamber's *"I've got a plan put together for you"* is flagged as the differentiator — *"it implies work already done, which raises the social cost of saying no."*
2. **Selection, not solicitation.** "I looked at a few and picked you" outperforms "can I pitch you."
3. **The T2 must be about them.** The go_fish loser died precisely because *"the whole text is about US."* This is the live risk with "playbook" — it's our system, so every draft below has to turn it back on the firm.

---

## The drafts

### B · Work already done — *my pick*
> Mapped out how the same playbook would work for {{companyName}} - happy to walk you through it. Free for 10 mins next week? - Matt, WISE Digital

**144 chars · 1 segment.** Chamber's highest-social-cost mechanic, in plain words. Claims effort already spent on *their* firm, which is what makes ignoring it feel rude. Closest thing to a straight upgrade on the current winner.

### E · Value-give
> Not asking for your business but could I walk you through the playbook we used? Yours to keep either way. - Matt, WISE Digital

**126 chars · 1 segment.** Lifts the go_fish winner's *"not asking for your business but could I at least share a few ideas"* — the phrasing that produced human replies instead of STOPs — and bolts on acceler8's *"yours to keep"* risk-reversal. Lowest-pressure option; best fit for the re-texted portion of the list, which is most of it.

### D · Referral reframe — *the one that uses the Leppert call*
> Ran the same playbook for firms stuck on referrals - the leads come in better qualified than the referrals did. Can I show you? - Matt, WISE Digital

**148 chars · 1 segment.** Straight from Patrick's own words on the Leppert call: *"most accounting firms are still stuck in [the referral mindset]"* [1261] and *"quality is way better than — I'd argue — than you're even getting through referrals"* [1277]. Attacks the belief rather than the volume. Highest-variance option — it contradicts something the buyer believes — but it's the only draft that says something they haven't heard.

### F · Cap scarcity
> Could run the same playbook at {{companyName}} - we only take 3 firms per market though. Worth exploring next week? - Matt, WISE Digital

**136 chars · 1 segment.** growth_lab's *"we only work with 3 firms per city"* appears in **three** separate winners — the most-repeated scarcity device in the whole winner set. ⚠️ **Only ship if it's true.** If WISE will take a fourth CPA firm in a market, this is a lie and it's the kind that surfaces on the call.

### C · Faucet — capacity objection
> Same playbook would work for {{companyName}} - and it's a faucet not a fire hose, you control the flow. Mind if I give you a ring next week? - Matt, WISE Digital

**161 chars · 2 segments ⚠️.** Patrick's own line [1281], answering the objection George actually raised. One char over — trim "and" or "Mind if I give you a ring" → "Worth a quick call" to get it under. Test only after B/E/D.

### A · Selection scarcity
> Been going through CPA firms in {{state}} to find a few best positioned to run the same playbook - {{companyName}} is one of them. Worth a quick call? - Matt, WISE Digital

**171 chars · 2 segments ⚠️.** Closest to the chamber_media winner, but that winner ran with a *recognisable artifact* (the ClickUp ad) doing the work. Needs a `{{state}}` merge field you may not have populated — and empty merge fields are already a live defect here. Lowest priority.

---

## Loser QA

| Failure mode (from Evergreen losers) | Which drafts risk it | Handled? |
|---|---|---|
| "The whole text is about US" (go_fish) | all of them — "playbook" is our system | B, D, F name the firm or their situation. E flips it with "not asking for your business". ✅ |
| T1 and T2 don't connect into one thread (wise_digital L7) | — | every draft says "the same playbook", pointing back at Dark Horse. ✅ |
| Agency-side revenue, not the buyer's unit (digital_resource) | — | no new numbers introduced in T2; $1.5m→$21m stays in T1. ✅ |
| Mechanism needs explaining (kynship) | C (faucet) | "faucet not a fire hose" is self-explaining. ✅ |
| Reads AI-written (seedx) | A | A is the longest and most constructed. Deprioritised. ⚠️ |

## On the CTA

The evidence conflicts and I'm not going to pretend otherwise:

- **growth_lab natural experiment:** identical copy, *"sometime this week"* beat *"after the holidays"* by **~2.5× per positive reply**.
- **acceler8, three arms of one T1:** the *no-window* CTA ("worth exploring?") was the volume workhorse; *"sometime this week"* had the **worst** ratio of the three.
- **Your own data:** *"next week"* beat *"this week"* — 6.25% vs 5.26%.

Your data and acceler8 both point away from urgency; growth_lab points toward it. I've used **"next week"** throughout because that's what your own account says. Worth an explicit CTA test once a variant wins.

---

## What I'd run

Restore Dark Horse with the **current** T2 first — that's the 1.76 meetings/1k configuration and the thing with evidence behind it. Then A/B **B** against it, and **E** on the retarget slice where pressure is the risk. Don't test six variants across 528 remaining leads; you'll learn nothing from any of them.
