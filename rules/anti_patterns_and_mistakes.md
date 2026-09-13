# Anti-Patterns and Common Mistakes

## Prompting Mistakes
1. **Overcomplicating Prompts**
   - ❌ Wrong: Writing 3-paragraph instructions with every possible scenario
   - ✅ Right: Use the simple template - do the 20% that gets 80% of results
2. **Assuming Data is Correct**
   - ❌ Wrong: Taking Claygent outputs at face value
   - ✅ Right: Always spot-check outputs and validate critical data
3. **Not Using Examples**
   - ❌ Wrong: Describing what you want in abstract terms
   - ✅ Right: Showing 10+ concrete examples of desired outputs
4. **Vague Instructions**
   - ❌ Wrong: "Find something interesting about the company"
   - ✅ Right: "Find their most recent product launch or feature announcement from the last 3 months"
5. **No Fallback Instructions**
   - ❌ Wrong: Letting Claygent make up data when nothing is found
   - ✅ Right: "Output 'Purple' if confidence is below 90%"

## ICP Mistakes
1. **100% Listening to the Client**
   - The Mistake: Taking client's ICP suggestions as the Bible & always listening to us.
   - Why It Fails: They hired us because they need outbound expertise. They know their industry, but not cold outreach dynamics.
   - The Fix: Use their industry knowledge as input, not direction. We're the cold email experts.
2. **Creating Lists That Are Too Small or Too Big**
   - The Mistake: Hyper-segmented ICPs with <1,000 companies or broad lists with 50k TAM.
   - Why It Fails: Campaigns burn through lists in 1 week, can't test properly & takes too much effort & too big just means generic email/data.
   - The Fix: Minimum 2,000-3,000 companies (5,000-10,000 contacts) per segment.
3. **Ignoring Market Saturation**
   - The Mistake: Targeting markets where everyone's already pitching.
   - Why It Fails: Prospects are email-blind from 50+ similar pitches daily.
   - The Fix: Look for underserved segments first, otherwise find unique angles/USP into saturated markets with super strong case studies.
4. **Weak or Missing Trigger Events**
   - The Mistake: "We'll just reach out to all SaaS companies".
   - Why It Fails: No urgency or relevance, sounds like spam.
   - The Fix: Always identify 2-3 specific, trackable triggers.
5. **Mismatched Case Studies**
   - The Mistake: Using B2C success stories to target B2B companies or trying to rely enterprise case studies to SMBs.
   - Why It Fails: Prospects can't see themselves in the results.
   - The Fix: Match case studies as closely as possible (industry, size, problem, their audience etc.).
6. **Analysis Paralysis**
   - The Mistake: Spending 3 hours researching one perfect ICP.
   - Why It Fails: We need to test fast and iterate.
   - The Fix: 60-90 minutes max, then test and refine based on real data.

## Market Research Mistakes
> Avoid #3 (flimsy sources) and #5 (missing voice-of-customer) by treating **Evergreen** as the sanctioned voice-of-customer store: mined `pains`/`lingo`/`objections` are drawn from real calls and confidence-scored + traced to the source call (`GET /api/clients/{slug}`, `POST /api/search`, `POST /api/clusters`). Pull from there before web-scraping, and verify claims against it. See FUNDAMENTALS → "Reaching Evergreen".

1. **Dumping Generic or Bulk AI content**: Overloading docs with copied, unchecked info—dilutes actionable insights and makes findings unusable for outreach.
2. **Ignoring Persona Segmentation**: Targeting industries or companies as a whole, instead of homing in on the real humans and their pain points, leads to bland, ineffective messaging.
3. **Relying on Flimsy Data Sources**: Using blog posts, AI-scraped summaries, or vendor PR instead of authentic customer interviews, forums, transcripts, or direct quotes results in disconnected, jargon-heavy research.
4. **Skipping Practical Filtering/Verification**: Accepting insights from a single source or not validating claims—rather than verifying with at least two independent sources—can spread inaccurate or shallow pain points.
5. **Missing Voice of Customer**: Filling research with analyst lingo or “industry speak,” instead of capturing the verbatim frustrations and language prospects use in forums, Slack, or LinkedIn.
6. **Documents Too Long or Broad**: Producing walls of text or unfocused research that no campaign or copywriter can quickly use or apply.
7. **Not Prioritizing Pain/Outcomes**: Listing pain points or data without ranking by severity and frequency—so the team can’t tell what really matters for messaging or testing.
8. **Targeting Imbalance**: Going too narrow on niche roles (missing volume) or too broad (losing relevance); always aim for the balance that matches your outreach capacity and ICP.

## Value Prop/Offer Mistakes (10 biggest Common Mistakes)
1. **Leading with Guarantees**: Most outreach leads with risk-free promises and money-back guarantees right upfront, which immediately triggers skepticism and makes prospects think it's too good to be true, and also bringing in cheap leads.
2. **Generic Surface-Level Problems**: Addressing obvious pain points that prospects already know about instead of uncovering deeper, unrecognised problems that they haven't identified yet.
3. **Outcome Showcasing Without Context**: Simply stating results or case studies without connecting them to the prospect's specific situation or demonstrating relevant understanding of their business.
4. **Self-Centered Messaging**: Making the pitch about your company, achievements, and features rather than focusing on the prospect's challenges and what matters to them.
5. **Feature-Focused Over Benefit-Focused**: Listing what your service includes rather than explaining the tangible business outcomes and measurable impact it delivers.
6. **Lack of Specificity**: Using vague, broad value propositions that try to solve everything instead of addressing one specific, well-researched pain point.
7. **Multiple Value Propositions**: Presenting several different benefits or solutions in one email, confusing prospects about what you actually specialise in.
8. **No Evolution or Testing**: Using the same value proposition and offer structure for months without testing new problem angles or adapting based on market feedback.
9. **Unrealistic Timing Promises**: Making commitments about specific timeframes and results that sound too aggressive or unrealistic for the prospect's situation.
10. **Assumption of problems that are wrong**: Positioning offers as if prospects are already aware they have a problem and are ready to buy, rather than meeting them where they are in their journey. (Comes from bad market research).
11. **Bonus #11**: Your offer just sucks & no one believes you ;)

## Copy & Sales Anti-Patterns (Sandler)

Full reference: [../skills/sandler-sales-rules.md](../skills/sandler-sales-rules.md)

1. **Spilling candy in the lobby** (Sandler #2): Dumping mechanism + 3 results + case study + calendar link in one SMS. → One pain, one mechanism, one proof, one ask.
2. **Answering unasked questions** (Sandler #5): Preempting objections with "I know you get a lot of these…" or "we're not cheap but…". → You just seeded the objection. Strip it.
3. **Stated-pain copy** (Sandler #38): Writing to the surface symptom ("need more leads") instead of the real pain (unpredictable revenue → can't hire/plan). → Push one layer deeper.
4. **Asserting the pain** (Sandler #27): "You have a pipeline problem" instead of "Still pulling pipeline from referrals after 3 years?". → Let them discover it via question.
5. **Pitching the service in cold SMS** (Sandler #8): CTA trying to close the deal instead of booking the call. → Sell the 15-min, not the offer.
6. **Vague "let me know" CTAs** (Sandler #4): No permission to say No = polite maybes clogging pipeline. → "If not relevant, just say pass."
7. **Competitor-paste-safe copy** (Sandler #35): If a competitor could swap their logo onto your SMS and send it, the UM is too weak. → Rewrite with sharper mechanism.
8. **Stat-hook openers** (Sandler #21): "Did you know 73% of agencies…" → Prospects don't pay for education they didn't ask for. Cut it.
9. **Hard-sell urgency** (Sandler #26): "Limited spots," "act now," "last chance." → Corrodes trust with sophisticated ICPs.
10. **Neediness leaking into voice** (Sandler #49): "Would love the chance to…", "hoping we can…", over-apology. → Your Child leaking. Strip it.
11. **Seagull painting** (Sandler #18): Adding uninvited features/promises/adjectives to the prospect's mental picture. → Every extra detail is a new reason to stall.
12. **Jargon dumps in first-touch** (Sandler #24): Acronyms and technical depth before pain is confirmed. → Plain English, one idea.
13. **Happy ears on replies** (Sandler #13, #37): Reading "interesting" or "maybe Q2" as buying intent. → Treat as ambiguity, ask a clarifying question.
14. **Permanent maybes in pipeline** (Sandler #31): Keeping lukewarm leads "nurturing" forever. → Close the sale or close the file.
15. **Blaming the list before the message** (Sandler #41): "These leads are bad" when the real issue is mechanism-market fit. → Audit messaging first.