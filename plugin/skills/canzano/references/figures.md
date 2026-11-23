# Diagrams, charts and ASCII

There is no chart library and no generator. Write the SVG by hand to these rules, starting from `examples/chart.html`.

## Every drawing

- Inline SVG with real `<text>` and class `dg` on the `<svg>`. That class sets ALL CAPS Geist Mono labels at 11px and gives `.s` (a stroke), `.s.q` (a quieter stroke), `.g` (a gridline), `.f` (a fill), `.a` (the accent, on any of them or on text), and `.mid` and `.dim` (quieter text). All colour comes through these, so both themes work.
- One stroke width, 1px. Put strokes on half pixels (`x="0.5"`) so they stay crisp.
- Monochrome. The accent marks the single thing the drawing is about. Nothing else is coloured.
- No gradients, shadows, glow, rounded nodes, curves, pill badges or icons.
- Wrap it in `<figure class="scroll">` and give the `<svg>` `width` and `height` attributes equal to its viewBox. It then keeps its drawn size and a phone scrolls it sideways; labels never shrink.
- Add `role="img"` and an `aria-label` that states the point, and a `<figcaption>`: `Fig 1 // What, unit, period`.
- Compute every coordinate. Then render it and look: no label touches another label, a stroke or the edge.

## Diagrams

- List the entities, the directed relationships and the boundaries before drawing.
- Connectors are straight and orthogonal, with a real source and destination.
- Brackets `[ ]` mark an entity or a scope. ASCII characters must mean something.
- Pick the structure the idea needs: a route, ordered stages, nesting, a state change. Not everything is a row of boxes.
- Animate only when the idea is a sequence. One small accent square moves along the existing connectors at constant speed. Add PLAY and STEP buttons, and do not autoplay with reduced motion. The still frame must already be a correct diagram.

## Charts

| The point is | Use |
|---|---|
| One category beats the others | Horizontal bars, sorted, the winner in the accent |
| A few values over a few periods | Bars |
| A trend, or one trend against others | Lines: the one that matters in the accent, the rest `.s.q` |
| Two numbers per item | A scatter of small squares |
| A value across two dimensions | A grid of cells in five steps of one hue (see `colour.md`) |
| A single number | A figure in a metric strip, not a chart |

- No pie, donut, gauge, radar or 3D.
- Grey carries context and the accent carries the point. More than one colour only for real categories: `--series-1` to `--series-8`, in order, at most eight.
- Label directly: values on the bars, names at the end of the lines. No legend box.
- Bars start at zero. A baseline in `.s`, at most three gridlines in `.g`.
- The headline or caption states what the chart shows, as a claim.

## ASCII

For a README, a terminal or a code comment, where SVG cannot go.

```
[ CLIENT ] --https--> [ API ] --enqueue--> [ QUEUE ] --> [ STORE ]

SERVICE        STATUS    TIME
checkout-api   LIVE      3m 58s
search-index   FAILED    0m 52s
```

- Plain ASCII in a fenced code block. Align columns with spaces and check every line's width.
- The same rules as a diagram: brackets for entities, straight connectors, labels in caps.
- Large banner text only when the user asks for it.
