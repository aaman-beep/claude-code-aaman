# Daily stats: start here (Bakhtawar)

## One-time setup (10 minutes)
1. Install Claude Code (VS Code extension or terminal) and log in with your Scaletopia Claude account.
2. Clone the repo: `git clone https://github.com/aaman-beep/claude-code-aaman.git` and open the folder in VS Code.
3. Aaman sends you a keys file privately (Slack DM). Save it to Downloads, then run from the repo folder:
   `bash tools/setup_scaletopia_stats.sh ~/Downloads/scaletopia-stats-keys.env`
   It should say "Set up: ..." and print yesterday's email numbers. Then delete the keys file.
4. Restart Claude Code.

## Every morning
Type in Claude Code: `/scaletopia-daily-stats` (or "run yesterday's stats").
It pulls GHL + EmailBison + Evergreen, reads every reply, and writes the report with a "fix today" list.
Send Aaman the report. Answer any warm reply nobody answered first.

## Side questions
Just ask Claude in plain words, for example:
- "Were Monday's people already texted before?"
- "How many emails went out this week?"
- "How many inboxes are connected and how many emails a day can we send?"
- "What copy is the 619 workflow sending?"
It knows how (see `references/side-questions.md`).

## Rules
- Never commit the keys file or anything in `local/`. The repo is public.
- Don't change live GHL workflows or EmailBison campaigns without Aaman saying so.
