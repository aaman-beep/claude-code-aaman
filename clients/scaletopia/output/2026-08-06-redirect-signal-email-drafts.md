# Redirect-signal campaign — email drafts (2026-08-06)

**STRAWMAN — redline me.** Two versions for comparison. Not cleared for send: see blockers at the bottom.

Campaign: Scaletopia → marketing agencies, 25–500 headcount, selected by redirect-domain count.
Merge vars: `{{firstName}}`, `{{companyName}}`, **`{{domainCount}}`** (must come out of the detector per company).

Relevance line credit: Aaman's manual draft. The key insight is that the redirect domains **are** the sending domains — so the line names the mechanic ("sending cold email *from* the N domains") rather than just counting them. That's the peer-level register `winning-sms/` Template #6 calls for on agency targets. The diagnostic question was moved to the end so it doubles as the CTA and there's one question mark.

---

## Version A — plan approach (states the signal)

### A1 · mechanism OFF · subject `your other domains` · 53 words

```
{{firstName}} - the {{domainCount}} domains redirecting to {{companyName}}'s site tell me you're already sending cold email.

We run email and SMS outbound for 26 marketing agencies. Since January we've helped Chamber Media close 14 retainers (74K MRR).

So which is it - working and you want more, or you've tried it and it hasn't landed?

Best,
Molly Barnes | Scaletopia

P.S. There's a 30-day pilot so you can test us before committing.
```

### A2 · mechanism ON · 59 words

Identical to A1, one clause added after the result:

```
...close 14 retainers (74K MRR) - mostly through text, not email.
```

**Why this mechanism.** True from our own records; avoids "AI-timed" / "signal-based", which is the exact phrasing Richard Dresser (Go Fish) told us burnt him and which sits in 29,294 sends of live copy; and on a list defined entirely by *email* infrastructure the channel is the sharpest true difference we have. It's also abstract rather than granular, matching the `email-playbook` standing lesson.

### Email 2 · same thread · 57 words

```
Quick context - Chamber were already running their own email when we started. We put SMS next to it and they paid on results for the first 30 days.

If yours is working, this sits next to it. If it's stalled, that's usually the reply handling, not the list.

Worth a look?
```

### Email 3 · new thread · subject `wrong time` · 48 words

```
{{firstName}} - probably caught you at a bad moment.

If outbound at {{companyName}} is handled, ignore this. If it's the thing you've been meaning to get to for a while, I'll send the pilot terms.

Want them?
```

"the thing you've been meaning to get to" is lifted from the Evergreen research — *"business has been good… we've just been meaning to do this for a long time."*

---

## Version B — external `cold-copywriting` skill (never states the signal)

Skill rules applied: ≤80 words, 2 lines per paragraph, exactly one question mark, no exclamations, no em dashes, subjects ≤3 words lowercase, E1+E2 share a thread, E3 is new. Core rule: **never state the signal — speak to what it means.**

### Email 1 · subject `third agency` · 52 words

```
{{firstName}} - most agencies running their own outbound end up on their third vendor before they stop blaming the list.

The copy usually isn't the problem. The replies come in and nobody answers them for two days, so they die.

Is that roughly where {{companyName}} is, or are you further along than that?
```

### Email 2 · same thread, no subject · 45 words

```
Chamber Media had the same setup - their own email running, decent copy, replies going cold.

We put SMS next to it and answered every reply inside the hour. 14 retainers in five months, and nothing about their targeting changed.

Familiar?
```

### Email 3 · new thread · subject `bad timing` · 48 words

```
{{firstName}} - I'll assume this landed at the wrong moment.

If outbound at {{companyName}} is already handled, I'll drop it. If it's the thing that keeps getting pushed to next quarter, there's a 30-day pilot where you only pay on results.

Want the terms?
```

**Two skill rules followed here that we would not ship as-is:** the skill bans naming your own company and bans signatures. Our `qa-checklist.md` has sender credibility as an **auto-fail (Q5)**, and our best-performing cold email carries a sig. Assume the sender block is appended by the sending profile.

---

## The axis decision

Version A states the signal on the plan's logic that it's the asset. Version B refuses to, on the skill's logic that stating it is the amateur move. That is a **second** test axis on top of mechanism on/off, and at ~1,500 per arm only one reads cleanly.

**Recommendation:** run **signal-stated vs signal-implied** on email — it tests the premise of the entire list — and carry mechanism on/off into the SMS layer on the winner.

---

## Blockers before send

Carried from Aaman's manual draft; all still open.

1. **"Ian Johnson, head of sales at Chamber Media"** — appears in no record we hold. Our Chamber contacts are Blake Wheeler / Stefan (discovery call) and Taylor Neuffer (CEO). Naming a real person at a client is checkable. **Confirm or cut** — currently cut from both versions.
2. **"14 retainers (74K MRR)" + "Since January"** — 14/74K is one of the contradicted number sets, and "since January" is a *seventh* timeframe (logged copy says "in 5 months"; Jan→Aug is seven). Used as written pending the lock; see the audit in `../REDIRECT-SIGNAL-CAMPAIGN.md`.
3. **"26 other marketing agencies"** — 26, 32 and 84 all appear in sent copy. Pick one.
4. **Retired opener** — "I'm sure you see a lot of these emails" is one step from "I know your inbox is full of agencies", which EMAIL-QA said to retire because six clients run it simultaneously. Cut from both versions.
5. **Pay-on-results** must be confirmed as genuinely offered before it ships in a P.S.
6. Neither version has been through the EMAIL-QA 5-point check. Nothing below 3/5 in that corpus has ever booked.
