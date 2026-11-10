# Judging replies

Judge per person, over everything they sent. A positive is a person, not a message.

| Label | Counts as | Examples (real) |
|---|---|---|
| **Warm** | positive | "Let's chat", "Kylie, sure. Let's chat.", "Call me", "Yes, send an email", "Email me", "Sure, how does it work", "Yes. I'd definitely like to see. Let me find a time", "Send me an email and lmk cost", "How do you define results?", "explain", "Take my money" (check the tone, count it, flag it) |
| **Booked** | positive + booked | agreed a time, or Kylie confirmed "I have booked us in" |
| **Engaged** | not counted, mention | gives their real segment or pushes back with detail ("Small medium sized commercial and municipal accounts are more interesting..."), compliments ("This is great outreach") |
| **Referral** | not counted, list it | "Ping David Chase on linked in", "Chad Collier is the CEO and is where you should start", "Katherine is CMO. She will evaluate not me" (Vantiq: list as warm-via-referral) |
| **Not a lead** | no | "no longer with", "wrong number", "This is not Tim", "I'm not the decision maker", company no longer exists |
| **No** | no | "Not interested", "not a fit", rude replies, "how did you get my number" with no interest |
| **Stop** | opt-out | STOP / unsubscribe / remove me (the script counts plain ones) |

Edge cases:
- Someone who left but says they still do something relevant (Ron Filkins, "no longer with Change but I still have programs") = not a lead.
- "Who is this?" alone = no, unless they come back warm after Kylie answers.
- Replies to the automated no-show text ("I joined the call and nobody was there") are not positives but go straight to "fix today".
- The do-not-chase list (`references/do-not-chase.md`) overrides everything. A one-person company booking is not a qualified call.
- Evergreen marks some warm replies "Disqualified" (e.g. Gene Blinkov asked for a video). Use the reply, and say Evergreen disagrees.
