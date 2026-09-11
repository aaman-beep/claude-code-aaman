# Strike Tax — Copy that landed the Won / Proposal / Next-Stage leads

**Date:** 2026-07-17 · Source: GHL SMS threads (ghl-strike-tax `export-messages`) + Airtable CRM (Master Inbox & CRM → Deals) for source/stage attribution.
**Coverage:** 13 pipeline leads. **10 were SMS-sourced** (full copy below). **3 were EmailBison-sourced** (no GHL SMS copy — flagged; pull from `emailbison.json` if needed).

---

## The headline: the winners were NOT the frozen "salaries likely qualify" blast
The copy that actually opened these deals falls into three named families — all **vertical-paired peer proof + a real dollar number + success-fee risk-reversal + a soft "10-min chat" CTA**. The generic burner template (§ Family D) mostly shows up as the **June re-target blast** that hit already-won contacts with the credibility leaks. And in every case, **a human setter handled the objection and booked "with our director Paul"** — the SMS opened the door; the conversation closed it.

### Family A — "Peer $2.7M / 10-min chat" (won the Machinery deals)
> **T1:** "Hi {name}, [I know this is wayy too random but] the Section 174 repeal means {company} could recover around at least **$750k** in retroactive R&D credits for 2022-2024."
> **T2:** "We helped **another {same vertical}** receive **$2.7M** in credits on a success based fee - **worth a 10-min chat** to run some numbers?"

Landed: **Kyle Hyland (WON)**, **Mark Winkelman (WON)**, **Taylor Miller (WON)**, **Eric Jacob (Proposal)**. Vertical-paired every time ("another industrial automation company", "another industrial coating companies", "another industrial touch companies", "another precision machining").

### Family B — "SecureCircle / CrowdStrike $668–688k" (won SaaS + Cyber)
> **T1:** "Hi {name}, it's Erika from Strike Tax - your {dev/eng} team's salaries at {company} likely qualify for R&D tax credits going back 3 yrs. we recently helped **SecureCircle (acquired by CrowdStrike) claim $668k** for 2022-2024"
> **T2:** deadline / "want a quick estimate? (success-fee)"

Landed: **Ashwin Swamy (WON, Cyber)**, **Tyler Andersen (WON, SaaS — variant: "$250k for RunDiffusion… we helped CrowdStrike receive $688k")**, **Shiv Gupta (Proposal)**, **Jamie Ahern (Proposal)**, **Claudia Belcsak (Next)**.

### Family C — "processes / technical problems + TX manufacturer $657k" (softer industrial)
> **T1:** "…the work your team puts into **developing processes and solving technical problems** likely qualifies for r&d tax credits - we helped **a manufacturer in texas** doing the same claim **$657k** for 2023-25"
> **T2:** "I think {company} could be sitting on something similar - lmk if it's worth exploring? …we only charge if we deliver"

Landed: **Brian James (Next)** — his *good* opener (Mar 30), before the June re-blast.

### Family D — the generic frozen blast (the June re-target, carries the leaks)
> "Hi {name}, it's **Cortney/Courtney** from Strike Tax - your engineering team's salaries at {company} likely qualify… recently we helped **Atlantis Industries Corporation claim $1.2M** for 2022-2024" + "federal deadline on **July 6 to claim credits for 2022, 23, and 24 all at once**"

This is the one the [COPY-AUDIT.md](COPY-AUDIT.md) flagged: **Atlantis $1.2M is a fabricated number** and **"claim 22/23/24 all at once" is the false-deadline leak**. It was **re-blasted at already-won / already-engaged contacts** (Kyle, Mark, Eric, Brian) months after they converted → see hygiene finding below.

---

## Per-lead detail

### WON (6)
| Lead | Company | Vertical | Channel | Opener that landed them |
|---|---|---|---|---|
| **Kyle Hyland** | Blackrock Automation | Machinery | SMS | Family A ("$750k… another industrial automation company $2.7M… 10-min chat"). Replied "Sure" → booked w/ Paul. *(Re-blasted Family D Jun 16 — after already Won.)* |
| **Mark Winkelman** | Professional Coating | Machinery | SMS | Family A ("wayy too random… $750k… another industrial coating $2.7M"). No-showed once, re-engaged, booked. *(Re-blasted Family D + Atlantis $1.2M Jun 30.)* |
| **Taylor Miller** | Faytech N.A. | Machinery | SMS | Family A ("another industrial touch companies $2.7M"). "Sure, happy to discuss" → booked w/ Paul. |
| **Ashwin Swamy** | Omega ATC | Cybersecurity | SMS | Family B (SecureCircle $688k). Objection "we only do integration, not software dev" → handled → chili-piper booking link. |
| **Tyler Andersen** | RunDiffusion | SaaS | SMS | Family B variant ("$250k… we helped CrowdStrike $688k, Erika, Inc.5000"). "Sounds promising, how is that possible?" → booked 2pm same day. |
| **Brady Wagstaff** | Uplink Robotics | Machinery | **EMAIL** | **EmailBison** (Machinery New Mailboxes). No SMS copy — pull from `emailbison.json`. |

### PROPOSAL SENT (3)
| Lead | Company | Vertical | Channel | Opener |
|---|---|---|---|---|
| **Eric Jacob** | Micron Precision Machining | Machinery | SMS | Family A ("another precision machining $2.7M"). Objection "not design responsible" handled beautifully over weeks ("another contract shop pulled $340k on fixture/process work") → booked 9am. *(Re-blasted Family D Jun 17.)* |
| **Shiv Gupta** | Breakout Learning | SaaS | SMS | Family B (SecureCircle $668k + July-6 deadline, V6). "Sure" → Paul sends estimate. |
| **Jamie Ahern** | Parabolic Auto | SaaS | SMS | Family B ("SecureCircle pre-CrowdStrike $688k"). Asked fee → "20% success-fee" → "Let's have a chat" → booked. |

### NEXT STAGE (4)
| Lead | Company | Vertical | Channel | Opener |
|---|---|---|---|---|
| **Brian James** | Electrical Apparatus & Machine | *industrial, tagged SaaS V5* | SMS | Family C ("TX manufacturer $657k") Mar 30 → "How did you find me?"; then **re-blasted Family B** Jun 5 → "Sure send me a little something". ⚠ industrial co. mis-tagged into a SaaS campaign. |
| **Claudia Belcsak** | Veridium | SaaS | SMS | Family B (SecureCircle $668k). Objection "**R&D is UK-only, not US**" → US-contractor angle → booked. ⚠ likely **out-of-ICP (UK R&D)** but advanced anyway. |
| **James Geyer** | AccountAim | SaaS | **EMAIL** | **EmailBison** (SaaS V4&V5 Google test). No SMS copy. |
| **Jose Luis Lopez** | JLS Industrial | Machinery | **EMAIL** | **EmailBison** (Machinery New Mailboxes). No SMS copy. |

---

## What this says (for the autopsy)
1. **We have a proven winner and it isn't the one we scaled.** Family A/B/C (vertical-paired peer proof + real number + 10-min chat) opened every SMS win. The frozen "salaries likely qualify" blast we put 40k+ prospects behind is Family D — the *re-target* copy, carrying the fabricated Atlantis number and the false July-6 line.
2. **Retargeting hygiene failure.** Kyle (Won Jan), Mark (Won Feb), Eric (Proposal), Brian all got re-blasted the generic leak-carrying template months later — i.e. we spammed our own converted/engaged contacts with our worst copy.
3. **The human setter closed, not the automation.** Every advance came from real, conversational objection-handling ("not design responsible", "integration only", "R&D is UK-only") and a booked call with "director Paul." That skill is the asset; the opener is just the key.
4. **Channel reality:** 10 of these 13 top deals were **SMS-sourced** (incl. 5 of 6 wins); only 3 came via email. (Consistent with the autopsy: email *converts* positives at a higher rate, but SMS *generated* more of the actual meetings.)
5. **ICP leakage reaches the pipeline, not just the top:** an industrial co. tagged into SaaS (Brian), and a UK-only-R&D company advanced to Next Stage (Claudia).
