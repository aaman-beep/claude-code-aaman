# Wise Digital → CPA firms | cold email campaign
**Ported from the Kynship email winner (EW1 / Evergreen copy 830). Strawman — redline it.**
Built 2026-09-02 · rev 2 (mechanism + structure per Aaman). Case study: Dark Horse CPAs (Evergreen case 222, tier S).

---

## 1. The bookings discrepancy — it's a counting bug, not a sync failure

**The data is in Evergreen and always was.** `/api/clients/{slug}/report` computes `booked` as
*"deals whose stage is currently `Meeting Booked`"*. But `stage` is a single current-state field,
not an event log — so the moment a meeting actually happens and the deal advances to `Show`,
`No Show`, `Won`, `Proposal Sent` or `Post Meeting Disqualified`, it **drops out of the booked
count**. The meeting still happened. `meeting_booked_at` is still populated. The report just
stops counting it.

The correct field is **`meeting_booked_at`**, not `stage`.

**Kynship email, counted properly:** 14 meetings, not the 0/1 the report showed per campaign.

| Campaign (db id) | Report says booked | Real meetings |
|---|---|---|
| business emails \| Google (717) | **0** | **4** (2 No Show, 2 Post-Meeting DQ — all Jul 29-30) |
| business emails \| Outlook \| new rev qual (803) | 1 | 1 |
| People list \| Outlook (904) | 0 | 2 |
| People list \| Google (905) | 1 | 2 |
| **EW1 copy family total** | **2** | **9** |
| Supplements \| Google + retargeting (77) | 1 | 4 |
| Household Goods (68) | 1 | 1 |

**So the EW1 copy family booked 9 of Kynship's 14 email meetings — and every single email meeting
since Aug 13 came from it:** Czech & Speake (Aug 13), Smile White (Aug 26), Lumity (Aug 28),
Jelly Drops (Sep 1), Windsor & Eton Brewery (Sep 2). That's the run you're describing, and it's
the strongest possible reason to port this copy.

The campaign I called "0 booked" — `business emails | Google` — actually booked 4 meetings in two
days. All four advanced past `Meeting Booked`, so the report zeroed them.

**This hits Wise harder than Kynship.** Wise has **53** deals with a real `meeting_booked_at`;
only **12** are still sitting in `Meeting Booked` stage. The report is undercounting Wise's
meetings by **41 — about 77% of them.** Their weekly KPI card ("1 booked, behind target") is
reading the same broken field.

**What to fix:** in the `/report` and `/stats` builders, count `meeting_booked_at IS NOT NULL`
within the period instead of `stage = 'Meeting Booked'`. Everything else about the endpoint is
fine. I have not touched the API — flagging it for whoever owns the Evergreen repo.

---

## 2. The winner we're porting, and why

**Evergreen copy 830 · `email-playbook/winners.csv` EW1 · status: winner**

> Hey, I know your inbox is flooded by agencies promising to grow {COMPANY}.
>
> But we recently took Purdy & Figg from GBP 452k to GBP 50m in 4 years, primarily via a mix of creator, UGC and customer-generated content at scale that turned them into a household brand.
>
> Figured I'd drop a note because we're crushing it in the UK scene rn (also working with Protein Works + Saltyface).
>
> Don't know if it's relevant at the moment, but can I walk you through what we did for them?
>
> Thanks, Cody Wittick | Founder & CEO, Kynship
> P.S. If this isn't relevant or of any interest at this point, reply back and I'll no longer contact you.

It beat a near-identical arm (EL1 / copy 831) on the same list in the same window; the only
meaningful difference was the **altitude of the mechanism line** — EW1 abstract, EL1
granular/throughput ("an engine that ships hundreds of top-performing assets a month" → 0 replies).
It is also, per §1, Kynship's booking engine on email right now.

---

## 3. The campaign

Structure per your call: **disarmer → case + mechanism + transformation → CTA.** The
"figured I'd drop a note / strong run in the space / also working with X + Y" beat is **cut**.

> Worth noting your instinct is backed by the data: Evergreen's own `why_it_worked` on Wise copy 19
> says *"Dark Horse CPAs is a name the whole niche knows and looks up to."* Purdy & Figg needed the
> Protein Works/Saltyface stack to establish credibility; Dark Horse doesn't. The case carries it alone.

### Subject line — spintax, `{COMPANY}` only

Kynship's live subject (campaign 1103, step 2542) is one spin block, lowercase, fragments not
sentences. Theirs leans on a Clay-built `{PRODUCT CATEGORY}` column. Wise doesn't have an
equivalent, so every slot below uses **`{COMPANY}` or static text only** — nothing that can
render empty. Eight slots, validated through `tools/spintax.py`:

```
{{COMPANY}<>WISE Digital|{COMPANY} referrals|dark horse cpas|{COMPANY} + organic search|referral ceiling|{COMPANY} pipeline|two offices to 50 locations|{COMPANY} growth}
```

| # | renders as | shape | why |
|---|---|---|---|
| 1 | `Dowell Group<>WISE Digital` | company <> sender | lifted from Kynship's slot 5; reads internal, not promotional |
| 2 | `Dowell Group referrals` | company + problem | the analogue of their `{COMPANY} creative gap` — points at the mechanism |
| 3 | `dark horse cpas` | bare name | see note below — the strongest one here |
| 4 | `Dowell Group + organic search` | company + solution | names the how instead of the problem |
| 5 | `referral ceiling` | bare problem | shortest; the confirmed pain in two words |
| 6 | `Dowell Group pipeline` | company + stake | their word, not ours — "pipeline" is what partners actually say |
| 7 | `two offices to 50 locations` | bare transformation | curiosity with no company name at all |
| 8 | `Dowell Group growth` | company + outcome | plainest fallback; safe, unremarkable |

**Slot 3 is the one I'd bet on.** Evergreen's `why_it_worked` on Wise copy 19 says *"Dark Horse
CPAs is a name the whole niche knows and looks up to."* That makes a bare-name subject work the
same way Chamber Media's ClickUp subject does (copy 41: *"the ClickUp ad is a recognisable
artifact — no mechanism needed, the work speaks for itself"*). It's the only slot here carrying
recognition rather than description.

These rotate for inbox variety — they are **not** an A/B. Bison picks one per send at random, so
you get eight different-looking subjects hitting the same domain, which helps placement. If you
want a real subject test, cut to two slots and read them separately.

**Dropped `per dark horse`** — "per X" implies a prior conversation, and on a cold list the reader
clocks that on open. Say the word and it goes in as slot 9. Left bare `cpa` out too: it describes
the reader, not the email, so it reads like a list name.

### Ship-ready spintax — EMAIL 1

Merge tags are EmailBison uppercase convention, matching Kynship. **4,374 variations.**

```
{Hi|Hey}, I know {you're pitched by|you're constantly pitched by|your inbox is full of} marketing agencies {promising to grow|promising growth for|pitching growth for} {COMPANY}.

But {we recently grew|we recently helped grow|we recently scaled} Dark Horse CPAs from $1.5m to $21m in 5 years, {primarily by using organic and AI search so the right clients found them, rather than their growth being capped by what referrals could send|mostly by using organic and AI search to bring in the clients they actually wanted, instead of waiting on referrals to send them|largely by getting them off referral dependence and into organic and AI search, so the clients they wanted came to them directly} - which took them from a two-office practice into a 50-location national firm.

{Not sure if this is relevant at the moment, but could I walk you through what we did for them?|No clue if it's relevant atm, but could I walk you through what we did for them?|Don't know if it's relevant right now, but mind if I walk you through what we did for them?}

{Best,|Cheers,|Thanks,}
{SENDER_EMAIL_SIGNATURE}

P.S. If this isn't relevant or of any interest at this point, {reply back|let me know|respond} and I'll no longer contact you.
```

The three mechanism spins are #4, #1 and #2 from the table below, so the slot A/B's itself.
Opening verb never spins to "took" — that would collide with your "which took them from".

---

### Ship-ready spintax — FOLLOW-UP (step 2, `Re:` + same subject, `thread_reply: true`)

Kynship added an objection pre-empt as step 2 on Sep 1 — *"You're probably assuming this only
works once you're already big… Purdy & Figg were at GBP 452k when we started."* Direct analogue,
and true: Dark Horse were two offices when Wise started. **2,187 variations.**

```
{You're probably assuming|My guess is you're assuming|Suspect you're assuming} this only works {once you're already one of the bigger firms|once you're already a big firm|when you're already one of the larger firms}.

Dark Horse were {two offices|a two-office practice|at two offices} when we started btw - {the growth came from search, not from adding partners|it came from search, not from hiring more partners|that growth came off search, not off adding partners}.

{No pressure at all|No pressure either way|Zero pressure} - just wondering if this sounds interesting or if it's {a complete miss|a total miss|completely off}?

{Best,|Cheers,|Thanks,}
{SENDER_EMAIL_SIGNATURE}
```

This replaces the old F2/F3/F4 ladder — Kynship's live winner runs two steps, not four, and the
step-2 objection pre-empt is doing more work than a generic bump would. F3/F4 below are optional.

---

### The mechanism slot — pick one

You didn't like "replacing referrals with organic search," and you're right: it makes referrals
the enemy when CPAs *like* referrals, and it says nothing. The reframe below makes the
**dependence** the problem, not the referrals — and puts the payoff on **the clients they wanted**,
which is Wise's own confirmed pain language (*"We don't get enough of the right type of clients"*,
*"Not attracting enough right-fit clients"*, *"Too many low-quality or wrong-fit leads"*).

| # | Line |
|---|---|
| **1** | by using organic and AI search to bring in the clients they actually wanted, instead of waiting on referrals to send them |
| **2** | by getting them off referral dependence and into organic and AI search, so the clients they wanted came to them directly |
| **3** | by taking the pressure off referrals and letting organic and AI search bring in the kind of clients they actually wanted |
| **4** | by using organic and AI search so the right clients found them, rather than their growth being capped by what referrals could send |
| **5** | by building a way to bring in the clients they wanted without waiting on referrals — organic and AI search doing the work referrals used to |
| **6** | by making referrals the bonus rather than the engine — organic and AI search brought in the clients they actually wanted |

**My pick: #4.** *"rather than their growth being capped by what referrals could send"* is almost
verbatim a confirmed Wise pain — **"We can only grow as fast as referrals allow"** (Partner/Wealth
persona). It's mined, not invented, and it names the ceiling without insulting referrals.
**#1** is the safest/plainest if you want less editorial.

⚠ **One accuracy call for you.** Dark Horse's growth ran over 5 years; AI search (GEO) is recent,
so crediting their $1.5m→$21m partly to *AI* search is slightly anachronistic. Three ways to play it:
keep it as-is (it describes what Wise does today and the mechanism is the pitch); drop to "organic
search" for the Dark Horse claim; or split it — *"…by organic search, and now AI search on top of
it for firms starting today."* It's defensible either way, but it's the one line a sharp CPA could
poke at, so it should be your decision, not mine.

---

### Optional later steps

**F3 — day 8 (optional)**
> Hi {first_name}, timing thought.
>
> Once the Oct 15 extension deadline clears, most firms we speak to go quiet until January — and that stretch is when next year's pipeline either gets built or doesn't. That's the window we'd be working in.
>
> Worth 15 minutes before then?
>
> Patrick Dillon | Founder/CEO, WISE Digital Partners (Inc. 5000)

**F4 — day 15, breakup**
> Hi {first_name}, I'll leave it here.
>
> If it's ever useful, the Dark Horse write-up is yours — reply "send it" and I'll pass it over, no call attached.
>
> Thanks, Patrick
>
> P.S. If you'd rather I didn't follow up again, just reply back and I'll close the file.

---

## 4. QA

| Check | Status |
|---|---|
| Doesn't repeat EL1's losing move (granular throughput mechanism) | ✅ mechanism sits at EW1's altitude |
| Mechanism reframed off "replacing referrals" | ✅ dependence is the problem, not referrals |
| Payoff uses confirmed pain language ("the clients they wanted") | ✅ three confirmed Wise pains |
| Numbers traceable | ✅ $1.5m→$21m / 50+ locations is Wise's own live-copy figure; case 222 |
| No invented geography or scene claim | ✅ beat removed entirely |
| Pre-empts "our agency doesn't understand accounting" (confirmed pain) | ✅ CPA-only case, no generic-agency language |
| Pre-empts "digital can't drive serious accounting clients" (confirmed belief) | ✅ $21m / 50 locations is the counter-example |
| Name-drop permission | ✅ moot — logo stack cut. Capstone/Deblanc are safe if ever re-added; **Gurian, Han Group, Seamless, Rock Solid are Scaletopia-closed clients, not published case studies — don't name without Wise's OK** |
| Subject matches Kynship's shipping format | ✅ lowercase spin block, 8 slots, fragments — all validated through `tools/spintax.py` |
| Merge-var safety | ✅ **no Clay variables anywhere** — subject and body use only `{COMPANY}` and `{SENDER_EMAIL_SIGNATURE}`. Nothing can render empty the way Wise's live copy does ("Checked out and saw you…", "Put together a couple ideas for .") |
| Opt-out present | ✅ |

---

## 5. Saved to Evergreen
Rev-2 copy saved as draft against `wise_digital` — **copy 1232** (mechanism #4) and **1233**
(mechanism #1), with disarmer / case_line / unique_mechanism / identity / cta components broken out.
Rev-1 drafts 1229-1231 are superseded. Not yet linked to a campaign
(`POST /api/copy/link` once the EmailBison campaign exists).

Raw spintax also at `clients/wise-digital/output/wise-cpa-email-spintax.txt` for paste into Bison.

**Note:** there is no `emailbison-wise-digital` MCP connector, so unlike Kynship I could not read
Wise's live Bison sequence or confirm their real merge-tag names. Tags above follow EmailBison's
uppercase convention as seen in Kynship campaign 1103. Check them against Wise's actual list
columns before launch.
