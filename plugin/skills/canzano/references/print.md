# PDFs and slides

## PDF

A PDF is the HTML page, printed. Do not build it in a separate tool with a separate look.

1. Write the page from `assets/template.html`. The stylesheet already holds the print rules: light theme, A4, 20mm margins, 10.5pt body, mono page numbers bottom right, no heading left alone at the foot of a page, no row split across pages.
2. Set the running header text in the template's `@page` rule: `NAME // DATE`.
3. Print it: `scripts/pdf.sh page.html out.pdf` (headless Chrome 131 or newer). For Letter, change `size` in the `@page` rule.
4. Open the PDF and look at every page: the fonts, the right margin, where the breaks fell. Use `break-before: page` on a section to move a bad break.

- A page holds about 300 words of text, less with a metric strip, a table or a chart. When it runs over, cut content. Never shrink type or margins.
- No cover page unless asked. Page one starts with the title and the answer.
- A dark page prints light. To print it dark, `<html>` needs `data-theme="dark"` and class `keep-theme`.
- A drawing wider than the page shrinks to fit. If its labels come out small, redraw it narrower.

## Slides

A deck is one HTML file of `<section class="slide">` elements. Copy the `<style>` block and the slides from `examples/slides.html`: slides are 16:9, scale with the window and print one per page with the same `scripts/pdf.sh`. If the user needs PowerPoint or Google Slides, build this first and rebuild it there with the same layouts, type and colours.

1. Write the deck's one claim in a sentence. That is the title slide.
2. Write the headlines only, in order. They must tell the whole story with no slide bodies.
3. For each headline choose one piece of evidence: a chart, a diagram, a number, a table. If there is none, the slide is a statement or it is cut.

- One point per slide. The headline states it as a claim, in sentence case, two lines at most.
- The body is one thing and it fills the slide. A small graphic in the middle of an empty slide is a fault: enlarge it or cut the slide.
- Draw a slide's chart in a viewBox about 1000 wide so its labels read at slide size.
- Body text is 20px or larger at full size. If it does not fit, cut words.
- No bullet dumps, no agenda, no "Thank you" slide, no logo on every slide.
- The last slide is what the audience must decide or do.
- Look at every slide at full size and check the PDF has one slide per page.
