#!/bin/sh
# Renders the readme images into showcase/. Run from anywhere: sh tools/showcase/build.sh
set -e
here="$(cd "$(dirname "$0")" && pwd)"; out="$here/../../showcase"
chrome="${CHROME:-/Applications/Google Chrome.app/Contents/MacOS/Google Chrome}"
shot() {   # name height
  prof="$(mktemp -d)"
  "$chrome" --user-data-dir="$prof" --headless=new --disable-gpu --no-first-run --hide-scrollbars --allow-file-access-from-files \
    --force-device-scale-factor=2 --window-size=1200,$2 --virtual-time-budget=8000 --screenshot="$out/$1.png" "file://$here/index.html?scene=$1" >/dev/null 2>&1
  rm -rf "$prof"; echo "$1"
}
shot hero 750; shot ui-dark 750; shot report 560; shot chart 680; shot slides 540; shot palette 560
