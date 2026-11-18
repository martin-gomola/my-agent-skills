# Research Boundary

Use this reference for NotebookLM, books, screenshots, or polished product references.

## Evidence record

For each candidate lesson, capture:

- observed mechanism and exact source locator;
- inferred user or system problem;
- transferable principle;
- rejected product-specific expression;
- local owner;
- acceptance check;
- reference weakness or uncertainty.

Do not publish NotebookLM prose directly. Check the answer against cited source locations, existing
product evidence, accessibility standards, and rendered behavior. If the source is unavailable or
the citation cannot be resolved, label the point unverified and omit it from normative guidance.

## Retained research findings

- Frame user need, product outcome, and technical feasibility before visual work.
- Map information architecture and the core user flow before building the global shell.
- Use a disposable textual flow and low-fidelity wireframe to expose missing decisions, content
  grouping, and element placement before implementation when the structure is non-trivial.
- Use disposable low-fidelity structure, then move into working code for interaction evidence.
- Centralize reusable visual decisions in tokens and components with complete states.
- Prefer de-emphasis and proximity over visual escalation and border proliferation.
- Keep permanent form labels, actionable empty states, and explicit recovery.
- Adapt loading feedback to delay and destination structure instead of showing a gratuitous splash.
- Make search reversible, and add filtering or suggestions from task complexity rather than a fixed
  item count.
- Mirror server-owned cooldowns and keep optional onboarding escapable without bypassing required
  security or legal steps.
- Follow platform dialog order and keyboard-avoidance behavior instead of promoting one iOS example.
- Keep narrow headers lean, let title regions flex, and move secondary metadata when long localized
  content would crowd essential controls; numeric element counts and example breakpoints are
  context-dependent prompts.
- Validate live code and rendered UI; user research may strengthen evidence but cannot be claimed when
  it was not performed.
- When visual direction is uncertain, explore a few distinct options against task and emotional
  criteria, select deliberately, inspect in context, then refine or discard. The number of options is
  a cost and uncertainty decision, not a fixed recipe.
- Expressive color, shape, size, motion, and containment can help communicate feeling and direct
  attention. Use them to clarify the task and key actions while preserving familiar interaction
  patterns, labels, and accessibility.
- For spatial interfaces only, use accurate and restrained depth cues to support hierarchy and
  spatial understanding. Keep text readable and avoid unnecessary depth changes; do not generalize
  visionOS layout mechanics to other platforms.

## Source-specific evidence

The [Apple HIG topic map](apple-hig.md) records the broader Foundations and Patterns review,
topic-level source links, retained decisions, and excluded platform-specific prescriptions.

- **Virpo, “Gacha prompting: ask for ten, keep one”** (`https://virpo.io/blog/how-this-room-was-made/`):
  the author generated directions and iterations, chose by visual judgment against stated product
  goals, inspected rendered assets, and rejected distracting or mismatched results. The transferable
  mechanism is deliberate exploration followed by selection and convergence, not asking for ten or
  using any particular image-generation workflow.
- **Google Design, “Expressive Design: Google's UX Research”**
  (`https://design.google/library/expressive-material-design-google-research?pubDate=20250521`):
  reports that expressive color, shape, size, motion, and containment can support attention and
  usability in tested Material designs, while familiar patterns and labels still matter and user
  preference varies. Treat its findings as evidence for purposeful expression, not a universal style
  or a guaranteed result in another product.
- **Apple Human Interface Guidelines, “Spatial layout”**
  (`https://developer.apple.com/design/human-interface-guidelines/spatial-layout/`): recommends
  centered important content, restrained and consistent depth cues, readable text, and sufficient
  space around spatial interactions for visionOS. These are spatial-platform rules; transfer only the
  underlying principle when it fits another interface.

- **Stephen Few, “Common Pitfalls in Dashboard Design”** (Perceptual Edge, February 2006):
  supports the at-a-glance monitoring sequence, comparison context, prominence for exceptions,
  subdued chrome and decoration, color restraint, and decision-level precision. It targets business
  monitoring dashboards and was a vendor-sponsored addendum: treat single-screen as a rule for the
  monitoring overview, not a ban on scrolling history or drill-down detail.
- **Google PAIR, People + AI Guidebook** (Explainability + Trust; Errors + Graceful Failure):
  supports trust calibration, data-source disclosure, decision-relevant confidence, and paths
  forward from AI failure. Apply only to probabilistic or generated output.

## Explicit exclusions

Do not turn these NotebookLM outputs into universal requirements:

- exactly five users guarantee discovery of 85 percent of usability problems;
- every dimension must be divisible by eight;
- colors must occupy exactly 60, 30, and 10 percent of a screen;
- sidebars must use one fixed pixel width;
- every raw pixel or color literal is invalid regardless of token ownership and exceptions;
- native mobile must use pure black while web must use charcoal;
- all bottom navigation must contain exactly five destinations;
- one type count, weight floor, line length, or line-height range fits every script and product.
- skeletons must appear at exactly three seconds;
- every gap must be a 4px or 8px multiple;
- selectors need search above exactly six to eight items;
- action sheets may contain exactly three actions;
- OTP resend always uses a 30-second cooldown;
- every onboarding step is skippable even when legally or securely required;
- dialogs always place Cancel left and Confirm right;
- mobile forms need a floating virtual-keyboard anchor;
- toolbars require translucency and blur;
- 3D imagery, iOS frame constants, San Francisco typography, or splash screens are defaults.
- every dashboard must fit one screen with no scrolling, whatever its history or detail;
- decorative imagery is never allowed on a monitoring surface;
- gauges, specific chart types, or Few's color-blindness percentages as fixed rules;
- every AI or agent result needs a numeric confidence score.

These may be useful prompts for evaluation, but local product constraints and measurable outcomes
decide.
