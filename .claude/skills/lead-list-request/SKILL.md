---
name: lead-list-request
description: "Turns a messy targeting brief (voice note, pasted notes, call scribbles) into a complete New Lead List Request in Airtable - campaign name, lead list type, targeting logic, job titles, Clay variables, niches - then files it as a Client Delivery record after one approval. Use this whenever the user wants a lead list built or requested - 'submit a lead list request', 'new lead list for [client]', 'fill in the lead list form', 'request a list', 'I need a list for [client]', 'build me a list of [titles] at [kind of company]' - or when they paste the New Lead List Request Form's fields and describe who to go after. Also use it when someone dictates targeting out loud and expects a filled form at the end. Do not use it for writing SMS or email copy, or for pulling the leads themselves; this skill files the request, the data team builds the list."
---

# Lead List Request

Files a New Lead List Request into Airtable (Operations & Data Analytics → Client Delivery)
from a spoken or written brief, without anyone touching the web form.

The form at `airtable.com/appP3VJXaEqNopR1l/shrqZ1f8s1yx0A4Xv` writes to a table this skill can
write to directly. Filling it by hand means twenty copy-pastes between a chat window and a
browser tab, and that is where the mistakes come from - half-pasted values, ASCII dividers
dragged into fields, a required field missed until the form rejects it. Skip the form.

## Evergreen — the shared knowledge API (check it first)

Scaletopia's knowledge lives in **Evergreen**, the one API every skill in this playbook shares.
It is the research/data **provider** — it serves evidence and numbers; it does **not** write copy
(that's this skill's job, and your proven copy stays yours). Before requesting a list, check Evergreen for who's already been touched so the data team doesn't rebuild a list of people we've already burned.

- **Base URL:** `https://knowledgebase-production-f52e.up.railway.app`
- **Auth (required):** send header `Authorization: Bearer $EVERGREEN_API_KEY` on every call — the key
  lives in this playbook's `.env` (gitignored). No header -> **401**.
- **Discover the API yourself:** `GET /api/docs` is the live index of every endpoint with its params
  and descriptions; `GET /api/openapi` is the full machine schema. Unsure which endpoint/field exists?
  Read `/api/docs` first — never guess a path or bulk-pull GHL/Airtable for what Evergreen already has.
- **Focused entry points:** `evergreen-research` (pull/save findings) · `evergreen-stats` (numbers) ·
  `evergreen-data` (full field-level catalogue).

**What THIS skill pulls from Evergreen:**
- `POST /api/prospects/lookup {"client":"{slug}","companies":[...]}` — touch history: matched vs
  fresh, `furthest_stage`, who we already reached, and `suggested_next` (who to go to instead).
- `GET /api/niches` — canonical niche / sub-niche ids for clean targeting.

## The shape of the job

The input is a brief: usually a transcribed voice note, sometimes pasted notes. It will be
non-linear, it will trail off mid-sentence, and it will contradict itself once or twice -
that is what thinking out loud sounds like, not a defect. It will not name every field.

Your job is to turn that into a complete, submittable request in **one pass**, and surface
what you had to decide in **one place**. A request that takes four exchanges to file has
already lost to doing it by hand.

**One approval gate.** Draft everything, show it, wait. On "go" / "yes" / "send it", create
the record. Never write to Airtable before that. Never run an interview - if something is
genuinely missing, put your best guess in and mark it, rather than stopping to ask.

## Workflow

### 0. A note on tool names

This skill needs an Airtable MCP server with write access to the base below. The tool names
differ by how that server is connected, so the calls are written here by their action rather
than by an exact name:

| Action | Claude Code / local MCP | Cowork device bridge | Anthropic connector |
|---|---|---|---|
| find a record | `mcp__airtable__search_records` | `mcp__remote-devices__airtable__search_records` | `mcp__Airtable__search_records` |
| read records | `mcp__airtable__list_records` | `mcp__remote-devices__airtable__list_records` | `mcp__Airtable__list_records_for_table` |
| create a record | `mcp__airtable__create_record` | `mcp__remote-devices__airtable__create_record` | `mcp__Airtable__create_records_for_table` |

Use whichever is present. If none is, jump to "When the Airtable connector is unavailable" at
the end. Parameter names differ slightly between them, so read the tool schema rather than
assuming the shapes below transfer verbatim - the base, table, field and record IDs do.

### 1. Load the map

Read `references/airtable-map.md`. It has the base, table, every field ID, the exact select
options, and which fields become required depending on the Lead List Type. Don't guess a
field name - Airtable form labels and underlying field names differ (the form says
"Deadline", the field is `Data Needed By`).

### 2. Resolve the client, then check what already exists

Search the Clients table for the client named in the brief and keep the record ID - the
Client field is a link, so it takes `["recXXXXXXXXXXXXXX"]`, not a name string.

```
<search records tool>
  baseId: appP3VJXaEqNopR1l
  tableId: tblX0E8Nek2xGeWxY
  searchTerm: <client name>
  maxRecords: 3
```

That table is wide and each record returns a wall of KPI fields - pull `maxRecords: 3` and
take the ID, nothing else. If no client matches, stop and ask; do not invent a link.

Then read that client's existing lead lists before drafting anything. The Clients record has
a `Lead Lists` field holding record IDs into Client Delivery; pull them with a narrow field
selection and look at what is already requested:

```
<read records tool>
  baseId: appP3VJXaEqNopR1l
  tableId: tbl8YUdvLqf8VJwyW
  recordIds: [<the Lead Lists IDs>]
  fieldIds: ["fldt2EBUpPK45JJVG", "fldjo1htYDuv0LHau", "fldtMzVxQhYpmYgP3",
             "fld3OFR06R4ZkMe6p", "fldNI8sWSzGlPp9Bi", "fldXqfVLJcL5thxEE"]
```

Always narrow to those field IDs. Client Delivery carries well over a hundred fields,
most of them copy bodies, and an unfiltered read buries the answer in noise.

This step exists because a strategist filing a request cannot see the queue, and an unbuilt
near-duplicate is expensive in a way nobody notices until the data team builds the same list
twice. If any existing list overlaps this brief on niche, titles or geography - especially
one whose `Status` is still `Not Built` - that goes at the top of the review as a blocker,
not buried among the inferences. Offer to amend the existing record instead of filing a
second one.

It also tells you facts the brief assumes you know. Whether Founders are already covered by
another list is not a rule to remember; it is a question the queue answers.

### 3. Pick the Lead List Type

This decides which extra fields the request needs, so decide it before drafting anything else.

| Type | Use when | Unlocks |
|---|---|---|
| **Persona** | Targeting is defined by who the person is - titles, seniority, department - and the company universe is broad | nothing extra |
| **Company With Persona** | You are naming the kind of company as well as the person: specific niches, industries, headcount, geography | Niche/Industry, Example Companies, Company Location, Headcount Range |
| **Event** | The list is people attending or exhibiting at named events | Event Names/URLs |
| **Signal** | The list is defined by a trigger - hiring, funding, tech stack, ad spend | Type of signal, Signal Priority |

The tell for Company With Persona: **if the brief names niches or industries, it is Company
With Persona.** Persona has nowhere to put a niche, so a niche list quietly gets lost -
that is the single most common misfile here. When in doubt between the two, choose Company
With Persona and let the extra fields be answered.

### 4. Draft every field

Read `references/field-craft.md` and build each value there. It covers the campaign naming
format, how to curate job titles down from a raw dump, how to write targeting logic, the
Clay variable pattern, and the traps that have bitten this form before.

Three things that are always true and worth repeating here:

- **The brief beats the reference, every time.** `field-craft.md` is full of example values,
  and they are examples, not defaults. If the brief says "$50k/mo **or** five employees" and
  the reference shows `employees ≥ 5`, the brief wins and the value is an OR. If the brief
  keeps a title the reference suggests cutting, the brief wins. The reference teaches shape;
  only the brief supplies content. Copying an example value that the brief contradicts is
  the worst failure this skill has, because it looks completely correct.
- **Field values carry no formatting furniture.** No `=====` dividers, no ALL-CAPS banners
  that belong to a chat rendering. Those get pasted into Airtable and have to be deleted by
  hand. The only in-field labels that earn their place are the group headers inside Job
  Titles (`ECOMMERCE / DTC:`, `OPERATIONS:` …), which the data team reads.
- **Exclusions come from this brief, not from memory.** Every campaign strips different
  titles and niches. Derive them from what the person actually said, list them in the review
  as their own line so a one-word override works, and never carry an exclusion forward into
  the next request because a previous one used it.

### 5. Show the review, then stop

One message. Compact enough to read on a phone.

```
LEAD LIST REQUEST - <Client>

Campaign      <Client> - <descriptor> | <headcount> | <geo> | <source>
Type          <Persona | Company With Persona | Event | Signal>
Priority      <…>
Needed by     <DD Mon YYYY>  (<n> days out)
Niches        <one line>                  ← Company With Persona only
Company       <location> · <headcount>    ← Company With Persona only
Titles        <n> titles across <departments>; excluding <…>
Location      <people location>
Clay          <n> columns: <names>
Copy ready    <Yes | No>

Check this
- <anything that should stop the filing: an overlapping list already in the queue, a
  client with no match, a brief that contradicts itself. Omit the section if empty.>

Calls I made
- <each inference, one line, phrased so a one-word override works>

Missing
- <anything you could not derive, with what you put instead>
```

`Check this` sits above the inferences because it is a different kind of thing. An inference
is "I picked Urgent, say the word." A blocker is "you already have this list on order." They
should not read alike, and a duplicate warning mixed into a list of routine guesses gets
skimmed past.

Then: **"Say go and I'll file it."** Do not submit on a message that only edits a field -
apply the edit, show the changed lines, and ask again.

Show the full text of the long fields (Targeting Logic, Job Titles, Clay Enrichments) only
if asked, or if one of them is the thing you are least sure about. The summary is the
deliverable; the wall of text is available on request.

### 6. File it

```
<create record tool>
  baseId: appP3VJXaEqNopR1l
  tableId: tbl8YUdvLqf8VJwyW
  fields: { … }
```

Use field **names** as keys. If Airtable rejects one as unknown, the field was renamed -
retry that key with its ID from the map, and mention the drift so the map gets fixed.

Set only the fields the form itself sets. Status, Sourcing Status and the TAM columns are
the data team's to fill; writing them here fakes progress that has not happened.

### 7. Confirm

Read the record back, confirm the required fields landed, and report:

> Filed - `<Campaign Name>`, needed by `<date>`.
> https://airtable.com/appP3VJXaEqNopR1l/tbl8YUdvLqf8VJwyW/<recordId>

**First run only:** this table has n8n workflows hanging off it ("Lead List Request To
Slack", "Client Delivery Button Handler") that normally fire on a form submission. An
API-created record should trip the same trigger, but nobody has verified it. Ask the user to
check the Slack channel once. If the notification does not appear, say so plainly and fall
back to the form for the next one rather than quietly filing requests nobody sees.

## When the Airtable connector is unavailable

If the Airtable tools are missing or erroring, there are two ways back, in order of
preference:

1. **Chrome.** The public form is at
   `airtable.com/appP3VJXaEqNopR1l/shrqZ1f8s1yx0A4Xv`. Use the `mcp__claude-in-chrome__*`
   tools - `navigate`, `read_page`, `form_input`, `computer` - to fill and submit it. Slower
   than the API and the conditional fields only appear after the Lead List Type is set, so
   set that field before reading the page again. Requires the Chrome extension to be
   connected and permitted on airtable.com.
2. **Paste block.** Print the values as a labelled block in form order - Client, Campaign
   Name, Lead List Type, Priority, Deadline, Targeting Logic, [conditional fields],
   Department, Seniority, Job Titles, People Location, Clay Variables, Notes, Copies ready -
   so it can be pasted field by field. This is the fallback of last resort; say plainly that
   it is one, because it is the workflow this skill exists to replace.
