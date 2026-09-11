# LinkedIn InMail Drafts — Scaletopia (ecom-focused marketing agencies)

**Case:** Chamber Media · **Persona:** ecom-focused agency founder/owner · **Built on:** the winning cold-SMS variant in [batches.json](batches.json) (1,748 prospects · 2.69% reply · 1.66% opt-out · `burner: false`) + the house [Voice Profile](../../../sms-playbook/Cold-SMS-Voice-Profile-Scaletopia.md).
**Date:** 2026-07-29 · **Channel rules:** LinkedIn InMail (short subject, ~60–90 word body, one soft "?" CTA, senior audience) × house Voice Profile (absolutes only, **no %**, native unit = retainers/clients, no small-talk filler).

> Adapts the winner into a softer register: the clipped two-text SMS → a warmer, fuller InMail; keeps the four things that made it rip — **peer proof (Chamber Media, 18 retainers/8 months)**, the **capped-intake status flip**, the **relevance bridge**, and **pay-on-results risk reversal** — and keeps the soft CTA pointed at the idea, not a hard meeting slot.

## Variables
`{{firstName}}` · `{{company}}` · `{{their_niche}}` (the kind of brands they serve, e.g. "ecom brands"). Sender = **Mel, Scaletopia** *(lock the real sender name/handle before send)*.

---

## V1 — Peer proof + capped intake  *(the ripper, softened · lever: status/scarcity + risk-reversal)*
**Subjects (pick 2 to A/B):** `18 retainers in 8 months` · `quick idea for {{company}}` · `capped intake`

> Hi {{firstName}},
>
> Quick one — we recently helped Chamber Media sign 18 retainers in 8 months from outbound, to the point they've actually capped their client intake.
>
> Saw {{company}} works with ecom brands too, so I think you could get similar results. We can run it on a pay-on-results basis, so there's no real risk on your end.
>
> Worth a quick look to see if it'd work for you?
>
> – Mel, Scaletopia

*~70 words · proof → status flip → relevance → risk-reversal → soft CTA. Closest to the live winner.*

---

## V2 — Value-give / "not a pitch"  *(lever: generosity / low-threat)*
**Subjects:** `not a pitch` · `idea for {{company}}` · `how Chamber did it`

> Hi {{firstName}},
>
> Not trying to win your business here — but we just got Chamber Media to 18 signed retainers in 8 months on outbound, enough that they've capped intake, and I had an idea that could work for {{company}}.
>
> Happy to walk you through exactly how we did it, and how I'd run it for an agency in your space — take it and run with it if it's useful.
>
> Would that be worth a quick chat?
>
> – Mel, Scaletopia

*~75 words · disarm ("not a pitch") → proof → value-give → soft CTA. Lowest-threat of the three.*

---

## V3 — Curiosity / "had an idea" + mechanism  *(lever: curiosity + specificity)*
**Subjects:** `been looking at {{company}}` · `an idea` · `{{their_niche}} + outbound`

> Hi {{firstName}},
>
> Been looking at {{company}} and had an idea I think could work well for you.
>
> We book Chamber Media meetings with brands like AthleanX (spending $10m a year on ads) using signal-based outbound — reaching the right people the moment they're in-market. For {{company}}, I'd go after your ideal clients the same way.
>
> Could I show you how it'd work?
>
> – Mel, Scaletopia

*~65 words · curiosity opener → mechanism + logo proof → relevance → default soft CTA ("could I show you how?").*

---

## QA / honesty
| Claim | Status | Note |
|---|---|---|
| **Chamber Media — 18 retainers in 8 months** | carried from live winner | already ran in-market on SMS; confirm it's the number Mel will defend |
| **"capped their client intake"** | ⚠ confirm | keep only if true/defensible — it's the status flip that makes V1/V2 land |
| **pay-on-results model** (V1) | ⚠ confirm offered | core to the risk-reversal; drop the line if the offer isn't actually pay-on-results |
| **AthleanX "$10m/yr on ads"** (V3) | ⚠ confirm | logo-drop from the winning-templates DB (#13); confirm defensible before send |
| **"signal-based outbound"** (V3) | mechanism framing | light touch only — the winner omitted an explicit mechanism; don't force it |
| Voice gates | ✅ | no %/decimals, native unit = retainers/clients, one soft "?" CTA, no small-talk filler |

**Burned patterns avoided (from the send log):** no "cracked the code" opener (was a `burner`), no "could I drop you an email?" CTA (flagged *avoid* in winners.csv W15).

## Register shift: SMS → softer InMail
- Fuller sentences, spelled-out "you / let me know" (dropped SMS "u / lmk"), warmer peer tone — **but zero small-talk filler** ("hope your week's going well" stays banned).
- Kept from the house voice: absolutes only, no %, native unit = retainers/clients, plain-language "closer-on-a-call" test, one soft CTA ending in "?", human over clever.
- Length tuned to ~60–90 words (InMail allows ~1,900 chars, but shorter converts); subjects short and lowercase-ish, like the email subjects.

## Recommendation
- **A/B the first touch:** V1 (the softened ripper) vs V2 (value-give). Subjects: test `18 retainers in 8 months` vs `not a pitch`.
- Hold V3 as the challenger — it swaps in the mechanism + a bigger logo, useful if the peer-proof angle fatigues.
- **Single InMail each** for this pass (per the brief). When you're ready, I can add a 2nd-touch follow-up InMail per variant (same thread, changes the value prop — e.g. a capacity/"only taking a couple" frame or a specific in-market signal for {{their_niche}}).
- Before any send: confirm the three live claims (18 retainers / capped intake / pay-on-results) and lock the sender name.
