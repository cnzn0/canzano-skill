#!/usr/bin/env python3
"""Regression check for the canzano skill. Run it before every release:

    python3 tests/check.py

It rebuilds the examples, checks the files against each other, renders the fixtures and every
example at phone and desktop width in headless Chrome, runs cz.lint() and the fixture assertions,
prints the deck and the report, and exits non-zero on any finding.
Set CHROME to the browser binary if it is not in a usual place. Use --static to skip the browser.
"""
import json, os, pathlib, re, shutil, subprocess, sys, tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKILL = ROOT / "plugin" / "skills" / "canzano"
fails = []

def fail(where, what):
    fails.append((where, what))

def chrome():
    for c in [os.environ.get("CHROME"), "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
              "/Applications/Chromium.app/Contents/MacOS/Chromium", shutil.which("google-chrome"),
              shutil.which("chromium"), shutil.which("chromium-browser"), "/opt/pw-browsers/chromium"]:
        if c and os.path.isfile(c) and os.access(c, os.X_OK):
            return c
    return None

# ---------------------------------------------------------------- static checks
def static():
    # 1. the three dark token blocks are the same
    t = (SKILL / "assets/tokens.css").read_text()
    blocks = [re.sub(r"\s+", " ", b).strip() for b in re.findall(r"(?:not\(\[data-theme=\"light\"\]\)|\[data-theme=\"dark\"\](?:\.keep-theme)?) \{(.*?)\n\s*\}", t, re.S)]
    if len(blocks) != 3 or len(set(blocks)) != 1:
        fail("tokens.css", f"expected 3 identical dark blocks, found {len(blocks)} with {len(set(blocks))} variants")

    # 2. scripts parse
    for js in ["assets/lint.js", "kits/charts/viz.js", "kits/decks/deck.js"]:
        r = subprocess.run(["node", "-e", f"new Function(require('fs').readFileSync({json.dumps(str(SKILL / js))},'utf8'))"], capture_output=True, text=True)
        if r.returncode: fail(js, "does not parse: " + r.stderr.strip().splitlines()[-1])
    for py in ["scripts/palette.py", "kits/ascii/ascii.py"]:
        r = subprocess.run([sys.executable, "-B", "-c", "import sys; compile(open(sys.argv[1]).read(), sys.argv[1], 'exec')", str(SKILL / py)], capture_output=True, text=True)
        if r.returncode: fail(py, "does not compile")

    # 3. the palette on disk is what the generator makes
    before = (SKILL / "assets/palette.css").read_text()
    subprocess.run([sys.executable, "-B", str(SKILL / "scripts/palette.py")], capture_output=True)
    if (SKILL / "assets/palette.css").read_text() != before:
        fail("palette.css", "differs from what scripts/palette.py generates"); (SKILL / "assets/palette.css").write_text(before)

    # 4. everything the docs name exists
    css = "".join(p.read_text() for p in SKILL.rglob("*.css"))
    markup = css + "".join(p.read_text() for p in list(SKILL.rglob("*.html")) + list(SKILL.rglob("*.js")))
    docs = [SKILL / "SKILL.md"] + sorted(SKILL.rglob("references/*.md")) + sorted(SKILL.rglob("kits/*/README.md"))
    for d in docs:
        text = d.read_text(); name = str(d.relative_to(SKILL))
        code = re.sub(r"```.*?```", "", text, flags=re.S)
        for tok in set(re.findall(r"`([^`\n]+)`", code)):
            for cls in re.findall(r"(?<![\w/.-])\.([a-z][a-z0-9-]*)\b", tok):
                if re.search(r"\.(md|css|js|html|py|sh|pdf|json|zip)$", "." + cls) or cls in ("md", "css", "js", "html", "py", "sh", "pdf", "json", "zip", "docx", "pptx", "claude"): continue
                if not re.search(r"\." + re.escape(cls) + r"(?![\w-])", css) and f'"{cls}' not in markup and f"'{cls}" not in markup:
                    fail(name, f"names class .{cls}, which no stylesheet defines")
            for var in re.findall(r"(--[a-z][a-z0-9-]*)", tok):
                if var + ":" not in css and not re.match(r"--(series|grey|red|orange|amber|yellow|lime|green|sky|blue|violet|purple|pink)-(N|\d)", var) and var not in ("--help", "--style", "--char", "--down", "--width", "--unit", "--core", "--static"):
                    fail(name, f"names token {var}, which is not defined")
            m = re.fullmatch(r"((?:assets|references|scripts|kits)/[\w./-]+\.\w+)", tok)
            if m and not (SKILL / m.group(1)).exists():
                fail(name, f"points at {m.group(1)}, which does not exist")
        for stale in ("references/charts.md", "references/decks.md", "references/ascii.md", "assets/viz.js", "assets/deck", "scripts/ascii.py"):
            if stale in text: fail(name, f"still mentions {stale}")

    # 5. the examples on disk are what the build makes
    snap = {p.name: p.read_text() for p in (ROOT / "examples").glob("*.html")}
    r = subprocess.run([sys.executable, "-B", str(ROOT / "build_examples.py")], capture_output=True, text=True)
    if r.returncode: fail("build_examples.py", r.stderr.strip().splitlines()[-1] if r.stderr.strip() else "failed")
    for p in (ROOT / "examples").glob("*.html"):
        if snap.get(p.name) != p.read_text(): fail("examples/" + p.name, "was out of date; rebuilt it, commit the result")

    # 6. no caches or tool folders are tracked inside the skill
    tracked = subprocess.run(["git", "-C", str(ROOT), "ls-files", "plugin"], capture_output=True, text=True).stdout.split()
    for f in tracked:
        if "__pycache__" in f or f.endswith((".pyc", ".DS_Store")) or "/.claude/" in f:
            fail(f, "should not be in the repository")

# ---------------------------------------------------------------- rendered checks
def render(c):
    pages = [ROOT / "tests/fixtures.html"] + sorted((ROOT / "examples").glob("*.html"))
    for page in pages:
        if page.name == "index.html": widths = [1100]          # the gallery frames other pages; they are checked on their own
        elif page.name == "deck.html": widths = [1312]          # a deck is for a screen, not a phone
        else: widths = [390, 1100]
        for w in widths:
            url = (ROOT / "tests/harness.html").as_uri() + f"?w={w}&src=" + page.as_uri()
            with tempfile.TemporaryDirectory() as prof:
                try:
                    r = subprocess.run([c, f"--user-data-dir={prof}", "--headless=new", "--disable-gpu", "--no-first-run", "--no-sandbox",
                                        "--allow-file-access-from-files", f"--window-size={max(w, 500) + 20},1000", "--virtual-time-budget=9000",
                                        "--timeout=12000", "--dump-dom", url], capture_output=True, text=True, timeout=90)
                except subprocess.TimeoutExpired:
                    fail(f"{page.name} @{w}", "Chrome timed out"); continue
            m = re.search(r"<title>RESULT (.*?)</title>", r.stdout, re.S)
            where = f"{page.name} @{w}"
            if not m: fail(where, "no result from the page"); continue
            res = json.loads(m.group(1).replace("&quot;", '"').replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">"))
            if res.get("error"): fail(where, res["error"]); continue
            if res["lint"] == "cz.lint missing": fail(where, "cz.lint is not loaded")
            else:
                for f in res["lint"]: fail(where, f"lint {f['issue']}: {f['text']}")
            for a in res["asserts"]: fail(where, a)
            if res["overflow"]: fail(where, f"page is {res['overflow']}px wider than the window")
            print(f"  rendered {where}")

def printing(c):
    env = dict(os.environ, CHROME=c)
    with tempfile.TemporaryDirectory() as tmp:
        for name, want in (("deck.html", None), ("report.html", (1, 2))):
            out = pathlib.Path(tmp) / (name + ".pdf")
            r = subprocess.run(["sh", str(SKILL / "scripts/pdf.sh"), str(ROOT / "examples" / name), str(out)], capture_output=True, text=True, env=env, timeout=120)
            if r.returncode or not out.exists(): fail("pdf.sh " + name, (r.stderr or "no PDF written").strip()); continue
            pages = len(re.findall(rb"/Type\s*/Page[^s]", out.read_bytes()))
            if want is None:
                slides = len(re.findall(r'<section class="slide', (ROOT / "examples" / name).read_text()))
                if pages != slides: fail("pdf.sh " + name, f"{pages} pages for {slides} slides")
            elif not want[0] <= pages <= want[1]: fail("pdf.sh " + name, f"{pages} pages, expected {want[0]} to {want[1]}")
            print(f"  printed {name}: {pages} pages")
        r = subprocess.run(["sh", str(SKILL / "scripts/pdf.sh"), str(ROOT / "examples/report.html"), str(pathlib.Path(tmp) / "x.pdf")], capture_output=True, text=True, env=dict(os.environ, CHROME="/usr/bin/false"))
        if r.returncode == 0: fail("pdf.sh", "exits 0 when Chrome fails")

def scripts():
    a = [sys.executable, "-B", str(SKILL / "kits/ascii/ascii.py")]
    good = [["banner", "OK", "--style", "half"], ["flow", "A -[x]-> B -> [C]"], ["flow", "A -> B", "--down"], ["seq", "A->B: hi", "B-->A: ok"],
            ["table", "a | b", "c | 1"], ["bars", "a=3", "b=1"], ["spark", "1", "2", "3"], ["box", "T", "line"]]
    bad = [["nope"], ["flow"], ["spark", "a"], ["bars", "x"], ["bars", "a=-1"], ["seq", "nonsense"], ["banner", "X", "--style", "nope"], ["banner", "a✓b"], ["box"], ["table", "a|b", "c"]]
    for g in good:
        r = subprocess.run(a + g, capture_output=True, text=True)
        if r.returncode or not r.stdout.strip(): fail("ascii.py " + " ".join(g), f"exit {r.returncode}")
        elif len({len(l) for l in r.stdout.splitlines() if l.startswith(("┌", "│", "└"))}) > 1 and g[0] in ("box",): fail("ascii.py " + g[0], "box lines differ in width")
    for b in bad:
        r = subprocess.run(a + b, capture_output=True, text=True, stdin=subprocess.DEVNULL)
        if r.returncode != 2 or len(r.stderr.strip().splitlines()) != 1: fail("ascii.py " + " ".join(b), f"expected exit 2 and one line, got exit {r.returncode} and {len(r.stderr.strip().splitlines())} lines")
    r = subprocess.run(a + ["tree"], input="Root\n  Leaf\n", capture_output=True, text=True)
    if "└── Leaf" not in r.stdout: fail("ascii.py tree", "did not draw the tree")
    with tempfile.TemporaryDirectory() as tmp:
        target = pathlib.Path(tmp) / "my skills"
        for _ in range(2):
            r = subprocess.run(["sh", str(ROOT / "install.sh"), str(target)], capture_output=True, text=True)
            if r.returncode: fail("install.sh", r.stderr.strip() or "failed")
        if not (target / "canzano/SKILL.md").exists() or not (target / "canzano.previous").exists(): fail("install.sh", "did not install or did not keep the previous copy")
        if list(target.rglob("__pycache__")): fail("install.sh", "copied a cache folder")

if __name__ == "__main__":
    print("static checks"); static()
    print("script checks"); scripts()
    if "--static" not in sys.argv:
        c = chrome()
        if not c: fail("chrome", "no Chrome found; set CHROME or pass --static")
        else:
            print("rendered checks"); render(c)
            print("print checks"); printing(c)
    if fails:
        print(f"\n{len(fails)} finding(s):")
        for where, what in fails: print(f"  {where}: {what}")
        sys.exit(1)
    print("\nall checks passed")
