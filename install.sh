#!/bin/sh
# Installs the canzano skill for the agents found on this machine.
# Usage: sh install.sh [target-skills-dir ...]
# With no arguments it installs into every one of these whose parent folder exists:
#   ~/.claude/skills   ~/.agents/skills   ~/.codex/skills
set -e
REPO="https://github.com/cnzn0/canzano-skill"

src="$(cd "$(dirname "$0")" 2>/dev/null && pwd)/skills/canzano"
if [ ! -f "$src/SKILL.md" ]; then
  tmp="$(mktemp -d)"
  trap 'rm -rf "$tmp"' EXIT
  git clone --depth 1 --quiet "$REPO" "$tmp/repo"
  src="$tmp/repo/skills/canzano"
fi

if [ "$#" -gt 0 ]; then
  targets="$*"
else
  targets=""
  for home in "$HOME/.claude" "$HOME/.agents" "$HOME/.codex"; do
    [ -d "$home" ] && targets="$targets $home/skills"
  done
  [ -n "$targets" ] || targets="$HOME/.claude/skills"
fi

for dir in $targets; do
  mkdir -p "$dir"
  if [ -e "$dir/canzano" ]; then          # keep the copy being replaced, in case it had local edits
    rm -rf "$dir/canzano.previous"
    mv "$dir/canzano" "$dir/canzano.previous"
    echo "kept the old copy at $dir/canzano.previous"
  fi
  cp -R "$src" "$dir/canzano"
  echo "installed $dir/canzano"
done
