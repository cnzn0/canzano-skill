# Controls, combos and forms

Read this before placing two controls next to each other or building any form.

## One recipe

Every control is the same object in a different role: the same height (`--control-h`, 27px), 6px radius, 1px edge and Inter 14/21. Buttons and selects carry the subtle fill. Inputs sit on the page colour. A segmented control is a panel track of the same outer height. `base.css` already does this; do not restyle a control locally.

Sizes are set once on the parent, never per control: `.sm` 23px for dense tables and toolbars inside panels, default 27px, `.lg` 34px for the main actions on a phone. A row never mixes sizes.

## Rows

Put side-by-side controls in `.row`. Then check the rendered row:

- Every box has the same height and its text shares one baseline. A text link or a `.check` label in the row centres on the same line.
- 8px between controls of one group. 16 to 24px, or `.push`, between groups.
- One primary per row at most, and it sits at the end the eye reaches last: right in a toolbar, first in a form's action row.
- Order by scope: view switches (segmented), then filters (search, select, checkbox), then the action.
- Inputs get a width that fits their content (`.w-xs` 64, `.w-s` 120, `.w-m` 200, `.w-l` 320), not the leftover space. Only a search box that is the point of the row takes `.grow`.
- On a narrow screen the row wraps as whole controls. The primary keeps its place or goes full width in a `.lg` action bar. Controls never shrink below their label.

## Which control

| Need | Control |
|---|---|
| 2 to 5 exclusive views or modes, all visible | Segmented |
| 6 or more options, or long labels | Select |
| Exclusive options that need a line of explanation each | Radios, stacked |
| An independent yes or no saved with the form | Checkbox |
| A setting that applies the moment it is flipped | Switch |
| A number with a unit | `.affix` input with the unit inside, mono |
| A small integer | `.joined` stepper: minus, input, plus |
| Free text with one action | `.joined` input and button |
| A range of numbers or dates | Two inputs with an en dash between, same widths |
| Something destructive | A secondary button with `.danger` text, never a red fill, and a confirmation that names the object |

Do not use a select for two options, a segmented control for eight, a switch inside a form with a Save button, or a row of secondary buttons where one segmented control would do.

## Combos

- **Joined** (`.joined`): controls that act as one share a single edge and round only the outer corners. Use it for search and its button, a stepper, an input with a copy button. Do not join unrelated controls.
- **Affix** (`.affix`): a unit, currency or prefix lives inside the input's box. Units are mono caps in `--ink-3`.
- **Filter bar**: segmented, then search, then selects, then a `.check`, then the primary pushed right. Active filters show as the control's own value, not as extra chips.
- **Settings row**: a ledger row with the label and one line of detail on the left and a single control on the right (switch, select or button). One control per row.
- **Inline edit**: the value as text, a `quiet` button next to it. On edit, the text becomes an input of the same height with Save and Cancel in the same row.
- **Pagination and counts**: mono figures between two `quiet` buttons, `1–20 of 314`.

## Forms

- One column. Use `.pair` only for two short fields that belong together (first and last name, start and end).
- Label above in mono caps, then the control, then at most one line: a hint or the error, never both.
- Field width signals the expected answer: a postcode is `.w-s`, an email `.w-l`. Do not stretch every field to the form width out of habit.
- Group with a mono caps label and space, not with boxes. Put a form in a panel only when it sits beside other content.
- Mark the optional fields, not the required ones, when most are required.
- Placeholders are examples of the format, never the label and never instructions.
- Validate on blur and on submit, not on every keystroke. On error: the field edge turns `--negative`, one sentence under it says what to fix, focus moves to the first invalid field. Wire it with `aria-invalid` and `aria-describedby`.
- The action row closes the form: primary first, then Cancel, left aligned on a page. In a dialog the row is right aligned with the primary last. The primary names the action ("Save", "Send invite"), not "Submit".
- While saving, the primary takes `aria-busy="true"`: it keeps its width and shows a spinner. Nothing else on the form moves. After saving, say "Saved" once, next to the button.
- Disabled is for controls that cannot apply. A primary that is waiting on a missing field stays enabled and reports the error on click.
- Use the right input type and `autocomplete`, `inputmode` and `enterkeyhint`, so phones show the right keyboard. Enter submits a single-field form.
- Text is 16px in inputs on phones so the page does not zoom.

## Before calling a control group done

1. Do all boxes in each row share one height, radius and edge, in both themes?
2. Is there exactly one primary in view?
3. Does each input's width fit what goes in it?
4. Tab through it. Is the order the reading order, and is focus visible on every control?
5. Narrow the window. Does the row wrap cleanly, with nothing clipped or squeezed?
