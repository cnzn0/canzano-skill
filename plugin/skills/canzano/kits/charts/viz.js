/* canzano viz. Dependency-free SVG charts and diagrams in the house style.
   Colours and type come from tokens.css through CSS variables, so both themes work.
   Use: put a JSON spec in a script tag of type application/json inside <figure class="chart" data-cz>,
   or call cz.chart(el, spec), cz.diagram(el, spec), cz.spark(el, values).
   Specs are documented in the README.md beside this file. Needs viz.css. */
(function () {
  const NS = 'http://www.w3.org/2000/svg';
  const $ = e => (typeof e === 'string' ? document.querySelector(e) : e);
  const px = v => Math.round(v) + 0.5;
  const up = s => String(s).toUpperCase();
  function el(tag, attrs, parent, txt) {
    const n = document.createElementNS(NS, tag);
    for (const k in attrs) if (attrs[k] != null) n.setAttribute(k, attrs[k]);
    if (txt != null) n.textContent = txt;
    if (parent) parent.appendChild(n);
    return n;
  }
  const text = (p, x, y, s, cls, anchor) => el('text', { x, y, class: cls || null, 'text-anchor': anchor || null }, p, s);
  const fsize = host => parseFloat(getComputedStyle(host).getPropertyValue('--viz-text')) || 11;
  const tw = (s, f) => String(s).length * f * 0.64;
  const room = host => { const b = host.closest && host.closest('.slide .body'); return b ? b.clientHeight - 44 : 0; };   // height to fill on a slide
  function fmt(s) {
    if (typeof s.format === 'function') return s.format;
    const nf = new Intl.NumberFormat('en', { notation: s.suffix || s.compact === false ? 'standard' : 'compact', maximumFractionDigits: s.digits == null ? 1 : s.digits });
    return v => (v < 0 ? '-' : '') + (s.prefix || '') + nf.format(Math.abs(v)) + (s.suffix || '');
  }
  function ticks(min, max, n) {
    const span = max - min || 1, raw = span / (n || 4), p = Math.pow(10, Math.floor(Math.log10(raw))), m = raw / p;
    const step = (m < 1.5 ? 1 : m < 3 ? 2 : m < 7 ? 5 : 10) * p, out = [];
    for (let v = Math.floor(min / step) * step; v <= max + step * 0.999; v += step) out.push(+v.toFixed(10));
    return out;
  }
  function root(host, W, H, label, natural) {
    host.innerHTML = '';
    const s = el('svg', { class: 'cz', viewBox: `0 0 ${W} ${H}`, role: 'img', 'aria-label': label || null }, host);
    if (natural) {
      // A drawing keeps its size. Wider than its container, it scales down, but never below 10px labels:
      // past that it stays put and its figure scrolls. On a slide it grows to fill the room it has.
      const slide = host.closest && host.closest('.slide'), wide = host.clientWidth, floor = 10 / fsize(host); let k = 1;
      if (slide && wide) { const body = host.closest('.body'), high = (body ? body.clientHeight : 480) - 40; k = Math.min(wide / W, high / H, 1.7); }
      else if (wide && W > wide) k = Math.max(wide / W, floor);
      s.setAttribute('style', `width:${Math.floor(W * k)}px;max-width:none`);
    }
    return s;
  }
  function norm(spec) {
    const s = Object.assign({}, spec);
    if (s.data && !s.series) { s.labels = s.data.map(d => d.label); s.series = [{ name: s.name || '', values: s.data.map(d => d.value) }]; }
    return s;
  }
  function colour(s, j) {
    const ser = s.series[j], n = s.series.length, greys = ['var(--ink-3)', 'var(--grey-400)', 'var(--grey-700)', 'var(--grey-300)'];
    if (ser.color) return ser.color;
    if (s.highlight != null && n > 1) {
      if (ser.name === s.highlight || j === s.highlight) return 'var(--accent)';
      return greys[s.series.slice(0, j).filter((x, i) => !(x.name === s.highlight || i === s.highlight)).length % greys.length];
    }
    return n === 1 ? 'var(--ink-3)' : `var(--series-${(j % 8) + 1})`;
  }
  function grid(g, T, Y, x0, x1, F, f) {
    T.forEach(t => {
      el('path', { class: t === 0 ? 'axis' : 'grid', d: `M${x0} ${px(Y(t))} H${x1}` }, g);
      text(g, x0 - 8, Y(t) + f * 0.36, F(t), 'dim', 'end');
    });
  }
  function legendLayout(s, x0, W, f) {             // where each legend entry goes; wraps at the right edge
    let x = x0, row = 0; const items = s.series.map(ser => { const w = 14 + tw(ser.name, f) + 20; if (x > x0 && x + w - 20 > W) { x = x0; row++; } const it = { x, row }; x += w; return it; });
    return { items, rows: row + 1, height: (row + 1) * (f + 9) };
  }
  function legend(g, s, L, f) {
    s.series.forEach((ser, j) => { const y = f + L.items[j].row * (f + 9);
      el('rect', { x: L.items[j].x, y: y - 8, width: 8, height: 8, style: `fill:${colour(s, j)}` }, g);
      text(g, L.items[j].x + 14, y, up(ser.name)); });
  }
  function spread(items, gap, lo, hi) {            // keep labels at least `gap` apart inside lo..hi
    items.sort((a, b) => a.y - b.y);
    for (let i = 1; i < items.length; i++) if (items[i].y - items[i - 1].y < gap) items[i].y = items[i - 1].y + gap;
    const over = items.length ? items[items.length - 1].y - hi : 0;
    if (over > 0) for (let i = items.length - 1; i >= 0; i--) { items[i].y -= over; if (i && items[i].y - items[i - 1].y >= gap) break; }
    items.forEach(it => { if (it.y < lo) it.y = lo; });
    return items;
  }
  function xLabels(g, labels, X, y, f, room) {       // thin out category labels that would collide
    const widest = Math.max(...labels.map(l => tw(l, f))) + 12, every = Math.max(1, Math.ceil(widest / room));
    labels.forEach((l, i) => { if (i % every === 0) text(g, X(i), y, up(l), 'dim', 'middle'); });
  }

  /* ---------------------------------------------------------------- charts */
  const C = {};

  C.bar = function (host, s, W, H) {
    const f = fsize(host), F = fmt(s), n = s.series.length, stacked = !!s.stacked && n > 1;
    const top = s.labels.map((_, i) => stacked ? s.series.reduce((a, x) => a + (x.values[i] || 0), 0) : Math.max(...s.series.map(x => x.values[i] || 0)));
    const low = Math.min(0, ...s.series.flatMap(x => x.values.filter(v => v != null)));
    const T = ticks(low, Math.max(...top, s.target ? s.target.value : 0)), y0 = T[0], y1 = T[T.length - 1];
    const ml = Math.max(...T.map(t => tw(F(t), f))) + 12, LG = n > 1 ? legendLayout(s, ml, W, f) : null;
    const m = { l: ml, r: 4, t: (LG ? LG.height + f + 8 : f + 10), b: f + 14 };
    const g = root(host, W, H, s.label), pw = W - m.l - m.r, ph = H - m.t - m.b, Y = v => m.t + ph - (v - y0) / (y1 - y0) * ph;
    grid(g, T, Y, m.l, W - m.r, F, f);
    if (LG) legend(g, s, LG, f);
    const bw = pw / s.labels.length, gap = Math.max(2, Math.min(14, bw * 0.18)), inner = bw - gap * 2;
    const each = n > 1 && !stacked && s.values !== false && s.series.every(ser => ser.values.every(v => v == null || inner / n - 2 > tw(F(v), f) + 2));   // grouped values: all or none
    s.labels.forEach((lab, i) => {
      const x = m.l + bw * i + gap; let acc = 0;
      s.series.forEach((ser, j) => {
        const v = ser.values[i]; if (v == null) return;
        let bx = x, w = inner, a, b;
        if (stacked) { b = Y(acc); acc += v; a = Y(acc); } else { w = inner / n - (n > 1 ? 2 : 0); bx = x + j * (inner / n); a = Y(Math.max(v, 0)); b = Y(Math.min(v, 0)); }
        const hi = n === 1 && (s.highlight === i || s.highlight === lab);
        el('rect', { x: bx, y: a, width: Math.max(1, w), height: Math.max(0, b - a), style: `fill:${hi ? 'var(--accent)' : colour(s, j)}` }, g);
        if (n === 1 && s.values !== false && bw > tw(F(v), f) + 2) text(g, bx + w / 2, v >= 0 ? a - 6 : b + f + 3, F(v), hi ? 'at' : 'ink', 'middle');
        else if (each) text(g, bx + w / 2, v >= 0 ? a - 5 : b + f + 2, F(v), 'dim', 'middle');
      });
      if (stacked && s.values !== false && bw > tw(F(acc), f) + 2) text(g, x + inner / 2, Y(acc) - 6, F(acc), 'ink', 'middle');
    });
    xLabels(g, s.labels, i => m.l + bw * (i + 0.5), H - 3, f, bw);
    if (s.target) { el('path', { class: 'axis dash', d: `M${m.l} ${px(Y(s.target.value))} H${W - m.r}` }, g); text(g, W - m.r, Y(s.target.value) - 6, up(s.target.label || F(s.target.value)), 'ink', 'end'); }
  };

  C.hbar = function (host, s, W, H) {
    const f = fsize(host), F = fmt(s), n = s.series.length, stacked = !!s.stacked && n > 1, rows = s.labels.length;
    const tot = s.labels.map((_, i) => stacked ? s.series.reduce((a, x) => a + (x.values[i] || 0), 0) : Math.max(...s.series.map(x => x.values[i] || 0)));
    const max = Math.max(...tot) || 1, lw = Math.min(Math.max(...s.labels.map(l => tw(l, f))) + 14, W * 0.42), vw = Math.max(...tot.map(v => tw(F(v), f))) + 10;
    const fit = l => { const room = Math.max(3, Math.floor((lw - 14) / (f * 0.64))); l = String(l); return l.length > room ? l.slice(0, room - 1) + '…' : l; };   // long row labels are cut, never allowed to squeeze the bars
    const LG = n > 1 ? legendLayout(s, 0, W, f) : null, top = LG ? LG.height + 8 : 0, rh = s.rowHeight || Math.max(f + 12, Math.min(40, ((s.height ? H : 0) - top) / rows || 30));
    H = s.height ? H : top + rows * rh;
    const g = root(host, W, H, s.label), pw = W - lw - vw, X = v => lw + v / max * pw;
    if (LG) legend(g, s, LG, f);
    el('path', { class: 'axis', d: `M${px(lw)} ${top} V${H}` }, g);
    s.labels.forEach((lab, i) => {
      const y = top + i * rh, bh = Math.min(rh - 8, 22), by = y + (rh - bh) / 2, hi = n === 1 && (s.highlight === i || s.highlight === lab);
      el('title', {}, text(g, 0, y + rh / 2 + f * 0.36, up(fit(lab)), hi ? 'ink' : null), String(lab));
      let acc = 0;
      s.series.forEach((ser, j) => {
        const v = ser.values[i]; if (v == null) return;
        const sub = stacked ? bh : bh / n, x = stacked ? X(acc) : lw, yy = stacked ? by : by + j * sub;
        el('rect', { x: x + (stacked && acc ? 1 : 0.5), y: yy, width: Math.max(1, X(v) - lw - (stacked && acc ? 1 : 0)), height: sub - (n > 1 && !stacked ? 1 : 0), style: `fill:${hi ? 'var(--accent)' : colour(s, j)}` }, g);
        if (stacked) acc += v; else if (n > 1 && s.values !== false) text(g, X(v) + 6, yy + sub / 2 + f * 0.36, F(v), 'dim');
      });
      if (s.values !== false && (n === 1 || stacked)) text(g, X(tot[i]) + 8, y + rh / 2 + f * 0.36, F(tot[i]), hi ? 'at' : 'ink');
    });
  };

  C.line = function (host, s, W, H) {
    const f = fsize(host), F = fmt(s), n = s.series.length, all = s.series.flatMap(x => x.values.filter(v => v != null));
    const T = ticks(s.zero === false && !s.area ? Math.min(...all) : Math.min(0, ...all), Math.max(...all, s.target ? s.target.value : 0)), y0 = T[0], y1 = T[T.length - 1];
    const tag = ser => { const v = ser.values.filter(v => v != null).pop(); return (ser.name ? up(ser.name) + ' ' : '') + F(v); };
    const m = { l: Math.max(...T.map(t => tw(F(t), f))) + 12, r: Math.max(...s.series.map(x => tw(tag(x), f))) + 14, t: f + 10, b: f + 14 };
    const g = root(host, W, H, s.label), pw = W - m.l - m.r, ph = H - m.t - m.b, N = s.labels.length;
    const X = i => m.l + (N > 1 ? i / (N - 1) : 0.5) * pw, Y = v => m.t + ph - (v - y0) / (y1 - y0) * ph;
    grid(g, T, Y, m.l, W - m.r, F, f);
    (s.marks || []).forEach(k => { const i = typeof k.at === 'number' ? k.at : s.labels.indexOf(k.at); el('path', { class: 'axis', d: `M${px(X(i))} ${m.t} V${m.t + ph}` }, g); text(g, X(i) + 6, m.t + f, up(k.text), 'ink halo'); });
    const ends = [];
    s.series.forEach((ser, j) => {
      const c = n === 1 ? 'var(--accent)' : colour(s, j), pts = ser.values.map((v, i) => v == null ? null : [X(i), Y(v)]).filter(Boolean);
      if (s.area && n === 1) el('path', { d: `M${pts[0][0]} ${Y(Math.max(y0, 0))} ` + pts.map(p => `L${p[0]} ${p[1]}`).join(' ') + ` L${pts[pts.length - 1][0]} ${Y(Math.max(y0, 0))} Z`, style: `fill:${c};fill-opacity:0.12` }, g);
      el('path', { class: 'ln', d: 'M' + pts.map(p => p[0].toFixed(1) + ' ' + p[1].toFixed(1)).join(' L'), style: `stroke:${c};stroke-width:${ser.name === s.highlight || n === 1 ? 1.5 : 1}` }, g);
      const last = pts[pts.length - 1];
      el('rect', { x: last[0] - 3, y: last[1] - 3, width: 6, height: 6, style: `fill:${c}` }, g);
      ends.push({ y: last[1], x: last[0], s: tag(ser), c });
    });
    spread(ends, f + 3, m.t + f * 0.4, m.t + ph).forEach(e => el('text', { x: e.x + 10, y: e.y + f * 0.36, style: `fill:${e.c}` }, g, e.s));
    xLabels(g, s.labels, X, H - 3, f, pw / Math.max(1, N - 1));
    if (s.target) { el('path', { class: 'axis dash', d: `M${m.l} ${px(Y(s.target.value))} H${W - m.r}` }, g); text(g, m.l + 6, Y(s.target.value) - 6, up(s.target.label || F(s.target.value)), 'ink'); }
  };

  C.scatter = function (host, s, W, H) {
    const f = fsize(host), FX = fmt(s.xAxis || {}), FY = fmt(s.yAxis || s), pts = s.series.flatMap(x => x.points), many = s.series.length > 1;
    const xs = pts.map(p => p.x), TY = ticks(Math.min(0, ...pts.map(p => p.y)), Math.max(...pts.map(p => p.y)));
    const far = pts.reduce((a, p) => (p.x > a.x ? p : a), pts[0]), ml = Math.max(...TY.map(t => tw(FY(t), f))) + 12, mr = Math.max(12, far.label ? Math.min(tw(far.label, f) + 14, W * 0.25) : 0);
    const want = Math.max(2, Math.min(5, Math.floor((W - ml - mr) / (tw(FX(Math.max(...xs)), f) + 28))));       // fewer x ticks on a narrow chart
    const TX = ticks(Math.min(...xs), Math.max(...xs), want), LG = many ? legendLayout(s, ml, W, f) : null;
    const m = { l: ml, r: mr, t: (LG ? LG.height : 0) + (s.y ? f + 8 : 0) + f, b: f * 2 + 22 };
    const g = root(host, W, H, s.label), pw = W - m.l - m.r, ph = H - m.t - m.b;
    const X = v => m.l + (v - TX[0]) / (TX[TX.length - 1] - TX[0]) * pw, Y = v => m.t + ph - (v - TY[0]) / (TY[TY.length - 1] - TY[0]) * ph;
    grid(g, TY, Y, m.l, W - m.r, FY, f);
    TX.forEach(t => text(g, X(t), m.t + ph + f + 6, FX(t), 'dim', 'middle'));
    if (s.x) text(g, W - m.r, H - 3, up(s.x), null, 'end');
    if (LG) legend(g, s, LG, f);
    if (s.y) text(g, m.l, (LG ? LG.height : 0) + f, up(s.y));
    s.series.forEach((ser, j) => ser.points.forEach(p => {
      const c = p.accent ? 'var(--accent)' : many ? colour(s, j) : 'var(--ink-3)', x = X(p.x), y = Y(p.y);
      el('rect', { class: 'mark', x: x - 3.5, y: y - 3.5, width: 7, height: 7, style: `fill:${c}` }, g);
      if (!p.label) return;
      const left = x + 8 + tw(p.label, f) > W;                                                             // a label that would leave the chart goes to the left of its point
      text(g, left ? x - 8 : x + 8, y + f * 0.36, up(p.label), (p.accent ? 'at' : 'ink') + ' halo', left ? 'end' : null);
    }));
  };

  C.heatmap = function (host, s, W, H) {
    const f = fsize(host), F = fmt(s), flat = s.values.flat(), lo = Math.min(...flat), hi = Math.max(...flat);
    const lw = Math.max(...s.rows.map(r => tw(r, f))) + 12, top = f + 10, cw = (W - lw) / s.cols.length, ch = s.rowHeight || Math.max(f + 14, Math.min(44, cw * 0.6));
    H = top + ch * s.rows.length;
    const g = root(host, W, H, s.label), hue = s.color || 'var(--accent)';
    s.cols.forEach((c, j) => text(g, lw + cw * (j + 0.5), f, up(c), 'dim', 'middle'));
    s.rows.forEach((r, i) => {
      text(g, 0, top + ch * (i + 0.5) + f * 0.36, up(r));
      s.cols.forEach((_, j) => {
        const v = s.values[i][j], k = hi === lo ? 1 : (v - lo) / (hi - lo);
        el('rect', { x: lw + cw * j + 1, y: top + ch * i + 1, width: cw - 2, height: ch - 2, style: `fill:${hue};fill-opacity:${(0.08 + 0.92 * k).toFixed(3)}` }, g);
        if (s.values !== false && s.showValues !== false && cw > tw(F(v), f) + 6) text(g, lw + cw * (j + 0.5), top + ch * (i + 0.5) + f * 0.36, F(v), k > 0.55 ? 'onfill' : 'ink', 'middle');
      });
    });
  };

  C.slope = function (host, s, W, H) {
    const f = fsize(host), F = fmt(s), all = s.series.flatMap(x => x.values), lo = Math.min(...all), hi = Math.max(...all);
    const lab = (ser, k) => k ? F(ser.values[1]) + ' ' + up(ser.name) : up(ser.name) + ' ' + F(ser.values[0]);
    const ml = Math.max(...s.series.map(x => tw(lab(x, 0), f))) + 12, mr = Math.max(...s.series.map(x => tw(lab(x, 1), f))) + 12, top = f + 16, bot = 8;
    const g = root(host, W, H, s.label), Y = v => top + (H - top - bot) * (1 - (v - lo) / (hi - lo || 1)), x0 = ml, x1 = W - mr;
    text(g, x0, f, up(s.labels[0]), 'dim', 'middle'); text(g, x1, f, up(s.labels[1]), 'dim', 'middle');
    el('path', { class: 'grid', d: `M${px(x0)} ${top - 6} V${H} M${px(x1)} ${top - 6} V${H}` }, g);
    const L = [], R = [];
    s.series.forEach((ser, j) => {
      const on = s.highlight == null || ser.name === s.highlight || j === s.highlight, c = on ? (s.highlight == null ? 'var(--ink)' : 'var(--accent)') : 'var(--ink-3)';
      el('path', { class: 'ln', d: `M${x0} ${Y(ser.values[0])} L${x1} ${Y(ser.values[1])}`, style: `stroke:${c};stroke-width:${on && s.highlight != null ? 1.5 : 1}` }, g);
      [[x0, ser.values[0]], [x1, ser.values[1]]].forEach(p => el('rect', { x: p[0] - 3, y: Y(p[1]) - 3, width: 6, height: 6, style: `fill:${c}` }, g));
      L.push({ y: Y(ser.values[0]), s: lab(ser, 0), c }); R.push({ y: Y(ser.values[1]), s: lab(ser, 1), c });
    });
    spread(L, f + 3, top, H - 2).forEach(e => el('text', { x: x0 - 10, y: e.y + f * 0.36, 'text-anchor': 'end', style: `fill:${e.c}` }, g, e.s));
    spread(R, f + 3, top, H - 2).forEach(e => el('text', { x: x1 + 10, y: e.y + f * 0.36, style: `fill:${e.c}` }, g, e.s));
  };

  C.waterfall = function (host, s, W, H) {             // data: [{label, value, total: true|false}]
    const f = fsize(host), F = fmt(s), rows = []; let run = 0;
    s.data.forEach(d => { if (d.total) { run = d.value != null ? d.value : run; rows.push({ d, a: 0, b: run }); } else { rows.push({ d, a: run, b: run + d.value }); run += d.value; } });
    const T = ticks(Math.min(0, ...rows.flatMap(r => [r.a, r.b])), Math.max(...rows.flatMap(r => [r.a, r.b]))), y0 = T[0], y1 = T[T.length - 1];
    const m = { l: Math.max(...T.map(t => tw(F(t), f))) + 12, r: 4, t: f + 10, b: f + 14 };
    const g = root(host, W, H, s.label), pw = W - m.l - m.r, ph = H - m.t - m.b, Y = v => m.t + ph - (v - y0) / (y1 - y0) * ph;
    grid(g, T, Y, m.l, W - m.r, F, f);
    const bw = pw / rows.length, gap = Math.max(2, Math.min(14, bw * 0.18));
    rows.forEach((r, i) => {
      const x = m.l + bw * i + gap, w = bw - gap * 2, a = Y(Math.max(r.a, r.b)), b = Y(Math.min(r.a, r.b));
      const up_ = r.d.value >= 0, good = s.good === 'down' ? !up_ : up_;
      const c = r.d.total ? 'var(--ink)' : s.good === 'none' ? 'var(--ink-3)' : good ? 'var(--positive)' : 'var(--negative)';
      el('rect', { x, y: a, width: w, height: Math.max(1, b - a), style: `fill:${c}` }, g);
      el('text', { x: x + w / 2, y: a - 6, 'text-anchor': 'middle', style: r.d.total ? null : `fill:${c}`, class: r.d.total ? 'ink' : null }, g, (r.d.total || r.d.value < 0 ? '' : '+') + F(r.d.total ? r.b : r.d.value));
      if (i < rows.length - 1) el('path', { class: 'axis', d: `M${x + w} ${px(Y(r.b))} H${x + w + gap * 2}` }, g);
    });
    xLabels(g, s.data.map(d => d.label), i => m.l + bw * (i + 0.5), H - 3, f, bw);
  };

  function chart(host, spec) {
    host = $(host);
    const tall = host.clientHeight > 120 ? host.clientHeight : 0;   // a host with its own height (a slide body) is filled
    const draw = () => { const s = norm(spec); if (!s.height && tall) s.height = tall; C[s.type](host, s, Math.max(220, host.clientWidth || 720), s.height || 320); };
    draw();
    if (window.ResizeObserver) { let w = host.clientWidth; new ResizeObserver(() => { if (Math.abs(host.clientWidth - w) > 2) { w = host.clientWidth; draw(); } }).observe(host); }
  }

  function spark(host, values, o) {
    host = $(host); o = o || {}; values = (values || []).map(Number).filter(v => !isNaN(v));
    const W = o.width || 96, H = o.height || 20, n = values.length, lo = Math.min(...values), hi = Math.max(...values);
    const X = i => n > 1 ? 1 + i / (n - 1) * (W - 8) : W / 2, Y = v => 3 + (H - 6) * (1 - (hi === lo ? 0.5 : (v - lo) / (hi - lo)));
    const g = root(host, W, H, o.label, true); g.style.display = 'inline-block'; g.style.verticalAlign = 'middle';
    if (!n) return;
    if (n > 1) el('path', { class: 'ln', d: 'M' + values.map((v, i) => X(i).toFixed(1) + ' ' + Y(v).toFixed(1)).join(' L') }, g);
    el('rect', { x: X(n - 1) - 2.5, y: Y(values[n - 1]) - 2.5, width: 5, height: 5, style: 'fill:var(--accent)' }, g);
  }

  /* ---------------------------------------------------------------- diagrams */
  const D = {};
  const head = (g, x, y, dir, cls) => el('path', { class: cls, d: dir === 'r' ? `M${x - 6} ${y - 4} L${x} ${y} L${x - 6} ${y + 4}` : dir === 'l' ? `M${x + 6} ${y - 4} L${x} ${y} L${x + 6} ${y + 4}` : dir === 'd' ? `M${x - 4} ${y - 6} L${x} ${y} L${x + 4} ${y - 6}` : `M${x - 4} ${y + 6} L${x} ${y} L${x + 4} ${y + 6}` }, g);
  function box(g, x, y, w, h, label, f, accent, cls) {
    el('rect', { class: 'ln' + (accent ? ' a' : ''), x: px(x), y: px(y), width: Math.round(w), height: Math.round(h) }, g);
    const lines = up(label).split('\n'), y0 = y + h / 2 - (lines.length - 1) * (f + 3) / 2 + f * 0.36;
    lines.forEach((l, i) => text(g, px(x) + Math.round(w) / 2, y0 + i * (f + 3), l, cls || (accent ? 'at' : 'ink'), 'middle'));
  }
  function wire(g, pts, e, f) {                        // orthogonal polyline with an arrowhead and a label
    const cls = 'ln' + (e.accent ? ' a' : '') + (e.dashed ? ' dash' : ''), P = pts.map(p => [px(p[0]), px(p[1])]);
    el('path', { class: cls, d: 'M' + P.map(p => p.join(' ')).join(' L') }, g);
    const a = P[P.length - 2], b = P[P.length - 1];
    if (e.arrow !== false) head(g, b[0], b[1], a[1] === b[1] ? (b[0] > a[0] ? 'r' : 'l') : (b[1] > a[1] ? 'd' : 'u'), 'ln' + (e.accent ? ' a' : ''));
    if (!e.label) return;
    let best = null;
    for (let i = 1; i < P.length; i++) if (P[i][1] === P[i - 1][1]) { const len = Math.abs(P[i][0] - P[i - 1][0]); if (!best || len > best.len) best = { len, x: (P[i][0] + P[i - 1][0]) / 2, y: P[i][1] }; }
    if (best && best.len >= tw(e.label, f) - 8) text(g, best.x, best.y - 7, up(e.label), (e.accent ? 'at' : 'dim') + ' halo', 'middle');
    else { const i = P.length > 2 ? 1 : 0; text(g, P[i][0] + 8, (P[i][1] + P[i + 1][1]) / 2 + f * 0.36, up(e.label), (e.accent ? 'at' : 'dim') + ' halo'); }
  }

  D.flow = function (host, s) {
    const f = fsize(host), c = Object.assign({ w: 140, h: 56, gy: 52 }, s.cell || {}), N = {}, E = s.edges || []; let mc = 0, mr = 0;
    if (!c.gx) c.gx = Math.max(72, ...E.map(e => tw(e.label || '', f) + 28));
    c.w = Math.max(c.w, ...s.nodes.map(n => Math.max(...String(n.label).split('\n').map(l => tw(l, f))) + (n.kind === 'store' ? 52 : 24)));
    s.nodes.forEach(n => { n.col = n.col || 0; n.row = n.row || 0; N[n.id] = n; mc = Math.max(mc, n.col); mr = Math.max(mr, n.row); });
    // A backward edge (to an earlier column) runs in the corridor under its row, or over it with via: "top".
    // Each one gets its own lane and its own ports, so two never share a line and none rides a forward wire.
    const noted = {}, lanes = {}; let deep = 0, high = 0;
    s.nodes.forEach(n => { if (n.note) noted[n.row] = 1; });
    E.forEach(e => {
      const a = N[e.from], b = N[e.to]; if (b.col >= a.col) return;
      const key = (e.via === 'top' ? 't' : 'b') + Math.max(a.row, b.row); e._k = lanes[key] = (lanes[key] || 0) + 1;
      const off = (e.via === 'top' ? (s.groups ? 34 : 16) : (noted[Math.max(a.row, b.row)] ? f + 30 : f + 16)) + (f + 8) * (e._k - 1); e._off = off;
      if (e.via === 'top') high = Math.max(high, off + f + 10); else deep = Math.max(deep, off + 12);
    });
    c.gy = Math.max(c.gy, deep + 10, high + 10);
    const below = {}, above = {};                     // which ports already carry a wire or a group label
    E.forEach(e => { const a = N[e.from], b = N[e.to];
      if (a.col === b.col) { const up_ = b.row < a.row; below[(up_ ? b : a).id] = 1; above[(up_ ? a : b).id] = 1; }
      else if (b.col < a.col) (e.via === 'top' ? above : below)[a.id] = (e.via === 'top' ? above : below)[b.id] = 1; });
    (s.groups || []).forEach(gr => { const top = Math.min(...gr.nodes.map(id => N[id].row)); gr.nodes.forEach(id => { if (N[id].row === top) above[id] = 1; }); });
    s.nodes.forEach(n => { n._lift = !!(n.note && below[n.id] && !above[n.id]); });   // a note moves above its node when a wire leaves below it
    const lift0 = s.nodes.some(n => n._lift && n.row === 0) ? f + 12 : 0;
    const padX = s.groups ? 28 : 1, padT = Math.max(s.groups ? 28 : 1, high, lift0), X = col => padX + col * (c.w + c.gx), Y = row => padT + row * (c.h + c.gy);
    let tail = s.groups ? 28 : 1; s.nodes.forEach(n => { if (n.note && n.row === mr) tail = Math.max(tail, f + 14); });
    const W = X(mc) + c.w + padX, H = Y(mr) + c.h + Math.max(tail, deep) + 1, g = root(host, W, H, s.label, !s.fit);
    (s.groups || []).forEach(gr => {
      const ns = gr.nodes.map(id => N[id]), x0 = Math.min(...ns.map(n => X(n.col))) - 18, y0 = Math.min(...ns.map(n => Y(n.row))) - 18;
      const x1 = Math.max(...ns.map(n => X(n.col))) + c.w + 18, y1 = Math.max(...ns.map(n => Y(n.row))) + c.h + 18, k = 12, a = px(x0), b = px(y0), d = px(x1), e = px(y1);
      el('path', { class: 'ln', d: `M${a} ${b + k} V${b} H${a + k} M${d - k} ${b} H${d} V${b + k} M${a} ${e - k} V${e} H${a + k} M${d - k} ${e} H${d} V${e - k}` }, g);
      text(g, (x0 + x1) / 2, y0 + f * 0.36, '[ ' + up(gr.label) + ' ]', 'halo', 'middle');
    });
    E.forEach(e => {
      const a = N[e.from], b = N[e.to], ax = X(a.col), ay = Y(a.row), bx = X(b.col), by = Y(b.row), acy = ay + c.h / 2, bcy = by + c.h / 2, acx = ax + c.w / 2, bcx = bx + c.w / 2; let p;
      if (b.col < a.col) {
        const shift = 14 + 12 * (e._k - 1), top = e.via === 'top', row = Math.max(a.row, b.row);
        const ly = top ? Y(Math.min(a.row, b.row)) - e._off : Y(row) + c.h + e._off;
        p = [[acx + shift, top ? ay : ay + c.h], [acx + shift, ly], [bcx - shift, ly], [bcx - shift, top ? by : by + c.h]];
        wire(g, p, Object.assign({}, e, { label: null }), f);
        if (e.label) text(g, px(acx + shift) - 8, ly - 6, up(e.label), (e.accent ? 'at' : 'dim') + ' halo', 'end');
        return;
      }
      else if (a.row === b.row) p = [[ax + c.w, acy], [bx, bcy]];
      else if (a.col === b.col) {
        p = b.row > a.row ? [[acx, ay + c.h], [bcx, by]] : [[acx, ay], [bcx, by + c.h]];
        wire(g, p, Object.assign({}, e, { label: null }), f);                                        // label sits just past the source, above any lane in the corridor
        if (e.label) text(g, px(acx) + 8, b.row > a.row ? ay + c.h + f + 3 : ay - 6, up(e.label), (e.accent ? 'at' : 'dim') + ' halo');
        return;
      }
      else { const mx = bx - c.gx / 2; p = [[ax + c.w, acy], [mx, acy], [mx, bcy], [bx, bcy]]; }
      wire(g, p, e, f);
    });
    s.nodes.forEach(n => {
      const x = X(n.col), y = Y(n.row);
      box(g, x, y, c.w, c.h, n.kind === 'store' ? '[ ' + n.label + ' ]' : n.label, f, n.accent);
      if (!n.note) return;
      if (n._lift) text(g, x + c.w / 2, y - 8, up(n.note), 'dim halo', 'middle');
      else if (below[n.id]) text(g, x + c.w / 2 - 10, y + c.h + f + 8, up(n.note), 'dim halo', 'end');
      else text(g, x + c.w / 2, y + c.h + f + 8, up(n.note), 'dim', 'middle');
    });
  };

  D.sequence = function (host, s) {
    const f = fsize(host), bw = 124, bh = 40, step = s.step || 38;
    const col = Math.max(170, ...s.messages.map(m => tw(m.label || '', f) + 44)), ix = {}, X = i => 1 + bw / 2 + i * col;
    s.actors.forEach((a, i) => ix[a.id] = i);
    const selfW = Math.max(0, ...s.messages.filter(m => m.from === m.to && ix[m.from] === s.actors.length - 1).map(m => 40 + tw(m.label || '', f)));
    const W = X(s.actors.length - 1) + Math.max(bw / 2, selfW) + 2, H = bh + step * (s.messages.length + 1) + 2, g = root(host, W, H, s.label, !s.fit);
    s.actors.forEach((a, i) => { el('path', { class: 'grid strong', d: `M${px(X(i))} ${bh} V${H - 1}` }, g); box(g, X(i) - bw / 2, 0, bw, bh, a.label, f, a.accent); });
    s.messages.forEach((m, k) => {
      const y = bh + step * (k + 1), a = X(ix[m.from]), b = X(ix[m.to]), e = { accent: m.accent, dashed: m.reply };
      if (a === b) { wire(g, [[a, y - 8], [a + 28, y - 8], [a + 28, y + 8], [a, y + 8]], e, f); if (m.label) text(g, a + 36, y + f * 0.36, up(m.label), m.accent ? 'at' : 'dim'); }
      else { wire(g, [[a, y], [b, y]], e, f); if (m.label) text(g, (a + b) / 2, y - 7, up(m.label), (m.accent ? 'at' : 'dim') + ' halo', 'middle'); }
    });
  };

  D.layers = function (host, s) {
    const f = fsize(host), W = s.width || Math.max(280, host.clientWidth || 720), gap = 12, bh0 = 40;
    const lw = Math.min(Math.max(...s.layers.map(l => tw(l.label, f))) + 24, W * 0.3), inner = W - lw - 1;
    const rows = s.layers.map(l => {
      const items = l.items.map(it => (typeof it === 'string' ? { label: it } : it)), need = Math.max(...items.map(it => tw(it.label, f))) + 20;
      const per = Math.max(1, Math.min(items.length, Math.floor((inner + gap) / (need + gap)))), lines = Math.ceil(items.length / per);
      return { l, items, per, lines };
    });
    const most = Math.max(...rows.map(r => r.lines)), base = s.rowHeight || Math.max(68, Math.min(120, room(host) / s.layers.length || 0)), bh = most > 1 ? bh0 : Math.min(64, base - 28);
    rows.forEach(r => { r.h = Math.max(base, r.lines * (bh + 8) + 20); });
    const H = rows.reduce((a, r) => a + r.h, 0) + 1, g = root(host, W, H, s.label, !s.fit); let y = 0;
    rows.forEach(r => {
      el('path', { class: 'grid', d: `M0 ${px(y)} H${W}` }, g);
      text(g, 0, y + r.h / 2 + f * 0.36, up(r.l.label));
      const y0 = y + (r.h - (r.lines * bh + (r.lines - 1) * 8)) / 2;
      r.items.forEach((it, j) => {
        const line = Math.floor(j / r.per), inLine = Math.min(r.per, r.items.length - line * r.per), w = (inner - gap * (inLine - 1)) / inLine;
        box(g, lw + (j % r.per) * (w + gap), y0 + line * (bh + 8), w, bh, it.label, f, it.accent);
      });
      y += r.h;
    });
    el('path', { class: 'grid', d: `M0 ${px(H - 1)} H${W}` }, g);
  };

  D.timeline = function (host, s) {                    // columns: [labels]; rows: [{label, from, to, accent} | {label, at, accent}]
    const f = fsize(host), W = s.width || Math.max(480, host.clientWidth || 720), lw = Math.max(...s.rows.map(r => tw(r.label, f))) + 20, top = f + 12, rh = s.rowHeight || Math.max(34, Math.min(96, (room(host) - top) / s.rows.length || 0));
    const foot = s.now != null ? f + 8 : 0, grid = top + rh * s.rows.length, H = grid + 1 + foot, g = root(host, W, H, s.label, !s.fit), cw = (W - lw - 1) / s.columns.length, X = v => lw + v * cw;
    s.columns.forEach((c, i) => { el('path', { class: 'grid', d: `M${px(X(i))} ${top} V${grid}` }, g); text(g, X(i) + 6, f, up(c), 'dim'); });
    el('path', { class: 'grid', d: `M${px(X(s.columns.length))} ${top} V${grid}` }, g);
    const nowX = s.now != null ? X(s.now) : null;
    if (nowX != null) { el('path', { class: 'ln a', d: `M${px(nowX)} ${top - 4} V${grid + 3}` }, g); const nl = up(s.nowLabel || 'now'), end = nowX + tw(nl, f) / 2 > W; text(g, end ? W : Math.max(nowX, lw + tw(nl, f) / 2), H - 2, nl, 'at', end ? 'end' : 'middle'); }
    s.rows.forEach((r, i) => {
      const y = top + i * rh, cy = y + rh / 2, c = r.accent ? 'var(--accent)' : 'var(--ink-3)';
      el('path', { class: 'grid', d: `M0 ${px(y)} H${W}` }, g);
      text(g, 0, cy + f * 0.36, up(r.label), r.accent ? 'ink' : null);
      const note = (x0, x1) => {                        // right of the mark, else left of it, else inside the bar; never onto the row label
        if (!r.note) return; const w = tw(r.note, f), cls = (r.accent ? 'at' : 'dim') + ' halo', y = cy + f * 0.36;
        const clear = (a, b) => nowX == null || nowX < a - 3 || nowX > b + 3;                              // a note does not sit on the "now" line
        const spots = [[x1 + 10, x1 + 10 + w, () => text(g, x1 + 10, y, up(r.note), cls), x1 + 10 + w <= W],
                       [x0 - 10 - w, x0 - 10, () => text(g, x0 - 10, y, up(r.note), cls, 'end'), x0 - 10 - w >= lw + 4],
                       [(x0 + x1 - w) / 2, (x0 + x1 + w) / 2, () => text(g, (x0 + x1) / 2, y, up(r.note), 'onfill', 'middle'), x1 - x0 >= w + 12]];
        const pick = spots.find(o => o[3] && clear(o[0], o[1])) || spots.find(o => o[3]);
        if (pick) pick[2](); else el('title', {}, g.lastChild, r.label + ': ' + r.note);
      };
      if (r.at != null) { el('rect', { x: X(r.at) - 4, y: cy - 4, width: 8, height: 8, style: `fill:${c}` }, g); note(X(r.at) - 4, X(r.at) + 4); }
      else { el('rect', { x: X(r.from), y: cy - 6, width: Math.max(2, X(r.to) - X(r.from)), height: 12, style: `fill:${c}` }, g); note(X(r.from), X(r.to)); }
    });
    el('path', { class: 'grid', d: `M0 ${px(grid)} H${W}` }, g);
  };

  D.quadrant = function (host, s) {                    // x: [low, high], y: [low, high], items: [{label, x, y, accent}] in 0..1
    const f = fsize(host), m = f + 14, wide = host.clientWidth || 0;
    const S = Math.max(220, Math.min(s.size || 420, wide ? wide - m - 14 : 420)), x0 = m, y0 = f, W = m + S + 12, H = y0 + S + m + 2, g = root(host, W, H, s.label, true);
    el('path', { class: 'axis', d: `M${px(x0 + S / 2)} ${y0} V${y0 + S} M${x0} ${px(y0 + S / 2)} H${x0 + S}` }, g);
    el('rect', { class: 'grid', x: px(x0), y: px(y0), width: S, height: S }, g);
    text(g, x0, H - 3, up(s.x[0]) + ' →', 'dim'); text(g, x0 + S, H - 3, up(s.x[1]), 'dim', 'end');
    el('text', { class: 'dim', transform: `translate(${f} ${y0 + S}) rotate(-90)` }, g, up(s.y[0]) + ' →');
    el('text', { class: 'dim', 'text-anchor': 'end', transform: `translate(${f} ${y0}) rotate(-90)` }, g, up(s.y[1]));
    const band = f + 12, midX = x0 + S / 2, midY = y0 + S / 2;   // the corner names own a strip along the top and bottom edge
    (s.corners || []).forEach((c, i) => c && text(g, x0 + (i % 2 ? S - 8 : 8), y0 + (i < 2 ? f + 6 : S - 8), up(c), 'dim', i % 2 ? 'end' : 'start'));
    s.items.forEach(it => {
      const x = x0 + it.x * S, y = y0 + (1 - it.y) * S, w = tw(it.label, f);
      let left = x + 9 + w > x0 + S - 4;                                                                  // near the right edge the label goes left of its point
      if (!left && x < midX && x + 9 + w > midX - 4 && x - 9 - w > x0 + 4) left = true;                   // and it does not straddle the vertical midline when it can avoid it
      let ty = y + f * 0.36;
      if (Math.abs(ty - f * 0.36 - midY) < f * 0.8) ty += (y <= midY ? -1 : 1) * f * 0.9;                 // nor sit on the horizontal one
      if (s.corners) ty = Math.max(y0 + band + f, Math.min(y0 + S - band - 4, ty));
      ty = Math.max(y0 + f, Math.min(y0 + S - 3, ty));
      el('rect', { class: 'mark', x: Math.max(x0, Math.min(x0 + S - 7, x - 3.5)), y: Math.max(y0, Math.min(y0 + S - 7, y - 3.5)), width: 7, height: 7, style: `fill:${it.accent ? 'var(--accent)' : 'var(--ink)'}` }, g);
      text(g, left ? x - 9 : x + 9, ty, up(it.label), (it.accent ? 'at' : 'ink') + ' halo', left ? 'end' : null);
    });
  };

  D.tree = function (host, s) {
    const f = fsize(host), h = 40, gy = s.gapY || 44, gx = 20, all = [];
    (function walk(n, d) { n.d = d; all.push(n); (n.children || []).forEach(c => walk(c, d + 1)); })(s.root, 0);
    const w = s.nodeWidth || Math.max(96, ...all.map(n => tw(n.label, f) + 24)); let next = 0, depth = 0;
    (function place(n) { depth = Math.max(depth, n.d); if (!n.children || !n.children.length) { n.x = next; next += w + gx; } else { n.children.forEach(place); n.x = (n.children[0].x + n.children[n.children.length - 1].x) / 2; } })(s.root);
    const W = next - gx + 2, H = (depth + 1) * h + depth * gy + 2, g = root(host, W, H, s.label, !s.fit), Y = d => 1 + d * (h + gy);
    all.forEach(n => {
      if (n.children && n.children.length) {
        const cx = px(n.x + w / 2), my = px(Y(n.d) + h + gy / 2), a = px(n.children[0].x + w / 2), b = px(n.children[n.children.length - 1].x + w / 2);
        el('path', { class: 'ln', d: `M${cx} ${Y(n.d) + h} V${my} M${a} ${my} H${b} ` + n.children.map(c => `M${px(c.x + w / 2)} ${my} V${Y(c.d)}`).join(' ') }, g);
      }
      box(g, n.x, Y(n.d), w, h, n.label, f, n.accent);
    });
  };

  function diagram(host, spec) { host = $(host); D[spec.type](host, JSON.parse(JSON.stringify(spec))); }

  function auto(scope) {
    (scope || document).querySelectorAll('[data-cz]').forEach(host => {
      const src = host.querySelector('script[type="application/json"]'); if (!src || host.dataset.czDone) return;
      const spec = JSON.parse(src.textContent); host.dataset.czDone = '1';
      const cap = host.querySelector('figcaption'), mount = document.createElement('div');
      host.insertBefore(mount, cap);
      (D[spec.type] ? diagram : chart)(mount, spec);
    });
  }
  window.cz = Object.assign(window.cz || {}, { chart, diagram, spark, auto });
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', () => auto()); else auto();
})();
