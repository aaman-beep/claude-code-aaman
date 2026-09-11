#!/usr/bin/env python3
"""Aaman's voice-note review of the Aug 24-28 unbooked replies, paired with the real threads.

Quotes are pulled from the pack JSON by row index rather than retyped, so what Jabare reads
is exactly what was sent. The commentary is Aaman's, transcribed from the voice note; the
counts under "the pattern" are computed from the same 82 rows.

USAGE
  python3 tools/reply_coaching_page.py
"""
import html as H
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ghl_mine as gm

OUT = os.path.join(gm.ROOT, "clients/_rollup/output")
SRC = os.path.join(OUT, "2026-08-24_to_2026-08-28-unbooked-replies.json")
D = json.load(open(SRC))
ROWS = D["rows"]
e = H.escape

# ---------------------------------------------------------------- the review
# (row index, heading, verdict paragraphs, rewrite or None, [(label, msg index)] to quote)
REVIEW = [
 dict(i=38, tag="the one that started it",
   verdict=["The tag is right. A pricing question sitting inside <i>“I’d love to learn more”</i> "
            "is fine as a More Info request, even though the price part reads as an objection.",
            "The reply is the problem, and it isn’t that it sounds like AI — saying that helps "
            "nobody. It’s that it sounds like we’re trying to <b>convince them onto a call</b>. "
            "That is what pushes people away. They asked one question. Answer it."],
   rewrite="Hey [name], typically it’s 5–10% of any incremental revenue we recover for you, "
           "and there’s no upfront or monthly cost at all. Happy to show you how the product "
           "works — if it still sounds interesting, how does next Wednesday work?",
   fu_verdict=["The follow-up is blabbering. It repeats the same sentence back at them with "
               "nothing new attached, and it opens with “Hey John” — which is not his name "
               "(see the CRM placeholder bug below)."],
   fu_rewrite="Hey [name], you asked about price — it’s purely performance. Do those economics "
              "make sense?\n\nThen: a case study. Then: still happy to show you how it works. "
              "Then: a break-up.",
   msgs=[("their reply", 1), ("what we sent", 2), ("the follow-up", 3)]),

 dict(i=47, tag="answered well, then undone by the follow-up",
   verdict=["The answer itself is good — they asked how it works and we actually explained how "
            "it works. That is the right instinct and it should be the template.",
            "Then the follow-up asks whether it’s <i>“worth me sending the details now”</i>. "
            "<b>We already sent the details, two days earlier, in the message directly above it.</b> "
            "It went out twice, one minute apart."],
   rewrite=None,
   msgs=[("their reply", 1), ("what we sent — this part is right", 2),
         ("the follow-up, sent twice", 3)]),

 dict(i=41, tag="they asked for information, we asked for a slot",
   verdict=["They said they’d be interested in <b>more information</b>. We came back with two "
            "meeting times. We didn’t read the call to action.",
            "And the message tells NO MINIMUMS we’ll walk them through how it would work "
            "<b>“for Tektonla”</b> — a different company entirely."],
   rewrite="Sounds good — here’s how it works: [the actual explanation]. If that lands, how "
           "does tomorrow afternoon or sometime earlier next week look?",
   msgs=[("their reply", 1), ("what we sent", 2), ("the follow-up", 3)]),

 dict(i=60, tag="a blob with no direction",
   verdict=["Part of this is that it’s a slightly unqualified lead — the CEO forwarded it to "
            "the Head of GTM, who is now asking on his behalf.",
            "But the real issue is the shape of the reply: <i>“really appreciate it, great to "
            "meet you”</i> and then <b>a blob of information with no direction</b>. Nothing in "
            "it tells Paul what he is supposed to do next, or what we think Loyalsnap should do."],
   rewrite=None,
   msgs=[("their reply", 1), ("what we sent", 2)]),

 dict(i=64, tag="close — one word away",
   verdict=["This is genuinely not bad. He offered Friday, Friday doesn’t work, we moved him.",
            "One change: <b>“a bit tight on my end” is vague</b>. Give a real reason — “I’m "
            "travelling Friday” — and it stops sounding like a brush-off. Small thing, and it’s "
            "still one of the better replies in the week."],
   rewrite="Friday I’m travelling — how about Thursday afternoon, or earlier next week?",
   msgs=[("their reply", 1), ("what we sent", 2)]),

 dict(i=53, tag="he offered an intro, we went straight to slots",
   verdict=["He offered <b>an intro</b> — a low-commitment, mutual thing. We answered with two "
            "specific slots and a note about our time zone.",
            "Don’t go into that mode. Either ask whether he’s still up for the intro, or "
            "reposition it — a phone call, or lead with the case study. This is exactly where a "
            "<b>Power Request follow-up structure</b> is missing."],
   rewrite=None,
   msgs=[("their reply", 1), ("what we sent", 2), ("the follow-up", 3)]),

 dict(i=54, tag="one time, one time zone",
   verdict=["One slot, one time zone, and then nothing. <b>Not enough follow-up at all.</b>",
            "“Yes” is a strong signal and we spent it on a single Friday morning."],
   rewrite=None,
   msgs=[("their reply", 1), ("what we sent", 2)]),

 dict(i=57, tag="“Ok” is not “yes”",
   verdict=["When someone writes <i>“Ok”</i>, that is usually not the best signal — and we "
            "opened with <b>“Awesome.”</b> Don’t. Go straight to something concrete they can "
            "answer in one word.",
            "There’s a speed problem here too, and then no follow-up or nurturing at all."],
   rewrite="How does 11am sound? Or shall I give you a ring?",
   msgs=[("their reply", 1), ("what we sent", 2)]),

 dict(i=70, tag="the reply is fine — the silence isn’t",
   verdict=["The reply here is actually not bad. Flexible, a couple of options, no waffle.",
            "In this situation the <b>follow-ups matter more than the reply does</b>. He said "
            "“we can connect” and then nothing happened."],
   rewrite=None,
   msgs=[("their reply", 1), ("what we sent", 2)]),

 dict(i=50, tag="she told us where she wanted to meet",
   verdict=["She said yes, then said <b>“we can meet at my business office to discuss further "
            "logistics.”</b> We replied with two Zoom-shaped time slots and did not acknowledge "
            "the office at all.",
            "This is the <i>“Yes” → “Awesome… happy to show you”</i> pattern — about a 6 out of "
            "10. <b>“Happy to show you” is a weak ask</b> when they have already said yes. "
            "Move to the time."],
   rewrite="Sounds good — how does tomorrow afternoon or sometime earlier next week look? "
           "Happy to come to you.",
   msgs=[("their reply", 1), ("and then", 2), ("what we sent", 3)]),

 dict(i=44, tag="he gave us everything and we asked nothing back",
   verdict=["He wrote a long, specific reply, brought a colleague in, told us exactly what kind "
            "of firm they are and what they don’t want — and <b>we didn’t ask a single question "
            "back.</b>",
            "What it needed: acknowledge the detail, use it (he’s a director, boutique, "
            "wineries — say so), then give times. If he had ended on “what do you think we "
            "should do?”, that’s a custom response and genuinely harder.",
            "The follow-up also went out twice in the same minute."],
   rewrite=None,
   msgs=[("their reply", 1), ("what we sent", 2), ("the follow-up, sent twice", 3)]),

 dict(i=51, tag="the good one",
   verdict=["<b>This is the best pricing reply of the week.</b> It answers the question, "
            "reframes to the audit, and moves to a time. Genuinely not the worst.",
            "The polish would be to make the range feel like a choice they control, and to put "
            "performance pricing on the table."],
   rewrite="Typically starts from 1–3k depending on how fast you want to grow, and we can "
           "potentially do performance-based pricing too. Either way, happy to run an audit "
           "to show you the gaps and the ROI. Are you free around [time]?",
   msgs=[("their reply", 1), ("what we sent", 2)]),
]

PATTERNS = [
 ("Follow-ups are the weakest link, by a distance",
  "Almost every follow-up repeats the reply above it with nothing new attached. "
  "“You asked about pricing — it’s performance based.” They know. That was the last message. "
  "A follow-up has to carry something the previous one didn’t: a case study, a different angle, "
  "or a straight break-up.", None),
 ("We push for a call when they asked for information",
  "Someone writes “send me more on how this works” and gets two meeting slots back. "
  "The call to action in their message is the thing to answer.", None),
 ("“Happy to show you” is not an ask",
  "It hands them an opt-out. When they have already said yes, name a time and make it a "
  "yes/no question.",
  "21 of the 40 answered threads contain no clock time at all. 5 more give exactly one."),
 ("One slot, one time zone",
  "A single Friday 10am est to a lead who just said yes. Give two, in their zone.", None),
 ("A blob of information with no direction",
  "Case studies and links pasted in with nothing telling them what to do with it, or what we "
  "think they should do.", None),
 ("Vague excuses instead of real reasons",
  "“A bit tight on my end” reads as a brush-off. “I’m travelling Friday” does not.", None),
 ("The detail they gave us goes unused",
  "When someone writes four paragraphs about their business, the reply has to prove we read it.",
  None),
]

BUILD = [
 ("A pricing answer, per client",
  "One approved way to answer “what does it cost” for each client, so nobody has to improvise "
  "their way to a call invite. Lives under the More Info branch."),
 ("A pricing follow-up sequence",
  "Separate from the general one. Beat 1: do those economics make sense. Beat 2: case study. "
  "Beat 3: still happy to show you how it works. Beat 4: break-up."),
 ("A More Info follow-up sequence",
  "Distinct again — the failure mode here is re-offering information we already sent."),
 ("A Power Request follow-up structure",
  "The gap Aaman named twice. They said yes and went quiet; there is currently nothing to send."),
 ("SMS follow-up reminders",
  "Nothing chased the SMS power requests at all this week."),
 ("Formal case studies",
  "Named as the missing ammunition for changing the angle on a follow-up."),
]

OPEN = [
 "On a Power Request where they already said yes and then went silent — what does the "
 "follow-up actually say? How do you change the angle without just re-asking for the call?",
 "Should the follow-up always connect back to the original CTA, or is a fresh angle better?",
]

FOUND = [
 ("A qualified buyer asked six questions and never got a reply", "redo", 5,
  "Dana, the e-commerce manager at Danielle Gerber, asked how the outreach works, how we handle "
  "non-opted-in customers, the AI-vs-human side, Shopify integration, and how pricing and "
  "attribution are structured. She offered to book a Zoom and gave her availability window. "
  "<b>Nobody ever answered.</b> This is the single worst miss in the week and it isn’t in the "
  "voice note."),
 ("We are calling people “John”", None, None,
  "Redo’s CRM stores the placeholder “John Doe” where the name is unknown, and the follow-up "
  "template merges it in. <b>Three threads this week open with “Hey John” to someone not named "
  "John</b> — Mo.Na. Gems, L’Animal and NO MINIMUMS. Aaman half-caught this live (“that’s not my "
  "name, but anyways”). It needs a guard: no first-name merge when the name is a placeholder."),
 ("One reply named the wrong company", "redo", 41,
  "NO MINIMUMS was told we’d walk them through how it would work <b>“for Tektonla.”</b>"),
 ("Six threads got the same follow-up twice", None, None,
  "Identical text, usually a minute apart: Guy Carl (Wise Digital), L’Animal (Redo), and four "
  "Kynship threads — Jon Pierre Francia, Corinne da Silva, Charles Hawkins, Karima El-hakkaoui."),
]

# ---------------------------------------------------------------- render
def msg(r, idx, label):
    m = r["messages"][idx]
    who = m["sender"] or ("them" if m["dir"] == "inbound" else "us")
    return (f'<div class="m {"in" if m["dir"] == "inbound" else "out"}">'
            f'<span class="w">{e(label)} · {e(who)} · {e(m["when"])}</span>{e(m["body"])}</div>')


def block(x):
    r = ROWS[x["i"]]
    lab = D["labels"].get(r["client_slug"], r["client_slug"])
    who = f'{r["contact"]} — {r["company"]}' if r.get("company") else r["contact"]
    head = (f'<div class="chips"><span class="chip client">{e(lab)}</span>'
            f'<span class="chip">{e(r["category"])}</span>'
            f'<span class="chip">{e(r["channel"])}</span>'
            f'<span class="chip tag">{e(x["tag"])}</span></div>')
    parts = [f'<article class="t"><h3>{e(who)}</h3>{head}']
    fu = [p for p in x["msgs"] if "follow-up" in p[0]]
    main = [p for p in x["msgs"] if "follow-up" not in p[0]]
    parts += [msg(r, i, l) for l, i in main]
    parts.append('<div class="v"><span class="vh">Aaman’s read</span>' +
                 "".join(f"<p>{p}</p>" for p in x["verdict"]) + "</div>")
    if x.get("rewrite"):
        parts.append('<div class="fix"><span class="vh">say this instead</span><p>' +
                     e(x["rewrite"]).replace("\n\n", "</p><p>") + "</p></div>")
    if fu:
        parts += [msg(r, i, l) for l, i in fu]
    if x.get("fu_verdict"):
        parts.append('<div class="v"><span class="vh">on the follow-up</span>' +
                     "".join(f"<p>{p}</p>" for p in x["fu_verdict"]) + "</div>")
    if x.get("fu_rewrite"):
        parts.append('<div class="fix"><span class="vh">say this instead</span><p>' +
                     e(x["fu_rewrite"]).replace("\n\n", "</p><p>") + "</p></div>")
    return "".join(parts) + "</article>"


pat = "".join(
    f'<li><b>{e(t)}</b><p>{d}</p>{f"<p class=num>{e(n)}</p>" if n else ""}</li>'
    for t, d, n in PATTERNS)
bld = "".join(f'<li><b>{e(t)}</b><p>{e(d)}</p></li>' for t, d in BUILD)
opn = "".join(f"<li>{e(q)}</li>" for q in OPEN)
fnd = "".join(f'<li><b>{e(t)}</b><p>{d}</p></li>' for t, _s, _i, d in FOUND)

CSS = """
:root{--paper:#F4F5F7;--card:#FFF;--ink:#171A20;--ink-2:#3D4453;--muted:#6B7280;
--line:#E1E4EA;--line-2:#EFF1F4;--accent:#B5771A;--accent-soft:#FBF0DC;
--good:#1B7A4B;--good-soft:#E9F4EE;--bad:#B8413A;--bad-soft:#FAE7E5;
--in-soft:#EAF1FB;--in-line:#2B5FA8;
--serif:"Iowan Old Style","Palatino Linotype",Palatino,Georgia,serif;
--sans:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;
--mono:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){
--paper:#0F1116;--card:#171A21;--ink:#E7E9ED;--ink-2:#B6BCC7;--muted:#818997;
--line:#272C36;--line-2:#1E222A;--accent:#E0A84C;--accent-soft:#2E2617;
--good:#4FBF85;--good-soft:#15291F;--bad:#E2726A;--bad-soft:#341C1A;
--in-soft:#16202E;--in-line:#5D93DA;}}
:root[data-theme="dark"]{--paper:#0F1116;--card:#171A21;--ink:#E7E9ED;--ink-2:#B6BCC7;
--muted:#818997;--line:#272C36;--line-2:#1E222A;--accent:#E0A84C;--accent-soft:#2E2617;
--good:#4FBF85;--good-soft:#15291F;--bad:#E2726A;--bad-soft:#341C1A;
--in-soft:#16202E;--in-line:#5D93DA;}
*{box-sizing:border-box;}
body{margin:0;background:var(--paper);color:var(--ink);font-family:var(--sans);
line-height:1.6;-webkit-font-smoothing:antialiased;}
.wrap{max-width:800px;margin:0 auto;padding:0 22px 110px;}
header{padding:46px 0 26px;border-bottom:1px solid var(--line);}
.eyebrow{font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--accent);
font-weight:650;margin:0 0 10px;}
h1{font-family:var(--serif);font-size:clamp(28px,4.4vw,42px);line-height:1.1;margin:0 0 14px;
font-weight:600;letter-spacing:-.015em;text-wrap:balance;}
.lede{color:var(--ink-2);margin:0 0 12px;font-size:16px;}
.lede b{color:var(--ink);font-weight:650;}
.straw{background:var(--accent-soft);border:1px solid var(--accent);border-radius:10px;
padding:13px 16px;font-size:14px;color:var(--ink);margin:20px 0 0;}
.straw b{font-weight:700;}
h2{font-family:var(--serif);font-size:26px;margin:52px 0 4px;font-weight:600;
letter-spacing:-.01em;}
h2+.sub{color:var(--muted);font-size:14px;margin:0 0 18px;}
h3{font-family:var(--serif);font-size:20px;margin:0 0 9px;font-weight:600;letter-spacing:-.01em;}
ol.pat,ul.plain{padding:0;margin:0;list-style:none;counter-reset:p;}
ol.pat>li{counter-increment:p;position:relative;padding:0 0 0 42px;margin:0 0 22px;}
ol.pat>li::before{content:counter(p);position:absolute;left:0;top:1px;width:27px;height:27px;
border-radius:50%;background:var(--bad-soft);color:var(--bad);font-size:13px;font-weight:700;
display:grid;place-items:center;font-variant-numeric:tabular-nums;}
ul.plain>li{margin:0 0 18px;padding:0 0 0 16px;border-left:2px solid var(--line);}
ol.pat b,ul.plain b{font-weight:650;}
ol.pat p,ul.plain p{margin:4px 0 0;color:var(--ink-2);font-size:14.5px;}
p.num{color:var(--accent)!important;font-variant-numeric:tabular-nums;font-size:13.5px!important;
font-weight:600;}
article.t{background:var(--card);border:1px solid var(--line);border-radius:12px;
padding:20px 22px;margin:0 0 20px;}
.chips{display:flex;flex-wrap:wrap;gap:6px;margin:0 0 15px;}
.chip{font-size:11px;padding:2.5px 9px;border-radius:20px;border:1px solid var(--line);
color:var(--ink-2);background:var(--paper);}
.chip.client{background:var(--accent-soft);border-color:var(--accent);color:var(--accent);
font-weight:650;}
.chip.tag{background:var(--line-2);font-style:italic;}
.m{font-size:14px;padding:11px 14px;border-radius:9px;margin:0 0 10px;white-space:pre-wrap;
line-height:1.55;word-break:break-word;}
.m.in{background:var(--in-soft);border-left:2px solid var(--in-line);}
.m.out{background:var(--line-2);border-left:2px solid var(--line);}
.m .w{display:block;font-size:10.5px;letter-spacing:.06em;text-transform:uppercase;
color:var(--muted);margin:0 0 5px;font-weight:700;}
.m.in .w{color:var(--in-line);}
.v,.fix{border-radius:9px;padding:13px 15px;margin:14px 0 0;}
.v{background:var(--accent-soft);border-left:3px solid var(--accent);}
.fix{background:var(--good-soft);border-left:3px solid var(--good);font-family:var(--mono);
font-size:13.5px;line-height:1.6;}
.vh{display:block;font-size:10.5px;letter-spacing:.07em;text-transform:uppercase;font-weight:700;
margin:0 0 7px;font-family:var(--sans);}
.v .vh{color:var(--accent);} .fix .vh{color:var(--good);}
.v p,.fix p{margin:0 0 9px;font-size:14.5px;}
.fix p{font-size:13.5px;}
.v p:last-child,.fix p:last-child{margin:0;}
footer{margin:60px 0 0;padding:20px 0 0;border-top:1px solid var(--line);font-size:13px;
color:var(--muted);}
footer a{color:var(--accent);}
"""

BODY = f"""<title>Reply Review, Aug 24–28</title>
<style>{CSS}</style>
<div class="wrap">
<header>
<p class="eyebrow">Inbox coaching · week of Aug 24</p>
<h1>What we said back, and what we should have said</h1>
<p class="lede">Twelve threads from the {len(ROWS)} replies that never became a meeting, with
what actually went out and what should have gone out instead. <b>The single biggest problem
is not the replies — it is the follow-ups.</b> Almost every one repeats the message above it
with nothing new attached.</p>
<div class="straw"><b>Strawman — redline it before it goes to Jabare.</b> The verdicts are
transcribed from Aaman's voice note and grouped by me; the wording is mine and the counts are
computed from the data. Change anything that doesn't sound like you.</div>
</header>

<h2>The pattern</h2>
<p class="sub">Seven things that came up more than once, worst first.</p>
<ol class="pat">{pat}</ol>

<h2>Thread by thread</h2>
<p class="sub">Their words, ours, and the fix. Quotes are verbatim from the send log.</p>
{"".join(block(x) for x in REVIEW)}

<h2>What to build</h2>
<p class="sub">The systemic fixes Aaman named — most of them are templates that don't exist yet.</p>
<ul class="plain">{bld}</ul>

<h2>Still open</h2>
<p class="sub">Flagged in the voice note as unresolved. Worth deciding before writing the templates.</p>
<ul class="plain">{opn}</ul>

<h2>Four things not in the voice note</h2>
<p class="sub">Found in the same 82 threads while matching up the commentary.</p>
<ul class="plain">{fnd}</ul>

<footer>Built from
<code>clients/_rollup/output/2026-08-24_to_2026-08-28-unbooked-replies.json</code> ·
rebuild with <code>python3 tools/reply_coaching_page.py</code> ·
the full 82-reply list is the companion page.</footer>
</div>
"""

dst = os.path.join(OUT, "2026-08-24_to_2026-08-28-reply-coaching.html")
open(dst, "w").write(BODY)
print(f"  {len(REVIEW)} threads reviewed -> {dst}")
