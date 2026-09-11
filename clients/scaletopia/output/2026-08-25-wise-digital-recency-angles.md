# Recency angle — WISE Digital case, W13 shape

**STRAWMAN — redline me.** 2026-08-25. For `Scaletopia - ICP Hook Enriched | 25-500E | NA`.

Built on [W13]'s skeleton (`"been looking at {company} and had an idea"` → case → `"I'd go after
{ICP_signal}"` → soft CTA), with the WISE Digital result swapped in for Chamber. The bite is
**recency** — a result that landed weeks ago, not 8 months ago.

## What's verified (Evergreen `/api/clients/wise_digital/deals`)

| claim | status |
|---|---|
| **8 retainers** | ✅ exactly 8 `Won` deals |
| **driven by text** | ✅ 6 of 8 are `channel: sms` |
| **text + email together** | ✅ campaign is literally `Engage Campaign \| SMS + Emails` |
| "during summer months" | ⚠️ **partly** — dated wins are Mar 26 ×2, Jun 22, Jul 6, Jul 16. Honest version: **8 since March, 3 over the summer** |
| "$380K annual" / "$34K MRR" | ❌ **unverified** — `closed_amount` is `$0` on all 8. Also conflicts with the already-sent *"close 260K USD in contracts"*, and 380K ≠ 34K×12 |
| "combining text with **calling**" | ❌ **not supported** — no calling anywhere in the Won threads; WISE's logged mechanism is local SEO. Replaced with text + email |

**Before sending:** confirm the revenue figure (or drop it — V1–V4 don't need one) and settle
260K vs 380K. This is how Chamber ended up with 13 conflicting versions.

---

## The variations

All: `took a look at {company} and had an idea` disarmer · one question mark · no `AI-timed`,
no `could do the same`, no email-handoff CTA · ≤250 chars.

### V1 · Recency-led — *lead recommendation*
```
T1: Hi {first_name}, took a look at {company} and had an idea. We just helped WISE Digital
    sign 8 retainers since March - 3 of those landed over the summer.

T2: for you guys I'd go after {ICP_signal}, texting and emailing them together.
    could I show you how?
```
Both numbers true, and "3 landed over the summer" is the recency beat without overclaiming.

### V2 · Summer-only — tightest recency
```
T1: Hi {first_name}, had a look at {company} and had an idea. WISE Digital signed 3 new
    retainers over the summer off our texts, while everyone else went quiet.

T2: for you guys I'd go after {ICP_signal}. could I show you how?
```

### V3 · Quiet-season contrast
```
T1: Hi {first_name}, took a look at {company} and had an idea. Summer's usually when this
    dries up - WISE Digital signed 3 retainers straight through it on text + email.

T2: I'd run the same at {ICP_signal} for you. could I show you how?
```
Strongest frame of the five: agencies *know* summer goes quiet, so the result does double duty
as proof and as timing.

### V4 · Number-forward, no timeframe risk
```
T1: Hi {first_name}, been looking at {company} and had an idea. We've put 8 retainers into
    WISE Digital Partners since March, mostly through text.

T2: for you guys I'd go after {ICP_signal} the same way. worth a look?
```
Safest — nothing here can be contradicted by the deal record.

### V5 · Your shape, revenue slot open
```
T1: Hi {first_name}, took a look at {company} and had an idea. We helped WISE Digital close
    8 retainers since March ({REVENUE}) by running text and email together.

T2: for you guys I'd go after {ICP_signal}. could I show you how?
```
⚠️ Do not ship until `{REVENUE}` is confirmed.

---

## Why this beats the Chamber line

The running T1 leads on *"Chamber Media sign 18 retainers in 8 months"* — a result that closed
months ago, from a client every one of these prospects has now been told about across 29k+ sends.
WISE is **fresh proof, same niche-adjacent buyer, and recent enough to be checkable.** It also
sidesteps the Chamber number contradiction entirely.

## Run it

Slot V1 or V3 against **A · Named-target** from
[2026-08-25-icp-hook-refreshed-angles.md](2026-08-25-icp-hook-refreshed-angles.md) — same
skeleton, different proof, so the test reads as *which case study carries* rather than
*which structure works*. Read on **opt-outs per positive** (baseline 7.2:1).
