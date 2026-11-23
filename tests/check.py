#!/usr/bin/env python3
"""Check for the canzano skill. Run it before a release:

    python3 tests/check.py

It checks the files against each other, renders the template and the examples at phone and desktop
width in both themes in headless Chrome, and prints the report and the slides. It exits non-zero on
any finding. Set CHROME to the browser binary if it is not in a usual place; --static skips the browser.
"""
import glob, json, os, pathlib, re, shutil, subprocess, sys, tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKILL = ROOT / "plugin" / "skills" / "canzano"
PAGES = ["assets/template.html", "examples/ui.html", "examples/chart.html", "examples/slides.html"]
fails = []

def fail(where, what):
    fails.append((where, what))

def chrome():
    for c in [os.environ.get("CHROME"), "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
              "/Applications/Chromium.app/Contents/MacOS/Chromium", shutil.which("google-chrome"),
              shutil.which("chromium"), shutil.which("chromium-browser")] + sorted(glob.glob("/opt/pw-browsers/chromium*/chrome-linux*/chrome")):
        if c and os.path.isfile(c) and os.access(c, os.X_OK):
            return c

def static():
    # The three dark token blocks are the same.
    t = (SKILL / "assets/tokens.css").read_text()
    blocks = [re.sub(r"\s+", " ", b).strip() for b in re.findall(r"(?:not\(\[data-theme=\"light\"\]\)|\[data-theme=\"dark\"\](?:\.keep-theme)?) \{(.*?)\n\s*\}", t, re.S)]
    if len(blocks) != 3 or len(set(blocks)) != 1:
        fail("tokens.css", f"expected 3 identical dark blocks, found {len(blocks)} with {len(set(blocks))} variants")

    # The palette on disk is what the generator makes.
    pal = SKILL / "assets/palette.css"; before = pal.read_text()
    subprocess.run([sys.executable, "-B", str(ROOT / "tools/palette.py")], capture_output=True)
    if pal.read_text() != before:
        fail("palette.css", "differs from what tools/palette.py generates"); pal.write_text(before)

    # Every class, token and file the guides name exists, and every class the pages use is defined.
    css = "".join(p.read_text() for p in sorted(SKILL.rglob("*.css")))
    html = "".join((SKILL / p).read_text() for p in PAGES)
    defined = set(re.findall(r"\.([a-z][a-z0-9-]*)", css + "".join(re.findall(r"<style>(.*?)</style>", html, re.S))))
    for d in [SKILL / "SKILL.md"] + sorted(SKILL.glob("references/*.md")):
        name = str(d.relative_to(SKILL))
        for tok in set(re.findall(r"`([^`\n]+)`", re.sub(r"```.*?```", "", d.read_text(), flags=re.S))):
            for cls in re.findall(r"(?<![\w/.-])\.([a-z][a-z0-9-]*)\b", tok):
                if cls not in defined and cls not in ("md", "css", "html", "sh", "pdf"):
                    fail(name, f"names class .{cls}, which no stylesheet defines")
            for var in re.findall(r"(--[a-z][a-z0-9-]*)", tok):
                if var + ":" not in css and not re.match(r"--(series|grey|red|orange|amber|yellow|lime|green|sky|blue|violet|purple|pink)-(N|\d)", var):
                    fail(name, f"names token {var}, which is not defined")
            m = re.fullmatch(r"((?:assets|references|scripts|examples)/[\w./-]+\.\w+)", tok)
            if m and not (SKILL / m.group(1)).exists():
                fail(name, f"points at {m.group(1)}, which does not exist")
    for p in PAGES:
        for classes in re.findall(r'class="([^"]+)"', (SKILL / p).read_text()):
            for cls in classes.split():
                if cls not in defined: fail(p, f"uses class {cls}, which no stylesheet defines")

    # The installer keeps the copy it replaces, without leaving a second SKILL.md.
    with tempfile.TemporaryDirectory() as tmp:
        target = pathlib.Path(tmp) / "my skills"
        for _ in range(2):
            r = subprocess.run(["sh", str(ROOT / "install.sh"), str(target)], capture_output=True, text=True)
            if r.returncode: fail("install.sh", r.stderr.strip() or "failed")
        if not (target / "canzano/SKILL.md").exists() or not (target / "canzano.previous").exists(): fail("install.sh", "did not install or did not keep the previous copy")
        if (target / "canzano.previous/SKILL.md").exists(): fail("install.sh", "the kept copy still has a SKILL.md")

def render(c):
    for p in PAGES:
        for w, theme in ((390, "light"), (390, "dark"), (760, "light"), (1100, "light"), (1100, "dark")):
            url = (ROOT / "tests/harness.html").as_uri() + f"?w={w}&theme={theme}&src=" + (SKILL / p).as_uri()
            where = f"{p} @{w} {theme}"
            with tempfile.TemporaryDirectory() as prof:
                try:
                    r = subprocess.run([c, f"--user-data-dir={prof}", "--headless=new", "--disable-gpu", "--no-first-run", "--no-sandbox",
                                        "--allow-file-access-from-files", f"--window-size={max(w, 500) + 20},1000", "--virtual-time-budget=9000",
                                        "--timeout=12000", "--dump-dom", url], capture_output=True, text=True, timeout=90)
                except subprocess.TimeoutExpired:
                    fail(where, "Chrome timed out"); continue
            m = re.search(r"<title>RESULT (.*?)</title>", r.stdout, re.S)
            if not m: fail(where, "no result from the page"); continue
            res = json.loads(m.group(1).replace("&quot;", '"'))
            if res["overflow"]: fail(where, f"page is {res['overflow']}px wider than the window")
            print(f"  rendered {where}")

def printing(c):
    env = dict(os.environ, CHROME=c)
    with tempfile.TemporaryDirectory() as tmp:
        odd = pathlib.Path(tmp) / "my docs #1 50%"; shutil.copytree(SKILL, odd)      # an awkward path on purpose
        for p, want in (("assets/template.html", 1), ("examples/slides.html", None)):
            out = odd / "out.pdf"
            r = subprocess.run(["sh", str(odd / "scripts/pdf.sh"), str(odd / p), str(out)], capture_output=True, text=True, env=env, timeout=120)
            if r.returncode or not out.exists(): fail("pdf.sh " + p, (r.stderr or "no PDF written").strip()); continue
            pages = len(re.findall(rb"/Type\s*/Page[^s]", out.read_bytes()))
            want = want or len(re.findall(r'<section class="slide', (odd / p).read_text()))
            if pages != want: fail("pdf.sh " + p, f"{pages} pages, expected {want}")
            print(f"  printed {p}: {pages} pages")
        r = subprocess.run(["sh", str(SKILL / "scripts/pdf.sh"), str(SKILL / PAGES[0]), str(pathlib.Path(tmp) / "x.pdf")], capture_output=True, text=True, env=dict(os.environ, CHROME="/usr/bin/false"))
        if r.returncode == 0: fail("pdf.sh", "exits 0 when Chrome fails")

if __name__ == "__main__":
    print("static checks"); static()
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
