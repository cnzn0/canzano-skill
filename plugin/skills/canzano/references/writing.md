# Words

These rules cover every word the agent produces: chat replies, reports, docs, captions and the copy inside a UI.

## Every text output

- The first line is the answer, the result or the decision. Evidence follows, then detail, and only as much as the reader needs to act.
- Length follows the question. A one-line question gets a one-line answer.
- Say each thing once. Do not repeat the heading in the first sentence, or the body in a summary.
- Use names and numbers, not adjectives. "Loads in 0.8 s", not "blazing fast".
- Plain words, short sentences. Headings are sentence case and say what the section holds.
- Say what was measured, what was inspected and what is still unverified. Never invent a figure to fill a layout.

Cut on sight:

- Openers: "Great question", "Sure", "Here is", "I have gone ahead and".
- Restating the ask before answering it.
- Signposts: "It is worth noting", "It is important to", "Additionally", "In summary", "Overall".
- Closers: recaps, "Let me know if", "I hope this helps", offers of more work nobody asked about.
- Stacked hedges: "might potentially", "could possibly". State the one real uncertainty once.
- Selling words: powerful, seamless, robust, comprehensive, elegant, effortless.
- Process narration when the result was asked for.
- Exclamation marks, emoji, slogans as headings, Title Case Headings.

## Wrapping

A heading, tagline or caption never ends with one short word alone on its last line, and a paragraph never ends on a stranded word.

- `base.css` balances headings, leads, captions and labels (`text-wrap: balance`) and tidies the last line of running text (`text-wrap: pretty`). Do not override it.
- Keep things together that read as one: a number and its unit (`0.88&nbsp;s`), a name and its number (`Fig&nbsp;1`), the last two words of a headline when the last is short. Use `&nbsp;`.
- A headline is two lines at most (a statement slide's single sentence may take four). If it runs over, cut words. Do not shrink the type or narrow the tracking to make it fit.
- Break a long title by sense when it must break: after the clause, not after "the", "of" or "a". Add `<br>` only when the balanced wrap still splits a phrase badly.
- No hyphenation in headings. No justified text.
- After rendering, load `assets/lint.js` and run `cz.lint()` in the page. It lists stranded last words, headlines over two lines, content that overflows a slide or the page, labels in a drawing that collide or are struck by a wire, and a drawing that fills under 30% of its slide. Fix every item it lists.

## UI copy

A UI is labels, numbers and actions. It does not explain itself.

Never write:

- A subtitle under the page title that says what the page is for.
- Helper text that restates the label, or a placeholder that repeats it.
- A section intro, a lede or a "Welcome back" line.
- A tooltip on a control whose label already says what it does.
- Instructions for the obvious: "Click the button below to", "Use the filters to".
- Footnotes, caveats and disclaimers that no law requires.
- A caption that describes what the reader can already see.
- An empty state longer than one line and one action.
- A success message longer than the name of the thing that happened: "Saved".
- "Learn more" links scattered through the interface.

Write:

- Buttons: a verb, one or two words. "Save", "Start run", "Roll back".
- Labels: the noun. "Name", not "Enter your name".
- Errors: what happened and the fix, in one sentence. "Card declined. Try another card."
- Confirmations for destructive actions: the object and the consequence. "Delete 3 files? This cannot be undone."
- Status: one word in mono caps next to the thing it describes.

The test: delete the sentence. If the screen still works, it stays deleted.

## Formal deliverables (reports, business documents, articles)

No em dashes, no semicolons, no contractions, no first or second person, no rhetorical questions, no exclamation marks, no idioms, no hype, no unsourced statistics, no filler openers.
