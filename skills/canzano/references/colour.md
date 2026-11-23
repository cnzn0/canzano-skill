# Colour

Three layers, all OKLCH. Use the highest layer that fits.

1. **Semantic tokens** (`assets/tokens.css`): `--page`, `--ink`, `--accent`, `--positive`, `--series-3` and so on. Pages use these. They switch with the theme.
2. **Palette** (`assets/palette.css`): eleven vivid hue scales of seven steps and a grey scale of thirteen. Reach in here only for the cases below, and only by token, never by typing a new colour value.
3. **Generator** (`scripts/palette.py`): add or change a hue there and regenerate. Do not hand-edit the palette.

## The palette

Hues: red, orange, amber, yellow, lime, green, sky, blue, violet, purple, pink. There is no teal, mint or seafoam and none should be added.

Steps: 100 (lightest) to 700 (darkest). Every step sits inside the lightness band where its hue is most saturated, at 96% of the chroma sRGB allows, so every step is vivid. Warm hues drift toward orange as they darken, so there is no brown and no olive. The palette has no pale tints and no near-black shades on purpose: a washed-out pink or a muddy amber is never the right answer.

Because the bands differ by hue, a step number is not a fixed lightness. `palette.css` prints each colour's contrast on white and on the dark page next to it. Read those numbers:

- Small text and thin lines need 4.5 or more against their page. Large figures, marks and fills need 3.
- Yellow, amber, lime and the light greens are bright by nature. On a white page use them as fills, bars and marks, with the label in ink beside them, not as text.
- On the dark page the lighter steps (100 to 300) of every hue work as text.

Grey: 0, 50, 100, 150, 200, 300, 400, 500, 600, 700, 800, 900, 950, with a faint cool tint.

## Which colour for which job

- **Structure and text.** The neutrals. Most of every output is grey, which is what lets the colour read as vivid.
- **The one live thing.** `--accent`. Never a button fill.
- **State.** `--positive`, `--warning`, `--negative`, `--info`, each next to a word.
- **A selected row, a diff line, a search highlight.** The matching `-soft` token as a background. It is the one pale colour in the system and it is only ever a row or a text highlight. Never a callout box, a chip or a card.
- **Categories in a chart.** `--series-1` to `--series-8`, in order. Stop at eight: with more categories, group the tail into "Other" in `--ink-3` or use small multiples. Label series directly.
- **One series that matters among many.** The rest in `--ink-3`, the one in `--accent`.
- **Magnitude (heatmap, choropleth, density).** One hue mixed toward the page in five steps: `color-mix(in oklab, var(--violet-400) N%, var(--page))` with N at 15, 35, 55, 75, 100. Violet by default. Not a rainbow.
- **Above and below a midpoint.** A diverging pair through grey: `--red-300`, `--red-100`, `--grey-200`, `--blue-100`, `--blue-400`. Use orange and violet when red and blue would read as bad and good and that is not meant.
- **A second brand or a tag colour the user asks for.** The nearest hue, at the step whose printed contrast fits the job.

## Rules

- Colour is rare and vivid. Never dusty, pastel, brownish, greyish or washed out, and never a second accent for decoration.
- Never rely on colour alone. Pair it with a word, a mark or a position.
- Mix colours `in oklab`, not `in oklch`: mixing toward white in oklch drifts every tint to pink.
- Gradients between palette colours are not used. The only gradient in the system is the control fill.
