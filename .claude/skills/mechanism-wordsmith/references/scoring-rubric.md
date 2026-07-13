# Scoring & Ranking Rubric

## Score range

Every variant receives a score from 0 to 4. Maximum possible is 4. Variants with a final score below 2 are dropped (they failed either Filter 1 or Filter 2 and shouldn't have made it this far).

| Score | Meaning |
|---|---|
| 4 | Ready to ship as-is. Passes jargon, length, anchor, and pain-dissolution. |
| 3 | Ships, but flagged. Either no anchor OR doesn't dissolve a top pain. Strategist should decide whether the missing dimension matters for their pick. |
| 2 | Floor. Passes the two disqualifying filters but neither scoring filter. Only use if no higher-scored variants exist for a needed pattern. |
| <2 | Never appears in output — filtered before ranking. |

---

## Tie-breaking

When two variants tie on raw score, rank by this priority list (top wins):

1. **Pattern leverage for the top brief pain** — use the table in `mechanism-patterns.md` (Decision Rule section). If the top pain is "buyer tired of category sameness", a Pattern 1 variant outranks a Pattern 8 variant at the same score.

2. **Sketchability** — can you draw the variant on a napkin? Pattern 4 (Trigger), Pattern 6 (Visual Theft), and Pattern 5 (Position Engineering) tend to win this. Sketchable variants outrank abstract ones.

3. **Word count (shorter wins)** — at equal everything else, a 10-word variant beats a 22-word one.

4. **Borrows from a winning template** — if one variant has phrasing that maps directly to a verbatim winning example ("without spending on ads", "the go-to voice for X", "to make X actually Y") and the other is a fresh construction, the borrower wins. The winning library is the source of truth.

---

## Pattern diversity rule

The final menu of 5–7 variants must include AT LEAST 4 distinct patterns. If applying the scoring naively produces 5 variants all using Pattern 3 (Constraint Negation), drop the lowest-scoring duplicates and add lower-scored variants from unused patterns until the menu has ≥ 4 distinct patterns.

**Why:** The strategist needs OPTIONS that are structurally different, not options that are tonal variations on the same pattern. Pattern diversity ensures the strategist can pick based on which pattern dissolves the top pain best — not get stuck choosing between five flavors of "without X".

---

## Lead variant selection

The output menu has a "Top pick" line at the bottom labeled `=== STRATEGIST PICK ===`. This is not a recommendation, but the skill should surface a default top pick based on:

1. Highest score (must be 4)
2. Pattern matches the top brief pain's preferred pattern (per the Decision Rule table)
3. Borrows from a verified winner's structural phrase
4. Sketchable

If multiple variants tie on all four, surface the one that uses the simplest pattern (lower-numbered patterns are preferred — Pattern 1 over Pattern 7, etc.). Lower-numbered patterns are higher-leverage in the library because they appear in more winning templates.

The strategist may override. The default exists to cut decision time, not to make the decision.

---

## When the menu fails the quality bar

The skill's quality bar (from SKILL.md): at least 3 of the 5–7 variants score 4/4 AND the strategist picks one within 5 minutes.

If a v1 run produces fewer than 3 variants at score 4, the failure mode is one of:

| Symptom | Likely cause | Fix |
|---|---|---|
| Most variants fail jargon | Literal mechanism is jargon-soup; agency hasn't translated their own tactic | Send back to Layer A — extract case study mechanism in plain English first |
| Most variants fail length | Mechanism has too many moving parts; over-explaining | Pick the SINGLE highest-leverage move from the literal mechanism, drop the rest |
| Most variants fail pain-dissolution | Case study doesn't actually dissolve the brief's top pains | Wrong case study choice — go back to Layer B |
| Most variants fail anchor | Mechanism is too abstract (no number, no contrarian word, no specific tactic) | Mine the case study for one concrete number or one named tactic to anchor on |

Log the failure pattern and the case study that produced it. After 5+ failures of the same type, the pattern library or the brief upstream needs revision.

---

## v1 success criteria

A v1 run is a success if:

- ≥ 3 variants score 4/4
- ≥ 4 distinct patterns appear in the menu
- The strategist picks one (or two — Email 1 + Email 3) within 5 minutes
- The strategist does NOT need to wordsmith their own variant after seeing the menu

A v1 run is a partial success if:

- 1–2 variants score 4/4, others score 3
- Strategist picks one but says "I wanted X angle and didn't see it" — that's a missing pattern; log it
- Strategist picks one but tweaks 1–2 words — acceptable, but the menu should have had the tweak as a separate variant

A v1 run is a failure if:

- 0 variants score 4/4
- Strategist writes their own variant from scratch
- Strategist rejects the entire menu

After failure, log:
- The literal mechanism input
- Which filters disqualified variants
- The variant the strategist wrote instead
- Which pattern (if any) it matches — or whether it's a new pattern to add

Failure logs drive the next iteration of the pattern library.
