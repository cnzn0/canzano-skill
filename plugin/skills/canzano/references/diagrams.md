# Diagrams

The brief in one line: very technical and utilitarian, ASCII brackets, one stroke width, monochromatic, all caps Geist Mono.

## Contract

- Every label is ALL CAPS Geist Mono, verified in the rendered output, not only declared in CSS.
- One stroke width for all structure, 1px at use size. Do not double shared edges; they read heavier.
- Connectors are straight and orthogonal. No curves and no direction changes without a reason.
- Monochrome: hierarchy through the three ink steps. The accent may mark the single path or state the diagram is about.
- Brackets `[ ]` group an entity, set, record or scope. ASCII characters must encode something. Never scatter terminal filler or invented metrics.
- Never use gradients, glow, shadows, rounded nodes, pill badges, avatars, check badges, sans-serif labels or decorative icons.
- Every connector has a real source and destination and attaches to a port, never to the open side of a bracket. Captions sit inside their group or on the edge they describe.
- Pick the structure the idea needs: a route, ordered stages, nested aggregation, a state diff or a register. Not everything is a row of boxes.

## Two ways to make one

- **Generate it.** The charts kit (`kits/charts/`) draws flow, sequence, layers, tree, timeline and quadrant diagrams from a JSON spec, already to this contract. Use it when the idea fits one of those shapes.
- **Draw it by hand** as SVG when none of them fits. The steps are below.
- For a README, a terminal or a code comment, where SVG cannot go, use the ASCII kit (`kits/ascii/`).

## Draw by hand

1. Write the one-sentence takeaway. List the entities, the directed relationships and the boundaries before drawing.
2. Build editable SVG with real `<text>` and give the `<svg>` class `dg`. That class sets the mono caps labels and gives you `.s` (a stroke), `.s.a` (the accented path), `.at` (accent text), `.mid` and `.dim` (quieter inks) and `.pkt` (a moving mark), all through the tokens so both themes work. Put strokes on half pixels (`x="0.5"`) so 1px stays 1px. Use `xml:space="preserve"` when columns depend on spaces. Wrap it in `<figure class="diagram">` and give the `<svg>` a `width` attribute equal to its viewBox width, so it keeps its drawn size and labels stay 11px; narrow screens scroll instead of shrinking the type. On a slide, set that width to the size you want it shown at. `assets/specimen.html` has a worked example.
3. Load `assets/lint.js` and run `cz.lint()`, then look at the rendered pixels at use size. Check connector attachment, collisions between text and lines, bracket grouping, column alignment and that the font loaded.

Mermaid and other auto-layout tools are acceptable only after restyling to this contract. Their default theme (rounded nodes, pastel fills, curved edges) is exactly the look to avoid.

## Animated diagrams

Animate only when the idea is a sequence: a request, a handshake, a state change over time. The static frame must already be a correct diagram.

- One thing moves: a small square mark (7px, accent) travelling along the existing connectors at a constant speed. Linear motion, no easing, no bounce, no trails or glow.
- The step in progress is the only accent. Its connectors and its node take the accent stroke; everything else stays ink.
- State changes are text changes: a register under the node (`LOG [ 41 ]` becomes `LOG [ 41 42 ]`), swapped at the moment the mark arrives. Nothing fades, scales or slides.
- Pair the drawing with a numbered step list and mark the current step, so a paused frame still explains itself.
- Give it PLAY/PAUSE and STEP buttons. With reduced motion, do not autoplay and let STEP jump between states.
- Loop with a short hold at the end and reset to the first state. Keep one pass under about ten seconds.
- Plain SVG plus a small script or CSS is enough. Do not add an animation library for this.

In print a diagram cannot scroll, so one wider than the page shrinks to fit it. Check the PDF: if its labels come out too small, redraw it narrower or split it.
