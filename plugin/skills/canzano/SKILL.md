---
name: canzano
description: The canzano house style and minimal design system (Inter, Geist Mono, OKLCH colour, hairlines, small crisp controls) for anything people read, review or use, with rules against fluff in text and UI copy. Covers HTML pages and artifacts, reports, docs, PDFs, decks, charts, diagrams, new UIs and written answers. Read it before writing the first line of any such output. It replaces the visual defaults of general design skills, not their technical contracts.
---

# canzano

Outputs should look like a precise instrument, not a template: neutral, typographic, built from hairlines, with the content leading and colour used rarely and vividly. An output that looks like a generic AI dashboard has failed, however well it is built.

## Precedence

1. The current brief and anything the user supplied (references, Figma, screenshots).
2. The project's own rules: its design system, brand guide, AGENTS or CLAUDE files. In an existing product, follow its tokens and components and take only the judgment from this skill.
3. This skill.
4. The visual defaults of general skills. Keep their technical contracts (file formats, CDN allowlists, theme contracts, accessibility, export steps). Replace their palettes, fonts, card styles and decoration with the rules below.

## What is here

| File | Use it for |
|---|---|
| `assets/palette.css`, `assets/tokens.css`, `assets/base.css` | Every HTML output. The whole design system: colour, type, tables, controls, panels, print |
| `assets/template.html` | The starting point for a page, report or PDF |
| `examples/ui.html` | An interface to copy from |
| `examples/chart.html` | Two charts and a diagram, hand-written SVG |
| `examples/slides.html` | A deck |
| `references/` | Short guides: `writing.md`, `colour.md`, `ui.md`, `figures.md`, `print.md` |
| `scripts/pdf.sh` | Print a page to PDF |

There is no chart library, no component framework and no script to run in the page. The skill is rules, tokens and examples; write the markup yourself to match them. For a single file, inline the three stylesheets into one `<style>` in the order palette, tokens, base.

The stylesheet uses cascade layers, so styles written in the page itself always win. Never add `!important` or raise a selector's specificity to beat it.

## The system

| Token | Value | Job |
|---|---|---|
| Structure face | Geist Mono 400 (500 for emphasis) | Headings, labels, table heads, captions, every figure |
| Reading face | Inter 400, 500, 600 | Prose and control text. Never a document headline |
| Sizes | Documents: 11 caps, 13, 15 body, 16 lead, 22 title, 28 figure. Interfaces: 11 caps, 14 controls, 15 body, 20 panel title, 26 page title | Use the scale; never an in-between size |
| Neutrals | `--page`, `--raised`, `--panel`, `--rule`, `--rule-strong`, `--ink-3`, `--ink-2`, `--ink` | Structure and text. Most of every output |
| Accent | `--accent` (violet) | Vivid. The one live thing, never a button fill |
| Status | `--positive`, `--warning`, `--negative`, `--info`, each with a `-soft` tint | A real state only: a small square beside a word in ink |
| Series | `--series-1` to `--series-8` | Chart categories, used in order |
| Palette | 11 hues x 7 vivid steps and 13 greys | Read `references/colour.md` before reaching in |
| Space | 4, 8, 12, 16, 24, 40, 80 (`--s1` to `--s7`) | |
| Radius | 6 controls and code, 12 panels, 0 document structure and diagrams | The switch is the one fully round control |
| Control | 27px tall (`.sm` 23, `.lg` 34), 1px edge, Inter 14 | Every button, input, select and segmented control |
| Motion | 120ms transitions, press scales to 0.97 | Nothing animates in on load or scroll |

Every colour is OKLCH and comes from a token. Never type a new colour value: use a semantic token, then a palette step. Change a token in `tokens.css`, never a one-off value in a page.

## The look

These hold for every output.

- **Surface.** A flat neutral page, white or near black. No tint, texture, glow or blur behind content.
- **Type.** Labels and table heads are ALL CAPS Geist Mono with +0.04em tracking. Prose is Inter at 15 to 16px on a 1.6 line height, capped at 68ch. Tabular numerals everywhere.
- **Colour.** Greyscale in three ink steps, plus one vivid accent for the single thing that matters: the current state, the series the chart is about, a key figure. Status colours mark a real state as a small square beside a word. Colour is rare and saturated, never dusty, pastel, brownish or greyish. No mint, seafoam or teal.
- **Gradients.** Only the control fill, within about three points of lightness. Never on a page, a hero, a panel or text.
- **Marks.** No emoji. No icon sets by default; use text labels. ASCII marks like `→ // [ ] ·` are fine when they mean something.
- **Wrapping.** No heading, tagline or caption ends on one stranded word, and a number keeps its unit (`0.88&nbsp;s`). The stylesheet balances headings; see `references/writing.md`.
- **Density.** Useful density beats air. The first line states the answer or result. Every element carries information.

Structure depends on what the output is.

- **A document** (page, report, doc, PDF) is square and built from hairlines and whitespace, not boxes. A section opens with a top rule and a mono caps label. Lists of things are ledgers: hairline rows, label left, value right. Figures sit in a metric strip between two rules. Headings are Geist Mono.
- **An interface** is built from small crisp controls and flat panels. Controls are 27px tall with a 6px radius, a 1px edge and a fill a touch lighter at the top and bottom. There is one primary action per view, dark on a light page and white on a dark page. Panels are a flat fill with a 12px radius, no edge and no shadow, holding a figure, a chart or a detail view. Lists and tables stay hairline ledgers. Inter leads; Geist Mono stays on labels, status and figures. Read `references/ui.md`.

## Words

No fluff, and no interface that explains itself. Read `references/writing.md` before writing prose or UI copy.

- The first line is the answer. Length follows the question. Say each thing once.
- Cut openers, restated asks, signposts, recaps, closing offers, stacked hedges and selling words.
- A UI is labels, numbers and actions. No subtitle under a title, no helper text that restates its label, no section intro, no instructions for the obvious.
- Delete the sentence. If the output still works, it stays deleted.

## Never ship

- Gradient heroes, gradient text, or a purple or indigo wash over the page (tinted backgrounds, coloured panels, gradient headers). The accent is violet, but it marks one thing on a neutral page; it is never the theme.
- Cards with drop shadows, radii above 12px or pill shapes. Grids of three "features" with an icon each.
- Decorative KPI tiles: a big number in a shadowed or outlined card with a trend arrow, an icon or a sparkline nobody asked for. Decorative progress bars, rings or meters.
- Emoji in headings, bullets, status or buttons. Coloured pill badges and chips.
- Glass and blur panels. Callout boxes with a coloured left border ("Tip", "Note", "Key insight").
- Everything centred. Hover lift or scale. Staggered fade-ins. Timeline dots.
- Fake window, browser or terminal chrome, and toy illustrations.
- Title Case Headings, exclamation marks and hype words.
- Curved or gradient diagram connectors, shadows on diagrams, several stroke weights.
- A sidebar-and-tiles "dashboard" when a single column would read better.

## By output

- **HTML page or artifact.** One reading column, or `.cols` for comparisons. A table beats a bullet list for anything with two or more attributes. Design light and dark through the tokens and look at both.
- **Report, explainer, comparison.** The answer, then the evidence, then the detail. Plain section labels.
- **Doc (Google Docs, Word, Markdown).** Text first. Short sentence-case headings, tables for comparisons, no emoji, no callout blocks, no rule spam.
- **PDF.** The same HTML, printed with `scripts/pdf.sh`. Read `references/print.md`.
- **UI.** Read `references/ui.md` and start from `examples/ui.html`.
- **Diagram.** Read `references/figures.md`: orthogonal, one stroke width, monochrome, ALL CAPS Geist Mono, hand-written SVG with class `dg`.
- **Chart.** Read `references/figures.md` and start from `examples/chart.html`. Grey carries context and the accent carries the point. No pie, donut, gauge or 3D.
- **Deck.** Read `references/print.md` and start from `examples/slides.html`. One claim per slide, evidence that fills the slide.
- **Plain text** (README, terminal, code comment). Aligned ASCII in a code block; see `references/figures.md`. Banner text only when asked.

## Before delivering

Render it and look at it: at full size and at phone width, in both themes when it has both, and in the PDF when it prints. Then check:

1. Does anything from the never-ship list appear?
2. Does any colour appear that is not a token, or a status or series colour without a job?
3. Are labels mono caps, prose in Inter, figures tabular, and did the fonts load?
4. Does the first screen state the point?
5. Does the output still work without each sentence and label? Delete the ones it does not need.
6. In every row of controls, do the boxes share one height and style, and is there one primary per view?
7. Does any heading end on a stranded word, any label collide with another, any graphic sit small in empty space, or the page scroll sideways on a phone?

Say what was rendered and checked, and what was not.
