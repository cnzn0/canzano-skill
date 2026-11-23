# Charts kit

Optional. Open this when an output needs a chart or a diagram that fits a standard shape.

`viz.js` is one dependency-free script that turns a JSON spec into SVG in the house style, in both themes. `viz.css` styles what it draws. Do not pull in a chart library and do not hand-place bars.

```html
<figure class="chart" data-cz>
  <script type="application/json">
    { "type": "bar", "height": 280, "highlight": "Q4", "prefix": "$",
      "data": [ { "label": "Q1", "value": 120 }, { "label": "Q4", "value": 340 } ] }
  </script>
  <figcaption>Fig 1 // Unit, period, source</figcaption>
</figure>
<link rel="stylesheet" href="kits/charts/viz.css">   <!-- after base.css -->
<script src="kits/charts/viz.js"></script>
```

For a single-file output inline both: `viz.css` after `base.css`, and `viz.js` before the closing `</body>`. For a spec that needs a function, call `cz.chart(element, spec)` instead.

## Which chart

| The point is | Use | Not |
|---|---|---|
| One category beats the others | `hbar`, sorted, the winner highlighted | A pie |
| A few values over a few periods | `bar` | A line with four points |
| Parts of a total over time | `bar` with `stacked` | Several pies |
| Parts of two or three totals | `hbar` with `stacked` | A donut |
| A trend, or several trends | `line` | Bars for forty periods |
| One trend against a goal | `line` with `area` and `target` | A gauge |
| How one total became another | `waterfall` | A stacked bar with a legend |
| Two numbers per item | `scatter` | Two bar charts |
| Before and after, per item | `slope` | Grouped bars |
| A value across two dimensions | `heatmap` | A 3D surface |
| A trend inside a sentence or a table cell | `cz.spark` | A full chart |

There is no pie, donut, gauge, radar or 3D chart, on purpose. A single number is a figure in a metric strip, not a chart.

## Spec

Every chart takes `type`, an optional `height` (default 320), `label` (the accessible description) and number formatting: `prefix`, `suffix`, `digits`.

Data comes in one of two shapes:

- One series: `"data": [ { "label": "Q1", "value": 120 }, ... ]`
- Several: `"labels": ["Q1", "Q2"], "series": [ { "name": "Free", "values": [900, 1100] }, ... ]`

| Type | Extra fields |
|---|---|
| `bar` | `stacked`, `highlight` (a label for one series, a series name for several), `target: { value, label }`, `values: false` to hide value labels |
| `hbar` | `stacked`, `highlight`, `rowHeight` |
| `line` | `area` (one series; always from zero, since a filled area that does not start at zero overstates the change), `highlight` (a series name; the rest go grey), `marks: [ { at, text } ]`, `target`, `zero: false` to let the axis start above zero |
| `scatter` | `series: [ { name, points: [ { x, y, label, accent } ] } ]`, `x`, `y` (axis names), `xAxis: { prefix, suffix }` |
| `slope` | `labels` (two), `series` with two values each, `highlight` |
| `waterfall` | `data: [ { label, value, total } ]`; a `total` row without a value takes the running total; `good: "down"` when a decrease is the good news, `good: "none"` for neutral |
| `heatmap` | `rows`, `cols`, `values` (a row of numbers per row), `showValues: false`, `color` |

`cz.spark(element, [3, 5, 4, 8], { width, height, label })` draws a 96 x 20 sparkline with the last point marked. It works inside a sentence or a table cell.

Other options: `compact: false` prints full numbers (`$1,840`, not `$1.8K`); `yAxis: { prefix, suffix }` on a scatter, `values: false` on any bar chart, `digits` for decimal places. With `highlight` on several series, the others take distinct greys. Long `hbar` row labels are cut with an ellipsis at 42% of the width so they cannot squeeze the bars; keep them short.

Narrow screens: charts are drawn at the width of their container, so label size holds. Check each chart at 390px as well as full width; cut series or categories when it gets crowded.

## Rules

- One chart, one point. The headline or caption states it; the chart proves it.
- Grey carries context and the accent carries the thing the chart is about. Use `highlight`.
- Series colours only when several series must be told apart. Eight at most. With more, group the tail into "Other".
- Label directly. `line` labels each series at its end. Single-series bars and stacked totals print their values; grouped bars print them when each bar is wide enough, and otherwise rely on the axis. A legend appears only for grouped and stacked bars and for a scatter with several series, and it wraps onto more rows on a narrow chart.
- Bars start at zero. A line may not, with `zero: false`, when the change is the point and the axis is labelled.
- Sort categories by value unless they have a natural order.
- Units go in `prefix` and `suffix`, never in the title alone. The caption names the unit, the period and the source.
- Never invent data to fill a chart. If the numbers are illustrative, the caption says so.
- Read the rendered chart before delivering: is the highlighted mark the right one, and do the numbers match the source?

## Diagrams

`viz.js` also draws six diagram types from a JSON spec, already to the contract in `references/diagrams.md`. Use them before drawing by hand; hand-drawn SVG is for a structure none of them fits.

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
```

| Type | For | Spec |
|---|---|---|
| `flow` | A route through a system, a pipeline, a fan-out | `nodes: [ { id, label, col, row, note, accent, kind: "store" } ]`, `edges: [ { from, to, label, accent, dashed } ]`, `groups: [ { label, nodes } ]`, `cell: { w, h, gx, gy }` |
| `sequence` | Who talks to whom, in order | `actors: [ { id, label } ]`, `messages: [ { from, to, label, accent, reply } ]` |
| `layers` | A stack, top to bottom | `layers: [ { label, items: [ "Web", { label, accent } ] } ]` |
| `tree` | A hierarchy or a breakdown | `root: { label, accent, children: [ ... ] }` |
| `timeline` | Spans and milestones on one scale | `columns: [...]`, `rows: [ { label, from, to, note, accent } or { label, at, note } ]`, `now`. `from`, `to`, `at` and `now` are column positions: 0 is the start of the first column, 1.5 is halfway through the second |
| `quadrant` | Items on two axes | `x: [low, high]`, `y: [low, high]`, `corners: [tl, tr, bl, br]`, `items: [ { label, x, y, accent } ]` with x and y from 0 to 1 |

A note sits under its node. When a wire leaves the node downward, the note moves above the node, or beside the wire if the top is taken too. Place flow nodes on a grid with `col` and `row`. Wires route themselves at right angles: forward along a row, down a column, or around a corner. Keep forward edges going left to right and put the store or the side effect one row down. Labels in a node may break with `\n`. A diagram keeps its drawn size. Wider than its container, it scales down until its labels reach 10px and then stops; the figure scrolls sideways from there. On a slide it grows to fill the room. `cz.lint()` reports `tiny-labels` when a drawing is shown too small: split it into two diagrams.

In print a diagram cannot scroll, so one wider than the page shrinks to fit it. Check the PDF: if its labels come out too small, give it fewer columns or split it. 

A quadrant sizes itself to a narrow container. An edge to an earlier column (a backward edge) runs in its own lane in the corridor under its row, with its own ports, so it never rides a forward wire. Add `"via": "top"` to send it over the row instead. More than two backward edges usually means the diagram should be a sequence or two flows.

Other options: `fit: true` scales any diagram to its container width; `cell: { w, h, gx, gy }` sizes flow nodes and gaps; `step` sets the row pitch of a sequence; `nodeWidth` and `gapY` size a tree; `rowHeight` and `width` size layers and timelines; `now` and `nowLabel` mark the present on a timeline; `size` sets a quadrant's side. Layers wrap their items onto more lines when the labels would not fit.

## Before delivering

Load `assets/lint.js` and run `cz.lint()`. It reports labels that overlap or are struck by a wire, a label sitting on another point's marker, a drawing shown too small to read, and a drawing that fills little of its slide. Fix each one, then look at the chart or diagram at full width, at phone width and in the PDF if it prints.
