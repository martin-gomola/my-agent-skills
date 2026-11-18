# Workflow Decisions

Load this reference for the three judgment calls the default workflow requires: pattern
classification, structure-artifact form, and repair-versus-redesign. Resolve each from the table
below rather than deciding freeform — that scattering of freeform micro-decisions across steps is
what produces uneven output run to run. Fill the Output Contract's structured block from these
tables.

## 1. Pattern classification (step 1)

Classify the affected pattern before styling:

| Signal | Classification |
| --- | --- |
| The element meets its job today; only a narrow, bounded defect is reported. | sound |
| The element mostly works; a bounded change fixes the reported failure without adding new information hierarchy. | repairable |
| The element cannot express the content, task, or hierarchy without breaking readability, accessibility, or the flow, even after a bounded fix. | structurally weak |

Existing code and `DESIGN.md` are evidence for this table, not proof of soundness on their own.
Reread the table if the request itself claims a pattern is broken beyond repair — the claim is
evidence, not the classification.

## 2. Structure-artifact form (step 2)

Choose the form before implementation:

| Condition | Form |
| --- | --- |
| Adds or restructures a screen or region with two or more content groups, or a layout that must recompose across viewports. | **full** — flow line, an ASCII wireframe per required viewport class (normally the narrowest supported width and desktop), and an inventory of every required element (including the longest plausible label or locale) assigned to a named region or a disclosure path. |
| Single-region addition that extends an established local pattern. | **flow-only** — the flow line alone (entry -> decisions -> action -> feedback -> recovery -> completion). |
| Narrow defect confined to one existing region, with no new information hierarchy or viewport recomposition. | **none**. |

State the chosen form and reason before implementation.

For a full artifact, also list only the reachable states that can change placement or hierarchy
(loading, empty, error, long content, keyboard open, offline), then critique the artifact against:

- no missing decision, feedback, or recovery step in the flow;
- related content shares a region while unrelated tasks do not;
- every inventoried element has a place;
- the narrowest layout has no crowded header, hidden action, or competing scroll owner.

Resolve structural gaps in the artifact before writing code. Do not begin implementation while a
required artifact has an unresolved element placement, mixed-purpose region, missing state, or
unanswered critique question. Discard the artifact once its structural decisions are locked — it is
not a deliverable.

## 3. Repair versus redesign (step 4)

Run this procedure only when step 1 classified the pattern as structurally weak, or a first repair
still leaves the task unclear.

1. Lock the invariants: user job, content semantics, product identity, accessibility, platform
   behavior, technical constraints, required states.
2. Produce two lanes: a constrained repair using sound local patterns, and a context-reset
   alternative that temporarily sets aside the current composition and component choice — not the
   invariants. Generate the alternative from the content type and task (message, evidence, status,
   choice, warning, control, navigation); do not wait for a supplied reference screenshot.
3. Compare the lanes on: task clarity, hierarchy, long-content readability, interaction states,
   responsive behavior, product coherence, and implementation cost.
4. Choose the stronger lane and record why, backed by rendered evidence rather than smallest diff
   size.

Skip the second lane only when step 1 classified the pattern as sound or repairable and the issue
is a narrow, bounded defect — building and comparing a context-reset alternative for a sound
pattern is unnecessary ceremony.
