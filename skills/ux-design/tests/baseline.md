# Consolidation baseline

Recorded on 2026-08-26 before authoring the skill now named `ux-design`.

The existing portfolio split application interface work across `ui-ux-pro-max` and durable design
authority across `mythosaur-design`. Both repeated the same authority-first, token ownership,
accessibility, responsive, reference-learning, and rendered-verification rules. The UI skill also
loaded a roughly 936 KB recommendation corpus and a broad design-system generator for tasks that
usually needed a small repository-specific change.

The replacement must correct these failures:

- route application UX/UI design, implementation, validation, and repository `DESIGN.md` ownership
  through one skill;
- preserve product identity and local authority instead of inventing palettes or copying reference
  brands;
- start from the core user flow and content rather than decorating an application shell;
- make complete states, accessibility, responsive behavior, and rendered verification delivery
  gates rather than optional checklists;
- keep detailed rules progressively disclosed and avoid loading style, product, framework, and
  landing-page catalogs by default;
- retain deterministic contrast and native-select validation without retaining the large search and
  design-system generation subsystem.

The NotebookLM research pass used the linked UX/UI notebook and four selected book sources. Its
output is draft evidence, not publication authority. Context-dependent or overstated claims such as
an exact 60-30-10 color allocation, universal fixed-width sidebars, every dimension being divisible
by eight, zero raw pixel values, or a five-user/85-percent guarantee are deliberately excluded.

## Preservation bias failure

Recorded on 2026-08-27 from a real handover-detail redesign. The existing `ux-design` instructions
overweighted repository preservation, reuse, and the smallest coherent change. Faced with an original
request that was visually lost, the skill kept the existing full-width section and escalated color,
font size, and weight. A longer request became harder to read. Without that preservation bias, a later
pass reclassified the content as an authored message and introduced a neutral inset bubble that was
clearer on desktop, mobile, and with long text.

The update must correct these failures:

- treat existing implementation and `DESIGN.md` as evidence and constraints, not quality approval;
- classify affected patterns as sound, repairable, or structurally weak before styling;
- compare a constrained repair with a context-reset alternative when the pattern is weak;
- allow a bounded element to be built from scratch without requiring a supplied reference;
- retain user needs, semantics, identity, accessibility, platform, and technical constraints during
  context-reset exploration;
- choose from rendered evidence instead of equating minimal diff size with design quality.

## Restored UI Professional manual gap

The reuploaded `The-UI-Professional-s-Design-Manual-600-Pages-2022.pdf` was healthy on 2026-08-26
under NotebookLM source `f5c7b279-0744-4979-84ff-cd95bc20466b`. Before this update, `ux-design`
did not explicitly cover adaptive loading representations, searchable-choice criteria, reversible
search, server-owned resend cooldown feedback, exits from optional onboarding, or platform-owned
dialog and virtual-keyboard behavior. The source also contains fixed timing, count, spacing, iOS,
typography, blur, and imagery prescriptions that must remain non-universal.

## Styled select indicator failure

Recorded on 2026-08-27 from the Slovak Garden Planner onboarding form. The deterministic helper
accepted end padding on styled native selects and the workflow reported success without recording
whether every arrow was visibly present. Native indicators happened to render on one browser, but
their visibility and placement remained platform-dependent and the skill had no same-rule decision
or one-arrow-per-select proof.

The update must correct these failures:

- reject styled selects that leave the native-versus-custom indicator strategy implicit;
- require `appearance: auto` in the styling rule or `appearance: none` with a deterministic visible
  replacement;
- require positioned, non-interactive custom indicators with explicit logical-end inset;
- state that end padding is not proof of indicator presence;
- verify exactly one arrow per styled select with long localized values on phone and desktop.

## Redundant visible placement instruction

Recorded on 2026-08-30 from the Slovak Garden Planner. Each empty grid cell already exposed an
accessible add action and a visible “Pridať” label, while a bed-level banner repeated the same
instruction with the selected crop name. The user identified that banner as unnecessary visual
text noise.

The update must keep actionable controls and state or error messaging while omitting visible helper
copy that restates an already clear action.

## Missing pre-code structure gate

Recorded on 2026-08-30 from two related Garden Planner failures. A page accumulated a crop picker,
bed map, planting quantities, water demand, calendar, companion guidance, and soil advice as one long
dashboard because the content groups were not externalized into the grower flow before code. A
mobile full-screen crop selector then tried to fit an icon, a long Slovak crop name, row spacing, an
evidence badge, and a close action into one header; the long name overlapped metadata. The repair
grouped the dashboard by task and moved secondary metadata out of the compact mobile header.

Step 2 required a task flow and disposable structure but no inspectable artifact, content inventory,
responsive element-placement comparison, or critique gate before implementation. The update must:

- require a textual flow, ASCII layout map, content/control inventory, and relevant state variants
  before implementation for new or restructured multi-group or responsive regions;
- block implementation while grouping, placement, long-content, or viewport questions remain;
- allow a flow-only or skipped artifact for an established single-region pattern or a narrow defect
  so the safeguard does not become generic design-process ceremony.

## Behavior-eval harness had no target repo

Recorded on 2026-08-31 after a report of persistently uneven delivered results. `make skill-check`
(lint plus trigger eval) was clean, but `make skill-test SKILL=ux-design` (`--runs 2`) scored
`pass_rate=0.15`. Reading the transcripts showed nearly every failure had the same shape: the
consumer correctly executed step 1 (resolve authority and scope), found no `DESIGN.md`, tokens, or
application surface, and halted to ask which repo hosted the target app — because
`eval-skill-behavior.py` launched the `claude` consumer with no working-directory override, so it
always ran from `mythosaur-tools` itself, a tools/skills repo that owns no application UI by its own
`CLAUDE.md`. The skill behaved correctly for that environment; the harness gave it no real target to
design against, so every downstream expectation about implementation and rendering failed for a
reason unrelated to the skill's instructions. A second, smaller source of eval noise: substring
`must_not_mention` checks (e.g. `"guarantee"`) fired even when the model correctly quoted a rejected
absolute claim to explain why it would not honor it.

The fix added a fixture-directory convention to the harness (`evals/fixtures/<skill>/`, used as the
consumer's working directory when present) and a minimal fixture app under
`evals/fixtures/ux-design/` (its own `CLAUDE.md`, a filled `DESIGN.md`, `src/styles/tokens.css`, and
`Button`/`TextField` components) so step 1 finds a real target and the rest of the workflow can
execute and be judged. This does not change `SKILL.md` guidance — the skill's step 1 behavior was
correct; the automated release-validation gate could not previously exercise steps 2 through 6 for
this skill at all, which is the real explanation for why observed field results still looked uneven
even after prior updates.

## Narrate-only harness cannot prove execution, and judgment calls were scattered across steps

Recorded on 2026-08-31, immediately after the fixture fix above. Re-running `make skill-test` with
the fixture wired in dropped the score further (0.15 -> 0.06) for a different, deeper reason: the
harness's `claude` consumer is single-shot and explicitly told "you do NOT have live tool execution,"
while several `eval.yaml` expectations demanded proof only real execution can produce ("validates...
in the rendered app," "verifies the rendered narrow viewport after implementation"). No skill
quality could ever satisfy those from a narrated response — the rubric and the consumer were
structurally mismatched.

Separately, `SKILL.md` spread three real judgment calls — pattern classification (sound/repairable/
structurally weak), structure-artifact form (full/flow-only/none), and repair-versus-redesign — as
prose scattered across steps 1, 2, and 4, each with its own "completion gate" sentence. This is the
exact shape the NotebookLM research names as a root cause of uneven output: unconstrained,
distributed micro-decisions resolved slightly differently every run, not a knowledge gap.

The fix, on the harness side, split `eval.yaml` rubrics into `expectations` (plan-provable, scored by
the fast narrate-only consumer used in `make skill-test`) and `execution_expectations` (require real
proof, scored only by a new `--consumer claude-execute`, which copies the fixture into a disposable
temp sandbox, runs with real tool execution scoped to that sandbox only, and grades against the
resulting `git diff`). On the skill side, the three judgment calls moved into
`references/workflow.md` as explicit decision tables, `SKILL.md`'s steps now point to that table
instead of restating it inline, and the Output Contract opens with a structured
`authority/pattern/artifact_form/decision` block instead of scattered prose — a missing field is now
immediately visible rather than silently skippable. Duplicated implementation detail already fully
covered in `references/interface-rules.md` and `references/validation.md` (the select-indicator
implementation paragraph, the control-alignment paragraph, the rendered-proof paragraphs) was removed
from `SKILL.md` rather than kept in two places.

## Pictogram-assisted settings navigation

Recorded on 2026-09-15 from the Beskar Shelf settings screen. Repeated settings and navigation rows
used text alone, making categories and destinations slower to distinguish. The user supplied a
reference whose transferable mechanism was a familiar pictogram beside each labeled row and asked
to retain that mechanism as reusable UX guidance.

The repaired Beskar screen kept its own dark/light tokens, typography, wording, layout, and icon
artwork. It added supplementary pictograms to repeated rows, kept visible labels as the source of
meaning, used disclosure chevrons only for navigation, and exposed segmented choices with semantic
pressed state. Rendered checks measured a 0px desktop centerline difference between labels and
controls, found and fixed a 16px narrow-phone segmented-control overflow, verified final 320px
client/scroll widths were equal, and raised a dark disclosure chevron from 2.73:1 to the required
3:1 non-text contrast threshold.

The retained rule is conditional: use familiar pictograms when they materially improve scanning or
navigation in repeated structures. Do not add icons to every row, replace text labels by default,
copy reference branding, or treat decorative icon count as evidence of usability.
