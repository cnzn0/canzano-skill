# PDFs

A PDF is the HTML page, printed. Do not build it in a separate tool with a separate look.

1. Write the page from `assets/template.html`. The core stylesheets already hold the print rules: light theme, A4, 20mm margins, 10.5pt body, mono page numbers bottom right, no orphaned headings, no rows split across pages. A dark page prints light. To print it dark, `<html>` needs both `data-theme="dark"` and class `keep-theme`.
2. Set the running header text in the template's `@page` rule. It is a literal string in mono caps: `NAME // DATE`. Its colour is written out as an `oklch()` value because page margin boxes cannot read custom properties; it is the one colour not taken from a token.
3. Print it: `scripts/pdf.sh page.html out.pdf` (headless Chrome 131 or newer, which the margin boxes need). For Letter, change `size` in the `@page` rule.
4. Open the PDF and look at every page. Check that the fonts embedded, that nothing is clipped at the right margin, and where the page breaks fell. Use `break-before: page` on a section to move a bad break.

Printing changes two things. Charts are drawn at the width of the printed text column, because `pdf.sh` lays the page out at that width first, so their labels print at full size. Diagrams cannot scroll on paper, so one wider than the page shrinks to fit: look at it in the PDF and split it if its labels got small.

A one-page report holds about 180 words under the title, plus either one small chart or one short table, not both. The template's metric strip counts as the chart. Print it, read the page count, and when it runs over, cut content: a row, a sentence, a figure. Never shrink type or margins to make it fit.

Rules:

- No cover page unless the brief asks for one. Page one starts with the title and the answer.
- No gradient or image backgrounds. No coloured header bands.
- Wide tables: reduce columns or set that section landscape with a named page. Do not shrink the type below 8pt.
- Charts and diagrams go in as inline SVG so they stay sharp.
