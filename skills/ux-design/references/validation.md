# Validation

Load this reference before delivery.

## Evidence sequence

1. Define the claim: which user can complete which task on which supported surface.
2. Run targeted unit or component tests for changed behavior.
3. Run applicable lint, typecheck, build, and accessibility automation.
4. Render the changed flow with representative data and states.
5. Exercise keyboard, pointer or touch, responsive layouts, supported themes, and reduced motion.
6. Fix failures and rerun the smallest proving check.

## State matrix

Test only reachable states, but do not omit a reachable state because fixture setup is inconvenient:

- first run and returning user;
- loading or progress;
- fast, delayed, partial, and cancelled loading transitions;
- empty with an appropriate next action;
- partial and long content;
- validation error and recovery;
- system error, slow network, stale, or offline;
- success and persistent save or sync status;
- disabled and permission-limited;
- destructive confirmation and cancellation;
- dialog open, Escape, dismissal, and focus return.
- search typing, clear, empty results, suggestion dismissal, and focus retention;
- retry cooldown returned by the server, duplicate prevention, refresh, expiry, and rejection;
- optional onboarding exit plus required-step explanation and progress preservation;
- software keyboard open with the focused control, error, and next action visible.
- when motion changes: interruption, rapid repeated actions, reduced motion, and equivalent state feedback without animation;
- when gestures change: keyboard or onscreen alternatives, valid and invalid drop targets, and undo;
- when permissions change: not-yet-requested, granted, denied, and revoked access without loss of unrelated work.

## Responsive and input matrix

Use the repository's supported viewport contract. If absent, sample a narrow phone, common phone,
phone landscape, tablet or intermediate width, and representative desktop. Check:

- no horizontal overflow, clipped labels, or content behind fixed UI;
- sensible reading measure, wrapping, and density;
- safe insets for text and controls;
- matching rendered x/y edges and heights for controls intended to align across repeated rows or
  stacked panels;
- edge alignment measured on glyph rectangles (the svg), not button rectangles; a hit area that touches the edge is not proof that the icon does;
- baselines of mixed-size inline items measured with a zero-size inline-block probe (vertical-align: baseline) in each item, equal within 0.5px;
- for pictogram-assisted navigation or settings, a consistent optical box and stroke family,
  recognizable concepts, aligned label/control centerlines, no duplicate screen-reader announcement,
  persistent text labels unless a proven local icon-only convention applies, and at least 3:1 contrast
  for essential non-text indicators in every supported theme;
- exactly one visible arrow for every styled select, with measurable separation from the longest
  localized value and the control border at phone and desktop widths;
- equal measured gaps between sibling form rows (field to field) and a larger gap between groups,
  read from element rectangles, not from the stylesheet;
- layout adaptation rather than desktop shrinkage;
- visible focus, logical order, semantic names, and non-color state;
- comfortable touch targets and no hover-only functionality;
- 200% text or zoom without loss of content or operation.
- for supported RTL locales, mixed-script text, numeric values, reading-order navigation, and directional icons;
- applicable system appearance, increased contrast, and reduced-transparency settings on supported platforms.

## Deterministic helper

Resolve `scripts/validate_delivery.py` relative to the loaded `ux-design` skill directory, not the
active repository, and run it with explicit rendered color pairs. HTML templates with inline style
blocks may also be passed through `--css`. The helper uses Python 3 standard library only and returns
exit 1 with actionable findings. It requires every styled native select to
declare `appearance: auto` or use `appearance: none` with a `.select-indicator`/`.select-chevron`
rule that is absolutely positioned, has an explicit logical-end inset, and cannot intercept pointer
events. It rejects a background-image arrow, a wrapper chevron combined with a platform arrow, and
literal end padding smaller than inset + indicator size. With `--spacing-scale` and
`--radius-scale` it reports padding, margin, gap, and radius literals off the scale (values written
as `var()` tokens resolve from `:root`), and vertical margins on field or row selectors. `--tells`
reports tracked ALL-CAPS labels, arrows appended to button or link text, and one soft grey shadow
reused across three or more rules; each finding needs a product reason or a fix.

The helper cannot inspect computed styles, gradients, transparency, DOM semantics, focus order,
layout, or interaction. It cannot prove that the indicator node is present in the rendered markup.
Record a screenshot or DOM count showing one indicator per styled select; padding alone is not proof.
