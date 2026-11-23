#!/bin/sh
# Print an HTML file to PDF with headless Chrome. Usage: pdf.sh input.html [output.pdf]
# Page size, margins, running header and page numbers come from the page's own print CSS.
set -e
in="$1"; out="${2:-${1%.html}.pdf}"
[ -f "$in" ] || { echo "usage: pdf.sh input.html [output.pdf]" >&2; exit 1; }
for c in "${CHROME:-}" \
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  "/Applications/Chromium.app/Contents/MacOS/Chromium" \
  "$(command -v google-chrome 2>/dev/null)" "$(command -v chromium 2>/dev/null)" \
  "$(command -v chromium-browser 2>/dev/null)"; do
  [ -n "$c" ] && [ -x "$c" ] && chrome="$c" && break
done
[ -n "$chrome" ] || { echo "No Chrome found. Set CHROME=/path/to/chrome." >&2; exit 1; }
abs="$(cd "$(dirname "$in")" && pwd)/$(basename "$in")"
# Lay out at the width of the printed text column (A4 minus 20mm margins, plus the page gutters), so
# charts are drawn at the size they print and their labels stay 11px. Override with PDF_WIDTH.
flags="--headless=new --disable-gpu --no-pdf-header-footer --hide-scrollbars --window-size=${PDF_WIDTH:-690},1000"
[ "$(id -u)" = "0" ] && flags="$flags --no-sandbox"      # Chrome refuses to run sandboxed as root
log="$(mktemp)"; rm -f "$out"
"$chrome" $flags ${CHROME_FLAGS:-} --virtual-time-budget=5000 --print-to-pdf="$out" "file://$abs" 2>"$log" || true
if [ ! -s "$out" ]; then echo "pdf.sh: Chrome did not write $out" >&2; tail -20 "$log" >&2; rm -f "$log"; exit 1; fi
rm -f "$log"
echo "$out"
