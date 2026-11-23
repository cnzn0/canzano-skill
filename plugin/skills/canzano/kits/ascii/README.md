# ASCII kit

Optional. Open this when the output is plain text.

For places an SVG cannot go: READMEs, terminals, code comments, commit messages, chat replies, plain-text email. Generate it with `kits/ascii/ascii.py`, which guarantees the columns line up. Hand-typed box drawings drift by a character and break.

```bash
python3 kits/ascii/ascii.py flow "Client -[POST]-> Gateway -> API -> [DB]"
python3 kits/ascii/ascii.py seq "Browser->App: sign in" "App-->Browser: 200"
python3 kits/ascii/ascii.py table "Plan | Seats | Price" "Team | 12 | $240"
python3 kits/ascii/ascii.py bars "Search=41" "Direct=24" --unit %
python3 kits/ascii/ascii.py spark 3 5 4 8 12 9 15
python3 kits/ascii/ascii.py tree < outline.txt
python3 kits/ascii/ascii.py box "Deploy" "api-gateway  a41f9c2"
python3 kits/ascii/ascii.py banner "SHIP IT" --style half
```

| Command | Gives |
|---|---|
| `flow` | A chain of boxes with labelled arrows. `--down` stacks it. `[Name]` marks a store |
| `seq` | A sequence diagram. `->` is a call, `-->` a dashed reply |
| `table` | An aligned table, header in caps, numbers right aligned |
| `bars` | Horizontal bars with eighth-block precision |
| `spark` | A one-line sparkline |
| `tree` | A tree from a two-space indented outline |
| `box` | A titled frame around lines |
| `banner` | Hero text in a 5-row pixel font: `block`, `half` (three lines tall), `shade`, or `char` with `--char` |

Put the output in a fenced code block in Markdown, or `<pre class="ascii">` in HTML (`<pre class="ascii hero">` for a banner, which scales with the page).

## Rules

- The same grammar as the SVG diagrams: boxes are entities, arrows have a real source and target, square brackets mark a store or a set. No decorative borders, no filler characters.
- `flow` draws one chain and cannot branch. Draw a branch as a second flow on its own line, or use `tree` when the shape is a hierarchy.
- Keep it under 100 columns so it survives a terminal and a code review. Use `--down` or split the diagram when a flow is wider.
- Hero text is opt-in: only when the user asks for a banner or a title treatment, once per output, and short (one to three words). It is never a substitute for stating the point, and a report or UI does not open with one.
- In an HTML page or a deck prefer the SVG diagrams from the charts kit. ASCII there is a deliberate choice of register, such as a terminal product or a developer README rendered as a page.
- Paste the script's output unchanged. If a label must change, rerun the script.
