# UIs

## Which case is it

- **An existing product.** Its tokens, components and platform conventions win. Do not bring these fonts, colours or square corners into it. Take only the judgment below. When a Figma component or reference is supplied, inspect it and match it instead of inventing a substitute.
- **A new tool, prototype or internal UI with no system.** Build it on `assets/palette.css`, `assets/tokens.css`, `assets/base.css` and `assets/ui.css`, with the recipe below.

## Judgment (both cases)

- **Restraint with precision.** Resolve alignment, spacing, type hierarchy and interaction before adding anything decorative. Minimal does not mean removing useful information.
- **Content leads.** The primary value or action is easy to find. Supporting labels and controls are sized to their real importance. Do not inflate a minor action into a card.
- **Density follows the task.** A working surface can be compact and information-rich. A single column usually beats a sidebar and tiles.
- **Coherent components.** Reuse the kit. When a problem repeats, fix the shared primitive, not the instance. Control sizes, radii, type and state treatments stay related.
- **Compact controls, separate touch reach.** The painted control stays small (27px high in this system, 34px for the main actions on a phone). The 44px touch target is an invisible hit area, added with a pseudo-element or wrapper, never by growing the fill, border or label. Hit areas must not overlap or clip. Check edge taps on the rendered result.
- **Clear state.** Selected and unselected must differ strongly: full ink on a raised thumb against a quiet ink step. Hover, focus, pressed, disabled, loading, empty and error all exist before it ships.
- **Native behaviour first.** Start from the platform's input, navigation and accessibility conventions. Custom behaviour needs a purpose and keeps exits, focus and gestures working.
- **Motion communicates.** Use it for response and spatial continuity. No entrance animations, compulsory staggers or bounce. Honour reduced motion.
- **Copy is lean.** Labels, numbers, actions. The interface does not explain itself. See the UI copy rules in `writing.md`.

## New UI on these tokens

The structure follows sfcompute.com (frame, small controls, flat panels), measured, not its brand.

- **Frame.** A sticky aside of about 224px with the name and the navigation, then one bordered main column. On a phone the aside becomes a top bar and the main actions sit above a bottom tab bar.
- **Type.** Inter leads: page title 26/32 at 500, panel title 20/26 at 600, body 15/22, controls and navigation 14/21 with +0.02em. Geist Mono caps at 11px for labels, table heads and status. Every figure is Geist Mono with tabular numerals.
- **Controls.** One recipe for every button, input, select and segmented control: 27px tall, radius 6, a 1px edge, Inter 14/21. Buttons and selects carry a four-stop fill that is lighter at the top, flat through the middle and slightly lighter at the bottom. One primary per view: ink with white text in light, white with dark text in dark, never the accent. `quiet` is text only. Hover shifts brightness, press scales to 0.97. No pill buttons, no outlined mono caps buttons.
- **Rows, combos and forms.** Read `controls.md`. Side-by-side controls go in `.row` and share one height and style. It also says which control fits which need and how a form is laid out, validated and closed.
- **Segmented control.** A `--panel` track the same height as a button. The selected segment is a raised thumb: white with a 1px soft shadow in light, a 12% light fill with a hairline edge in dark. It does not slide or spring. Never an accent border on a control.
- **Panels.** `--panel` fill, radius 12, 16px padding, no edge and no shadow. Use one for a figure with its label, a chart with its controls, or a detail view. Never nest panels and never wrap a whole table in one. Rows inside a panel divide with `--rule-strong`.
- **Lists and tables.** Hairline ledgers and tables on the page, as in documents. The selected row is full ink with a `→` mark.
- **Navigation.** Text links in `--ink-3`, the current one in `--ink`. No icons, no active pill.
- **Status.** One mono caps word in `--positive`, `--warning` or `--negative`. No coloured chips.
- **Accent.** The one live thing: the running item, the key figure, the current bar in a chart. Never a button fill.
- Design light and dark separately through the tokens and look at both.

## Before calling it done

Render it. Check the real thing at desktop and phone width, in both themes, with the keyboard, and with long and empty content. Report what was implemented, what was inspected and what is still unverified.
