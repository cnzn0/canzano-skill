/* canzano viz. Dependency-free SVG charts and diagrams in the house style.
   Colours and type come from tokens.css through CSS variables, so both themes work.
   Use: put a JSON spec in a script tag of type application/json inside <figure class="chart" data-cz>,
   or call cz.chart(el, spec), cz.diagram(el, spec), cz.spark(el, values).
   Specs are documented in references/charts.md and references/diagrams.md. */
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
    const nf = new Intl.NumberFormat('en', { notation: s.suffix ? 'standard' : 'compact', maximumFractionDigits: s.digits == null ? 1 : s.digits });
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
      const slide = host.closest && host.closest('.slide'), room = host.clientWidth; let k = room && W > room ? room / W : 1;
      if (slide && room) { const body = host.closest('.body'), high = (body ? body.clientHeight : 480) - 40; k = Math.min(room / W, high / H, 1.7); }   // on a slide, grow to fill
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
    const ser = s.series[j], n = s.series.length;
    if (ser.color) return ser.color;
    if (s.highlight != null && n > 1) return ser.name === s.highlight || j === s.highlight ? 'var(--accent)' : 'var(--ink-3)';
    return n === 1 ? 'var(--ink-3)' : `var(--series-${(j % 8) + 1})`;
  }
  function grid(g, T, Y, x0, x1, F, f) {
    T.forEach(t => {
      el('path', { class: t === 0 ? 'axis' : 'grid', d: `M${x0} ${px(Y(t))} H${x1}` }, g);
      text(g, x0 - 8, Y(t) + f * 0.36, F(t), 'dim', 'end');
    });
  }
  function legend(g, s, x, y, f) {
    s.series.forEach((ser, j) => {
      el('rect', { x, y: y - 8, width: 8, height: 8, style: `fill:${colour(s, j)}` }, g);
      text(g, x + 14, y, up(ser.name));
      x += 14 + tw(ser.name, f) + 20;
    });
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
    const m = { l: Math.max(...T.map(t => tw(F(t), f))) + 12, r: 4, t: (n > 1 ? f + 20 : f + 10), b: f + 14 };
    const g = root(host, W, H, s.label), pw = W - m.l - m.r, ph = H - m.t - m.b, Y = v => m.t + ph - (v - y0) / (y1 - y0) * ph;
    grid(g, T, Y, m.l, W - m.r, F, f);
    if (n > 1) legend(g, s, m.l, f, f);
    const bw = pw / s.labels.length, gap = Math.max(2, Math.min(14, bw * 0.18)), inner = bw - gap * 2;
    s.labels.forEach((lab, i) => {
      const x = m.l + bw * i + gap; let acc = 0;
      s.series.forEach((ser, j) => {
        const v = ser.values[i]; if (v == null) return;
        let bx = x, w = inner, a, b;
        if (stacked) { b = Y(acc); acc += v; a = Y(acc); } else { w = inner / n - (n > 1 ? 2 : 0); bx = x + j * (inner / n); a = Y(Math.max(v, 0)); b = Y(Math.min(v, 0)); }
        const hi = n === 1 && (s.highlight === i || s.highlight === lab);
        el('rect', { x: bx, y: a, width: Math.max(1, w), height: Math.max(0, b - a), style: `fill:${hi ? 'var(--accent)' : colour(s, j)}` }, g);
        if (n === 1 && s.values !== false && bw > tw(F(v), f) + 2) text(g, bx + w / 2, v >= 0 ? a - 6 : b + f + 3, F(v), hi ? 'at' : 'ink', 'middle');
      });
      if (stacked && s.values !== false && bw > tw(F(acc), f) + 2) text(g, x + inner / 2, Y(acc) - 6, F(acc), 'ink', 'middle');
    });
    xLabels(g, s.labels, i => m.l + bw * (i + 0.5), H - 3, f, bw);
    if (s.target) { el('path', { class: 'axis dash', d: `M${m.l} ${px(Y(s.target.value))} H${W - m.r}` }, g); text(g, W - m.r, Y(s.target.value) - 6, up(s.target.label || F(s.target.value)), 'ink', 'end'); }
  };

  C.hbar = function (host, s, W, H) {
    const f = fsize(host), F = fmt(s), n = s.series.length, stacked = !!s.stacked && n > 1, rows = s.labels.length;
    const tot = s.labels.map((_, i) => stacked ? s.series.reduce((a, x) => a + (x.values[i] || 0), 0) : Math.max(...s.series.map(x => x.values[i] || 0)));
    const max = Math.max(...tot), lw = Math.max(...s.labels.map(l => tw(l, f))) + 14, vw = Math.max(...tot.map(v => tw(F(v), f))) + 10;
    const top = n > 1 ? f + 16 : 0, rh = s.rowHeight || Math.max(f + 12, Math.min(40, ((s.height ? H : 0) - top) / rows || 30));
    H = s.height ? H : top + rows * rh;
    const g = root(host, W, H, s.label), pw = W - lw - vw, X = v => lw + v / max * pw;
    if (n > 1) legend(g, s, lw, f, f);
    el('path', { class: 'axis', d: `M${px(lw)} ${top} V${H}` }, g);
    s.labels.forEach((lab, i) => {
      const y = top + i * rh, bh = Math.min(rh - 8, 22), by = y + (rh - bh) / 2, hi = n === 1 && (s.highlight === i || s.highlight === lab);
      text(g, 0, y + rh / 2 + f * 0.36, up(lab), hi ? 'ink' : null);
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
    const T = ticks(s.zero === false ? Math.min(...all) : Math.min(0, ...all), Math.max(...all, s.target ? s.target.value : 0)), y0 = T[0], y1 = T[T.length - 1];
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
    const f = fsize(host), FX = fmt(s.xAxis || {}), FY = fmt(s.yAxis || s), pts = s.series.flatMap(x => x.points);
    const TX = ticks(Math.min(...pts.map(p => p.x)), Math.max(...pts.map(p => p.x))), TY = ticks(Math.min(0, ...pts.map(p => p.y)), Math.max(...pts.map(p => p.y)));
    const far = pts.reduce((a, p) => (p.x > a.x ? p : a), pts[0]);
    const m = { l: Math.max(...TY.map(t => tw(FY(t), f))) + 12, r: Math.max(12, far.label ? tw(far.label, f) + 14 : 0), t: f + (s.series.length > 1 ? 20 : 10), b: f * 2 + 22 };
    const g = root(host, W, H, s.label), pw = W - m.l - m.r, ph = H - m.t - m.b;
    const X = v => m.l + (v - TX[0]) / (TX[TX.length - 1] - TX[0]) * pw, Y = v => m.t + ph - (v - TY[0]) / (TY[TY.length - 1] - TY[0]) * ph;
    grid(g, TY, Y, m.l, W - m.r, FY, f);
    TX.forEach(t => text(g, X(t), m.t + ph + f + 6, FX(t), 'dim', 'middle'));
    if (s.x) text(g, W - m.r, H - 3, up(s.x), null, 'end');
    if (s.y) text(g, m.l, f, up(s.y));
    if (s.series.length > 1) legend(g, s, s.y ? m.l + tw(s.y, f) + 24 : m.l, f, f);
    s.series.forEach((ser, j) => ser.points.forEach(p => {
      const c = p.accent ? 'var(--accent)' : s.series.length > 1 ? colour(s, j) : 'var(--ink-3)';
      el('rect', { x: X(p.x) - 3.5, y: Y(p.y) - 3.5, width: 7, height: 7, style: `fill:${c}` }, g);
      if (p.label) text(g, X(p.x) + 8, Y(p.y) + f * 0.36, up(p.label), (p.accent ? 'at' : 'ink') + ' halo');
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
    host = $(host); o = o || {};
    const W = o.width || 96, H = o.height || 20, lo = Math.min(...values), hi = Math.max(...values), X = i => 1 + i / (values.length - 1) * (W - 8), Y = v => 3 + (H - 6) * (1 - (v - lo) / (hi - lo || 1));
    const g = root(host, W, H, o.label, true); g.style.display = 'inline-block'; g.style.verticalAlign = 'middle';
    el('path', { class: 'ln', d: 'M' + values.map((v, i) => X(i).toFixed(1) + ' ' + Y(v).toFixed(1)).join(' L') }, g);
    el('rect', { x: X(values.length - 1) - 2.5, y: Y(values[values.length - 1]) - 2.5, width: 5, height: 5, style: 'fill:var(--accent)' }, g);
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
    const f = fsize(host), c = Object.assign({ w: 140, h: 56, gy: 52 }, s.cell || {}), N = {}; let mc = 0, mr = 0, lane = 0, notes = 0;
    if (!c.gx) c.gx = Math.max(72, ...(s.edges || []).map(e => tw(e.label || '', f) + 28));
    c.w = Math.max(c.w, ...s.nodes.map(n => Math.max(...String(n.label).split('\n').map(l => tw(l, f))) + (n.kind === 'store' ? 52 : 24)));
    s.nodes.forEach(n => { n.col = n.col || 0; n.row = n.row || 0; N[n.id] = n; mc = Math.max(mc, n.col); mr = Math.max(mr, n.row); });
    const pad = s.groups ? 28 : 1, X = col => pad + col * (c.w + c.gx), Y = row => pad + row * (c.h + c.gy);
    (s.edges || []).forEach(e => { const a = N[e.from], b = N[e.to]; if (a.row === b.row && b.col < a.col && a.row === mr) lane = 26; });
    s.nodes.forEach(n => { if (n.note && n.row === mr) notes = f + 12; });
    const W = X(mc) + c.w + pad, H = Y(mr) + c.h + Math.max(lane, notes, s.groups ? 28 : 1) + 1, g = root(host, W, H, s.label, !s.fit);
    (s.groups || []).forEach(gr => {
      const ns = gr.nodes.map(id => N[id]), x0 = Math.min(...ns.map(n => X(n.col))) - 18, y0 = Math.min(...ns.map(n => Y(n.row))) - 18;
      const x1 = Math.max(...ns.map(n => X(n.col))) + c.w + 18, y1 = Math.max(...ns.map(n => Y(n.row))) + c.h + 18, k = 12, a = px(x0), b = px(y0), d = px(x1), e = px(y1);
      el('path', { class: 'ln', d: `M${a} ${b + k} V${b} H${a + k} M${d - k} ${b} H${d} V${b + k} M${a} ${e - k} V${e} H${a + k} M${d - k} ${e} H${d} V${e - k}` }, g);
      text(g, (x0 + x1) / 2, y0 + f * 0.36, '[ ' + up(gr.label) + ' ]', null, 'middle');
    });
    (s.edges || []).forEach(e => {
      const a = N[e.from], b = N[e.to], ax = X(a.col), ay = Y(a.row), bx = X(b.col), by = Y(b.row), acy = ay + c.h / 2, bcy = by + c.h / 2, acx = ax + c.w / 2, bcx = bx + c.w / 2; let p;
      if (a.row === b.row && b.col > a.col) p = [[ax + c.w, acy], [bx, bcy]];
      else if (a.col === b.col) p = b.row > a.row ? [[acx, ay + c.h], [bcx, by]] : [[acx, ay], [bcx, by + c.h]];
      else if (b.col > a.col) { const mx = bx - c.gx / 2; p = [[ax + c.w, acy], [mx, acy], [mx, bcy], [bx, bcy]]; }
      else if (a.row === b.row) { const ly = ay + c.h + 22; p = [[acx, ay + c.h], [acx, ly], [bcx, ly], [bcx, by + c.h]]; }
      else { const mx = ax - c.gx / 2; p = [[ax, acy], [mx, acy], [mx, bcy], [bx + c.w, bcy]]; }
      wire(g, p, e, f);
    });
    s.nodes.forEach(n => {
      box(g, X(n.col), Y(n.row), c.w, c.h, n.kind === 'store' ? '[ ' + n.label + ' ]' : n.label, f, n.accent);
      if (n.note) text(g, X(n.col) + c.w / 2, Y(n.row) + c.h + f + 8, up(n.note), 'dim', 'middle');
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
    const f = fsize(host), W = s.width || Math.max(480, host.clientWidth || 720), lw = Math.max(...s.layers.map(l => tw(l.label, f))) + 24, rh = s.rowHeight || Math.max(68, Math.min(120, room(host) / s.layers.length || 0)), bh = Math.min(64, rh - 28), gap = 12;
    const H = rh * s.layers.length + 1, g = root(host, W, H, s.label, !s.fit);
    s.layers.forEach((l, i) => {
      const y = i * rh; el('path', { class: 'grid', d: `M0 ${px(y)} H${W}` }, g);
      text(g, 0, y + rh / 2 + f * 0.36, up(l.label));
      const n = l.items.length, w = (W - lw - gap * (n - 1) - 1) / n;
      l.items.forEach((it, j) => { const o = typeof it === 'string' ? { label: it } : it; box(g, lw + j * (w + gap), y + (rh - bh) / 2, w, bh, o.label, f, o.accent); });
    });
    el('path', { class: 'grid', d: `M0 ${px(H - 1)} H${W}` }, g);
  };

  D.timeline = function (host, s) {                    // columns: [labels]; rows: [{label, from, to, accent} | {label, at, accent}]
    const f = fsize(host), W = s.width || Math.max(480, host.clientWidth || 720), lw = Math.max(...s.rows.map(r => tw(r.label, f))) + 20, top = f + 12, rh = s.rowHeight || Math.max(34, Math.min(96, (room(host) - top) / s.rows.length || 0));
    const H = top + rh * s.rows.length + 1, g = root(host, W, H, s.label, !s.fit), cw = (W - lw - 1) / s.columns.length, X = v => lw + v * cw;
    s.columns.forEach((c, i) => { el('path', { class: 'grid', d: `M${px(X(i))} ${top} V${H}` }, g); text(g, X(i) + 6, f, up(c), 'dim'); });
    el('path', { class: 'grid', d: `M${px(X(s.columns.length))} ${top} V${H}` }, g);
    if (s.now != null) { el('path', { class: 'ln a', d: `M${px(X(s.now))} ${top - 4} V${H}` }, g); text(g, X(s.now) + 6, top + f, up(s.nowLabel || 'now'), 'at'); }
    s.rows.forEach((r, i) => {
      const y = top + i * rh, cy = y + rh / 2, c = r.accent ? 'var(--accent)' : 'var(--ink-3)';
      el('path', { class: 'grid', d: `M0 ${px(y)} H${W}` }, g);
      text(g, 0, cy + f * 0.36, up(r.label), r.accent ? 'ink' : null);
      const note = (x0, x1) => { if (!r.note) return; const fits = x1 + 10 + tw(r.note, f) <= W; text(g, fits ? x1 + 10 : x0 - 10, cy + f * 0.36, up(r.note), (r.accent ? 'at' : 'dim') + ' halo', fits ? null : 'end'); };
      if (r.at != null) { el('rect', { x: X(r.at) - 4, y: cy - 4, width: 8, height: 8, style: `fill:${c}` }, g); note(X(r.at) - 4, X(r.at) + 4); }
      else { el('rect', { x: X(r.from), y: cy - 6, width: Math.max(2, X(r.to) - X(r.from)), height: 12, style: `fill:${c}` }, g); note(X(r.from), X(r.to)); }
    });
    el('path', { class: 'grid', d: `M0 ${px(H - 1)} H${W}` }, g);
  };

  D.quadrant = function (host, s) {                    // x: [low, high], y: [low, high], items: [{label, x, y, accent}] in 0..1
    const f = fsize(host), S = s.size || 420, m = f + 14, room = Math.max(40, ...s.items.filter(i => i.x > 0.6).map(i => tw(i.label, f) + 12 - (1 - i.x) * S));
    const W = m + S + room, H = S + m + 2, g = root(host, W, H, s.label, true), x0 = m, y0 = 1;
    el('path', { class: 'axis', d: `M${px(x0 + S / 2)} ${y0} V${y0 + S} M${x0} ${px(y0 + S / 2)} H${x0 + S}` }, g);
    el('rect', { class: 'grid', x: px(x0), y: px(y0), width: S, height: S }, g);
    text(g, x0, H - 3, up(s.x[0]) + ' \u2192', 'dim'); text(g, x0 + S, H - 3, up(s.x[1]), 'dim', 'end');
    el('text', { class: 'dim', transform: `translate(${f} ${y0 + S}) rotate(-90)` }, g, up(s.y[0]) + ' \u2192');
    el('text', { class: 'dim', 'text-anchor': 'end', transform: `translate(${f} ${y0}) rotate(-90)` }, g, up(s.y[1]));
    (s.corners || []).forEach((c, i) => c && text(g, x0 + (i % 2 ? S - 8 : 8), y0 + (i < 2 ? f + 6 : S - 8), up(c), 'dim', i % 2 ? 'end' : 'start'));
    s.items.forEach(it => {
      const x = x0 + it.x * S, y = y0 + (1 - it.y) * S;
      el('rect', { x: x - 3.5, y: y - 3.5, width: 7, height: 7, style: `fill:${it.accent ? 'var(--accent)' : 'var(--ink)'}` }, g);
      text(g, x + 9, y + f * 0.36, up(it.label), (it.accent ? 'at' : 'ink') + ' halo');
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
  /* Lint: finds the layout faults that are easy to miss. Run cz.lint() in the page and fix what it lists.
     stranded: a heading or line whose last line is one short word. long-headline: more than two lines on a slide.
     overflow: content cut off by its slide or wider than the page. */
  function lint(scope) {
    const out = [], lines = n => { const r = document.createRange(); r.selectNodeContents(n); const rows = []; [...r.getClientRects()].forEach(q => { if (q.width < 1) return; const row = rows.find(x => Math.abs(x.top - q.top) < q.height / 2); if (row) { row.left = Math.min(row.left, q.left); row.right = Math.max(row.right, q.right); } else rows.push({ top: q.top, left: q.left, right: q.right }); }); return rows.sort((a, b) => a.top - b.top); };
    (scope || document).querySelectorAll('h1, h2, h3, p, li, figcaption, .lead').forEach(n => {
      if (!n.offsetParent || n.closest('svg')) return;
      const rows = lines(n), txt = n.textContent.trim().replace(/\s+/g, ' '); if (rows.length < 2) return;
      const widest = Math.max(...rows.map(r => r.right - r.left)), last = rows[rows.length - 1], lastWord = txt.split(' ').pop();
      if ((last.right - last.left) < widest * 0.2 || (rows.length <= 3 && /^H[123]$/.test(n.tagName) && (last.right - last.left) < widest * 0.34 && lastWord.length < 9)) out.push({ issue: 'stranded', text: txt.slice(0, 80) });
      if (n.closest('.slide') && !n.closest('.statement, .title') && /^H[12]$/.test(n.tagName) && rows.length > 2) out.push({ issue: 'long-headline', text: txt.slice(0, 80) });
    });
    (scope || document).querySelectorAll('.slide').forEach((sl, i) => { if (sl.scrollHeight > sl.clientHeight + 2 || sl.scrollWidth > sl.clientWidth + 2) out.push({ issue: 'overflow', text: 'slide ' + (i + 1) }); });
    if (document.documentElement.scrollWidth > document.documentElement.clientWidth + 2 && !document.querySelector('.deck')) out.push({ issue: 'overflow', text: 'page is wider than the window' });
    return out;
  }
  window.cz = { chart, diagram, spark, auto, lint };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', () => auto()); else auto();
})();
