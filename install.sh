#!/bin/sh
# Installs the canzano skill for the agents found on this machine.
# Usage: sh install.sh [target-skills-dir ...]
# With no arguments it installs into every one of these whose parent folder exists:
#   ~/.claude/skills   ~/.agents/skills   ~/.codex/skills
set -e
REPO="https://github.com/cnzn0/canzano-skill"

# Use the checkout this script sits in, but only when it was run as a file. Piped through sh,
# $0 is the shell, and the current folder must not be mistaken for a checkout.
src=""
case "$0" in
  */install.sh|install.sh)
    here="$(cd "$(dirname "$0")" 2>/dev/null && pwd)"
    [ -f "$here/plugin/skills/canzano/SKILL.md" ] && src="$here/plugin/skills/canzano" ;;
esac
if [ -z "$src" ]; then
  tmp="$(mktemp -d)"
  trap 'rm -rf "$tmp"' EXIT
  git clone --depth 1 --quiet "$REPO" "$tmp/repo"
  src="$tmp/repo/plugin/skills/canzano"
fi

if [ "$#" -eq 0 ]; then
  for home in "$HOME/.claude" "$HOME/.agents" "$HOME/.codex"; do
    [ -d "$home" ] && set -- "$@" "$home/skills"
  done
  [ "$#" -gt 0 ] || set -- "$HOME/.claude/skills"
fi

for dir in "$@"; do
  mkdir -p "$dir"
  if [ -e "$dir/canzano" ]; then          # keep the copy being replaced, in case it had local edits
    rm -rf "$dir/canzano.previous"
    mv "$dir/canzano" "$dir/canzano.previous"
    echo "kept the old copy at $dir/canzano.previous"
  fi
  cp -R "$src" "$dir/canzano"
  find "$dir/canzano" -name "__pycache__" -type d -prune -exec rm -rf {} + 2>/dev/null || true
  echo "installed $dir/canzano"
done
