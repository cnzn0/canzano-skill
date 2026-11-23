# PDFs

A PDF is the HTML page, printed. Do not build it in a separate tool with a separate look.

1. Write the page from `assets/template.html`. `base.css` already has the print rules: light theme, A4, 20mm margins, 10.5pt body, mono page numbers bottom right, no orphaned headings, no rows split across pages.
2. Set the running header text in the template's `@page` rule. It is a literal string in mono caps: `NAME // DATE`.
3. Print it: `scripts/pdf.sh page.html out.pdf` (headless Chrome 131 or newer, which the margin boxes need). For Letter, change `size` in the `@page` rule.
4. Open the PDF and look at every page. Check that the fonts embedded, that nothing is clipped at the right margin, and where the page breaks fell. Use `break-before: page` on a section to move a bad break.

Rules:

- No cover page unless the brief asks for one. Page one starts with the title and the answer.
- No gradient or image backgrounds. No coloured header bands.
- Wide tables: reduce columns or set that section landscape with a named page. Do not shrink the type below 8pt.
- Charts and diagrams go in as inline SVG so they stay sharp.
