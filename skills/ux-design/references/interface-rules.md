# Interface Rules

Load this reference when designing or implementing an application flow or component.

## Hierarchy and layout

- Start with the core content and task, then wrap it in the smallest navigation shell it needs.
- Express action priority through placement, order, contrast, and de-emphasis. Destructive severity
  does not make an action primary; reserve strong warning treatment for the confirmation boundary.
- Use whitespace and tonal surfaces before repeated borders, cards, shadows, pills, accent rails, or
  glows. Reserve accent rails for focus, selection, active wayfinding, or live state.
- Group by proximity. Define inline gaps, stack gaps, and component inset padding as distinct token
  relationships rather than applying one value everywhere.
- Repeated scope bars, filter rows, and toolbars that present related controls should share explicit
  grid tracks or alignment primitives. Compare rendered start edges, end edges, baselines, and
  heights across the repeated regions; similar-looking independent grids are not alignment proof.
- Alignment and inset defaults, applied without being asked:
  - Name the inset roles in the token owner: page gutter, text inset inside a control, and trailing indicator inset (chevron, divider, count); controls take their padding from these roles, not one-off values.
  - Align an icon-only control at a content edge by its glyph, not its hit area: offset it by half the difference between hit size and glyph size so the visible icon meets the edge.
  - Align mixed-size inline items in one row (pills, badges, counts, metadata) on the text baseline, not by box center.
  - When rows that read as one line live in separate containers (a sidebar brand and a top bar), give them the same top inset token and verify equal center y.
  - Separate metadata with spacing or layout before glyphs; a middle-dot string (`A · B · C`) is a
    generated default. When a separator is needed:
  - Put separators after their item, so a wrapped line never starts with a separator.
  - Give a sticky region over scrolling content a visible edge (hairline or padding), so content passes under a boundary instead of looking clipped.
  - Align a list's continuation action (Load more) with the list it extends; under a full-width list, center it.
- Follow the repository spacing scale. An 8-point or 5-point base is a system choice, not a universal
  rule. Do not require every rendered dimension to divide cleanly by that base. When the repository
  has none, use [dimension defaults](dimension-defaults.md) instead of inventing one-off values.
- Let the parent stack own row rhythm with `gap`; rows, fields, and form groups carry no vertical
  margin. Mixed margins and gaps produce uneven rows.
- Keep spacing in one selector per element. A type selector (`.section`) and an element selector
  (`.cta`) that both set padding or margin cancel each other unpredictably. Verify computed padding
  and gap against the token in the browser, not only the authored CSS.
- Keep fluid regions flexible but bound sidebars, reading columns, and dense panels by their content
  needs. Test instead of imposing a universal fixed or percentage width.

## Typography and content

- Define a text role as size, weight, line-height, and letter-spacing together.
- Keep body copy comfortably readable and constrain long prose to a reasonable measure. Treat exact
  line-height ranges and character counts as starting heuristics unless local authority defines them.
- Preserve complete labels and critical metadata. If truncation is necessary, provide a clear path to
  the full value.
- Use tabular numbers for aligned metrics. Keep passive metadata unboxed; use pills for filters,
  choices, or exceptional compact states rather than decoration.
- Prefer user language, specific verbs, and actionable error or empty-state copy.
- Name an action by what happens ("Save changes", not "Submit") and keep that name through the
  flow: the "Publish" button produces a "Published" toast. Name things by what users manage, not by
  how the system is built.
- Errors state what happened and how to fix it, in the interface voice: no apology, no vagueness.
  An empty state offers the next action. Use sentence case and let each text do one job.
- Audit visible copy as part of hierarchy. Omit generic helper text, repeated prompts, decorative
  labels, and per-item instructions when the control, placement, or state already makes the action
  clear. Add visible supporting text only when it resolves a demonstrated uncertainty, constraint,
  state, or recovery need. This does not remove accessible names, persistent form labels, actionable
  errors, status messages, or necessary empty-state and recovery copy.

## Components, forms, and feedback

- Reuse existing primitives when they fit the target job and required states. If a primitive or
  composition encodes the observed failure, compare repair with replacement instead of forcing a
  cosmetic variant. A bounded one-off treatment may remain local; a new reusable primitive needs
  repeated need, named ownership, complete states, and tests.
- Keep field labels visible and programmatically associated. Connect hint and error text, preserve
  input after failure, and never encode required or invalid state by color alone.
- For every styled native select, use one indicator path, declared in the same rule that styles
  the control. Default: `appearance: none` plus a positioned wrapper with an `aria-hidden` SVG
  chevron, explicit size and logical-end inset, and `pointer-events: none`, with end padding of
  inset + indicator size + gap (canonical code in [dimension defaults](dimension-defaults.md)).
  Keep `appearance: auto` only when the product deliberately uses the platform arrow; Chrome then
  ignores the end padding. Never combine a wrapper chevron with `appearance: auto` or a
  `background-image` arrow, and do not rely on a pseudo-element attached to the select. End padding
  alone does not prove an arrow exists. Keep the native select as the focusable semantic control. Verify exactly one visible indicator, long localized
  values, focus, disabled state, and phone/desktop rendering. Replace the native indicator when it is
  absent, faint, clipped, or inconsistent on a supported surface.
- When using native rendering, preserve platform appearance and verify it in each supported browser.
- Put persistent save, sync, privacy, or trust status near the workflow. Keep transient feedback
  bounded and semantically announced without repeatedly interrupting screen-reader users.
- Provide explicit loading, empty, error, success, disabled, stale/offline, and destructive states
  where the product can reach them.
- Keep routine feedback in context; reserve modal interruption for a clear task benefit or critical actionable information.
- Request private-data permissions when the feature needs them, explain the purpose, and support denial or revocation without misleading prompts.

## Navigation and responsive behavior

- Keep the current location and next action clear. Long flows show current, completed, and future
  progress without relying on color alone, plus a direct recovery path to the affected step or field.
- Use familiar pictograms when they materially shorten scanning or distinguish repeated navigation,
  settings, or action rows; keep text labels as the primary meaning unless the local platform already
  establishes a clear icon-only convention. Reuse the product's icon family and align repeated icon
  boxes, strokes, labels, controls, and disclosure indicators on explicit tracks. Hide supplementary
  pictograms from assistive technology, give meaningful icon-only controls an accessible name, and
  remove icons that are ambiguous, decorative noise, or harder to distinguish than the labels.
- Treat narrow headers as bounded layout regions. Let the title region flex, wrap, or truncate by the
  local product contract and keep essential controls bounded.
  Relocate secondary metadata instead of compressing it into the header.
  Test the longest supported locale at the narrowest viewport.
  A two-or-three-primary-element mobile header is a useful crowding prompt, not a universal cap.
- Keep primary mobile actions reachable, but do not hardcode thumb-zone placement when platform
  conventions, safe areas, or task risk require another location.
- Adapt layout, density, order, and interaction for content and input mode; do not merely shrink the
  desktop surface.
- Full-bleed outer surfaces do not authorize edge-to-edge text or controls. Preserve safe content
  insets and prevent sticky controls from covering content.
- For RTL locales, adapt reading-order navigation and layout without blindly mirroring numbers, media controls, photographs, or logos.
- Provide an accessible alternative to drag or custom gestures, make move-versus-copy consequences clear, and support undo where the operation permits it.
- Keep task-specific options near the task; use settings for infrequent preferences and respect system accessibility and appearance choices.

## Loading, search, and constrained flows

- Match loading feedback to expected duration, continuity, and destination predictability. Keep fast
  transitions quiet; use progress or a structural skeleton when delay would otherwise look frozen.
- Use a structural skeleton when it reduces uncertainty and the destination layout is known. Keep
  placeholders distinct from real content, respect reduced motion, and transition without layout
  shift. Treat the manual's three-second threshold as a heuristic, not a universal timer.
- Choose a searchable selector from option complexity, familiarity, label length, and retrieval cost.
  Do not add or omit filtering from a universal six-to-eight-item threshold.
- Give active search a one-action clear control that preserves focus. Reset results and suggestions
  predictably; add autocomplete only when suggestions are relevant, reliable, accessible, and
  acceptable for privacy, latency, and cost.
- Keep contextual mobile action menus focused and scannable. Move complex configuration to a
  dedicated view using the active platform pattern instead of enforcing a fixed action count.
- Treat retry cooldowns and rate limits as server or security-policy authority. Reflect returned
  retry state, prevent duplicate requests, announce status without chatter, and restore the action
  when the authoritative window expires.
- Let users skip, defer, go back, or exit optional onboarding. Do not bypass security, legal, or
  task-critical requirements; explain why a required step blocks completion and preserve progress
  when appropriate.
- Inherit dialog action order from the active platform or repository design system. Do not hardcode
  cancel-left or confirm-right across web, iOS, Windows, and other conventions.
- Keep the focused control, associated error, and next action visible when a software keyboard opens.
  Prefer standard viewport, scroll, and keyboard-avoidance behavior over a custom floating anchor.

## Accessibility and motion

- Use semantic elements and accessible names. Make grouped content a list or group when that
  relationship matters.
- Show visible keyboard focus and preserve a logical focus order. Dialogs need an accessible name,
  intentional initial focus, containment, Escape handling, and focus return.
- For normal text, compute and require a contrast ratio of at least 4.5:1 against its actual rendered background.
- Verify large text and essential non-text UI indicators at 3:1 or better in every supported theme.
- Follow the active platform or design-system target-size contract. Where it is silent, favor generous
  touch targets and spacing, and validate common one-handed use rather than relying on a nominal box.
- Provide a reduced-motion path for decorative, scroll-triggered, and continuous animation.
- Tie custom motion to feedback or spatial continuity, follow gesture expectations, and keep it brief and interruptible.
- Never make animation the sole carrier of essential state or block the next action just to finish a repeated animation.
- Test zoom or 200% text, long localized content, keyboard-only use, and touch or pointer input on the
  rendered surface.

## Generated-default tells

These appear in generated UI regardless of subject. Each is legitimate when the product or brief
chooses it; do not use one by default:

- a tracked-out ALL-CAPS eyebrow label above every heading;
- `→` appended to button or link text;
- a monospace face for small data labels that are not code;
- one accent word in a heading (italic, bold, or colored);
- numbered markers (01 / 02 / 03) on content that is not a sequence;
- every region in an identical rounded card with the same soft grey shadow;
- tinted near-black (`#111`, `#0B0B0B`) standing in for the product's text color;
- gradient washes or entrance animations on every section as decoration.

Before delivery, list any of these in the rendered surface and keep each only with a product reason.

## Style heuristics, not requirements

Treat these as context-dependent: exact 60-30-10 color allocation, pure black versus charcoal dark
themes, a fixed maximum of two font families, strict font-weight floors, bottom-navigation item
counts, exact line-length ranges, universal fixed-width sidebars, or one spacing divisor. Preserve
local authority and validate usability, accessibility, and content fit instead. Also keep fixed
loading delays, selector item thresholds, action-sheet counts, retry durations, dialog order,
translucent toolbars, platform frame constants, default fonts, and imagery trends non-universal.
