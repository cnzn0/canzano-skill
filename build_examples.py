#!/usr/bin/env python3
"""Builds examples/*.html as single files with the skill's tokens.css and base.css inlined."""
import pathlib, sys
sys.dont_write_bytecode = True
root = pathlib.Path(__file__).parent
css = (root/"plugin/skills/canzano/assets/palette.css").read_text() + "\n" + (root/"plugin/skills/canzano/assets/tokens.css").read_text() + "\n" + (root/"plugin/skills/canzano/assets/base.css").read_text()
uicss = (root/"plugin/skills/canzano/assets/ui.css").read_text()
vizjs = (root/"plugin/skills/canzano/kits/charts/viz.js").read_text()
vizcss = (root/"plugin/skills/canzano/kits/charts/viz.css").read_text()
lintjs = (root/"plugin/skills/canzano/assets/lint.js").read_text()
deckcss = (root/"plugin/skills/canzano/kits/decks/deck.css").read_text()
deckjs = (root/"plugin/skills/canzano/kits/decks/deck.js").read_text()
out = root/"examples"

def page(name, title, running, extra, body, script="", ui=False, viz=False, deck=False, theme=None, dest=None):
    html = f"""<!doctype html>
<html lang="en"{theme or ""}>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Geist+Mono:wght@400;500&family=Inter:ital,wght@0,400;0,500;0,600;1,400&display=swap" rel="stylesheet">
<style>
{css}
{'' if deck else '@page { @top-left { content: "' + running + '"; font: 8pt "Geist Mono", monospace; letter-spacing: 0.04em; color: oklch(0.557 0.008 286); } }'}
{uicss if ui else ''}
{vizcss if viz else ''}
{deckcss if deck else ''}
{extra}
</style>
</head>
<body{" class=\"deck-page\"" if deck else ""}>
{body}
<script>{lintjs}</script>
{('<script>' + vizjs + '</script>') if viz else ''}
{('<script>' + deckjs + '</script>') if deck else ''}
{('<script>' + script + '</script>') if script else ''}
</body>
</html>
"""
    ((dest or out)/name).write_text(html)

import json
def cz(kind, spec, caption=None):
    return f'<figure class="{kind}" data-cz><script type="application/json">{json.dumps({k: v for k, v in spec.items() if v is not None})}</script>' + (f'<figcaption>{caption}</figcaption>' if caption else '') + '</figure>'

def R(x, y, d="r"):  # arrowhead ending at x,y
    return {"r": f"M{x-6} {y-4} L{x} {y} L{x-6} {y+4}", "d": f"M{x-4} {y-6} L{x} {y} L{x+4} {y-6}"}[d]

# ---------------------------------------------------------------- 01 report / PDF
page("report.html", "Hosting options", "ORDERS API // HOSTING OPTIONS // 23 NOV 2026", """
""", f"""<main>
  <header>
    <div class="meta">Infrastructure // 23 Nov 2026 // Example with illustrative figures</div>
    <h1>Managed containers meet the 99.95% target at the lowest cost</h1>
    <p class="lead read">Of the three hosting options reviewed for the orders API, managed containers cost $1,840 per month at projected load and need no change to the on-call rotation. The other two options cost more or miss the availability target.</p>
  </header>

  <div class="metrics">
    <div><span class="label">Monthly cost</span><span class="figure accent">$1,840</span><span class="meta">At 1,200 requests per second</span></div>
    <div><span class="label">Availability</span><span class="figure">99.95%</span><span class="meta">Provider commitment</span></div>
    <div><span class="label">Migration</span><span class="figure">3 weeks</span><span class="meta">Two engineers</span></div>
  </div>

  <section>
    <h2>Comparison</h2>
    <div class="table-wrap"><table>
      <thead><tr><th>Option</th><th class="num">Availability</th><th>Operations</th><th class="num">Migration</th><th class="num">Monthly cost</th></tr></thead>
      <tbody>
        <tr><td><strong>Managed containers</strong></td><td class="num">99.95%</td><td>The provider runs the cluster. No on-call change.</td><td class="num">3 weeks</td><td class="num accent">$1,840</td></tr>
        <tr><td>Self-run cluster</td><td class="num">99.99%</td><td>Full control. Requires a second on-call rotation.</td><td class="num">8 weeks</td><td class="num">$2,650</td></tr>
        <tr><td>Serverless functions</td><td class="num">99.90%</td><td>No servers to run. Cold starts add up to 400 ms.</td><td class="num">5 weeks</td><td class="num">$3,120</td></tr>
      </tbody>
    </table></div>
  </section>

  <section>
    <h2>Monthly cost at projected load</h2>
    {cz("chart", {"type":"hbar","highlight":"Managed containers","prefix":"$","label":"Monthly cost: managed containers 1,840 dollars, self-run cluster 2,650, serverless functions 3,120","data":[{"label":"Managed containers","value":1840},{"label":"Self-run cluster","value":2650},{"label":"Serverless functions","value":3120}],"compact":False,"digits":0}, "Fig 1 // USD per month at 1,200 requests per second, list prices")}
  </section>

  <section>
    <h2>Risks</h2>
    <ul class="ledger">
      <li><span>Provider price change at renewal</span><span>REVIEW IN Q3 2027</span></li>
      <li><span>Regional outage while running in one region</span><span>SECOND REGION, +$610 / MONTH</span></li>
      <li><span>Migration overlaps the December freeze</span><span>START 11 JAN 2027</span></li>
    </ul>
  </section>

  <section>
    <h2>Next steps</h2>
    <div class="table-wrap"><table>
      <thead><tr><th>Step</th><th>Owner</th><th class="num">Date</th></tr></thead>
      <tbody>
        <tr><td>Approve the managed containers budget</td><td>Head of engineering</td><td class="num">4 Dec 2026</td></tr>
        <tr><td>Run the orders API in staging on the new platform</td><td>Platform team</td><td class="num">18 Jan 2027</td></tr>
        <tr><td>Move production traffic in three stages</td><td>Platform team</td><td class="num">1 Feb 2027</td></tr>
      </tbody>
    </table></div>
  </section>
</main>""", viz=True)

# ---------------------------------------------------------------- 02 diagram
diagram = f"""
<svg class="dg" viewBox="0 0 1061 221" style="width:1061px" role="img" aria-label="Checkout request path from client through gateway and order service to the queue and two workers">
  <!-- sync path, accent -->
  <rect class="s" x="0.5" y="60.5" width="140" height="56"/><text x="70.5" y="92" text-anchor="middle">CLIENT</text>
  <g class="s a"><path d="M140.5 88.5 H270.5"/><path d="{R(270.5,88.5)}"/></g>
  <text class="at" x="205.5" y="78" text-anchor="middle">POST /CHECKOUT</text>
  <rect class="s" x="270.5" y="60.5" width="120" height="56"/><text x="330.5" y="92" text-anchor="middle">GATEWAY</text>
  <text class="dim" x="330.5" y="136" text-anchor="middle">RATE LIMIT + AUTH</text>
  <g class="s a"><path d="M390.5 88.5 H500.5"/><path d="{R(500.5,88.5)}"/></g>
  <text class="at" x="430.5" y="78" text-anchor="middle">AUTH OK</text>
  <!-- group: corner marks leave the sides open for connectors -->
  <g class="s"><path d="M470.5 32.5 V20.5 H482.5"/><path d="M638.5 20.5 H650.5 V32.5"/><path d="M470.5 188.5 V200.5 H482.5"/><path d="M638.5 200.5 H650.5 V188.5"/></g>
  <text class="mid" x="560.5" y="42" text-anchor="middle">[ ORDER SERVICE ]</text>
  <rect class="s" x="500.5" y="60.5" width="120" height="56"/><text x="560.5" y="92" text-anchor="middle">ORDERS API</text>
  <g class="s a"><path d="M560.5 116.5 V140.5"/><path d="{R(560.5,140.5,'d')}"/></g>
  <text class="at" x="572" y="132">INSERT</text>
  <rect class="s" x="500.5" y="140.5" width="120" height="44"/><text x="560.5" y="166" text-anchor="middle">ORDERS DB</text>
  <!-- async path -->
  <g class="s"><path d="M620.5 88.5 H760.5"/><path d="{R(760.5,88.5)}"/></g>
  <text class="dim" x="705.5" y="78" text-anchor="middle">ORDER.PLACED</text>
  <rect class="s" x="760.5" y="60.5" width="120" height="56"/><text x="820.5" y="92" text-anchor="middle">QUEUE</text>
  <text class="dim" x="820.5" y="136" text-anchor="middle">AT LEAST ONCE</text>
  <g class="s"><path d="M880.5 88.5 H900.5"/><path d="M900.5 48.5 V128.5"/><path d="M900.5 48.5 H920.5"/><path d="{R(920.5,48.5)}"/><path d="M900.5 128.5 H920.5"/><path d="{R(920.5,128.5)}"/></g>
  <rect class="s" x="920.5" y="20.5" width="140" height="56"/><text x="990.5" y="52" text-anchor="middle">EMAIL WORKER</text>
  <rect class="s" x="920.5" y="100.5" width="140" height="56"/><text x="990.5" y="132" text-anchor="middle">INVOICE WORKER</text>
</svg>"""
page("diagram.html", "Checkout path", "CHECKOUT // REQUEST PATH", "", f"""<main>
  <header>
    <div class="meta">Architecture // Checkout // Example</div>
    <h1>A checkout is one synchronous write, then two async jobs</h1>
    <p class="lead read">The client waits only until the order row is written. Email and invoicing run from the queue and can retry without the client.</p>
  </header>
  <section>
    <h2>Request path</h2>
    <figure class="diagram">{diagram}
      <figcaption>Fig 1 // Synchronous path in accent</figcaption>
    </figure>
  </section>
  <section>
    <h2>Edges</h2>
    <div class="table-wrap"><table>
      <thead><tr><th>From</th><th>To</th><th>Carries</th><th>Mode</th><th class="num">Budget</th></tr></thead>
      <tbody>
        <tr><td>Client</td><td>Gateway</td><td>POST /checkout with the cart and a payment token</td><td>Sync</td><td class="num">20 ms</td></tr>
        <tr><td>Gateway</td><td>Orders API</td><td>The authenticated request</td><td>Sync</td><td class="num">60 ms</td></tr>
        <tr><td>Orders API</td><td>Orders DB</td><td>One insert in one transaction</td><td>Sync</td><td class="num">15 ms</td></tr>
        <tr><td>Orders API</td><td>Queue</td><td>An order.placed event</td><td>Async</td><td class="num">n/a</td></tr>
        <tr><td>Queue</td><td>Workers</td><td>The same event, delivered at least once</td><td>Async</td><td class="num">n/a</td></tr>
      </tbody>
    </table></div>
  </section>
</main>""")

# ---------------------------------------------------------------- 03 web UI
rows = [
 ("api-gateway","a41f9c2","M. Okafor","RUNNING","1m 12s","Now","Raise the rate limit for partner keys"),
 ("orders","9d03e7b","L. Brandt","LIVE","3m 48s","14 min ago","Add idempotency keys to checkout"),
 ("billing","77c2a10","S. Ito","FAILED","0m 41s","1 h ago","Move invoice numbering to a sequence"),
 ("search","e5b81d4","M. Okafor","LIVE","5m 02s","3 h ago","Reindex products nightly"),
 ("web","1c9f0aa","A. Reyes","LIVE","2m 17s","5 h ago","Shorten the cart drawer copy"),
 ("notifications","4b7d2e9","L. Brandt","ROLLED BACK","2m 55s","Yesterday","Batch push notifications"),
]
cls = {"RUNNING":"accent","FAILED":"negative","LIVE":"","ROLLED BACK":"quiet"}
trs = "\n".join(f'''        <tr tabindex="0" data-status="{s}" data-msg="{m}" aria-selected="{'true' if i==0 else 'false'}"><td class="mark">→</td><td>{svc}</td><td class="mono">{c}</td><td>{a}</td><td class="status {cls[s]}">{s}</td><td class="num">{d}</td><td class="num when">{w}</td></tr>''' for i,(svc,c,a,s,d,w,m) in enumerate(rows))
page("web-ui.html", "Deploys", "DEPLOYS", """
.brand { font: var(--text-label)/1.6 var(--mono); letter-spacing: var(--tracking-caps); text-transform: uppercase; color: var(--ink); }
.foot { margin-top: auto; }
.work { display: grid; grid-template-columns: minmax(0, 1fr) 300px; gap: var(--s5); align-items: start; margin-top: var(--s5); }
.tools { margin: var(--s5) 0 0; }
td.mark { width: 20px; padding-right: 0; font-family: var(--mono); color: transparent; }
tbody tr { cursor: pointer; }
tbody td { color: var(--ink-2); transition: color var(--fast); }
tbody tr:hover td, tbody tr[aria-selected="true"] td { color: var(--ink); }
tbody tr[aria-selected="true"] td.mark { color: var(--ink); }
tbody tr:focus-visible { outline-offset: -2px; }
td.mono { font-family: var(--mono); font-size: var(--text-small); }
td.status { font: var(--text-label)/1.6 var(--mono); letter-spacing: var(--tracking-caps); }
tbody tr td.status.accent { color: var(--accent); }
tbody tr td.status.negative { color: var(--negative); }
tbody tr td.status.quiet { color: var(--ink-3); }
.detail h2 { margin: var(--s1) 0; }
.detail p { margin: 0; }
.detail .ledger { margin: var(--s3) 0 var(--s4); }
.detail .ledger li { flex-direction: row; border-color: var(--rule-strong); }
.detail .ledger li > :last-child { text-align: right; }
.detail .ledger li > :first-child { font: var(--text-label)/1.6 var(--mono); letter-spacing: var(--tracking-caps); text-transform: uppercase; color: var(--ink-2); }
@media (max-width: 1000px) { .work { grid-template-columns: 1fr; } .when, th.when { display: none; } }
""", f"""<div class="shell">
  <aside>
    <span class="brand">Acme // Deploys</span>
    <nav class="nav"><a href="#" aria-current="page">Deploys</a><a href="#">Services</a><a href="#">Logs</a><a href="#">Settings</a></nav>
    <span class="meta foot positive">All systems normal</span>
  </aside>
  <main>
    <div class="head"><h1>Deploys</h1><button class="primary">Deploy</button></div>
    <div class="panels">
      <div class="panel"><span class="label">Today</span><span class="figure">14</span></div>
      <div class="panel"><span class="label">Running</span><span class="figure accent">1</span></div>
      <div class="panel"><span class="label">Failed</span><span class="figure">1</span></div>
      <div class="panel"><span class="label">Median</span><span class="figure">3m 02s</span></div>
    </div>
    <div class="row tools">
      <div class="segmented" role="group" aria-label="Filter">
        <button aria-pressed="true" data-f="ALL">All</button><button aria-pressed="false" data-f="RUNNING">Running</button><button aria-pressed="false" data-f="FAILED">Failed</button>
      </div>
      <input type="search" placeholder="Service" aria-label="Filter by service">
    </div>
    <div class="work">
      <div class="table-wrap"><table>
        <thead><tr><th></th><th>Service</th><th>Commit</th><th>Author</th><th>Status</th><th class="num">Duration</th><th class="num when">Started</th></tr></thead>
        <tbody>
{trs}
        </tbody>
      </table></div>
      <div class="panel detail" aria-live="polite">
        <div class="meta" id="d-status">Running</div>
        <h2 id="d-svc">api-gateway</h2>
        <p id="d-msg">Raise the rate limit for partner keys</p>
        <ul class="ledger">
          <li><span>Commit</span><span id="d-commit">a41f9c2</span></li>
          <li><span>Author</span><span id="d-author">M. Okafor</span></li>
          <li><span>Started</span><span id="d-when">Now</span></li>
          <li><span>Duration</span><span id="d-dur">1m 12s</span></li>
        </ul>
        <div class="row"><button>View logs</button><button>Roll back</button></div>
      </div>
    </div>
  </main>
</div>""", """
const rows=[...document.querySelectorAll('tbody tr')],q=document.querySelector('input[type=search]');let f='ALL';
function select(r){rows.forEach(x=>x.setAttribute('aria-selected',x===r));const c=r.children;
  const set=(id,v)=>document.getElementById(id).textContent=v;
  set('d-svc',c[1].textContent);set('d-commit',c[2].textContent);set('d-author',c[3].textContent);
  set('d-status',c[4].textContent);set('d-dur',c[5].textContent);set('d-when',c[6].textContent);set('d-msg',r.dataset.msg);}
function filter(){rows.forEach(r=>{r.hidden=!((f==='ALL'||r.dataset.status===f)&&r.children[1].textContent.includes(q.value.trim().toLowerCase()));});}
rows.forEach(r=>{r.onclick=()=>select(r);r.onkeydown=e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();select(r);}};});
document.querySelectorAll('.segmented button').forEach(b=>b.onclick=()=>{f=b.dataset.f;document.querySelectorAll('.segmented button').forEach(x=>x.setAttribute('aria-pressed',x===b));filter();});
q.oninput=filter;
""", ui=True)

# ---------------------------------------------------------------- 04 mobile UI
BARS = '<text class="dim" x="21" y="118" text-anchor="middle">MON</text><rect x="55" y="47" width="34" height="53" style="fill:var(--ink-3)"/><text class="dim" x="72" y="41" text-anchor="middle">8.2</text><text class="dim" x="72" y="118" text-anchor="middle">TUE</text><rect x="106" y="68" width="34" height="32" style="fill:var(--ink-3)"/><text class="dim" x="123" y="62" text-anchor="middle">5.0</text><text class="dim" x="123" y="118" text-anchor="middle">WED</text><text class="dim" x="174" y="118" text-anchor="middle">THU</text><rect x="208" y="32" width="34" height="68" style="fill:var(--ink-3)"/><text class="dim" x="225" y="26" text-anchor="middle">10.4</text><text class="dim" x="225" y="118" text-anchor="middle">FRI</text><rect x="259" y="60" width="34" height="40" style="fill:var(--ink-3)"/><text class="dim" x="276" y="54" text-anchor="middle">6.1</text><text class="dim" x="276" y="118" text-anchor="middle">SAT</text><rect x="310" y="19" width="34" height="81" style="fill:var(--accent)"/><text class="at" x="327" y="13" text-anchor="middle">12.4</text><text class="dim" x="327" y="118" text-anchor="middle">SUN</text>'
page("mobile-ui.html", "Runs", "RUNS", """
:root { --gutter: 16px; }
.screen { width: 390px; max-width: 100%; min-height: 100vh; display: flex; flex-direction: column; border-right: 1px solid var(--rule); }
.top { display: flex; justify-content: space-between; align-items: center; height: 44px; padding: 0 var(--s2) 0 var(--gutter); }
.top h1 { font: 600 17px/22px var(--sans); letter-spacing: -0.01em; }
.pad { padding: 0 var(--gutter); display: grid; gap: var(--s2); }
.hero { padding: var(--s4) var(--gutter) var(--s5); }
.hero .figure { font-size: 36px; margin-top: var(--s2); }
.hero .meta { display: block; margin-top: var(--s2); }
.panels { grid-template-columns: repeat(3, 1fr); }
.panel .figure { font-size: 18px; }
.chart .segmented { display: flex; margin-bottom: var(--s4); background: var(--page); }
.chart .segmented button { flex: 1; }
.chart svg { display: block; width: 100%; height: auto; }
.screen section { margin-top: var(--s4); }
.screen .label { display: block; }
.screen .ledger li { flex-direction: row; }
.screen .ledger li > :last-child { text-align: right; }
.screen .ledger small { display: block; font: var(--text-label)/1.6 var(--mono); letter-spacing: var(--tracking-caps); text-transform: uppercase; color: var(--ink-3); }
.screen > .actions { display: grid; grid-template-columns: 1fr 1fr; gap: var(--s2); padding: var(--s4) var(--gutter); margin-top: auto; }
.tabs { position: sticky; bottom: 0; display: grid; grid-template-columns: repeat(4, 1fr); background: var(--page); border-top: 1px solid var(--rule); padding-bottom: env(safe-area-inset-bottom); }
.tabs a { position: relative; border: 0; text-align: center; font: 500 12px/1 var(--sans); letter-spacing: 0.02em; color: var(--ink-3); padding: 16px 0; }
.tabs a[aria-current] { color: var(--ink); }
""", """<div class="screen">
  <div class="top"><h1>Runs</h1><button class="quiet">Settings</button></div>

  <div class="hero">
    <span class="label">This week</span>
    <span class="figure">42.1 km</span>
    <span class="meta">Goal 50 km // <span class="accent">7.9 to go</span></span>
  </div>

  <div class="pad">
    <div class="panels">
      <div class="panel"><span class="label">Runs</span><span class="figure">5</span></div>
      <div class="panel"><span class="label">Pace</span><span class="figure">5:12</span></div>
      <div class="panel"><span class="label">Time</span><span class="figure">3:39</span></div>
    </div>

    <div class="panel chart">
      <div class="segmented" role="group" aria-label="Range">
        <button aria-pressed="true">Week</button><button aria-pressed="false">Month</button><button aria-pressed="false">Year</button>
      </div>
      <svg class="dg" viewBox="0 0 358 124" role="img" aria-label="Distance per day this week, longest on Sunday at 12.4 km">
        <path class="s" style="stroke:var(--rule-strong)" d="M0 100.5 H358"/>
        BARS
      </svg>
    </div>

    <section>
      <span class="label">Recent</span>
      <ul class="ledger">
        <li><span>Long run<small>Sun // 5:31 / km</small></span><span>12.4 km</span></li>
        <li><span>Easy<small>Sat // 5:40 / km</small></span><span>6.1 km</span></li>
        <li><span>Tempo<small>Fri // 4:48 / km</small></span><span>10.4 km</span></li>
      </ul>
    </section>
  </div>

  <div class="actions lg"><button class="primary">Start run</button><button>Add manually</button></div>
  <nav class="tabs"><a href="#">Today</a><a href="#" aria-current="page">Runs</a><a href="#">Plan</a><a href="#">More</a></nav>
</div>""".replace("BARS", BARS), """
document.querySelectorAll('.segmented button').forEach(b=>b.onclick=()=>document.querySelectorAll('.segmented button').forEach(x=>x.setAttribute('aria-pressed',x===b)));
""", ui=True)

# ---------------------------------------------------------------- 05 animated diagram
anim = f"""
<svg class="dg" viewBox="0 0 701 290" style="width:701px" role="img" aria-label="A write goes from the client to the leader, is replicated to two followers, acknowledged, then confirmed to the client">
  <rect class="s" id="n-client" x="0.5" y="120.5" width="120" height="56"/><text x="60.5" y="152" text-anchor="middle">CLIENT</text>
  <text class="dim" id="t-client" x="60.5" y="196" text-anchor="middle">IDLE</text>
  <g class="s" id="e-cl"><path d="M120.5 148.5 H240.5"/><path d="{R(240.5,148.5)}"/></g>
  <text class="at" id="l-cl" x="180.5" y="138" text-anchor="middle"></text>
  <rect class="s" id="n-leader" x="240.5" y="120.5" width="120" height="56"/><text x="300.5" y="152" text-anchor="middle">LEADER</text>
  <text class="dim" id="t-leader" x="300.5" y="196" text-anchor="middle">LOG [ 41 ]</text>
  <g class="s" id="e-tr"><path d="M360.5 148.5 H460.5"/></g>
  <text class="at" id="l-tr" x="410.5" y="138" text-anchor="middle"></text>
  <g class="s" id="e-a"><path d="M460.5 148.5 V68.5 H560.5"/><path d="{R(560.5,68.5)}"/></g>
  <g class="s" id="e-b"><path d="M460.5 148.5 V228.5 H560.5"/><path d="{R(560.5,228.5)}"/></g>
  <rect class="s" id="n-a" x="560.5" y="40.5" width="140" height="56"/><text x="630.5" y="72" text-anchor="middle">FOLLOWER A</text>
  <text class="dim" id="t-a" x="630.5" y="116" text-anchor="middle">LOG [ 41 ]</text>
  <rect class="s" id="n-b" x="560.5" y="200.5" width="140" height="56"/><text x="630.5" y="232" text-anchor="middle">FOLLOWER B</text>
  <text class="dim" id="t-b" x="630.5" y="276" text-anchor="middle">LOG [ 41 ]</text>
  <rect class="pkt" id="p0" width="7" height="7" visibility="hidden"/><rect class="pkt" id="p1" width="7" height="7" visibility="hidden"/>
</svg>"""
page("animated-diagram.html", "Replicated write", "REPLICATION // WRITE PATH", """
.controls { display: flex; gap: var(--s2); align-items: center; margin-bottom: var(--s4); }
.steps { list-style: none; margin: 0; padding: 0; }
.steps li { display: grid; grid-template-columns: 36px 120px 1fr; gap: var(--s3); align-items: baseline; padding: 11px 0; border-bottom: 1px solid var(--rule); color: var(--ink-3); transition: color var(--fast); }
.steps li > :nth-child(-n+2) { font: var(--text-label)/1.6 var(--mono); letter-spacing: var(--tracking-caps); text-transform: uppercase; }
.steps li[aria-current] { color: var(--ink); }
.steps li[aria-current] > :first-child { color: var(--accent); }
@media (max-width: 640px) { .steps li { grid-template-columns: 28px 1fr; } .steps li > :last-child { grid-column: 2; } }
@media print { .controls { display: none; } }
""", f"""<main>
  <header>
    <div class="meta">Replication // Animated // Example</div>
    <h1>A write is committed after both followers acknowledge it</h1>
    <p class="lead read">The leader appends first, replicates to both followers, and answers the client only when both have the entry.</p>
  </header>
  <section>
    <h2>Write path</h2>
    <div class="controls"><button id="play" aria-pressed="true">Pause</button><button id="step">Step</button></div>
    <figure class="diagram">{anim}
      <figcaption>Fig 1 // Entry 42</figcaption>
    </figure>
  </section>
  <section>
    <h2>Steps</h2>
    <ol class="steps">
      <li><span>01</span><span>Write</span><span>The client sends entry 42 to the leader and waits.</span></li>
      <li><span>02</span><span>Append</span><span>The leader appends 42 to its own log.</span></li>
      <li><span>03</span><span>Replicate</span><span>The leader sends 42 to both followers at once.</span></li>
      <li><span>04</span><span>Acknowledge</span><span>Each follower appends 42 and acknowledges.</span></li>
      <li><span>05</span><span>Commit</span><span>The leader marks 42 committed and answers the client.</span></li>
    </ol>
  </section>
</main>""", """
const $=id=>document.getElementById(id), reduced=matchMedia('(prefers-reduced-motion: reduce)').matches;
const P={cl:[[120.5,148.5],[240.5,148.5]],a:[[360.5,148.5],[460.5,148.5],[460.5,68.5],[560.5,68.5]],b:[[360.5,148.5],[460.5,148.5],[460.5,228.5],[560.5,228.5]]};
const len=p=>p.slice(1).reduce((s,q,i)=>s+Math.abs(q[0]-p[i][0])+Math.abs(q[1]-p[i][1]),0);
function at(p,k){let d=k*len(p);for(let i=1;i<p.length;i++){const a=p[i-1],b=p[i],l=Math.abs(b[0]-a[0])+Math.abs(b[1]-a[1]);if(d<=l)return[a[0]+(b[0]-a[0])*d/l,a[1]+(b[1]-a[1])*d/l];d-=l;}return p[p.length-1];}
const set=(id,v)=>$(id).textContent=v, L2='LOG [ 41 42 ]';
const S=[
 {edges:['cl'],moves:[['cl',0]],lbl:['l-cl','WRITE 42'],pre(){set('t-client','WAITING');}},
 {nodes:['leader'],pre(){set('t-leader',L2);}},
 {edges:['tr','a','b'],moves:[['a',0],['b',0]],lbl:['l-tr','APPEND 42'],post(){set('t-a',L2);set('t-b',L2);}},
 {edges:['tr','a','b'],moves:[['a',1],['b',1]],lbl:['l-tr','ACK 42']},
 {edges:['cl'],moves:[['cl',1]],lbl:['l-cl','OK 42'],post(){set('t-client','COMMITTED 42');}},
];
const items=[...document.querySelectorAll('.steps li')], pk=[$('p0'),$('p1')];
let playing=!reduced, once=false, wake=null;
function clear(){document.querySelectorAll('svg .a').forEach(e=>e.classList.remove('a'));set('l-cl','');set('l-tr','');pk.forEach(p=>p.setAttribute('visibility','hidden'));items.forEach(li=>li.removeAttribute('aria-current'));}
function reset(){clear();['t-leader','t-a','t-b'].forEach(id=>set(id,'LOG [ 41 ]'));set('t-client','IDLE');}
function show(s,i){clear();(s.edges||[]).forEach(e=>$('e-'+e).classList.add('a'));(s.nodes||[]).forEach(n=>$('n-'+n).classList.add('a'));if(s.lbl)set(s.lbl[0],s.lbl[1]);items[i].setAttribute('aria-current','step');}
function place(s,k){(s.moves||[]).forEach(([p,rev],j)=>{const [x,y]=at(P[p],rev?1-k:k);pk[j].setAttribute('x',x-3.5);pk[j].setAttribute('y',y-3.5);pk[j].setAttribute('visibility','visible');});}
const tween=(ms,fn)=>new Promise(res=>{let el=0,last=null;(function f(t){if(last!==null&&(playing||once))el+=t-last;last=t;const k=ms?Math.min(1,el/ms):1;fn(k);k<1?requestAnimationFrame(f):res();})(performance.now());});
const gate=()=>(playing||once)?Promise.resolve():new Promise(r=>wake=r);
async function run(){for(;;){reset();for(let i=0;i<S.length;i++){await gate();const s=S[i];show(s,i);s.pre&&s.pre();
  const ms=s.moves?(reduced?0:len(P[s.moves[0][0]])/0.16):(reduced?0:800);await tween(ms,k=>place(s,k));s.post&&s.post();
  if(once){once=false;}else await tween(350,()=>{});}
  await gate();await tween(reduced?0:1400,()=>{});}}
function ui(){$('play').textContent=playing?'Pause':'Play';$('play').setAttribute('aria-pressed',playing);}
$('play').onclick=()=>{playing=!playing;ui();if(playing&&wake){wake();wake=null;}};
$('step').onclick=()=>{playing=false;once=true;ui();if(wake){wake();wake=null;}};
ui();
const [hs,hk]=location.hash.slice(1).split('@'), h=parseInt(hs);
if(h>=1&&h<=S.length){playing=false;ui();reset();for(let i=0;i<h-1;i++){S[i].pre&&S[i].pre();S[i].post&&S[i].post();}const s=S[h-1];show(s,h-1);s.pre&&s.pre();place(s,hk===undefined?0.55:parseFloat(hk));if(parseFloat(hk)>=1&&s.post)s.post();}else run();
""")

# ---------------------------------------------------------------- 06 settings form
page("settings.html", "Settings", "SETTINGS", """
.brand { font: var(--text-label)/1.6 var(--mono); letter-spacing: var(--tracking-caps); text-transform: uppercase; color: var(--ink); }
.shell > main > section { margin-top: var(--s6); max-width: 640px; }
.shell > main > section > .label { display: block; margin-bottom: var(--s3); }
.saved { font: var(--text-label)/1 var(--mono); letter-spacing: var(--tracking-caps); text-transform: uppercase; color: var(--positive); }
""", """<div class="shell">
  <aside>
    <span class="brand">Acme // Deploys</span>
    <nav class="nav"><a href="#">Deploys</a><a href="#">Services</a><a href="#">Logs</a><a href="#" aria-current="page">Settings</a></nav>
  </aside>
  <main>
    <div class="head"><h1>Settings</h1></div>

    <section style="margin-top:0">
      <span class="label">Team</span>
      <div class="row">
        <div class="segmented" role="group" aria-label="Members"><button aria-pressed="true">Members</button><button aria-pressed="false">Invited</button></div>
        <input type="search" class="w-m" placeholder="Name or email" aria-label="Find a member">
        <select class="w-s" aria-label="Role"><option>All roles</option><option>Admin</option><option>Member</option></select>
        <button class="push">Invite</button>
      </div>
    </section>

    <section>
      <span class="label">Invite</span>
      <form class="form" onsubmit="return false">
        <div class="pair">
          <div class="field"><label for="n1">First name</label><input id="n1" autocomplete="given-name" value="Lena"></div>
          <div class="field"><label for="n2">Last name</label><input id="n2" autocomplete="family-name" value="Brandt"></div>
        </div>
        <div class="field"><label for="em">Email</label><input id="em" type="email" autocomplete="email" value="lena@" aria-invalid="true" aria-describedby="em-e"><span class="error" id="em-e">Enter a full email address.</span></div>
        <div class="field"><label for="ro">Role</label><select id="ro" class="w-m"><option>Member</option><option>Admin</option></select></div>
        <div class="field"><label for="se">Seats</label>
          <div class="row">
            <div class="joined stepper"><button type="button" aria-label="Fewer seats">-</button><input id="se" class="w-xs" inputmode="numeric" value="12"><button type="button" aria-label="More seats">+</button></div>
            <label class="affix w-s"><span>$</span><input value="240" aria-label="Monthly cost" readonly><span>/ mo</span></label>
          </div>
        </div>
        <div class="actions"><button class="primary">Send invite</button><button type="button">Cancel</button></div>
      </form>
    </section>

    <section>
      <span class="label">Notifications</span>
      <ul class="ledger settings">
        <li><span>Failed deploys<small>Email the author and the on-call engineer</small></span><span><input type="checkbox" class="switch" checked aria-label="Failed deploys"></span></li>
        <li><span>Weekly summary<small>Mondays at 09:00</small></span><span><input type="checkbox" class="switch" aria-label="Weekly summary"></span></li>
        <li><span>Channel</span><span><select class="w-m" aria-label="Channel"><option>#deploys</option><option>#engineering</option></select></span></li>
      </ul>
    </section>

    <section>
      <span class="label">Danger</span>
      <ul class="ledger settings">
        <li><span>Delete this workspace<small>Removes 14 services and their logs</small></span><span><button class="danger">Delete workspace</button></span></li>
      </ul>
    </section>
  </main>
</div>""", ui=True)

# ---------------------------------------------------------------- 07 viz gallery
months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
G = {}
G["bar"] = cz("chart", {"type":"bar","label":"Signups per quarter","highlight":"Q4","data":[{"label":"Q1","value":1240},{"label":"Q2","value":1610},{"label":"Q3","value":2130},{"label":"Q4","value":3420}],"height":280}, "Bar // one series, the bar that matters in accent")
G["grouped"] = cz("chart", {"type":"bar","labels":["Q1","Q2","Q3","Q4"],"series":[{"name":"Free","values":[900,1100,1400,2100]},{"name":"Team","values":[280,400,560,980]},{"name":"Enterprise","values":[60,110,170,340]}],"height":280}, "Bar // grouped series")
G["stacked"] = cz("chart", {"type":"bar","stacked":True,"labels":months[:8],"series":[{"name":"Web","values":[40,44,52,58,61,70,76,84]},{"name":"iOS","values":[22,25,27,33,38,41,47,52]},{"name":"Android","values":[12,14,15,18,22,25,27,31]}],"suffix":"k","height":280}, "Bar // stacked")
G["hbar"] = cz("chart", {"type":"hbar","highlight":"Search","suffix":"%","data":[{"label":"Search","value":41},{"label":"Direct","value":24},{"label":"Referral","value":17},{"label":"Social","value":11},{"label":"Email","value":7}]}, "Horizontal bar // ranked categories")
G["share"] = cz("chart", {"type":"hbar","stacked":True,"labels":["2025","2026"],"series":[{"name":"Compute","values":[52,44]},{"name":"Storage","values":[28,25]},{"name":"Network","values":[12,18]},{"name":"Support","values":[8,13]}],"suffix":"%","rowHeight":40}, "Horizontal bar // stacked shares")
G["line"] = cz("chart", {"type":"line","labels":months,"series":[{"name":"p50","values":[120,118,121,117,112,110,108,104,99,96,92,88]},{"name":"p95","values":[310,305,322,298,280,276,251,240,221,214,203,190]},{"name":"p99","values":[620,640,610,580,571,540,498,470,455,430,401,380]}],"suffix":" ms","marks":[{"at":"Jul","text":"Cache shipped"}],"height":300}, "Line // direct labels, one marked event")
G["area"] = cz("chart", {"type":"line","area":True,"labels":months,"series":[{"name":"","values":[2.1,2.4,2.9,3.1,3.8,4.6,5.2,6.1,7.4,8.2,9.6,11.3]}],"prefix":"$","suffix":"M","target":{"value":10,"label":"Plan $10M"},"height":300}, "Line // single series with area and a target")
G["scatter"] = cz("chart", {"type":"scatter","x":"Monthly price","y":"Retention at 12 months","xAxis":{"prefix":"$"},"suffix":"%","series":[{"name":"Plans","points":[{"x":9,"y":48,"label":"Solo"},{"x":29,"y":61,"label":"Team"},{"x":79,"y":74,"label":"Business","accent":True},{"x":149,"y":71,"label":"Scale"},{"x":19,"y":52},{"x":49,"y":66},{"x":99,"y":70}]}],"height":320}, "Scatter // labelled points")
G["heatmap"] = cz("chart", {"type":"heatmap","rows":["Mon","Tue","Wed","Thu","Fri","Sat","Sun"],"cols":["00","03","06","09","12","15","18","21"],"values":[[2,1,4,22,31,28,19,8],[3,1,5,25,34,30,21,9],[2,2,6,27,36,33,22,10],[3,1,5,26,35,31,24,11],[2,1,4,21,29,26,27,16],[4,2,2,8,14,16,18,15],[5,3,2,6,11,13,12,9]]}, "Heatmap // one hue, value printed in each cell")
G["slope"] = cz("chart", {"type":"slope","labels":["2025","2026"],"highlight":"Mobile","suffix":"%","series":[{"name":"Desktop","values":[58,44]},{"name":"Mobile","values":[31,47]},{"name":"Tablet","values":[11,9]}],"height":260}, "Slope // before and after")
G["waterfall"] = cz("chart", {"type":"waterfall","prefix":"$","suffix":"k","data":[{"label":"2025","value":820,"total":True},{"label":"New","value":310},{"label":"Expansion","value":140},{"label":"Churn","value":-95},{"label":"Downgrade","value":-45},{"label":"2026","total":True}],"height":300}, "Waterfall // how one total becomes the next")
G["flow"] = cz("diagram", {"type":"flow","label":"Checkout path","nodes":[{"id":"c","label":"Client","col":0,"row":0},{"id":"g","label":"Gateway","col":1,"row":0,"note":"Rate limit + auth"},{"id":"a","label":"Orders API","col":2,"row":0},{"id":"d","label":"Orders DB","col":2,"row":1,"kind":"store"},{"id":"q","label":"Queue","col":3,"row":0,"note":"At least once"},{"id":"e","label":"Email worker","col":4,"row":0},{"id":"i","label":"Invoice worker","col":4,"row":1}],"edges":[{"from":"c","to":"g","label":"POST /checkout","accent":True},{"from":"g","to":"a","label":"Auth ok","accent":True},{"from":"a","to":"d","label":"Insert","accent":True},{"from":"a","to":"q","label":"order.placed"},{"from":"q","to":"e"},{"from":"q","to":"i"}],"groups":[{"label":"Order service","nodes":["a","d"]}]}, "Flow // grid of nodes, orthogonal wires, one group")
G["sequence"] = cz("diagram", {"type":"sequence","actors":[{"id":"u","label":"Browser"},{"id":"a","label":"App"},{"id":"i","label":"Identity"},{"id":"r","label":"API"}],"messages":[{"from":"u","to":"a","label":"Sign in"},{"from":"a","to":"i","label":"Redirect with challenge","accent":True},{"from":"i","to":"i","label":"Verify user"},{"from":"i","to":"a","label":"Code","reply":True},{"from":"a","to":"i","label":"Code + verifier","accent":True},{"from":"i","to":"a","label":"Token","reply":True},{"from":"a","to":"r","label":"Request + token"},{"from":"r","to":"a","label":"200","reply":True}]}, "Sequence // who talks to whom, in order")
G["layers"] = cz("diagram", {"type":"layers","layers":[{"label":"Clients","items":["Web","iOS","Android","CLI"]},{"label":"Edge","items":["CDN","Gateway"]},{"label":"Services","items":["Orders","Billing",{"label":"Search","accent":True},"Notify"]},{"label":"Data","items":["Postgres","Queue","Object store"]}]}, "Layers // a stack, top to bottom")
G["timeline"] = cz("diagram", {"type":"timeline","columns":["Jan","Feb","Mar","Apr","May","Jun"],"now":2.4,"rows":[{"label":"Discovery","from":0,"to":1.2},{"label":"Design","from":0.8,"to":2.4},{"label":"Build","from":2,"to":4.6,"accent":True,"note":"Critical path"},{"label":"Beta","from":4.2,"to":5.3},{"label":"Launch","at":5.5,"note":"16 Jun","accent":True}]}, "Timeline // spans and milestones on one scale")
G["quadrant"] = cz("diagram", {"type":"quadrant","x":["Low effort","High effort"],"y":["Low impact","High impact"],"corners":["Do now","Plan","Skip","Avoid"],"items":[{"label":"Saved filters","x":0.22,"y":0.81,"accent":True},{"label":"Bulk edit","x":0.38,"y":0.66},{"label":"Offline mode","x":0.84,"y":0.78},{"label":"Themes","x":0.3,"y":0.2},{"label":"Rewrite sync","x":0.9,"y":0.34}],"size":360}, "Quadrant // two axes, labelled points")
G["tree"] = cz("diagram", {"type":"tree","root":{"label":"Revenue","children":[{"label":"New","children":[{"label":"Self serve"},{"label":"Sales led","accent":True}]},{"label":"Expansion","children":[{"label":"Seats"},{"label":"Usage"}]},{"label":"Renewal"}]}}, "Tree // a hierarchy, top down")
def sec(title, *figs): return f'  <section>\n    <h2>{title}</h2>\n' + "\n".join("    "+f for f in figs) + '\n  </section>'
def duo(a, b): return f'<div class="duo">{a}{b}</div>'
page("viz.html", "Charts and diagrams", "CHARTS AND DIAGRAMS", """
.duo { display: grid; grid-template-columns: 1fr 1fr; gap: var(--s6); }
.duo > figure { min-width: 0; }
@media (max-width: 800px) { .duo { grid-template-columns: 1fr; } }
section > figure + figure, section > .duo + figure, section > figure + .duo { margin-top: var(--s6); }
""", f"""<main>
  <header>
    <div class="meta">canzano // viz.js</div>
    <h1>Eight charts and six diagrams from one small script</h1>
  </header>
{sec("Bars", duo(G["bar"], G["grouped"]), duo(G["stacked"], G["waterfall"]), duo(G["hbar"], G["share"]))}
{sec("Lines", duo(G["line"], G["area"]))}
{sec("Relations", duo(G["scatter"], G["slope"]), G["heatmap"])}
{sec("Flow", G["flow"])}
{sec("Sequence", G["sequence"])}
{sec("Structure", G["layers"], G["tree"])}
{sec("Plans", G["timeline"], G["quadrant"])}
</main>""", viz=True)

# ---------------------------------------------------------------- 08 deck
D = {}
D["line"] = cz("chart", {"type":"line","labels":months,"highlight":"p95","series":[{"name":"p50","values":[120,118,121,117,112,110,108,104,99,96,92,88]},{"name":"p95","values":[310,305,322,298,280,276,251,240,221,214,203,190]},{"name":"p99","values":[620,640,610,580,571,540,498,470,455,430,401,380]}],"suffix":" ms","marks":[{"at":"Jul","text":"Cache shipped"}]}, "Fig 1 // API latency by percentile, 2026")
D["fall"] = cz("chart", {"type":"waterfall","good":"down","suffix":" ms","data":[{"label":"Jan","value":1800,"total":True},{"label":"Edge cache","value":-420},{"label":"Image CDN","value":-260},{"label":"Query batching","value":-170},{"label":"Smaller bundle","value":-70},{"label":"Dec","total":True}]}, "Fig 3 // Median checkout time, change by project")
D["flow"] = cz("diagram", {"type":"flow","nodes":[{"id":"c","label":"Client","col":0},{"id":"g","label":"Gateway","col":1},{"id":"k","label":"Cache","col":2,"accent":True,"note":"94% of reads stop here"},{"id":"a","label":"API","col":3},{"id":"d","label":"DB","col":3,"row":1,"kind":"store"}],"edges":[{"from":"c","to":"g"},{"from":"g","to":"k","label":"Read","accent":True},{"from":"k","to":"a","label":"Miss"},{"from":"a","to":"d"}]}, "Fig 2 // The cache sits behind the gateway, so auth and rate limits still apply")
D["time"] = cz("diagram", {"type":"timeline","columns":["Jan","Feb","Mar","Apr","May","Jun"],"rows":[{"label":"Search rewrite","from":0,"to":3.6,"accent":True,"note":"Critical path"},{"label":"Saved filters","from":0.5,"to":1.8},{"label":"Bulk edit","from":1.8,"to":3.2},{"label":"Offline mode","from":3.6,"to":5.6},{"label":"Checkout v3","at":5.7,"note":"24 Jun","accent":True}]}, "Fig 5 // H1 2027")
D["quad"] = cz("diagram", {"type":"quadrant","size":360,"x":["Low effort","High effort"],"y":["Low impact","High impact"],"corners":["Do now","Plan","Skip","Avoid"],"items":[{"label":"Saved filters","x":0.22,"y":0.81,"accent":True},{"label":"Bulk edit","x":0.38,"y":0.66},{"label":"Offline mode","x":0.84,"y":0.78},{"label":"Themes","x":0.3,"y":0.2},{"label":"Rewrite sync","x":0.88,"y":0.3}]})
D["bar"] = cz("chart", {"type":"bar","labels":["Q1","Q2","Q3","Q4"],"series":[{"name":"Desktop","values":[3.1,3.2,3.6,4.4]},{"name":"Mobile","values":[1.9,2.0,2.9,4.1]}],"suffix":"%"}, "Fig 4 // Checkout conversion by device")
page("deck.html", "Checkout review", "", """
""", f"""<div class="deck" data-label="Checkout review // Q4 2026 // Example">

  <section class="slide title">
    <h1>Checkout got 51% faster in 2026</h1>
    <p>Platform review // 23 Nov 2026 // Example with illustrative figures</p>
  </section>

  <section class="slide statement">
    <h2>Median checkout time fell from 1.8 s to 0.88 s, and conversion rose 2.1 points.</h2>
  </section>

  <section class="slide">
    <h2>Checkout is twice as fast and converts 2.1 points better</h2>
    <div class="body">
      <div class="metrics">
        <div><span class="label">Median checkout</span><span class="figure accent">0.88 s</span><span class="meta">From 1.8 s</span></div>
        <div><span class="label">API p95</span><span class="figure">190 ms</span><span class="meta">From 310 ms</span></div>
        <div><span class="label">Conversion</span><span class="figure">+2.1 pts</span><span class="meta">Mobile +2.2</span></div>
        <div><span class="label">Added revenue</span><span class="figure">$1.4M</span><span class="meta">Annualised</span></div>
      </div>
    </div>
  </section>

  <section class="slide">
    <h2>Every release since July moved p95 down</h2>
    <div class="body">{D["line"]}</div>
  </section>

  <section class="slide">
    <h2>One cache in front of the API did most of it</h2>
    <div class="body">{D["flow"]}</div>
  </section>

  <section class="slide">
    <h2>The edge cache removed almost half of the 920&nbsp;ms</h2>
    <div class="body">{D["fall"]}</div>
  </section>

  <section class="slide">
    <h2>Mobile closed the gap with desktop</h2>
    <div class="body">{D["bar"]}</div>
  </section>

  <section class="slide">
    <h2>All four projects shipped inside sixteen weeks</h2>
    <div class="body middle">
      <div class="table-wrap"><table>
        <thead><tr><th>Project</th><th class="num">Saved</th><th class="num">Cost</th></tr></thead>
        <tbody>
          <tr><td>Edge cache</td><td class="num">420 ms</td><td class="num">6 weeks</td></tr>
          <tr><td>Image CDN</td><td class="num">260 ms</td><td class="num">3 weeks</td></tr>
          <tr><td>Query batching</td><td class="num">170 ms</td><td class="num">5 weeks</td></tr>
          <tr><td>Smaller bundle</td><td class="num">70 ms</td><td class="num">2 weeks</td></tr>
        </tbody>
      </table></div>
    </div>
  </section>

  <section class="slide section">
    <span class="meta">02</span>
    <h2>The 2027 plan</h2>
  </section>

  <section class="slide">
    <h2>Search is the critical path for the first half</h2>
    <div class="body">{D["time"]}</div>
  </section>

  <section class="slide split flip">
    <h2>Saved filters come first: high impact, two weeks</h2>
    <div class="body">
      {D["quad"]}
      <div><p class="lead">It is the only item in the top left.</p><p>Offline mode matters as much but takes a quarter. It follows the search rewrite.</p></div>
    </div>
  </section>

  <section class="slide">
    <h2>Three decisions needed today</h2>
    <div class="body"><ol class="points"><li>Approve two engineers for the search rewrite from 6 Jan</li><li>Move offline mode to Q2</li><li>Set the 2027 target: median checkout under 0.7 s</li></ol></div>
  </section>

</div>""", viz=True, deck=True, theme=' data-theme="dark" class="keep-theme"')

# ---------------------------------------------------------------- 09 ascii
import sys, html as _html
sys.path.insert(0, str(root/"plugin/skills/canzano/kits/ascii"))
import ascii as A
def pre(txt, cls="ascii"): return f'<pre class="{cls}">{_html.escape(txt)}</pre>'
page("ascii.html", "ASCII", "ASCII", """
""", f"""<main>
  <header>
    <div class="meta">canzano // kits/ascii/ascii.py</div>
    {pre(A.banner("SHIP IT", "half"), "ascii hero")}
  </header>
  <section><h2>Flow</h2>{pre(A.flow("Client -[POST /checkout]-> Gateway -[auth ok]-> Orders API -> [Orders DB]"))}</section>
  <section><h2>Sequence</h2>{pre(A.seq(["Browser->App: sign in", "App->Identity: redirect with challenge", "Identity->Identity: verify", "Identity-->App: code", "App->API: request + token", "API-->App: 200"]))}</section>
  <section><h2>Table and bars</h2>
    <div class="cols">
      <div>{pre(A.table(["Plan | Seats | Price", "Team | 12 | $240", "Scale | 80 | $1,400", "Enterprise | 400 | $6,000"]))}</div>
      <div>{pre(A.bars(["Search=41", "Direct=24", "Referral=17", "Social=11", "Email=7"], 24, "%"))}</div>
    </div>
  </section>
  <section><h2>Tree, box, sparkline</h2>
    <div class="cols">
      <div>{pre(A.tree("Revenue\n  New\n    Self serve\n    Sales led\n  Expansion\n    Seats\n    Usage\n  Renewal"))}</div>
      <div>{pre(A.box("Deploy", ["api-gateway  a41f9c2", "status       RUNNING", "p95 ms       " + A.spark([310,305,322,298,280,276,251,240,221,214,203,190])]))}</div>
    </div>
  </section>
  <section><h2>Hero text</h2>{pre(A.banner("CANZANO", "block"), "ascii hero")}{pre(A.banner("V1.1", "shade"), "ascii hero")}</section>
</main>""")

# ---------------------------------------------------------------- index
ex = [
 ("01","PDF report","Compare our three hosting options for the orders API and give me a short report as a PDF.","report.pdf","report.html",760),
 ("02","Diagram","Draw how a checkout request moves through our services.","diagram.html","diagram.html",640),
 ("03","Animated diagram","Animate how a write gets replicated before it is committed.","animated-diagram.html","animated-diagram.html",760),
 ("04","Web UI","Quick internal tool to review today's deploys.","web-ui.html","web-ui.html",560),
 ("05","Mobile UI","A phone screen for this week's runs.","mobile-ui.html","mobile-ui.html",844),
 ("06","Form and settings","A settings page: find members, invite one, notification switches.","settings.html","settings.html",900),
 ("07","Deck","Turn the checkout review into slides for Thursday.","deck.html","deck.html",760),
 ("08","Charts and diagrams","Every chart and diagram type the skill can draw.","viz.html","viz.html",900),
 ("09","ASCII","A README diagram of the checkout path, and a banner.","ascii.html","ascii.html",700),
]
secs = "\n".join(f"""  <section>
    <h2>{n} // {t}</h2>
    <ul class="ledger"><li><span class="label">Ask</span><span class="ask">{ask}</span></li><li><span class="label">Outcome</span><span><a href="{href}">{href}</a></span></li></ul>
    <iframe src="{src}" title="{t}" loading="lazy" style="height:{h}px{';width:390px' if n=='05' else ''}"></iframe>
  </section>""" for n,t,ask,href,src,h in ex)
page("index.html", "canzano examples", "CANZANO // EXAMPLES", """
iframe { display: block; width: 100%; max-width: 100%; border: 1px solid var(--rule-strong); margin-top: var(--s4); background: var(--page); }
.ledger li > .ask { font-family: var(--sans); text-align: right; max-width: 60ch; }
""", f"""<main>
  <header>
    <div class="meta">canzano // examples</div>
    <h1>Nine asks and what the skill returns</h1>
    
  </header>
{secs}
</main>""")

# ---------------------------------------------------------------- test fixtures
# tests/fixtures.html holds the cases that have broken before. tests/check.py renders it at phone and
# desktop width, runs cz.lint() and the assertions in window.__assert, and fails on any finding.
F = [
 cz("diagram", {"type":"flow","nodes":[{"id":"a","label":"Client","col":0},{"id":"b","label":"Gateway","col":1,"note":"Auth"},{"id":"c","label":"Orders API","col":2},{"id":"d","label":"Queue","col":3},{"id":"e","label":"Worker","col":4},{"id":"f","label":"Orders DB","col":2,"row":1,"kind":"store"}],"edges":[{"from":"a","to":"b","label":"Post"},{"from":"b","to":"c","label":"Auth ok","accent":True},{"from":"c","to":"f","label":"Write"},{"from":"c","to":"d","label":"Enqueue"},{"from":"d","to":"e","label":"Dequeue"},{"from":"e","to":"c","label":"Backpressure"},{"from":"d","to":"b","label":"Reject","via":"top"}],"groups":[{"label":"Order service","nodes":["c","f"]}]}, "flow: group, backward edges below and above"),
 cz("diagram", {"type":"flow","nodes":[{"id":"a","label":"Draft","col":0},{"id":"b","label":"Review","col":1},{"id":"c","label":"Live","col":2}],"edges":[{"from":"a","to":"b","label":"Submit"},{"from":"b","to":"c","label":"Publish"},{"from":"b","to":"a","label":"Reject"},{"from":"c","to":"a","label":"Unpublish"}]}, "flow: two backward edges on one row"),
 cz("diagram", {"type":"flow","nodes":[{"id":"a","label":"Sign up","col":0},{"id":"b","label":"Connect bank","col":1,"note":"71% finish, was 48%"},{"id":"c","label":"First invoice","col":2},{"id":"d","label":"Ledger","col":1,"row":1,"kind":"store"}],"edges":[{"from":"a","to":"b"},{"from":"b","to":"c"},{"from":"b","to":"d","label":"Sync"}]}, "flow: note on a node with a wire below"),
 cz("diagram", {"type":"layers","layers":[{"label":"Clients","items":["Web","iOS","Android","Partner API"]},{"label":"Services","items":["Gateway","Orders","Payments","Inventory","Notifications","Search"]},{"label":"Data","items":["Postgres","Queue","Object storage"]}]}, "layers: six items in a row"),
 cz("diagram", {"type":"tree","root":{"label":"Revenue","children":[{"label":"New","children":[{"label":"Self serve"},{"label":"Sales led"},{"label":"Partner"}]},{"label":"Expansion","children":[{"label":"Seats"},{"label":"Usage"},{"label":"Add-ons"}]},{"label":"Renewal","children":[{"label":"Annual"},{"label":"Monthly"}]}]}}, "tree: eight leaves"),
 cz("diagram", {"type":"timeline","columns":["Jul","Aug","Sep","Oct","Nov","Dec"],"now":2.4,"rows":[{"label":"Approval flows","from":3.2,"to":5.6,"note":"Agency request","accent":True},{"label":"Bank feeds","from":0,"to":2.4,"note":"Shipped"},{"label":"Launch","at":5.8,"note":"12 Dec","accent":True}]}, "timeline: notes near the right edge"),
 cz("diagram", {"type":"quadrant","x":["Low effort","High effort"],"y":["Low impact","High impact"],"corners":["Do now","Plan","Skip","Avoid"],"items":[{"label":"Top right corner","x":1,"y":1},{"label":"Origin","x":0,"y":0},{"label":"Far right","x":0.98,"y":0.5,"accent":True},{"label":"On the midline","x":0.3,"y":0.5}]}, "quadrant: points on the edges and the midline"),
 cz("diagram", {"type":"sequence","actors":[{"id":"u","label":"Browser"},{"id":"a","label":"App"},{"id":"i","label":"Identity"}],"messages":[{"from":"u","to":"a","label":"Sign in"},{"from":"a","to":"i","label":"Redirect with challenge","accent":True},{"from":"i","to":"i","label":"Verify"},{"from":"i","to":"a","label":"Code","reply":True}]}, "sequence"),
 cz("chart", {"type":"bar","labels":["Q1","Q2","Q3","Q4"],"highlight":"Pro","series":[{"name":"Free","values":[4,5,7,9]},{"name":"Pro","values":[3,4,8,12]},{"name":"Team plan with a long name","values":[2,2,3,10]},{"name":"Resellers","values":[1,2,2,3]}],"height":220}, "grouped bar: long legend, highlight"),
 cz("chart", {"type":"hbar","stacked":True,"labels":["Enterprise accounts in North America","Europe"],"series":[{"name":"New business","values":[52,44]},{"name":"Expansion of existing accounts","values":[28,31]},{"name":"Renewals","values":[20,25]}],"suffix":"%"}, "stacked hbar: long labels and legend"),
 cz("chart", {"type":"line","labels":months,"series":[{"name":"Account","values":[620,640,610,580,571,540,498,470,455,430,449,449]},{"name":"Checkout","values":[610,605,622,598,580,576,551,540,521,514,403,410]}],"suffix":" ms","height":240}, "line: two series ending close together"),
 cz("chart", {"type":"scatter","x":"Latency","y":"Hit rate","xAxis":{"suffix":" ms"},"suffix":"%","series":[{"name":"p","points":[{"x":40,"y":96,"label":"Tokyo"},{"x":120,"y":91,"label":"Frankfurt"},{"x":410,"y":72,"label":"Edge cache hit","accent":True},{"x":300,"y":80}]}],"height":240}, "scatter: label near the right edge"),
 cz("chart", {"type":"waterfall","suffix":"k","prefix":"$","data":[{"label":"2025","value":820,"total":True},{"label":"New","value":310},{"label":"Churn","value":-95},{"label":"2026","total":True}],"height":220}, "waterfall"),
 cz("chart", {"type":"heatmap","rows":["Mon","Tue","Wed"],"cols":["00","06","12","18"],"values":[[2,4,31,19],[3,5,34,21],[2,6,36,22]]}, "heatmap"),
]
page("fixtures.html", "Fixtures", "FIXTURES", "", f"""<main>
  <header><div class="meta">canzano // test fixtures</div><h1>The cases that have broken before</h1></header>
  {''.join('<section>' + f + '</section>' for f in F)}
  <section><h2>Controls</h2>
    <div class="row" id="row">
      <div class="segmented" role="group" aria-label="Range"><button aria-pressed="true">Day</button><button aria-pressed="false">Week</button></div>
      <input type="search" class="w-m" placeholder="Service" aria-label="Service">
      <select class="w-s" aria-label="Region"><option>All regions</option></select>
      <label class="check"><input type="checkbox" checked>Failed only</label>
      <button class="primary push">Deploy</button>
    </div>
    <div class="row sm" id="row-sm" style="margin-top:12px"><button>Small</button><input class="w-s" aria-label="Small input"><select class="w-s" aria-label="s"><option>Small</option></select></div>
    <div class="row" style="margin-top:12px">
      <div class="joined stepper" id="stepper"><button aria-label="Fewer">-</button><input value="12" aria-label="Seats"><button aria-label="More">+</button></div>
      <div class="joined" id="search"><input type="search" placeholder="Search" aria-label="Search"><button>Search</button></div>
      <label class="affix w-s" id="affix"><span>$</span><input value="240" aria-label="Cost"><span>/ mo</span></label>
      <label class="check"><input type="checkbox" class="switch" checked>Notify</label>
    </div>
    <form class="form" style="margin-top:16px" onsubmit="return false">
      <div class="field"><label for="fx-email">Email</label><input id="fx-email" class="w-l" value="lena@" aria-invalid="true"><span class="error">Enter a full email address.</span></div>
      <div class="field"><label for="fx-name">Name</label><input id="fx-name" value="Lena Brandt"></div>
      <div class="stack" role="radiogroup" aria-label="Billing"><label class="check"><input type="radio" name="b" checked><span>Monthly<small>Cancel any time</small></span></label><label class="check"><input type="radio" name="b"><span>Yearly<small>Two months free</small></span></label></div>
      <div class="actions"><button class="primary" id="fx-save">Save</button><button type="button">Cancel</button><button type="button" class="danger" id="fx-danger">Delete</button></div>
    </form>
    <div style="position:relative;height:110px;margin-top:16px"><div class="menu" id="menu"><button>Rename</button><a href="#">Open in new tab</a><button class="danger">Delete</button></div></div>
  </section>
  <section><h2>Rows and figures</h2>
    <div class="table-wrap"><table id="sel"><thead><tr><th></th><th>Name</th><th>Owner</th><th class="num">Seats</th><th class="num">Cost</th></tr></thead><tbody><tr aria-selected="true"><td class="mark">→</td><td>Team</td><td>L. Brandt</td><td class="num">12</td><td class="num">$240</td></tr><tr aria-selected="false"><td class="mark">→</td><td>Scale</td><td>M. Okafor</td><td class="num">80</td><td class="num">$1,400</td></tr></tbody></table></div>
    <div class="metrics" id="metrics"><div><span class="label">Net revenue retention across all plans</span><span class="figure">118%</span></div><div><span class="label">ARR</span><span class="figure accent">$4.2M</span></div><div><span class="label">Churn</span><span class="figure">1.9%</span></div></div>
    <ul class="ledger"><li><span>A ledger row with a fairly long label on it</span><span>2</span></li><li><span>Status</span><span class="positive">PASSED</span></li></ul>
    <ul class="ledger settings"><li><span>Failed deploys<small>Email the author</small></span><span><input type="checkbox" class="switch" checked aria-label="Failed deploys"></span></li></ul>
    <p id="emph">Bold <b>b</b> and <strong>strong</strong> and <em>italic</em>. <code>code <b>bold</b> <em>em</em></code>. A trend <span id="sp1"></span> and one point <span id="sp2"></span>.</p>
    <figure class="diagram"><svg class="dg" viewBox="0 0 900 80" width="900" id="hand"><rect class="s" x="0.5" y="0.5" width="899" height="79"/><text x="450" y="44" text-anchor="middle">HAND DRAWN, 900 WIDE</text></svg></figure>
  </section>
</main>""", """
cz.spark('#sp1', [3, 5, 4, 8]); cz.spark('#sp2', [5]);
window.__assert = function () {
  var bad = [], q = function (s) { return document.querySelector(s) }, all = function (s) { return [].slice.call(document.querySelectorAll(s)) }, cs = getComputedStyle, phone = innerWidth <= 640;
  function ok(cond, msg) { if (!cond) bad.push(msg) }
  function hs(sel) { return all(sel).map(function (e) { return Math.round(e.getBoundingClientRect().height * 10) / 10 }) }
  function same(a) { return a.every(function (v) { return Math.abs(v - a[0]) < 0.6 }) }
  var rowH = hs('#row > .segmented, #row > input, #row > select, #row > button');
  ok(same(rowH) && Math.abs(rowH[0] - 27) < 0.6, 'row controls are not all 27px: ' + rowH);
  ok(same(hs('#row-sm > *')) && Math.abs(hs('#row-sm > *')[0] - 23) < 0.6, '.sm row is not all 23px: ' + hs('#row-sm > *'));
  var st = all('#stepper > *');
  ok(Math.abs(st[0].getBoundingClientRect().width - st[2].getBoundingClientRect().width) < 0.6, 'stepper buttons differ in width');
  ok(cs(st[0]).borderRadius === '6px 0px 0px 6px' && cs(st[1]).borderRadius === '0px' && cs(st[2]).borderRadius === '0px 6px 6px 0px', 'stepper corners: ' + st.map(function (e) { return cs(e).borderRadius }).join(' | '));
  ok(cs(all('#search > *')[0]).borderRadius === '6px 0px 0px 6px', 'joined search input corners: ' + cs(all('#search > *')[0]).borderRadius);
  ok(Math.abs(q('#fx-email').getBoundingClientRect().width - Math.min(320, q('#fx-email').parentElement.clientWidth)) < 1, 'input.w-l in a field is ' + q('#fx-email').getBoundingClientRect().width + 'px');
  ok(q('#fx-name').getBoundingClientRect().width > 330 || phone, 'a plain input in a field should fill it');
  var want = phone ? '16px' : '14px', fonts = ['#row input', '#row select', '#row button.primary', '#row .check'].map(function (s) { return cs(q(s)).fontSize });
  ok(fonts.every(function (f) { return f === want }), 'row control text should all be ' + want + ': ' + fonts);
  ok(cs(q('#row-sm button')).fontSize === (phone ? '16px' : '13px'), '.sm button text is ' + cs(q('#row-sm button')).fontSize);
  ok(cs(q('#menu .danger')).color === cs(q('#fx-danger')).color && cs(q('#fx-danger')).color !== cs(q('#fx-save')).color, 'menu danger item is not the danger colour');
  ok(same(hs('#menu > *')), 'menu items differ in height: ' + hs('#menu > *'));
  var cells = all('#sel tbody tr').map(function (r) { return cs(r.children[1]).color }), marks = all('#sel td.mark').map(function (m) { return cs(m).color });
  ok(cells[0] !== cells[1], 'selected and unselected rows have the same ink');
  ok(marks[0] !== marks[1], 'the row mark shows on unselected rows');
  var rows = {}; all('#metrics > div').forEach(function (d) { var k = Math.round(d.getBoundingClientRect().top); (rows[k] = rows[k] || []).push(Math.round(d.querySelector('.figure').getBoundingClientRect().top)); });
  Object.keys(rows).forEach(function (k) { ok(same(rows[k]), 'metric figures in one row are not on one baseline: ' + rows[k]); });
  ok(cs(q('#metrics .figure.accent')).color !== cs(q('#metrics .figure')).color, '.accent does not colour a metric figure');
  ok(cs(q('#emph b')).fontWeight === '600' && cs(q('#emph code b')).fontWeight === '500' && cs(q('#emph code em')).fontStyle === 'normal', 'bold or italic asks for a face that is not loaded');
  ok(Math.abs(q('#hand').getBoundingClientRect().width - 900) < 1, 'hand-drawn diagram is ' + q('#hand').getBoundingClientRect().width + 'px wide, not 900');
  ok(q('#sp2 svg') && !/NaN/.test(q('#sp2').innerHTML), 'one-value sparkline has NaN');
  all('svg.cz').forEach(function (v, i) { var t = v.querySelector('text'); if (!t) return; var px = parseFloat(cs(t).fontSize) * v.clientWidth / v.viewBox.baseVal.width; ok(px >= 9.9, 'drawing ' + i + ' labels render at ' + px.toFixed(1) + 'px'); });
  ok(document.fonts.check('12px "Geist Mono"') && document.fonts.check('12px Inter'), 'the web fonts did not load');
  all('svg.cz text').forEach(function (t) { var b = t.getBBox(), vb = t.ownerSVGElement.viewBox.baseVal; if (t.getAttribute('transform')) return; ok(b.x >= -1 && b.x + b.width <= vb.width + 1 && b.y >= -2 && b.y + b.height <= vb.height + 3, 'label leaves its drawing: ' + t.textContent); });
  return bad;
};
""", viz=True, dest=root/"tests")

# Colour helper shared by the fixture assertions: contrast of an element's text against the page.
CONTRAST_JS = """
function __rgb(c) { var x = document.createElement('canvas'); x.width = x.height = 1; var g = x.getContext('2d'); g.fillStyle = c; g.fillRect(0, 0, 1, 1); return g.getImageData(0, 0, 1, 1).data; }
function __lum(c) { var d = __rgb(c), f = function (v) { v /= 255; return v <= 0.04045 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4) }; return 0.2126 * f(d[0]) + 0.7152 * f(d[1]) + 0.0722 * f(d[2]); }
function __contrast(el) { var a = __lum(getComputedStyle(el).color), b = __lum(getComputedStyle(document.body).backgroundColor); return (Math.max(a, b) + 0.05) / (Math.min(a, b) + 0.05); }
"""

page("fixtures-ui.html", "UI fixtures", "UI FIXTURES", """
.fx-page { border-radius: 3px; }   /* a page-level rule: it must beat the layered .joined rule without !important */
""", f"""<div class="shell">
  <aside>
    <span class="label" style="color:var(--ink)">Acme // Keys</span>
    <nav class="nav"><a href="#" aria-current="page">Keys</a><a href="#">Usage</a><a href="#">Settings</a></nav>
  </aside>
  <main>
    <div class="head"><h1>API keys</h1><button class="primary">Create key</button></div>
    <div class="panels"><div class="panel"><span class="label">Active</span><span class="figure">6</span></div><div class="panel"><span class="label">Calls today</span><span class="figure accent">18,204</span></div><div class="panel"><span class="label">Errors</span><span class="figure">12</span></div></div>
    <div class="row" style="margin:16px 0">
      <div class="segmented" role="group" aria-label="State"><button aria-pressed="true">Active</button><button aria-pressed="false">Revoked</button></div>
      <input type="search" class="w-s" id="ws" placeholder="Name" aria-label="Name">
      <div class="joined"><input class="fx-page" id="pagewin" aria-label="Prefix" value="sk_"><button>Copy</button></div>
    </div>
    <div class="table-wrap"><table>
      <thead><tr><th>Name</th><th>Prefix</th><th>Created</th><th>Last used</th><th>Scope</th><th>Status</th><th class="num">Calls</th></tr></thead>
      <tbody>
        <tr><td>Production server</td><td class="num">sk_live_9f2a</td><td>4 Nov 2026</td><td>2 minutes ago</td><td>Read and write</td><td><span class="status positive" id="st-pos">Active</span></td><td class="num">14,902</td></tr>
        <tr><td>Staging</td><td class="num">sk_test_41bc</td><td>12 Oct 2026</td><td>Yesterday</td><td>Read and write</td><td><span class="status warning" id="st-warn">Expires soon</span></td><td class="num">3,120</td></tr>
        <tr><td>Old laptop</td><td class="num">sk_live_07de</td><td>2 Feb 2026</td><td>Never</td><td>Read only</td><td><span class="status negative" id="st-neg">Revoked</span></td><td class="num">0</td></tr>
        <tr><td>Reporting job</td><td class="num">sk_live_c3a1</td><td>9 Sep 2026</td><td>1 hour ago</td><td>Read only</td><td><span class="status info" id="st-info">Rotating</span></td><td class="num">182</td></tr>
      </tbody>
    </table></div>
    <ul class="ledger settings" style="margin-top:16px"><li><span>Alert on errors<small>Email the owner</small></span><span><input type="checkbox" class="switch" checked aria-label="Alert on errors"></span></li></ul>
    <div style="position:relative;height:110px;margin-top:16px"><div class="menu" id="menu"><button>Rename</button><button>Duplicate</button><button class="danger">Revoke</button></div></div>
    <p><span class="accent" id="st-acc">Accent text</span></p>
    <figure class="diagram"><svg class="dg" id="bad" viewBox="0 0 300 90" width="300"><text x="10" y="30">OVERLAPPING</text><text x="14" y="33">LABELS</text><path class="s" d="M0 70.5 H300"/><text x="100" y="74">STRUCK</text></svg></figure>
    <div class="actionbar" id="actionbar"><button class="primary">Create key</button><button>Import</button></div>
    <nav class="tabbar" id="tabbar"><a href="#" aria-current="page">Keys</a><a href="#">Usage</a><a href="#">Settings</a></nav>
  </main>
</div>""", CONTRAST_JS + """
window.__lintOk = ['label-overlap', 'label-struck'];      // the deliberately bad hand-drawn svg below must be reported
window.__assert = function () {
  var bad = [], q = function (s) { return document.querySelector(s) }, cs = getComputedStyle, w = innerWidth;
  function ok(cond, msg) { if (!cond) bad.push(msg) }
  var found = cz.lint().map(function (f) { return f.issue });
  ok(found.indexOf('label-overlap') > -1 && found.indexOf('label-struck') > -1, 'lint misses overlapping or struck labels in a hand-drawn svg.dg: ' + found);
  ok(cs(q('#pagewin')).borderTopLeftRadius === '3px', 'a page-level rule does not beat the layered component: radius ' + cs(q('#pagewin')).borderTopLeftRadius);
  ok(Math.abs(q('#ws').getBoundingClientRect().width - 120) < 1, 'the .w-s helper does not beat .row > input: ' + q('#ws').getBoundingClientRect().width);
  ['#st-pos', '#st-warn', '#st-neg', '#st-info', '#st-acc'].forEach(function (s) { var c = __contrast(q(s)); ok(c >= 4.5, s + ' text contrast is ' + c.toFixed(2) + ', under 4.5'); });
  var items = [].slice.call(document.querySelectorAll('#menu > *'));
  q('#menu').scrollIntoView({ block: 'center' });       // elementFromPoint only sees what is in the viewport
  items.forEach(function (it, i) { var r = it.getBoundingClientRect(), hit = document.elementFromPoint(r.left + r.width / 2, r.bottom - 2); ok(hit === it, 'the bottom edge of menu item ' + (i + 1) + ' belongs to another element'); });
  var phone = w <= 800, shown = function (s) { return cs(q(s)).display !== 'none' };
  ok(shown('#tabbar') === phone && shown('#actionbar') === phone, 'tab bar and action bar should show only at 800px and under (width ' + w + ')');
  ok(phone ? cs(q('.shell > aside')).position === 'static' : cs(q('.shell > aside')).position === 'sticky', 'the aside did not switch for width ' + w);
  return bad;
};
""", ui=True, dest=root/"tests")

page("fixtures-deck.html", "Deck fixtures", "", "", f"""<div class="deck" data-label="Deck fixtures">
  <section class="slide split" id="small">
    <h2>A split slide whose drawing is too small</h2>
    <div class="body"><div><p class="lead">The lint must report this one.</p></div>
      {cz("diagram", {"type":"flow","nodes":[{"id":"a","label":"A","col":0},{"id":"b","label":"B","col":1}],"edges":[{"from":"a","to":"b"}],"cell":{"w":60,"h":30}})}
    </div>
  </section>
  <section class="slide split" id="fine">
    <h2>A split slide whose drawing fills its column</h2>
    <div class="body"><div><p class="lead">This one is fine.</p></div>
      {cz("diagram", {"type":"flow","nodes":[{"id":"a","label":"Input","col":0},{"id":"b","label":"Step","col":1},{"id":"c","label":"Output","col":2},{"id":"s","label":"Store","col":1,"row":1,"kind":"store"},{"id":"l","label":"Log","col":2,"row":1,"kind":"store"}],"edges":[{"from":"a","to":"b","label":"raw","accent":True},{"from":"b","to":"c","label":"clean"},{"from":"b","to":"s"},{"from":"c","to":"l"}]})}
    </div>
  </section>
  <section class="slide title"><h1>Edge caching halved checkout latency in six weeks</h1><p>A 49-character title</p></section>
  <section class="slide"><h2>A chart with no height fills the slide body</h2><div class="body">{cz("chart", {"type":"bar","highlight":"Q4","data":[{"label":"Q1","value":120},{"label":"Q2","value":160},{"label":"Q3","value":210},{"label":"Q4","value":340}]})}</div></section>
</div>""", """
window.__lintOk = ['small-graphic'];
window.__assert = function () {
  var bad = [], q = function (s) { return document.querySelector(s) };
  function ok(cond, msg) { if (!cond) bad.push(msg) }
  var small = cz.lint(q('#small')), fine = cz.lint(q('#fine'));
  ok(small.some(function (f) { return f.issue === 'small-graphic' }), 'lint does not report a small drawing on a split slide');
  ok(!fine.some(function (f) { return f.issue === 'small-graphic' }), 'lint reports a drawing that fills its column: ' + JSON.stringify(fine));
  var h1 = q('.title h1'), r = document.createRange(); r.selectNodeContents(h1);
  var lines = []; [].forEach.call(r.getClientRects(), function (x) { var t = Math.round(x.top); if (lines.indexOf(t) < 0) lines.push(t) });
  ok(lines.length === 2, 'a 49-character title wraps to ' + lines.length + ' lines, not 2');
  var svg = document.querySelectorAll('.slide')[3].querySelector('svg.cz'), body = svg.closest('.body');
  ok(svg.getBoundingClientRect().height > 0.8 * body.getBoundingClientRect().height, 'a chart with no height does not fill its slide body');
  var h2 = q('#fine h2'), gap = q('#fine .body').getBoundingClientRect().top - h2.getBoundingClientRect().bottom, z = q('#fine').getBoundingClientRect().width / 1280;
  ok(gap / z > 40, 'the headline sits ' + Math.round(gap / z) + 'px above the body, under 40');
  return bad;
};
""", viz=True, deck=True, dest=root/"tests")
print("built", sorted(p.name for p in out.glob("*.html")), "+ tests/fixtures*.html")
