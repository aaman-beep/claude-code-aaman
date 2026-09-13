# Web Search Prompts (Tier 3 Scraping Templates)

When Tier 1 (transcripts) and Tier 2 (Master Sheet) don't fill a field, the skill falls back to Tier 3 web research via `scripts/fetch_web_research.py`. This Blueprint defines the search queries used per field, so we don't reinvent them on every run.

> First check **Evergreen (Tier 0)** and cross-client `POST /api/clusters` — a pain validated across clients (`client_count>1`) beats any web scrape. Only reach for these web templates once Evergreen and the client's own calls come up short.

All queries assume substitution of `{persona}` (e.g., "VP of Marketing"), `{industry}` (e.g., "DTC supplements"), and `{tool_category}` (e.g., "SEO agencies", "marketing agencies"), provided by the calling skill.

---

## For Field 4b — Service Hidden Objections

The goal: find what {persona} thinks when they receive cold outreach from {tool_category}.

### Reddit queries (via WebSearch)
- `site:reddit.com "cold email" OR "cold outreach" {tool_category} frustrating`
- `site:reddit.com "marketing agency" OR "{tool_category}" red flags`
- `site:reddit.com {persona} "tired of" cold outreach`
- `site:reddit.com "another agency" pitched me`
- `site:reddit.com agency promises empty`

### Subreddit-specific patterns
For B2B SaaS personas, also search:
- `site:reddit.com/r/sales OR site:reddit.com/r/marketing cold outreach agency`
- `site:reddit.com/r/SaaS agency pitched`

For DTC ecommerce personas:
- `site:reddit.com/r/ecommerce agency horror story`
- `site:reddit.com/r/Entrepreneur marketing agency disappeared`
- `site:reddit.com/r/shopify hired agency budget burned`

### X queries (if X search is available)
- `from:* {persona} "another agency" OR "cold outreach"`
- `"DM'd by an agency" OR "yet another marketing pitch"`

### What to extract from results
Read each linked thread. Pull statements that describe:
- A negative reaction to receiving cold outreach
- A perception about {tool_category} as a category
- A specific reason they ignored, rejected, or felt skeptical about an outreach attempt

Tag each as `[source: <reddit_thread_url>]` and pass to the scoring step.

---

## For Field 3 — Their Language (verbatim quotes)

The goal: find verbatim quotes from {persona} in {industry} describing their problems, success criteria, or vocabulary.

### G2 / Capterra queries (via WebFetch)
- `site:g2.com {tool_used_by_persona} reviews`
- `site:capterra.com {tool_used_by_persona} reviews`

Read the review pages. Pull verbatim sentences where reviewers describe:
- The pain they had before the tool
- How they describe their job and outcomes
- Industry-specific vocabulary they use casually

### Reddit + LinkedIn (via WebSearch)
- `site:reddit.com {persona} {industry} "the worst part is" OR "what's frustrating"`
- `site:reddit.com {persona} {industry} "I wish" OR "if only"`
- `{persona} {industry} "we use the term" OR "in our industry"`

### What to extract
Direct quotes (1-2 sentences) in the buyer's voice. Each tagged with source URL.

Reject quotes that:
- Sound like vendor copywriting (probably written by the company, not a real user)
- Are too generic ("I love this product!")
- Are clearly from a different industry or persona

---

## For Field 4a — Industry Mistaken Beliefs

The goal: find what {persona} in {industry} commonly believes that is contrary to what's actually working in the market.

### Industry-forum queries
- `site:reddit.com {industry} "is SEO dead" OR "is X dead"`
- `site:reddit.com {industry} "AI replacing"`
- `site:linkedin.com/pulse {industry} myth OR misconception`

### Specific belief-pattern searches
- `{industry} "common myth" OR "biggest misconception"`
- `{industry} "I used to think" agency OR marketing`

### What to extract
Belief statements that:
- Are clearly held by the persona (not just thrown out hypothetically)
- Would shape how they evaluate your outreach
- Are wrong or at least debatable in 2025-26 market reality

Tag each with `[source: <url>]` plus a note on WHY this is a mistaken belief.

---

## For Field 5 — Dream Outcome (Tier 3 fallback only)

If transcripts don't surface dream outcomes and Master Sheet phrasing is bland, fall back to:

### LinkedIn queries
- `site:linkedin.com/posts {persona} {industry} "my goal" OR "this quarter"`
- `site:linkedin.com/pulse {persona} "what success looks like"`

### Reddit
- `site:reddit.com {persona} {industry} "if I could just"`
- `site:reddit.com {persona} {industry} "what I really want"`

### What to extract
Statements that describe the future the persona is working toward, in their own words. Tag each.

---

## Query construction rules

1. **Always substitute the specifics.** Never run a query with `{persona}` un-filled. The whole point is to find buyer-evidence for THIS specific client+segment.

2. **Use `site:` operators** for Reddit, G2, Capterra, LinkedIn. Without them, results get polluted with low-quality content.

3. **Take 10-20 results per query.** Skim, don't deep-read. The goal is volume of evidence + a few high-signal extractions, not exhaustive analysis.

4. **Always tag extractions with source URLs.** Tier 3 evidence with no URL = unusable. Drop it.

5. **One query per field, multiple sub-queries OK.** Don't run 50 queries for Field 4b. Run 4-6, get a sample of evidence, score it against Tier 1+2 data.

---

## What NOT to scrape

- News articles (too generic, often vendor-influenced)
- Vendor blogs (obviously biased)
- Press releases
- "Top 10 X" listicle pages
- AI-generated content farms

If a result reads like marketing copy rather than a real user voice, skip it.

---

## Future improvement

These query templates will evolve over time as we see what produces high-signal extractions vs. noise. Treat this file as iteratively improved — add new queries that work, remove ones that don't.
