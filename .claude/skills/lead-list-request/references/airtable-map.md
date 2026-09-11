# Airtable map - New Lead List Request

Everything needed to write the record without opening the form.

- **Base** - `appP3VJXaEqNopR1l` · Operations & Data Analytics
- **Table** - `tbl8YUdvLqf8VJwyW` · Client Delivery
- **Form view** - `viwnMThD7jxMxNr1w` · "New Lead List Request Form"
- **Public form** - `https://airtable.com/appP3VJXaEqNopR1l/shrqZ1f8s1yx0A4Xv`
- **Clients table** - `tblX0E8Nek2xGeWxY`, primary field `Client Name`

Verified 27 Jul 2026. Field IDs survive renames; names do not. Write with names, fall back to
IDs on `UNKNOWN_FIELD_NAME`.

## Field map

Form label ≠ field name in several places - the mismatches are where mistakes happen, so they
are marked ⚠.

| Form label | Field name | Field ID | Type |
|---|---|---|---|
| Client * | `📂 Clients` ⚠ | `fldqJCxeaxIOjl7ug` | link → `tblX0E8Nek2xGeWxY` |
| Campaign Name * | `Campaign Name` | `fldt2EBUpPK45JJVG` | singleLineText |
| Lead List Type * | `Lead List Type` | `fldjo1htYDuv0LHau` | singleSelect |
| Priority * | `Priority` | `fldXqfVLJcL5thxEE` | singleSelect |
| Deadline * | `Data Needed By` ⚠ | `fld3OFR06R4ZkMe6p` | date |
| Targeting Logic | `Targeting Logic` | `fldfGCoXqMmh9xux5` | multilineText |
| Niche/Industry | `Niche/Industry` | `fldNI8sWSzGlPp9Bi` | singleLineText |
| Example Companies URLS * | `Example Companies` ⚠ | `fldMxAF23EH4HjBoN` | multilineText |
| Company Location * | `Company Location` | `fld0h4uIdiaPgF81H` | singleLineText |
| Company Headcount Range * | `Headcount Range` ⚠ | `fldqmTFd7RXkgY59K` | singleLineText |
| Department | `Department` | `fldc8aOFC90G4sW9c` | multilineText |
| Seniority | `Seniority` | `fldLNz68IpJdlZAWD` | multilineText |
| Job Titles * | `Job Titles` | `fldftuFJmd1KRMG8M` | multilineText |
| People Location | `People Location` | `fldkiLO2oyIGVlBVt` | singleLineText |
| Clay Variables & Instructions | `Clay Enrichments` ⚠ | `fldsn3M7qLItqdIO2` | multilineText |
| Notes (If Any) | `Custom Notes` ⚠ | `fldMVh0hKwnPj4LCa` | multilineText |
| Do you have the scripts/copies ready? * | `Copies ready?` ⚠ | `fld1IQ1ZLhHIh5Xb2` | singleSelect |

Type-conditional fields, on the form and in the table:

| Appears when Lead List Type = | Field name | Field ID | Type |
|---|---|---|---|
| Company With Persona | `Niche/Industry`, `Example Companies`, `Company Location`, `Headcount Range` | see above | - |
| Event | `Event Names/URLs` | `fldQ3bMeYiYDO2zZL` | multilineText |
| Signal | `Type of signal` | `fldem7hCngEUKMZyD` | multilineText |
| Signal | `Signal Priority` | `fldyOQDbFSOHLm3L5` | multilineText |

## Select options - use these strings exactly

Airtable rejects anything not on the list, and near-misses ("urgent", "Company w/ Persona")
fail. Copy verbatim.

- **Lead List Type** - `Persona` · `Company With Persona` · `Event` · `Signal`
- **Priority** - `Urgent` · `High` · `Medium` · `Low` · `Pause` · `Build ASAP`
- **Copies ready?** - `Yes` · `No`

## Value shapes

- **`📂 Clients`** - array of record IDs: `["rec6AI1zzahdLCTvH"]`. Never a name string.
- **`Data Needed By`** - `YYYY-MM-DD`. The form shows `dd/mm/yyyy`; the API wants ISO. This
  is a real trip hazard: `07/08/2026` is ambiguous, `2026-08-07` is not.
- **Multiline fields** - real newlines. No `\n` escapes, no markdown, no `====` rules.

## Required, and what "required" actually means

Always: Client, Campaign Name, Lead List Type, Priority, Data Needed By, Job Titles,
Copies ready?

Additionally when Lead List Type = `Company With Persona`: Example Companies, Company
Location, Headcount Range.

Two of those are easy to lose. **Company Location** is separate from People Location and the
form refuses to submit without it - filling only People Location is the classic failure.
**Example Companies** is required even when there are no reference accounts; `n/a` is an
accepted and honest answer, and better than inventing lookalikes that skew the build.

The API does not enforce any of this - a record missing Company Location saves happily and
then stalls in the data team's queue. Enforce it yourself before writing.

## Fields to leave alone

The form does not set these, so neither should this skill: `Status`, `Sourcing Status`,
`Approval Status`, every `* TAM` number, every `* (Lead List)` URL, `Task ID`,
`Slack Message ID`, and the whole copy block (`SMS V1`, `V1 Email Body`, …). They belong to
the data and copy teams. Writing them here fabricates progress and, for `Task ID` and
`Slack Message ID`, can confuse the n8n workflows that own them.

## Downstream automations

Fields on this table carry warnings naming n8n workflows: **"Lead List Request To Slack"**
(owns `Task ID`, `Slack Message ID`) and **"Client Delivery Button Handler"** (owns the TAM
and approval fields). A record created through the API lands in the same table as a form
submission and should trigger the same watcher, but that has not been confirmed end to end.
Check once, then stop worrying about it.
