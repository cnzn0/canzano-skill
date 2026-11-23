#!/usr/bin/env python3
"""ASCII output that lines up: hero text, boxes, flows, sequences, tables, bars, sparklines, trees.

For READMEs, terminals, code comments, commit messages and any place an SVG cannot go.
Run it and paste the result into a fenced code block (or <pre class="ascii"> in HTML).

  ascii.py banner "SHIP IT" [--style block|half|shade|char] [--char #]
  ascii.py flow "Client -[POST]-> Gateway -> API -> [DB]" [--down]
  ascii.py seq "Browser->App: sign in" "App->Identity: redirect" "Identity-->App: code"
  ascii.py table "Plan | Seats | Price" "Team | 12 | $240" "Scale | 80 | $1,400"
  ascii.py bars "Search=41" "Direct=24" "Referral=17" [--width 32] [--unit %]
  ascii.py spark 3 5 4 8 12 9 15
  ascii.py tree < outline.txt        (indent with two spaces per level)
  ascii.py box "Title" "first line" "second line"
"""
import re, sys

FONT = {
 'A': [" ### ", "#   #", "#####", "#   #", "#   #"], 'B': ["#### ", "#   #", "#### ", "#   #", "#### "],
 'C': [" ####", "#    ", "#    ", "#    ", " ####"], 'D': ["#### ", "#   #", "#   #", "#   #", "#### "],
 'E': ["#####", "#    ", "#### ", "#    ", "#####"], 'F': ["#####", "#    ", "#### ", "#    ", "#    "],
 'G': [" ####", "#    ", "#  ##", "#   #", " ####"], 'H': ["#   #", "#   #", "#####", "#   #", "#   #"],
 'I': ["###", " # ", " # ", " # ", "###"],           'J': ["  ###", "    #", "    #", "#   #", " ### "],
 'K': ["#   #", "#  # ", "###  ", "#  # ", "#   #"], 'L': ["#    ", "#    ", "#    ", "#    ", "#####"],
 'M': ["#   #", "## ##", "# # #", "#   #", "#   #"], 'N': ["#   #", "##  #", "# # #", "#  ##", "#   #"],
 'O': [" ### ", "#   #", "#   #", "#   #", " ### "], 'P': ["#### ", "#   #", "#### ", "#    ", "#    "],
 'Q': [" ### ", "#   #", "# # #", "#  # ", " ## #"], 'R': ["#### ", "#   #", "#### ", "#  # ", "#   #"],
 'S': [" ####", "#    ", " ### ", "    #", "#### "], 'T': ["#####", "  #  ", "  #  ", "  #  ", "  #  "],
 'U': ["#   #", "#   #", "#   #", "#   #", " ### "], 'V': ["#   #", "#   #", "#   #", " # # ", "  #  "],
 'W': ["#   #", "#   #", "# # #", "## ##", "#   #"], 'X': ["#   #", " # # ", "  #  ", " # # ", "#   #"],
 'Y': ["#   #", " # # ", "  #  ", "  #  ", "  #  "], 'Z': ["#####", "   # ", "  #  ", " #   ", "#####"],
 '0': [" ### ", "#  ##", "# # #", "##  #", " ### "], '1': [" # ", "## ", " # ", " # ", "###"],
 '2': [" ### ", "#   #", "  ## ", " #   ", "#####"], '3': ["#### ", "    #", " ### ", "    #", "#### "],
 '4': ["#   #", "#   #", "#####", "    #", "    #"], '5': ["#####", "#    ", "#### ", "    #", "#### "],
 '6': [" ### ", "#    ", "#### ", "#   #", " ### "], '7': ["#####", "    #", "   # ", "  #  ", "  #  "],
 '8': [" ### ", "#   #", " ### ", "#   #", " ### "], '9': [" ### ", "#   #", " ####", "    #", " ### "],
 ' ': ["   "] * 5, '.': [" ", " ", " ", " ", "#"], ',': ["  ", "  ", "  ", " #", "# "], ':': [" ", "#", " ", "#", " "],
 '-': ["    ", "    ", "####", "    ", "    "], '+': ["     ", "  #  ", "#####", "  #  ", "     "],
 '/': ["    #", "   # ", "  #  ", " #   ", "#    "], '!': ["#", "#", "#", " ", "#"],
 '?': [" ### ", "#   #", "  ## ", "     ", "  #  "], '%': ["#   #", "   # ", "  #  ", " #   ", "#   #"],
 "'": ["#", "#", " ", " ", " "], '&': [" ##  ", "#  # ", " ## #", "#  # ", " ## #"], '>': ["#  ", " # ", "  #", " # ", "#  "],
}

def _pixels(text):
    rows = [""] * 5
    for ch in text.upper():
        g = FONT.get(ch, FONT['?'])
        for i in range(5):
            rows[i] += g[i] + " "
    return [r[:-1] for r in rows]

def banner(text, style="block", char="#"):
    """Hero text in a 5-row pixel font. block: full squares; half: three lines tall; shade: fades down; char: any character."""
    px = _pixels(text)
    if style == "half":
        px.append(" " * len(px[0])); out = []
        for i in range(0, 6, 2):
            out.append("".join("█" if a != " " and b != " " else "▀" if a != " " else "▄" if b != " " else " " for a, b in zip(px[i], px[i + 1])))
        return "\n".join(l.rstrip() for l in out)
    fills = {"block": ["██"] * 5, "shade": ["░░", "▒▒", "▓▓", "██", "██"], "char": [char * 2] * 5}[style]
    return "\n".join("".join(fills[i] if c != " " else "  " for c in row).rstrip() for i, row in enumerate(px))

def box(title, lines=(), width=None):
    lines = list(lines); inner = max([len(l) for l in lines] + [len(title) + 2, (width or 0) - 4])
    top = "┌─ " + title + " " + "─" * (inner - len(title) - 1) + "┐" if title else "┌" + "─" * (inner + 2) + "┐"
    return "\n".join([top] + ["│ " + l.ljust(inner) + " │" for l in lines] + ["└" + "─" * (inner + 2) + "┘"])

def _parse_flow(spec):
    parts = re.split(r"\s*(-\[[^\]]*\]->|-->|->)\s*", spec.strip()); nodes, labels = parts[0::2], []
    for arrow in parts[1::2]:
        m = re.match(r"-\[(.*)\]->", arrow); labels.append(m.group(1) if m else "")
    return nodes, labels

def flow(spec, down=False):
    """A chain of boxes. 'A -[label]-> B -> [Store]'. Square brackets around a name mark a store."""
    nodes, labels = _parse_flow(spec)
    if down:
        w = max(len(n) for n in nodes) + 4; out = []
        for i, n in enumerate(nodes):
            out += ["┌" + "─" * (w - 2) + "┐", "│" + n.center(w - 2) + "│", "└" + "─" * (w - 2) + "┘"]
            if i < len(labels):
                pad = " " * (w // 2)
                out += [pad + "│" + (" " + labels[i] if labels[i] else ""), pad + "▼"]
        return "\n".join(l.rstrip() for l in out)
    top = mid = bot = ""
    for i, n in enumerate(nodes):
        w = len(n) + 2
        top += "┌" + "─" * w + "┐"; mid += "│ " + n + " │"; bot += "└" + "─" * w + "┘"
        if i < len(labels):
            wire = "── " + labels[i] + " ──▶" if labels[i] else "────▶"
            top += " " * len(wire); mid += wire; bot += " " * len(wire)
    return "\n".join(l.rstrip() for l in (top, mid, bot))

def seq(messages):
    """Sequence diagram. 'A->B: text' is a call, 'B-->A: text' is a reply (dashed)."""
    msgs, actors = [], []
    for m in messages:
        g = re.match(r"\s*(.+?)\s*(-->|->)\s*(.+?)\s*(?::\s*(.*))?$", m)
        a, arrow, b, label = g.group(1), g.group(2), g.group(3), g.group(4) or ""
        for x in (a, b):
            if x not in actors: actors.append(x)
        msgs.append((a, b, label, arrow == "-->"))
    gap = max([len(m[2]) + 6 for m in msgs] + [len(a) + 6 for a in actors] + [16])
    col = {a: i * gap + gap // 2 for i, a in enumerate(actors)}; width = gap * len(actors)
    def blank():
        row = [" "] * width
        for a in actors: row[col[a]] = "│"
        return row
    def put(row, x, s):
        for i, ch in enumerate(s):
            if 0 <= x + i < width: row[x + i] = ch
    head = [[" "] * width for _ in range(3)]
    for a in actors:
        w = len(a) + 4; x = col[a] - w // 2
        put(head[0], x, "┌" + "─" * (w - 2) + "┐"); put(head[1], x, "│ " + a + " │"); put(head[2], x, "└" + "─" * (w - 2) + "┘")
        head[2][col[a]] = "┬"
    out = ["".join(r) for r in head]
    for a, b, label, reply in msgs:
        lab, arr = blank(), blank(); line = "┄" if reply else "─"
        if a == b:
            put(lab, col[a] + 2, label); put(arr, col[a] + 1, "◀─┐")
        else:
            lo, hi = sorted((col[a], col[b])); put(lab, lo + (hi - lo - len(label)) // 2 + 1, label)
            put(arr, lo + 1, line * (hi - lo - 1)); arr[hi - 1 if col[b] > col[a] else lo + 1] = "▶" if col[b] > col[a] else "◀"
        out += ["".join(lab), "".join(arr)]
    out.append("".join(blank()))
    return "\n".join(l.rstrip() for l in out)

def table(rows):
    """Aligned table. The first row is the header. Numbers align right."""
    rows = [[c.strip() for c in (r.split("|") if isinstance(r, str) else r)] for r in rows]
    n = max(len(r) for r in rows); rows = [r + [""] * (n - len(r)) for r in rows]
    w = [max(len(r[i]) for r in rows) for i in range(n)]
    num = [all(re.fullmatch(r"[-+$€£]?[\d,.]+\s?[%a-zA-Z/]*", r[i]) for r in rows[1:] if r[i]) for i in range(n)]
    fmt = lambda r: "  ".join(c.rjust(w[i]) if num[i] else c.ljust(w[i]) for i, c in enumerate(r)).rstrip()
    return "\n".join([fmt([c.upper() for c in rows[0]]), "  ".join("─" * x for x in w)] + [fmt(r) for r in rows[1:]])

def bars(pairs, width=32, unit=""):
    """Horizontal bars. pairs: [(label, value)] or ['label=value']."""
    pairs = [(p.split("=")[0].strip(), float(p.split("=")[1])) if isinstance(p, str) else p for p in pairs]
    top = max(v for _, v in pairs) or 1; lw = max(len(l) for l, _ in pairs); eighths = " ▏▎▍▌▋▊▉"; out = []
    for l, v in pairs:
        cells = v / top * width; full = int(cells); part = eighths[int((cells - full) * 8)]
        out.append(f"{l.ljust(lw)}  {'█' * full}{part if part != ' ' else ''} {v:g}{unit}")
    return "\n".join(out)

def spark(values):
    values = [float(v) for v in values]; lo, hi = min(values), max(values)
    return "".join("▁▂▃▄▅▆▇█"[min(7, int((v - lo) / ((hi - lo) or 1) * 8))] for v in values)

def tree(text):
    """Outline to a tree. Indent with two spaces per level."""
    items = [((len(l) - len(l.lstrip())) // 2, l.strip()) for l in text.splitlines() if l.strip()]; out = []
    for i, (d, name) in enumerate(items):
        if d == 0: out.append(name); continue
        last = lambda j, depth: not any(dd == depth for dd, _ in _until(items, j, depth))
        prefix = "".join("    " if last(i, k) else "│   " for k in range(1, d))
        out.append(prefix + ("└── " if last(i, d) else "├── ") + name)
    return "\n".join(out)

def _until(items, i, depth):
    for d, n in items[i + 1:]:
        if d < depth: return
        yield d, n

def main(argv):
    if len(argv) < 2 or argv[1] in ("-h", "--help"): print(__doc__); return
    cmd, args = argv[1], argv[2:]
    def opt(name, default=None):
        if name in args:
            i = args.index(name); v = args[i + 1]; del args[i:i + 2]; return v
        return default
    def flag(name):
        if name in args: args.remove(name); return True
        return False
    if cmd == "banner": style, char = opt("--style", "block"), opt("--char", "#"); print(banner(" ".join(args), style, char))
    elif cmd == "flow": down = flag("--down"); print(flow(" ".join(args), down))
    elif cmd == "seq": print(seq(args or sys.stdin.read().splitlines()))
    elif cmd == "table": print(table(args or sys.stdin.read().splitlines()))
    elif cmd == "bars": width, unit = int(opt("--width", 32)), opt("--unit", ""); print(bars(args, width, unit))
    elif cmd == "spark": print(spark(args))
    elif cmd == "tree": print(tree(sys.stdin.read()))
    elif cmd == "box": print(box(args[0] if args else "", args[1:]))
    else: print(__doc__)

if __name__ == "__main__":
    main(sys.argv)
