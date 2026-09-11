# Setting up this workspace on a new machine

This gets you (a Scaletopia GTM strategist) running the exact same Claude Code
setup Aaman uses: all the SMS skills, the playbook, the client tools, and the
connections to Evergreen, EmailBison and GoHighLevel.

Time needed: ~20 minutes. You'll need two things from Aaman first:
1. The **keys file** (sent privately — it is never stored in this repo).
2. A GitHub account that Hilal has added as a collaborator on this repo.

---

## 1. Install the basics

1. **Claude Code** — download the desktop app or install the CLI:
   https://claude.com/claude-code
2. **Git** — on a Mac, open Terminal and type `git --version`; if it's missing,
   macOS will offer to install it. Say yes.

## 2. Clone the repo

Open Terminal, go to the folder where you keep work, and run:

```bash
git clone https://github.com/hilalaziz32/ICP-development.git
cd ICP-development
```

If it asks you to log in, use your GitHub account (the one Hilal added).

## 3. Add your keys

1. Duplicate the file `.env.example` and rename the copy to `.env`.
2. Open `.env` and paste in the values from the keys file Aaman sent you.
3. **Never** commit `.env` or paste keys into any file inside the repo —
   git is configured to ignore `.env`, keep it that way.

## 4. Connect the client accounts (MCP servers)

The keys file from Aaman also contains a list of ready-made `claude mcp add …`
commands — one per client account (EmailBison for email, GoHighLevel for SMS).

Paste them into Terminal one at a time (from any folder — they install
user-wide). Then verify with:

```bash
claude mcp list
```

You should see the `emailbison-*` and `ghl-*` servers listed as connected.
Which client uses which server is mapped in [clients/registry.json](clients/registry.json).

## 5. Python tools (one-time)

Some tools (GHL SMS mining, transcript search) are Python scripts. Set them up with:

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

## 6. Start working

Open Claude Code **in this folder** (`claude` in Terminal, or open the folder
in the desktop app). That's it — the skills load automatically from
`.claude/skills/`, nothing to install.

The main workflow, in order:

| Step | Skill | What it does |
|---|---|---|
| 1 | `sms-brief` | Layer A market research brief for a client + segment |
| 2 | `case-study-developer` | Turns a chosen case study into proof + mechanism menus |
| 3 | `mechanism-wordsmith` | Reframes a literal mechanism into SMS-ready lines |
| 4 | `sms-draft` | Assembles ship-ready T1/T2 SMS variants and QAs them |
| — | `sms-performance` | Mines GHL for what a client's copy actually did |
| — | `evergreen-stats` | Numbers from the Evergreen API: sent, PRs, booked, which variant won |
| — | `evergreen-research` | Pulls pains/proof/winners/objections; saves findings back |
| — | `evergreen-data` | Reference only — the full Evergreen endpoint catalogue |
| — | `call-corpus-search` | Searches sales-call transcripts for a pain/theme |

Just describe what you want in plain English ("draft the brief for Big Leap",
"what SMS copy has Strike Tax run?") — the right skill triggers on its own.

## Where things live

- `.claude/skills/` — the skills (the reasoning engine)
- `sms-playbook/` — winners.csv / losers.csv + the playbook docs
- `clients/` — per-client workspaces and outputs (`registry.json` maps each
  client to its channels)
- `tools/` — Python scripts the skills call under the hood

## Keeping in sync

Before you start a session, pull the latest:

```bash
git pull
```

When you've produced work worth sharing, ask Claude Code:
"commit my changes and push to GitHub" — it will handle git for you.
