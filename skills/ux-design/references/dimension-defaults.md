# Dimension Defaults

Load this reference before writing spacing, padding, radius, control-height, elevation, or select
styling when the repository has no spacing or shape authority. A repository `DESIGN.md` or token
owner always wins; these defaults fill silence, they do not override a product.

The values come from a verified production product UI token set. Only dimensions are adopted. Do
not adopt its colors, typography, logo, or voice; colors stay neutral or come from the target repo.

## Spacing scale

The durable rule is proportional: space between groups is larger than space inside a group, and
steps grow non-linearly. The exact values below are product defaults, not a book mandate; a
repository scale with intermediate steps (12, 24, 48) is equally valid.

Use only these values for padding, margin, and gap: `0`, `4`, `8`, `16`, `32`, `64` px.

| Token | px | Use |
| --- | ---: | --- |
| `--space-xs` | 4 | Label to control, hint or error to control, tightly related icons |
| `--space-sm` | 8 | Icon to text, buttons in one row, inline items |
| `--space-md` | 16 | Field to field, default stack gap, control text inset, phone page gutter |
| `--space-lg` | 32 | Group to group, section separation, desktop page gutter (>= 768 px) |
| `--space-xl` | 64 | Sparse major separation only |

A composite value (select end padding) is a `calc()` of tokens, not a new literal.

## Vertical rhythm

- The parent stack owns spacing between rows: `display: flex|grid` plus `gap`. Rows, fields, and
  form groups carry no vertical margin, so gaps never stack or collapse unevenly.
  This is an implementation default that keeps rhythm in one place, not a sourced ban on margins.
- Inside a field: label, control, hint/error separated by `--space-xs`.
- Between fields: `--space-md`. Between field groups or sections: `--space-lg`. The group gap must
  be visibly larger than the field gap.
- Text roles keep their own line-height; do not fix row rhythm with line-height or padding hacks.

## Inset roles

| Role | Value |
| --- | --- |
| Page gutter | 16 px below 768 px, 32 px at 768 px and above |
| Control text inset (button, input, select start) | 16 px inline |
| Trailing indicator inset (chevron, count, clear) | 16 px from the control end |
| Indicator to value gap | 8 px |
| Alert / banner | 8 px block, 16 px inline, 8 px icon-text gap |

## Control sizes

| Size | Height | Use |
| --- | ---: | --- |
| compact | 32 | Dense toolbars and tables |
| default | 40 | Inputs, selects, buttons on pointer surfaces |
| touch | 44 | Below 768 px or touch-first surfaces |

Inputs, selects, and buttons in one row share one height. Icon-only buttons are square in hit area
and circular in shape at the same three sizes.

## Radius by component

Radius is per component, not one universal ladder.

| Component | Radius |
| --- | --- |
| Button, input, select, alert | 8 px |
| Icon-only button, toggle, avatar | 50% (circular) |
| Tag, badge, inline code | 4 px (shared default) |
| Card, dialog, popover (when the product uses a contained surface) | 16 px (shared default) |
| Pill filter or chip | 9999 px |
| Layout containers without a visible surface | none |

Nested surfaces: inner radius = outer radius minus the inner padding, never larger than the outer. This is an
engineering default, not a sourced rule.

## Elevation

Flat content uses no shadow. Raised surfaces use one step:

| Step | Shadow | Use |
| --- | --- | --- |
| 1 | `0 2px 4px rgba(0,0,0,.16), 0 0 1px rgba(0,0,0,.18)` | Hovered rows, raised buttons |
| 2 | `0 4px 8px rgba(0,0,0,.16), 0 0 1px rgba(0,0,0,.16)` | Menus |
| 3 | `0 8px 16px rgba(0,0,0,.16), 0 0 1px rgba(0,0,0,.14)` | Popovers, tooltips, side panels |
| 4 | `0 24px 48px rgba(0,0,0,.20), 0 0 1px rgba(0,0,0,.12)` | Dialogs |

## Breakpoints

Width: 300, 360, 440, 600, 768 (touch UI), 992, 1200, 1440 px. Height: 537, 700, 811 px. Compose
from these; do not invent a 12-column grid or a fixed gutter contract.

## Canonical select

One pattern. Do not mix it with `appearance: auto` or a `background-image` arrow: either combination
renders two arrows on some browsers or ignores the end padding.

```html
<div class="select-control">
  <select id="region" name="region">…</select>
  <svg class="select-indicator" aria-hidden="true" width="16" height="16" viewBox="0 0 16 16">
    <path d="M4 6l4 4 4-4" fill="none" stroke="currentColor" stroke-width="1.5"/>
  </svg>
</div>
```

```css
:root { --select-indicator-size: 16px; --select-indicator-inset: 16px; }
.select-control { position: relative; }
.select-control select {
  appearance: none;
  -webkit-appearance: none;
  inline-size: 100%;
  min-block-size: 40px;
  padding-inline-start: 16px;
  padding-inline-end: calc(var(--select-indicator-inset) + var(--select-indicator-size) + 8px);
  border-radius: 8px;
  text-overflow: ellipsis;
}
.select-indicator {
  position: absolute;
  inset-inline-end: var(--select-indicator-inset);
  inset-block-start: 50%;
  translate: 0 -50%;
  inline-size: var(--select-indicator-size);
  block-size: var(--select-indicator-size);
  pointer-events: none;
}
```

The `select` stays the labelled, focusable control. The focus ring sits on the `select`, not the
wrapper. Check that exactly one arrow shows, that it is vertically centered, and that a long value
truncates before the arrow.

## Checking

```bash
python3 <ux-design-skill-directory>/scripts/validate_delivery.py --css app.css \
  --spacing-scale 0,4,8,16,32,64 --radius-scale 0,4,8,16,50%,9999 --tells
```

Pass the repository's own scales instead when it has them.
