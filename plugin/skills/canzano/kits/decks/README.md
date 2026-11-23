# Decks kit

Optional. Open this when the output is a slide deck.

A deck is an HTML file built from `kits/decks/deck.html`, with `deck.css` and `deck.js` from this folder on top of the core stylesheets, and the charts kit for its charts and diagrams. Slides are a fixed 1280 x 720, scale to the window, move with the arrow keys, and print one per page: `scripts/pdf.sh deck.html deck.pdf`. If the user needs PowerPoint or Google Slides, build this first, then rebuild it in that format slide by slide with the same layouts, type and colours.

## Before writing a slide

1. Write the deck's one claim in a sentence. That is the title slide.
2. Write the headlines only, in order. Read them top to bottom: they must tell the whole story with no slide bodies. Fix the story here, not later.
3. For each headline choose the one piece of evidence: a chart, a diagram, a number, a table. If there is none, the slide is a statement or it is cut.

## Slides

Each slide is `<section class="slide ...">` with an `<h2>` headline and a `<div class="body">`.

| Layout | Class | Holds |
|---|---|---|
| Title | `slide title` | `<h1>` the claim, one line of who and when |
| Statement | `slide statement` | One sentence in the `<h2>`, nothing else |
| Figure | `slide` | Headline and one chart or diagram filling the body |
| Split | `slide split` | Two sentences on the left, the evidence on the right. `flip` swaps sides, `even` makes halves |
| Numbers | `slide` with `.metrics` | Three or four figures in a strip, one in the accent |
| Table | `slide` with a table | Five rows at most |
| Points | `slide` with `ol.points` | Three to five one-line items. For decisions and next steps only |
| Section | `slide section` | A mono number and the section name |

Set `data-label` on `.deck` for the running label. Slide numbers are automatic. For a dark deck put `data-theme="dark" class="keep-theme"` on `<html>`; it then prints dark too.

## Rules

- One point per slide, and the headline states it as a claim: "Mobile closed the gap with desktop", not "Mobile conversion".
- Headlines are sentence case mono, two lines at most: about 60 characters. The title is about 60 as well. A statement slide is the exception: its one sentence may run to four lines. Body text (paragraphs, list items, table cells) is 20px or larger; labels, captions and chart text are 12 to 13px. If it does not fit, cut words, never shrink type.
- A slide body is one thing. Not a chart and three bullets and a callout.
- The evidence fills the slide. The body starts right under the headline and a chart with no `height` takes all the room there is. Diagrams grow to fit. A small graphic floating in the middle of an empty slide is a fault: enlarge it, switch to a split layout, or cut the slide.
- Headlines wrap in balanced lines with no stranded last word. Keep a number with its unit using `&nbsp;`.
- No bullet dumps, no agenda slide for a deck under fifteen slides, no "Thank you" or "Questions?" slide, no logo on every slide, no clip art or stock imagery.
- Charts and generated diagrams follow `kits/charts/README.md`; hand-drawn ones follow `references/diagrams.md`. Leave `height` off a chart on a slide so it fills the body.
- On a split slide the graphic should still fill most of its column; if it comes out small, give it the whole slide and move the sentence to the caption or the headline.
- Decks print at 1280 x 720 only. Do not set `@page { size: ... }` in a deck; A4 and Letter are for reports.
- The same layout for the same kind of content throughout. Three or four layouts carry most decks.
- Speaker detail goes in notes or an appendix, not onto the slide.
- The last slide is what the audience must decide or do.

## Before delivering

Render every slide and look at each one at full size. Run `cz.lint()` (from `assets/lint.js`, which the deck template loads) and fix what it lists. Check that nothing is clipped at the slide edge, that the headlines alone still tell the story, that every chart's highlighted mark matches its headline, and that the PDF has one slide per page.
