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

## Boilerplates

`assets/viz.js` draws six diagram types from a JSON spec, already to this contract. Use them before drawing by hand; hand-drawn SVG is for a structure none of them fits.

```html
<figure class="diagram" data-cz>
  <script type="application/json">
    { "type": "flow",
      "nodes": [ { "id": "c", "label": "Client", "col": 0 }, { "id": "a", "label": "API", "col": 1 },
                 { "id": "d", "label": "DB", "col": 1, "row": 1, "kind": "store" } ],
      "edges": [ { "from": "c", "to": "a", "label": "POST", "accent": true }, { "from": "a", "to": "d" } ],
      "groups": [ { "label": "Service", "nodes": ["a", "d"] } ] }
  </script>
</figure>
<script src="viz.js"></script>
```

| Type | For | Spec |
|---|---|---|
| `flow` | A route through a system, a pipeline, a fan-out | `nodes: [ { id, label, col, row, note, accent, kind: "store" } ]`, `edges: [ { from, to, label, accent, dashed } ]`, `groups: [ { label, nodes } ]`, `cell: { w, h, gx, gy }` |
| `sequence` | Who talks to whom, in order | `actors: [ { id, label } ]`, `messages: [ { from, to, label, accent, reply } ]` |
| `layers` | A stack, top to bottom | `layers: [ { label, items: [ "Web", { label, accent } ] } ]` |
| `tree` | A hierarchy or a breakdown | `root: { label, accent, children: [ ... ] }` |
| `timeline` | Spans and milestones on one scale | `columns: [...]`, `rows: [ { label, from, to, note, accent } or { label, at, note } ]`, `now` |
| `quadrant` | Items on two axes | `x: [low, high]`, `y: [low, high]`, `corners: [tl, tr, bl, br]`, `items: [ { label, x, y, accent } ]` with x and y from 0 to 1 |

Place flow nodes on a grid with `col` and `row`. Wires route themselves at right angles: forward along a row, down a column, or around a corner. Keep forward edges going left to right and put the store or the side effect one row down. Labels in a node may break with `\n`. A diagram wider than its container scales down; split it when the labels would fall under 10px.

For text-only places (a README, a terminal, a code comment) use `scripts/ascii.py`, described in `ascii.md`.

## Build and check

1. Write the one-sentence takeaway. List the entities, the directed relationships and the boundaries before drawing.
2. Build editable SVG with real `<text>`, coloured through the tokens (`stroke: var(--ink)`) so both themes work. Put strokes on half pixels (`x="0.5"`) so 1px stays 1px. Use `xml:space="preserve"` when columns depend on spaces. Wrap it in `<figure class="diagram">` so it keeps its drawn size and labels stay 11px; narrow screens scroll instead of shrinking the type. `assets/specimen.html` has a worked example.
3. Look at the rendered pixels at use size. Check connector attachment, collisions between text and lines, bracket grouping, column alignment and that the font loaded.

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
