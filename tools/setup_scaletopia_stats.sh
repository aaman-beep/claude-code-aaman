#!/usr/bin/env bash
# One-time setup so Claude Code can run Scaletopia's daily stats and answer side questions.
#
#   bash tools/setup_scaletopia_stats.sh ~/Downloads/scaletopia-stats-keys.env
#
# The keys file comes from Aaman (sent privately, never committed). It adds three MCP servers to
# ~/.claude.json (GHL legacy, GHL toll-free, EmailBison) and the Evergreen key to this repo's .env.
# A backup of ~/.claude.json is saved first. Nothing is printed except what was set up.
set -euo pipefail
KEYS="${1:-}"
if [ -z "$KEYS" ] || [ ! -f "$KEYS" ]; then
  echo "Usage: bash tools/setup_scaletopia_stats.sh <path to scaletopia-stats-keys.env>"; exit 1
fi
REPO="$(cd "$(dirname "$0")/.." && pwd)"
python3 - "$KEYS" "$REPO" <<'PY'
import json, os, shutil, sys, time
keys_file, repo = sys.argv[1], sys.argv[2]
k = {}
for line in open(keys_file):
    line = line.strip()
    if line and not line.startswith("#") and "=" in line:
        a, b = line.split("=", 1); k[a.strip()] = b.strip().strip('"')
need = ["GHL_LEGACY_TOKEN", "GHL_TOLLFREE_TOKEN", "EMAILBISON_KEY", "EVERGREEN_API_KEY"]
miss = [n for n in need if not k.get(n)]
if miss: sys.exit(f"Keys file is missing: {miss}")

path = os.path.expanduser("~/.claude.json")
cfg = json.load(open(path)) if os.path.exists(path) else {}
if os.path.exists(path):
    shutil.copy(path, f"{path}.bak-{int(time.time())}")
ghl = "https://services.leadconnectorhq.com/mcp/anthropic/v2"
cfg.setdefault("mcpServers", {})
cfg["mcpServers"]["ghl-scaletopia-legacy"] = {"type": "http", "url": ghl, "headers": {
    "Authorization": "Bearer " + k["GHL_LEGACY_TOKEN"], "locationId": "UqMcuYNiET94KiGWH5Ec"}}
cfg["mcpServers"]["ghl-scaletopia"] = {"type": "http", "url": ghl, "headers": {
    "Authorization": "Bearer " + k["GHL_TOLLFREE_TOKEN"], "locationId": "TYVYHj7lX8bamHkOKz4s"}}
cfg["mcpServers"]["emailbison-scaletopia"] = {"type": "http", "url": "https://mcp.emailbison.com/mcp", "headers": {
    "Authorization": "Bearer " + k["EMAILBISON_KEY"],
    "Instance-URL": k.get("EMAILBISON_URL", "https://send.scaletopia.io")}}
json.dump(cfg, open(path, "w"), indent=2)

env = os.path.join(repo, ".env")
lines = [l for l in open(env)] if os.path.exists(env) else []
lines = [l for l in lines if not l.startswith("EVERGREEN_API_KEY=")]
lines.append(f"EVERGREEN_API_KEY={k['EVERGREEN_API_KEY']}\n")
open(env, "w").writelines(lines)
print("Set up: ghl-scaletopia-legacy, ghl-scaletopia, emailbison-scaletopia (in ~/.claude.json) and EVERGREEN_API_KEY (in .env)")
PY
echo "Testing email access..."
python3 "$REPO/.claude/skills/scaletopia-daily-stats/scripts/side_checks.py" email "$(date -v-1d +%F 2>/dev/null || date -d yesterday +%F)" 2>/dev/null \
  || echo "Email test FAILED: the EmailBison key is wrong. Fix the keys file and run this again."
echo
echo "Done. Delete the keys file now: rm \"$KEYS\""
echo "Then restart Claude Code, open this folder, and type: /scaletopia-daily-stats"
