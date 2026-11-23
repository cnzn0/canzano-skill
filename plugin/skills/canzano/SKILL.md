---
name: canzano
description: The canzano house style and minimal design system (Inter, Geist Mono, OKLCH neutrals, hairlines, one accent) for anything people read, review or use, plus rules against fluff in text and UI copy. Covers HTML pages and artifacts, reports, docs, PDFs, decks, charts, dashboards, diagrams, new UIs and written answers. Read it before writing the first line of any such output. It replaces the visual defaults of general design skills, not their technical contracts.
---

# canzano

Outputs should look like a precise instrument, not a template. They are neutral and typographic, with structure made of hairlines, and the content leads. A page that looks like a generic AI dashboard has failed, however well it is built.

## Precedence

1. The current brief and anything the user supplied (references, Figma, screenshots).
2. The project's own rules: its design system, brand guide, AGENTS or CLAUDE files. In an existing product, follow its tokens and components and take only the judgment from this skill.
3. This skill.
4. The visual defaults of general skills. Keep their technical contracts (file formats, CDN allowlists, theme contracts, accessibility, export steps). Replace their palettes, fonts, card styles and decoration with the rules below.

## The design system

The raw colours are in `assets/palette.css` and everything a page uses is in `assets/tokens.css`. Open `assets/specimen.html` to see it rendered.

| Token | Value | Job |
|---|---|---|
| Structure face | Geist Mono 400 | Headings, labels, navigation, table heads, captions, every figure |
| Reading face | Inter 400 / 600 | Prose and control text. Never a headline |
| Sizes | 11 caps, 13, 15 body, 16 lead, 22 title, 28 figure | Three sizes per view at most |
| Neutrals | `--page`, `--raised`, `--panel`, `--rule`, `--rule-strong`, `--ink-3`, `--ink-2`, `--ink` | Structure and text. Most of every output |
| Accent | `--accent` (violet) | Vivid. The one live thing, never a button fill. Point it at another hue to rebrand |
| Status | `--positive`, `--warning`, `--negative`, `--info`, each with a `-soft` tint | A real state only, always next to a word |
| Series | `--series-1` to `--series-8` | Categorical chart colours, used in order |
| Palette | 11 hues x 7 vivid steps and 13 greys in `assets/palette.css` | Charts, heatmaps, extra tags. Read `references/colour.md` |
| Space | 4, 8, 12, 16, 24, 40, 80 | |
| Panel | `--panel` (grey 100, dark grey 900) | Flat panel fill, code blocks, segmented tracks |
| Radius | 6 controls, 12 panels, 0 for document structure and diagrams | |
| Control | 27px tall (`.sm` 23, `.lg` 34), 8px side padding, 1px edge, Inter 14 | Every button, input, select and segmented control, so any mix lines up |
| Motion | 120ms transitions, press scales to 0.97 | |

Start every HTML output from `assets/template.html` with `palette.css`, `tokens.css` and `base.css`. Interfaces add `assets/ui.css` after them. For a single-file output, inline them into one `<style>` in that order. Every colour is OKLCH and comes from a token. Neutrals stay quiet so the colours can be vivid. Never type a new colour value: use a semantic token, then a palette step, then add a hue with `scripts/palette.py`. Change a token in `tokens.css`, never a one-off value in the page. A user who wants their own accent or faces changes them there once.

## The look

- **Surface.** A flat neutral page, white or near black. Never a tint, gradient, texture, glow or blur behind content.
- **Type.** Labels and table heads are ALL CAPS Geist Mono with +0.04em tracking. Prose is Inter at 15 to 16px on a 1.6 line height, capped at 68ch. Tabular numerals everywhere.
- **Structure.** Build with 1px hairlines and whitespace, not boxes. A section opens with a top rule and a mono caps label. Lists of things are ledgers: hairline rows with the label left and the value right. In a document, metrics sit in a strip of columns between two rules, not in tiles. In a UI a figure may sit in a flat panel.
- **Geometry.** Document structure and diagrams are square. Controls and code blocks have a 6px radius and panels 12px. The switch is the one fully rounded control. No drop shadows, except the selected segment and a floating menu.
- **Colour.** Greyscale in three ink steps, plus one vivid accent: the current state, the series that matters or a key figure. Colour is rare and saturated, never dusty, pastel, brownish or greyish. Status colours mark a real state and sit next to a word. Series colours appear only in a chart that needs them. Never mint, seafoam or teal on dark.
- **Marks.** No emoji. No icon sets by default; use text labels. ASCII marks like `→ // [ ] ·` are fine when they mean something.
- **Controls.** Small and crisp: 27px tall, radius 6, a 1px edge and a fill that is a touch lighter at its top and bottom edge. The primary action is dark on a light page and white on a dark page, never the accent. Everything else is the light fill or a text link with a 1px underline. Buttons exist only when something is clickable. A segmented control is a panel track with a raised thumb that does not slide. Controls placed side by side share one height, radius and edge; read `references/controls.md` before building a control row, a combo or a form.
- **Panels.** A flat `--panel` fill with a 12px radius groups a figure, a chart or a detail view. No edge, no shadow, no panel inside a panel. Lists and tables stay hairline ledgers.
- **Gradients.** Only the control fill, and only within about three points of lightness. Never on the page, a hero, a panel or text.
- **Motion.** None by default. Nothing fades or slides in on load or scroll.
- **Density.** Useful density beats air. The first line states the answer or result. Every element carries information. No hero banner, no decorative stats, no "Overview" section that repeats the title.

## Words

No fluff, and no interface that explains itself. Read `references/writing.md` before writing prose or UI copy. The short version:

- The first line is the answer. Length follows the question. Say each thing once.
- Cut openers, restated asks, signposts, recaps, closing offers, stacked hedges and selling words.
- A UI is labels, numbers and actions. No subtitles under titles, helper text that restates a label, section intros, obvious tooltips, instructions, footnotes or captions that describe what is visible.
- Delete the sentence. If the output still works, it stays deleted.

## The generic AI look (never ship these)

- Gradient heroes, gradient text, and a purple or indigo wash over the page: tinted backgrounds, coloured panels, gradient headers. The accent is violet, but it marks one thing on a neutral page; it is never the theme.
- Cards with soft drop shadows, radii above 12px or pill shapes. Grids of three "features" with an icon each.
- Emoji in headings, bullets, status or buttons. Coloured pill badges and chips on everything.
- Decorative KPI tiles: a big number in a shadowed or outlined card with a trend arrow, an icon or a sparkline nobody asked for. (A flat panel holding one labelled figure in a UI is fine; in a document, figures sit in a strip.) Decorative progress bars, rings or meters.
- Glass and blur panels. Callout boxes with a coloured left border ("Tip", "Note", "Key insight").
- Everything centred. Hover lift or scale. Staggered fade-ins. Timeline dots.
- Fake window, browser or terminal chrome, and toy illustrations.
- Title Case Headings, exclamation marks and hype words.
- Explanatory copy in a UI: a subtitle under every title, helper text that restates its label, an intro paragraph per section. A settings row may carry one line that states a fact the label cannot, such as when or to whom.
- Curved or gradient diagram connectors, shadows on diagrams, several stroke weights.
- A sidebar-and-tiles "dashboard" when a single column would read better.

## Formats

- **HTML page or artifact.** One reading column, or a grid for comparisons. A table beats a bullet list for anything with two or more attributes. Design dark and light independently through the tokens.
- **Report, explainer or comparison.** The answer, then the evidence, then the detail. Plain section labels. See `references/writing.md`.
- **Doc (Google Docs, Word, Markdown).** Text first. Short sentence-case headings, tables for comparisons, no emoji, no callout blocks, no rule spam.
- **PDF.** The same HTML, printed. Read `references/pdf.md`.
- **Deck.** Read `references/decks.md` and start from `assets/deck.html`. One claim per slide in the headline, one piece of evidence in the body, 1280 x 720 slides that print one per page.
- **Chart.** Read `references/charts.md` and draw with `assets/viz.js` (bar, hbar, line, scatter, slope, waterfall, heatmap, sparkline). Greys carry context and the accent carries the series that matters. Use the series colours in order when several series must be told apart, and label them directly. Heatmaps and diverging scales follow `references/colour.md`. Direct labels instead of legends where possible, mono caps axis labels, tabular figures, a hairline axis, gridlines at 10% ink at most. No gradients, rounded bar tops or 3D.
- **Diagram.** Read `references/diagrams.md`. `assets/viz.js` draws flow, sequence, layers, tree, timeline and quadrant diagrams from a spec. Orthogonal, one stroke width, monochrome, ALL CAPS Geist Mono.
- **ASCII.** For READMEs, terminals and code comments, and for hero text when asked. Read `references/ascii.md` and generate it with `scripts/ascii.py` so it lines up.
- **UI.** Read `references/ui.md`. Small rounded controls, flat panels, a sidebar frame, Inter leading and mono for labels and figures. It also covers how to behave inside an existing product.
- **Contact or review sheet.** The work at true aspect ratio on the dark page, mono caps labels under each item, no frames.

## Before delivering

Render it and look at it, at full size and at phone width, in both themes when it has both. Then check:

1. Does anything from the generic AI list appear? Remove it.
2. Does any colour appear that is not a token, or a status or series colour without a job? Remove it.
3. Are labels mono caps, prose in Inter, figures tabular, and did the fonts actually load?
4. Does the first screen state the point?
5. Read every sentence and label. Does the output still work without it? Delete it.
6. In every row of controls, do the boxes share one height and style, with one primary?
7. Does any heading, tagline or paragraph end on one stranded word, does any label in a drawing collide with another label or a wire, or does any graphic sit small in empty space? Where `viz.js` is loaded, run `cz.lint()` and fix what it lists, then still look: the lint catches the common cases, not all of them.

Fix what you find before showing it. Say what was rendered and checked, and what was not.
