# Charts

Draw charts with `assets/viz.js`. It is one dependency-free script that turns a JSON spec into SVG in the house style, in both themes. Do not pull in a chart library and do not hand-place bars.

```html
<figure class="chart" data-cz>
  <script type="application/json">
    { "type": "bar", "height": 280, "highlight": "Q4", "prefix": "$",
      "data": [ { "label": "Q1", "value": 120 }, { "label": "Q4", "value": 340 } ] }
  </script>
  <figcaption>Fig 1 // Unit, period, source</figcaption>
</figure>
<script src="viz.js"></script>
```

Inline `viz.js` for a single-file output. For a spec that needs a function, call `cz.chart(element, spec)` instead.

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
- Read the rendered chart before delivering: are any labels clipped or overlapping, is the highlighted mark the right one, do the numbers match the source?
