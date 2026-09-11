# Field craft - turning a brief into field values

How to write each field so the data team can build from it without coming back with
questions. Read this while drafting; the worked example at the bottom shows all of it
assembled.

The person receiving this request is building a list in Storeleads, Apollo or Clay. They
need filter criteria, not prose. Every field should read like something you could hand to a
person and have them start clicking within a minute.

---

## Campaign Name

The form states the convention: `Client name - Campaign Name`. In practice the second half
carries four slots, pipe-separated:

```
<Client> - <descriptor> | <headcount> | <geo> | <source>
```

Examples, both real:

```
Leadgenix - Painters | 2-350E | NA | Apollo
Redo - Ecom/Ops/Finance/Growth DMs | 5E+ | US+CAN | Storeleads
```

- **descriptor** - what makes this list different from the client's other lists, in 2–5
  words. A formula in the Campaigns table extracts exactly this slice (between the first `-`
  and the first `|`), so keep the punctuation clean and don't use another `-` inside it.

  Both a persona cut (`Ecom/Ops/Finance/Growth DMs`) and an industry cut (`Painters`,
  `Fitness Equipment & Sporting Goods`) are correct - pick whichever axis the brief is
  actually slicing on. The test is the client's existing list names from step 2: the
  descriptor has to distinguish this list from those at a glance. When the brief offers
  several candidate phrases, take the one that does that, and drop the rest rather than
  cramming them in with parentheses.
- **headcount** - `5E+`, `2-350E`, `50-500E`. `E` is employees.
- **geo** - `US`, `US+CAN`, `NA`, `UK`, `EU`.
- **source** - where the list actually gets pulled from. Pick from the sources this base
  recognises, matched to the universe:

  | Universe | Source |
  |---|---|
  | Ecommerce / DTC brands - anything needing a storefront or cart | `Storeleads` |
  | Title- or department-led B2B, any industry | `Apollo` |
  | Local and service businesses | `GMB` / `Google Maps` |
  | Agencies | `Clutch` |
  | Defined by tech stack | `Built With` |
  | Defined by funding | `Crunchbase` |
  | Enrichment layered on any of the above | `Clay` |

  The brief usually names the source out loud ("it'll be Storeleads ideally"). Take what
  they said. The table above is only for when they didn't say.

  No source is wrong, but sources differ in what they can prove. Storeleads knows who has a
  live cart; Apollo does not. Apollo is perfectly usable for an ecommerce list - it just
  means the qualifying criterion has to be enforced somewhere else, and that somewhere is a
  strict Clay filter column. Whenever the chosen source cannot confirm a criterion the
  campaign depends on, add that filter to Clay Enrichments rather than quietly hoping the
  list comes back clean. See the "Qualifying filters" note under Clay Enrichments.

## Priority and Deadline

Both are required and neither is usually stated out loud.

- **Priority** - take it from urgency language in the brief ("need this today", "no rush").
  With nothing to go on, `Urgent` is the working default for a strategist filing their own
  request, but say so in the review so it can be knocked down in a word.
- **Data Needed By** - the form's own rule is **minimum 48 hours**. Default to today + 2
  days unless the brief names a date. Write it `YYYY-MM-DD`. State it in the review as
  `DD Mon YYYY (n days out)` so an off-by-one is visible at a glance.

## Targeting Logic

The filter set, written as a boolean stack. This is what someone reproduces in the tool, so
it should be mechanical, not descriptive.

```
Ecommerce/DTC brands (must have an online store / checkout -
NO physical-only, NO restaurants/food-service)
 AND employees ≥ 5 (~$50k/mo+ revenue)
 AND niche IN [included list below]
 AND title IN [Job Titles below]
 AND seniority = Manager → C-Suite, EXCLUDING Founder/Owner/CEO
 AND location = US or Canada.
Volume: pull the ENTIRE matching universe (no cap).
```

What makes this version work: the first line defines the universe *and* names what it
excludes, each `AND` is one filter a person can set, and the last line answers "how many?"
before anyone asks. Cross-reference the other fields rather than duplicating them - `title
IN [Job Titles below]` beats repeating forty titles here.

Say the volume explicitly. "Pull the entire matching universe (no cap)" and "cap at 5,000"
produce very different work, and silence gets read as either one.

## Job Titles

Usually the field that takes the most judgement, and usually the field the brief is
vaguest about. The brief tends to arrive as either a raw dump from a title-frequency
export, or a spoken sketch ("COO, director of ops, whatever you think").

Group by department with a header line, comma-separated within each group, then a final
exclusion line:

```
ECOMMERCE / DTC / DIGITAL:
Chief Ecommerce Officer, Chief Digital Officer, VP of Ecommerce, Head of Ecommerce, …

OPERATIONS:
Chief Operating Officer (COO), VP of Operations, Head of Operations, Director of Operations, …

FINANCE:
Chief Financial Officer (CFO), VP of Finance, Head of Finance, Finance Director, …

GROWTH:
VP of Growth, Head of Growth, Director of Growth, Growth Manager

EXCLUDE (do NOT pull): Founder, Co-Founder, Owner, CEO, President, …
```

The department headers stay - this is the one field where in-value labels earn their keep,
because whoever builds the list works department by department.

Curating down from a dump:

- **Cut what the offer doesn't touch.** A title is on-target only if that person owns the
  problem the campaign is about. For an operations-and-margin pitch, Retention, CX,
  Customer Success, Lifecycle, brand/social/creative and email-CRM titles are adjacent, not
  buying. Cut them.
- **Watch for titles that mean something else at scale.** "Store Manager" and "General
  Manager" are location-level, not company-level. "Marketing Finance" and FP&A are
  budget-holders inside marketing, not P&L owners.
- **Keep the exclusion line explicit.** A negative list is doing real work - it stops the
  build from silently expanding.
- **Founder-type titles are a decision, not a default.** They are excluded when a separate
  founder list already covers them. That is a fact about the client's current campaign set,
  not a rule - so ask it as part of the review rather than assuming it, and never carry a
  previous campaign's answer forward.

## Department and Seniority

Short, one line each, using `·` between items. They restate the Job Titles at a level the
tools filter on directly:

```
Department:  Operations · Finance · E-commerce / Digital · Growth
Seniority:   C-Suite (excl. Founder/Owner/CEO) · VP · Head · Director · Senior Manager · Manager
```

Keeping the seniority exclusion visible here matters - some tools filter on seniority band
rather than title string, and the exclusion has to survive both routes.

## Niche/Industry - Company With Persona only

Single-line text, so the value must be **one physical line** - the block below is wrapped for
reading, not for pasting. A newline here is silently truncated or rejected.

Name what's in and what's out:

```
INCLUDE: Health & Wellness · Skincare & Beauty · Makeup/Cosmetics · Fashion & Apparel ·
Sporting & Outdoor Goods · Fitness · Toys & Hobbies · Pets & Animals · Home & Garden ·
Smoking/Vaping/CBD · Sports  -  EXCLUDE: Food & Drink (and all restaurants / food-service)
```

The exclusions belong here rather than only in Targeting Logic, because the person filtering
by category sees this field. Derive both lists from the brief - a niche list from a previous
campaign is worse than no niche list, because it looks deliberate.

## Example Companies - Company With Persona only

Required. The form asks for **URLs, not brand names** and shows its own example:
✗ `Scaletopia` ✓ `scaletopia.io`. Domains, one per line.

If the brief names no reference accounts, write `n/a`. Inventing plausible lookalikes here
is worse than leaving it blank - the build gets anchored on companies nobody chose.

One live record in this table holds
`CategoryBrandDomainBagsPortland Gear (anchor)portlandgear.comBagsWOLFpak…` - a table
copy-pasted out of a doc with every space eaten, sitting in the field unreadable. Another
holds the campaign's *exclusion rationale* in Niche/Industry instead of its niches. Both are
the copy-paste failure mode this skill exists to remove: build each value deliberately and
check it reads as itself before writing.

## Company Location and Headcount Range - Company With Persona only

Both required, both easy to skip.

- **Company Location** - where the companies are (`US / Canada`). Distinct from People
  Location; the form blocks submission without it.
- **Headcount Range** - a *range*, e.g. `5-200`. If the brief only gives a floor
  ("5 employees and above"), pick a sensible ceiling and flag it in the review. An
  open-ended `5+` isn't a range and the tools won't take it.

## People Location

Where the *contacts* are: `United States & Canada`. Plain text, no codes.

## Clay Enrichments - "Clay Variables & Instructions"

Extra columns Clay generates per lead, which the copy then merges. The form asks for one
column per variable, so number them and give each three things - instruction, format, and
an example - because the person configuring Clay is writing a prompt from this text.

```
1) main_products
   Instruction: From the brand's website/store, list their 2–4 hero
   products they actually sell.
   Format = 1 column, comma-separated
   (e.g. "vitamin gummies, greens powder, hydration sticks")

2) role_hook  (title abbreviation / "I know you lead ___" line)
   Instruction: Map the contact's department to a short clause -
     Ecommerce/DTC → "I know you lead ecommerce & DTC"
     Operations    → "I know you run ops"
     Finance       → "I know you head up finance"
     Growth        → "I know you drive growth"
   Format = 1 column, one finished clause per lead

3) brand_category
   Instruction: Classify the brand into ONE short category phrase
   usable inline.
   Format = 1 column, single phrase
   (e.g. "skincare brand", "beauty & makeup brand", "pet brand")
```

The pattern generalises: a **what-they-sell** variable, a **who-they-are** variable that
mirrors the personalisation the copy needs, and a **category** variable for inline mentions.
Give a literal example string for each - variables described abstractly come back formatted
wrong, and a bad column is discovered at send time.

### Qualifying filters

Clay columns are not only personalisation. They are also where a criterion gets enforced
when the source cannot enforce it itself. Apollo, for instance, will happily return a
wholesale-only brand or an Amazon-only seller for an ecommerce query, because it does not
know what a checkout is.

So when the campaign depends on something the source cannot prove, add a strict filter
column and write the pass condition as an exact value, not a vibe. Strict means a column
whose output is a fixed token you can filter on, and an instruction that says what to do
when the answer is unclear:

```
0) has_own_checkout   (QUALIFYING FILTER - strict)
   Instruction: Visit the brand's site. Does it sell directly with its own
   cart/checkout (not wholesale-only, not Amazon/marketplace-only, not
   "where to buy" retail locator)?
   Output EXACTLY one of: YES / NO / UNSURE
   Format = 1 column, single token
   KEEP only rows = YES. Drop NO and UNSURE.
```

Number qualifying filters ahead of the personalisation variables so the build order is
obvious: filter first, enrich what survives. Say which value passes and what happens to the
rest, because "check if they have a checkout" without a keep rule produces a column nobody
filters on.

Two filters is usually the ceiling. Each one costs a Clay run over the whole list, so
enforce what the campaign genuinely depends on and let the rest be caught by the niche and
headcount criteria.

## Custom Notes

The context the request would be misread without: what the offer actually is, who is
deliberately excluded and why, how many contacts per company, anything already tried.

```
- Ecommerce/DTC ONLY - must sell online (has a cart/checkout). The offer is
  abandoned-checkout recovery, so physical-only brands, restaurants and
  multi-location food-service GMs are off-target (the last CPG list was ~9%
  restaurant GMs - avoid that here).
- Owners/Founders are intentionally excluded - they're covered by a separate list;
  this one is for the Ops/Finance/Ecom/Growth operators.
- Prefer 1 best contact per brand (most senior relevant title); allow 2 if both a
  functional lead + their manager exist.
```

Notes naming a concrete past failure ("the last list was 9% restaurant GMs") are the ones
that change the build. Generic notes get skimmed.

## Copies ready?

Whether SMS/email copy exists for this campaign.

If the brief says, take the brief. If it is silent, file `No` and flag it in the review -
do not stop to ask, and do not reason your way to `Yes`. "There's existing copy we could
reuse" is not the same answer as "the copy for this campaign is written", and a wrong `Yes`
sends the request straight to build with nothing to send. `No` on a campaign that does have
copy costs one correction; `Yes` on one that doesn't costs a build cycle.

---

## Worked example

**This is a real filed record (Redo, 27 Jul 2026), reproduced to show the shape of a finished
request. Do not copy its values.** It is here because seeing all seventeen fields agree with
each other teaches more than seventeen isolated rules. But a Redo brief will resemble it
closely enough that lifting the values feels like drafting, and it is not - the next Redo
list will differ in exactly the details that matter. Derive every value from the brief in
front of you, then use this to check whether the set hangs together.


Brief, roughly: *ecommerce/DTC brands, ops and finance and ecom decision-makers, strip the
founders because we already have those, 5 employees and up, health & wellness / skincare /
beauty / apparel / sporting goods / fitness / toys / pets / home & garden / vaping / sports
but not food & drink, US and Canada, Clay columns for their main products and a role hook
and the brand category.*

| Field | Value |
|---|---|
| 📂 Clients | `["rec6AI1zzahdLCTvH"]` (Redo) |
| Campaign Name | `Redo - Ecom/Ops/Finance/Growth DMs \| 5E+ \| US+CAN \| Storeleads` |
| Lead List Type | `Company With Persona` - niches named, so Persona would drop them |
| Priority | `Urgent` |
| Data Needed By | `2026-07-29` (2 days out) |
| Targeting Logic | the boolean stack above |
| Niche/Industry | the INCLUDE/EXCLUDE line above |
| Example Companies | `n/a` |
| Company Location | `US / Canada` |
| Headcount Range | `5-200` (brief gave a floor only - ceiling flagged) |
| Department | `Operations · Finance · E-commerce / Digital · Growth` |
| Seniority | `C-Suite (excl. Founder/Owner/CEO) · VP · Head · Director · Senior Manager · Manager` |
| Job Titles | the four groups + EXCLUDE line above |
| People Location | `United States & Canada` |
| Clay Enrichments | the three numbered columns above |
| Custom Notes | the three bullets above |
| Copies ready? | `No` |

Worth noticing in that run: `Storeleads` not `Apollo` because the universe is carts;
`Company With Persona` not `Persona` because niches were named; `5-200` not `5+` because the
field wants a range; and `No` on copy even though reusable copy existed. Four judgement
calls, all of which belong in the review as their own lines.
