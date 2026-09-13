# Quality Bar and QA Self-Check

This is the accuracy contract for the brief AND the checklist for the Step 8 Internal QA pass.

The skill applies these checks BEFORE the strategist sees anything. The point is to catch generic statements, unsourced claims, and fake-verbatim quotes internally — not to make the strategist catch them.

> A claim backed by an **Evergreen** mined item (confidence-scored, traced to a source call) counts as sourced — cite it like any other source. Prefer confirmed-confidence Evergreen items; mark `needs_more` ones as unverified, same as a single-source Master Sheet row.

---

## The Four Tests

Every claim in the brief must pass all four tests. If a claim fails, it gets rewritten or removed.

### Test 1 — Pattern-level specificity

The brief describes the COMPOSITE buyer for this client's segment, built from COMMONALITY observed across multiple sources. Every claim sits at the pattern level — not too generic, not too narrow.

Two sub-tests run together:

#### Test 1a — Not too generic

**Question:** Would this statement apply to 90% of buyers in any industry?

**If YES → FAIL.** Too generic. The statement is filler — true of everyone, useful to nobody. Rewrite with the segment-specific pattern, or drop.

**Anti-pattern library (too generic):**

- "CaC is high"
- "They struggle with lead generation"
- "Competition is fierce in their market"
- "They want more pipeline"
- "They care about ROI"
- "They're under pressure from leadership"
- "They've tried agencies before and been disappointed"
- "They want results faster"
- "They're skeptical of cold outreach"
- "Their team is overworked"
- "They want to scale"
- "They want better attribution"

#### Test 1b — Not too specific (the new one)

**Question:** Is this claim a single-prospect, single-moment data point that doesn't generalize across the segment?

**If YES → FAIL.** Too specific. This belongs in a citation (as evidence supporting a pattern), not as the headline claim itself. Rewrite at the pattern level OR demote the data point to a supporting citation under a pattern-level claim.

**Anti-pattern library (too specific):**

- "Brand X's blended CAC went from $89 to $134 in Q3"  (one company, one quarter — not a pattern)
- "Prospect at company Y said they have a board meeting in 6 weeks"  (one prospect's calendar, not a category trait)
- "Their CMO can't tell which of 4 paid channels drove $1.2M in Q3"  (single instance — doesn't characterize the segment)
- "BloodCat A1A7 1.1.2 had issues with iOS attribution"  (too narrow to mean anything to the next prospect)

These items can still appear in the brief — but as CITATIONS supporting a pattern claim, not as the claim itself.

#### The right level: the pattern

**A good claim describes a pattern observable across multiple sources for this segment.** It generalizes to the segment but is specific to it — wouldn't be true of other industries.

**Worked examples (DTC health & wellness segment):**

❌ Too generic: "CaC is high"
❌ Too specific: "BloodCat's CAC went $89 → $134 in Q3 due to iOS"
✓ Right: "DTC health & wellness brands at $5-30M ARR are seeing 30-60% blended CAC inflation post-iOS attribution changes, compounded by regulatory creative restrictions specific to supplements/wellness"
  - [pattern observed in 5 of 7 sales transcripts, Master Sheet Tab 2 row for DTC Health & Wellness, 12 Reddit threads in r/ecommerce]
  - Supporting citations show the specific instances (e.g., "BloodCat $89→$134" as ONE data point under this pattern)

❌ Too generic: "They struggle with lead gen"
❌ Too specific: "Brand X's demo requests dropped 240→95 after AI Overview"
✓ Right: "Mid-size DTC health brands are seeing organic discovery collapse — AI Overview and zero-click search compressing the long-tail informational keywords that historically drove top-funnel traffic"
  - [pattern observed in 4 transcripts; corroborated in Master Sheet; G2 reviews of competing tools mention same concern]

❌ Too generic: "They want better attribution"
❌ Too specific: "Brand Y's CMO can't allocate $1.2M across 4 channels"
✓ Right: "Marketing leaders in this segment are losing confidence in per-channel attribution post-iOS; they're shifting toward MMM or blended CAC views and need agencies who speak that language"
  - [pattern across 3 transcripts; one Reddit thread series in r/marketing]

**The test for pattern-level:**

Read each claim and ask two questions:
1. "Could I swap in any other industry's name and this would still be true?" → if YES, too generic (1a).
2. "Is this true ONLY of one prospect or one moment — would another buyer in the same segment NOT recognize this?" → if YES, too specific (1b).

The right claim sits in the middle: TRUE for buyers in this segment, NOT TRUE for buyers in other industries, supported by EVIDENCE FROM MULTIPLE SOURCES.

### Test 2 — Traceability

**Question:** Does every claim have a source citation?

**If NO → FAIL.** Remove the unsourced portion.

The skill never produces a claim without a source. There are no "general knowledge" assertions about the buyer's industry that don't trace back to a transcript, a Master Sheet row, a Reddit thread, or a similar source.

**Format requirement:** Every claim has an inline citation like:
- `[source: transcript-prospect-name-date.docx, ~12:34]`
- `[source: Master Sheet Tab 2, row 7 "B2B SaaS"]`
- `[source: reddit.com/r/marketing/comments/xyz123]`
- `[source: G2 review for HubSpot, posted 2024-09]`

If you wrote something and there's no citation, you either invented it or you need to find the source.

### Test 3 — Verbatim

**Question:** Does every quoted phrase appear VERBATIM in a real source?

**If NO → FAIL.** Either find the verbatim version, or remove the quotation marks and rephrase as paraphrase.

**What counts as a quoted phrase:**
- Anything wrapped in "double quotes"
- Anything attributed to "they say..." or "the buyer described it as..."

**What doesn't need to be verbatim:**
- Paraphrased descriptions you wrote in your own words
- Summaries of multiple sources combined

**Common failure:** You read a transcript where the prospect said "I'm being squeezed on cost per acquisition lately," and you wrote in the brief: "they say their CAC is crushing them." That's paraphrased. Drop the quote marks.

Verbatim quoting is the highest-leverage thing about Field 3 (Their Language). Fake quotes destroy the whole point of the field.

### Test 4 — Rule of Two

**Question:** For pain points, language quotes, and service hidden objections — does the item appear in ≥2 sources, OR is it Tier 1 (transcript) alone?

**If NO (single Tier 2 or Tier 3 source) → FLAG as `[unverified — needs corroboration]`**.

This is your defense against the "AI takes the Master Sheet literally" failure mode. Items appearing only in Master Sheet Tab 2 without any transcript or other corroboration get explicitly marked as unverified — the strategist sees the flag and decides whether to trust it.

Items appearing only in a single Reddit thread without other corroboration also get flagged.

Tier 1 items (transcripts) can stand alone because they're live buyer data — the highest-fidelity source. But even Tier 1 single-source items are worth flagging if you only have 1 transcript and the field calls for a recurring pattern.

---

## The QA Pass Workflow

When you reach Step 8 in the SKILL.md workflow, do this:

For each filled field in the brief:

1. **Run Test 1 (Specificity)** on every sentence/claim.
   - If FAIL: try to rewrite with sharper evidence from your existing source extractions. If you can't find sharper evidence, mark the claim as `[needs sharper source — currently too generic]` or drop it.

2. **Run Test 2 (Traceability)** on every sentence/claim.
   - If FAIL: either add the citation (you may have it but forgot to include) or remove the unsourced portion.

3. **Run Test 3 (Verbatim)** on every quoted phrase.
   - If FAIL: drop the quote marks and rephrase as paraphrase, OR find the actual verbatim version in your sources.

4. **Run Test 4 (Rule of Two)** on Field 2, Field 3, Field 4a, Field 4b items.
   - If FAIL (single Tier 2/3 source): add the `[unverified — needs corroboration]` tag inline.

After all four tests, produce a **QA Report** to include in the brief's appendix:

```
QA PASS SUMMARY
- Field 1: 4/4 tests passed
- Field 2: 5 pain points checked. 4 passed all tests. 1 flagged unverified.
- Field 3: 14 verbatim quotes checked. 13 passed. 1 rewritten as paraphrase.
- Field 4a: 3 beliefs checked. All passed.
- Field 4b: 5 objections checked. 4 passed. 1 flagged unverified (Reddit-only).
- Field 5: passed all tests; transcript phrasing replaced Master Sheet seed.
- Field 6: passed.
- Field 7: GAP — no prior campaign data for this segment.

REWRITES THIS PASS:
- Field 2 #3 was originally "CaC is creeping up" — too generic. Rewritten to: 
  "Blended CAC jumped from $89 to $134 in Q3 after iOS attribution loss" 
  [source: transcript-007.docx, ~18:45]

DROPS THIS PASS:
- Field 3 had a quoted phrase "we need to grow faster" which appears nowhere 
  verbatim in any source. Dropped.
```

The strategist sees this QA report alongside the brief — so they know what the skill caught and how to interpret the flags.

---

## What this is NOT

This QA pass is NOT for:

- Style edits (those happen at Layer C / writer's QA)
- Layer B angle decisions
- Picking the psychological lever (that's Layer C)
- Selecting which case studies to feature (that's Layer B / sms-synthesis)
- Filter scenarios F1-F7 (those are the broader QA gate AFTER copy is written)

This QA pass is ONLY about whether the buyer evidence in the brief is accurate, specific, and traceable.

---

## Failure modes to watch

If the same field keeps failing across multiple iterations, the issue isn't the QA pass — it's upstream:

- **Field 2 keeps producing generic pains:** the transcript extraction step (Step 3) is missing the specific moments. Sharpen `transcript-analysis.md` and re-extract.
- **Field 3 keeps having paraphrased "quotes":** you're not actually reading transcripts carefully enough. Slow down, re-read with quote-extraction in mind.
- **Field 4b keeps coming up empty:** you don't have enough transcripts. Flag it back to the user — they need to record more.
- **Field 5 keeps reading like the Master Sheet:** transcripts didn't surface dream-outcome statements (maybe the salespeople didn't ask the right questions). Note this pattern and mention it to the user as a discovery-call coaching opportunity.

If a failure pattern persists across multiple briefs for different clients, it means the SKILL.md or this Blueprint needs to be updated.
