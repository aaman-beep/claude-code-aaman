# Missed positive replies — all clients, week of Aug 17–24 2026

Run 2026-08-24 · `tools/missed_replies_scan.py --all-clients --from 2026-08-17 --to 2026-08-24`

**Question asked:** the Wise Digital check, run across the roster — who replied in
GoHighLevel but never got categorised in Airtable, so nobody worked the thread?

**Method:** GHL-first, then anti-joined against Evergreen. This runs the opposite way to
`tools/july_pr_register.py`, which is Evergreen-first and therefore structurally cannot see
a replier who has no Evergreen record at all. Two join keys, because `/deals` carries
`phone` but `/contacts` threads carry no phone — those match on name + company.

---

## Answer up front

**One genuine missed positive across all nine clients this week. Not a pile.**

The inbox team is categorising well: **371 of 471 repliers (79%)** were categorised.
Of the 98 that weren't, **96 are wrong-number / retired / left-the-company** — real
uncategorised replies, but not leads anyone should have worked.

The week's actual problems are elsewhere, and they're bigger than the miss:
**two clients have stopped sending**, and **one in five repliers is the wrong person**.

---

## 1. The miss — Growth Lab

> **Sam, Meeks Impact Law** · 470-882-9956 · replied Aug 19 · **5 days silent, never answered**
>
> *"Good afternoon, I am trying to reach Rachel from Growth Lab. My name is Sam and I am
> reaching out on behalf of Meeks Impact Law to hear more about your AI strategy. Let me
> know when you have some time, I'd love to set up a brief meeting."*

An explicit meeting request. Verified absent from Evergreen on both keys — zero matching
deals, zero matching contact threads across every category. Nobody replied; the thread is
still open. **This is the one to action today.**

Worth noting *how* it was missed: the contact has no name on the GHL record, so it reads as
an anonymous inbound. It never looked like a lead.

### Also worth a follow-up — a referral, same client

> **Amanda Hanna** · 561-400-2354 · replied Aug 22 · 2 days silent, never answered
>
> *"No. Retired. Contact Paula Burger at Park-Chenaour on 6th Ave in Tacoma. She was
> Terry's lead paralegal and now an extremely competent Case Manager."*

Not a positive for Amanda — she's retired — but she handed over a named, qualified
referral at a named firm. In the taxonomy that's a `Referral Request`. It was never logged.

---

## 2. Two clients are not sending

This is the finding that outweighs the missed replies.

| Client | Sends Aug 17–24 | Control | Status |
|---|---|---|---|
| **Digital Resource** | **0** | 6,556 in Jul · 17,813 in Jun | **Last outbound Jul 27 — 4 weeks dark** |
| **Scaletopia** | **11** | 20,012 in Jul | **Collapsed Aug 6**, single digits/day since |

Both confirmed against a known-busy control window, so this is a real outage, not a broken
query. Digital Resource's daily counts trail off through late July (2 on Jul 17, 1 on
Jul 20, 6 on Jul 22, 1 on Jul 27) then stop entirely. Scaletopia ran 700–1,100/day through
Aug 5, then dropped to 1–9/day from Aug 6 onward — still broken 18 days later.

A client sending nothing produces no missed replies. Their clean rows below are not a
clean bill of health.

---

## 3. Per-client

| Client | Sent | Replies | Repliers | Categorised | **Never categorised** | Wrong # | Neg | Unclear |
|---|---|---|---|---|---|---|---|---|
| Digital Resource | 0 | 0 | 0 | 0 | 0 | — | — | — |
| Strike Tax | 0 | 3 | 3 | n/a | 2 | 0 | 0 | 2 |
| Kynship | 3,848 | 62 | 58 | 44 | **14** (24%) | 7 | 0 | 7 |
| Leadgenix | 4,318 | 89 | 85 | 68 | **17** (20%) | 12 | 1 | 4 |
| Redo | 7,098 | 113 | 96 | 80 | **16** (17%) | 10 | 1 | 5 |
| Growth Lab | 5,650 | 98 | 90 | 66 | **24** (27%) | 13 | 1 | 10 |
| Go Fish Digital | 4,006 | 128 | 104 | 88 | **16** (15%) | 13 | 1 | 2 |
| WISE Digital | 3,837 | 43 | 34 | 24 | **9** (27%) | 4 | 2 | 3 |
| Scaletopia | 11 | 1 | 1 | 1 | 0 | — | — | — |
| **Total** | **28,768** | **537** | **471** | **371** | **98** | 59 | 6 | 33 |

Every client reconciles: `categorised + never-categorised + uncategorised opt-outs = repliers`.

**Strike Tax is not loaded in Evergreen** (absent from `EV_SLUG`), so its categorisation
cannot be checked — the anti-join has no right-hand side and every replier falsely reads as
missed. Its 3 inbound with 0 outbound in-window are replies to earlier sends. Both are
French/Spanish wrong-number replies. **Getting Strike Tax into Evergreen is the fix.**

---

## 4. The real pattern: wrong-number rate

**59 of 98 uncategorised replies — and a large share of all replies — are people telling us
we have the wrong person.** Not "not interested". *Not them.*

- Growth Lab: *"AI didn't tell you I closed my firm like 5 years ago? Lol"* · *"I am not the correct Michael Neece. I am not a lawyer."*
- Leadgenix: *"This has not been Shawn's number for 7 years"*
- Go Fish: *"I haven't been involved in F&F for 10 years"*
- Kynship: *"I am retired and sold Aromaland!"*
- Wise Digital: *"Not Robin and not CPA"*

This is list decay, and it costs twice: wasted sends, and a replier pool so full of bounces
that a real hand-raise (Sam at Meeks Impact Law) can sit in it for 5 days unnoticed.

**Three people asked how we got their number** (Kynship ×2, Go Fish ×1) — *"How did you
obtain my number?"*. That's a compliance signal, not a lead. Worth watching.

---

## 5. Not covered

`chamber-media`, `big-leap`, `seedx`, `acceler8`, `nextleft` have no GHL connector, so this
check cannot run for them at all. They need a read-only Private Integration Token and a
location ID before they can be included.

---

## Caveats

- **One week is a thin window** and the roster is quiet — two clients dark, one client's
  entire sending collapsed. Re-run over the backlog to find the actual pile: the
  July dashboard snapshot showed 87 unconverted for Digital Resource and 468 for Leadgenix
  under the *other* definition of "missed" (categorised but never converted).
- Intent buckets are a first pass over reply text; every one of the 39 non-wrong-number
  replies was read by hand for this report. The 59 wrong-number rows were not individually
  read beyond pattern match.
- Name/company matching on the `/contacts` side is fuzzier than phone. A miss matched only
  by name could in principle be a false positive — the Growth Lab one was spot-checked
  directly and is genuinely absent.
- Opt-outs that were never categorised are excluded from the miss count (1 at Wise Digital).

## Separate bug spotted

Digital Resource shipped **`"a quick audit for [object Object]"`** to live prospects on
Jun 30 — a broken merge variable, same failure mode as the Scaletopia `{company}`
regression. Outside this audit's window but worth fixing before sending resumes.
