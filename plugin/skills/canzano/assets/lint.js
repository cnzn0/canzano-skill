/* canzano lint. Finds the layout faults that are easy to miss. Load it on any page, run cz.lint() in
   the console or from a script, and fix what it lists. It returns an array of { issue, text }:

     stranded           a heading or line whose last line is one short word
     long-headline      a slide headline over two lines (four on a statement slide)
     overflow           content cut off by its slide, or a page wider than the window
     label-overlap      two labels in a drawing collide
     label-struck       a wire runs through a label
     label-covers-mark  a label sits on another point's marker
     tiny-labels        a drawing shown so small its labels fall under 9.5px
     small-graphic      a drawing under 30% of the room it has on a slide

   An empty array means none of these were found, not that the page is right: still look at it. */
(function () {
  function lint(scope) {
    const out = [], lines = n => { const r = document.createRange(); r.selectNodeContents(n); const rows = []; [...r.getClientRects()].forEach(q => { if (q.width < 1) return; const row = rows.find(x => Math.abs(x.top - q.top) < q.height / 2); if (row) { row.left = Math.min(row.left, q.left); row.right = Math.max(row.right, q.right); } else rows.push({ top: q.top, left: q.left, right: q.right }); }); return rows.sort((a, b) => a.top - b.top); };
    (scope || document).querySelectorAll('h1, h2, h3, p, li, figcaption, .lead').forEach(n => {
      if (!n.offsetParent || n.closest('svg') || /flex|grid/.test(getComputedStyle(n).display)) return;   // a row of parts is laid out, not wrapped
      const rows = lines(n), txt = n.textContent.trim().replace(/\s+/g, ' '); if (rows.length < 2) return;
      const widest = Math.max(...rows.map(r => r.right - r.left)), last = rows[rows.length - 1], lastWord = txt.split(' ').pop();
      if ((last.right - last.left) < widest * 0.2 || (rows.length <= 3 && /^H[123]$/.test(n.tagName) && (last.right - last.left) < widest * 0.34 && lastWord.length < 9)) out.push({ issue: 'stranded', text: txt.slice(0, 80) });
      if (n.closest('.slide') && /^H[12]$/.test(n.tagName) && rows.length > (n.closest('.statement') ? 4 : 2)) out.push({ issue: 'long-headline', text: txt.slice(0, 80) });
    });
    (scope || document).querySelectorAll('.slide').forEach((sl, i) => { if (sl.scrollHeight > sl.clientHeight + 2 || sl.scrollWidth > sl.clientWidth + 2) out.push({ issue: 'overflow', text: 'slide ' + (i + 1) }); });
    (scope || document).querySelectorAll('svg.cz').forEach(svg => {
      const T = [...svg.querySelectorAll('text')].filter(t => t.textContent.trim() && !t.getAttribute('transform')).map(t => ({ t, b: t.getBBox() }));
      const hit = (a, b) => Math.max(0, Math.min(a.x + a.width, b.x + b.width) - Math.max(a.x, b.x)) * Math.max(0, Math.min(a.y + a.height, b.y + b.height) - Math.max(a.y, b.y));
      T.forEach((a, i) => T.slice(i + 1).forEach(b => { if (hit(a.b, b.b) > 0.15 * Math.min(a.b.width * a.b.height, b.b.width * b.b.height)) out.push({ issue: 'label-overlap', text: a.t.textContent + ' / ' + b.t.textContent }); }));
      const vb = svg.viewBox.baseVal, shown = vb && vb.width ? svg.clientWidth / vb.width : 1, size = T.length ? parseFloat(getComputedStyle(T[0].t).fontSize) * shown : 99;
      if (size < 9.5) out.push({ issue: 'tiny-labels', text: 'labels render at ' + size.toFixed(1) + 'px; split the drawing or give it more room' });
      svg.querySelectorAll('rect.mark').forEach(mk => { const b = mk.getBBox(), cx = b.x + b.width / 2, cy = b.y + b.height / 2, x = T.find(o => cx > o.b.x && cx < o.b.x + o.b.width && cy > o.b.y && cy < o.b.y + o.b.height); if (x) out.push({ issue: 'label-covers-mark', text: x.t.textContent }); });
      svg.querySelectorAll('path.ln').forEach(p => {
        const len = p.getTotalLength(); if (!len) return;
        for (let d = 0; d <= len; d += 3) { const q = p.getPointAtLength(d), x = T.find(o => !o.struck && q.x > o.b.x + 2 && q.x < o.b.x + o.b.width - 2 && q.y > o.b.y + 3 && q.y < o.b.y + o.b.height - 3); if (x) { x.struck = 1; out.push({ issue: 'label-struck', text: x.t.textContent }); } }
      });
    });
    (scope || document).querySelectorAll('.slide .body svg').forEach(svg => {
      const body = svg.closest('.body'); if (svg.closest('p, td, li, .metrics')) return;
      const cell = svg.closest('.split') ? [...body.children].find(ch => ch.contains(svg)) || body : body;   // on a split slide the room is the column
      const r = svg.getBoundingClientRect(), bb = cell.getBoundingClientRect();
      if (r.width * r.height < 0.3 * bb.width * bb.height) out.push({ issue: 'small-graphic', text: 'fills ' + Math.round(100 * r.width * r.height / (bb.width * bb.height)) + '% of its slide body' });
    });
    if (document.documentElement.scrollWidth > document.documentElement.clientWidth + 2 && !document.querySelector('.deck')) out.push({ issue: 'overflow', text: 'page is wider than the window' });
    return out;
  }
  window.cz = Object.assign(window.cz || {}, { lint });
})();
