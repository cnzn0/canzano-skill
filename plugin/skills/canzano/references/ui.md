# Interfaces

## Which case is it

- **An existing product.** Its tokens, components and platform conventions win. Do not bring these fonts, colours or corners into it; take only the judgment below. When a Figma component or reference is supplied, match it.
- **A new tool, prototype or internal UI with no system.** Build it on the three stylesheets with class `ui` on `<body>`. Start from `examples/ui.html`.

## Judgment

- **Content leads.** The primary value or action is easy to find. Do not inflate a minor action into a card. A single column usually beats a sidebar and tiles.
- **One recipe for every control.** 27px tall, radius 6, a 1px edge, Inter 14. Buttons and selects carry a fill that is a touch lighter at the top and bottom; inputs sit on the page colour. `base.css` does this; never restyle a control locally.
- **One primary per view.** Ink with white text on a light page, white with dark text on a dark page. Never the accent, never a colour. `quiet` is text only. `danger` is red text on a normal button, never a red fill.
- **Compact controls, separate touch reach.** The painted control stays small. The 44px touch target is an invisible hit area, never a bigger fill.
- **Clear state.** Selected and unselected differ strongly. Hover, focus, disabled, empty and error exist before it ships.
- **Panels.** A flat `--panel` fill, radius 12, no edge and no shadow, for a figure with its label or a chart. Never nest panels and never wrap a table in one.
- **Lists and tables.** Hairline tables and ledgers on the page, as in documents.
- **Status.** One mono caps word beside a small square in the status colour (`.status`). No chips.
- **Copy is lean.** Labels, numbers, actions. See the UI copy rules in `writing.md`.

## Parts

Everything is in `examples/ui.html`. Copy from it.

| Part | Markup |
|---|---|
| Navigation | `<nav class="nav">` with text links; the current one has `aria-current` |
| Page head | `.head` holding the `<h1>` and the one primary button |
| Figures | `.panels` of `.panel`, each a `.label` and a `.figure` |
| Controls side by side | `.row`. Every box shares one height. Add `.grow` to a search box that should take the room, `.push` to send the last control right |
| Segmented control | `.segmented` of buttons with `aria-pressed` |
| Input with its button | `.joined`: one shared edge, outer corners only |
| Table | `<table>` inside `.scroll`, numbers in `td.num` |
| Settings | `.ledger` rows: label and one line of `<small>` left, one switch or button right |
| Form | `.form` of `.field` (label, control, then one `.hint` or `.error`), closed by a `.row` of buttons |
| Sizes | `.sm` (23px) or `.lg` (34px) on a parent, never per control |

To hide something, use the `hidden` attribute. Give an input whose content has a known length a width in the page's own style.

## Which control

| Need | Control |
|---|---|
| 2 to 5 exclusive views, all visible | Segmented |
| 6 or more options, or long labels | Select |
| A yes or no saved with the form | Checkbox |
| A setting that applies the moment it is flipped | Switch (`input.switch`) |
| Free text with one action | `.joined` input and button |
| Something destructive | A `danger` button and a confirmation that names the object |

## Rows and forms

- In a row: view switches first, then filters, then the action. 8px between controls. A row never mixes sizes.
- A form is one column. Label above in mono caps, then the control, then at most one line: a hint or the error, never both.
- Placeholders are examples of the format, never the label.
- On error the field edge turns `--negative` and one sentence under it says what to fix. Wire it with `aria-invalid` and `aria-describedby`.
- The primary names the action ("Save", "Send invite"), not "Submit".
- On a phone every control's text steps up to 16px so the page does not zoom. Put the main actions in a `.lg` row.

## Before calling it done

Render it at desktop and phone width, in both themes. Check that every row of controls shares one height and style, that there is one primary in view, that nothing scrolls sideways, and that long and empty content hold. Say what was checked and what was not.
