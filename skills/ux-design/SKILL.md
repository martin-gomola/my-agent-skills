---
name: ux-design
description: Designs and implements useful application UX/UI with clear tasks, low cognitive effort, visual feedback, progressive disclosure, and rendered verification. Use for app screens, editors, creation tools, dashboards, internal tools, forms, settings, beginner workflows, confusing tabs, ineffective use of workspace, and application redesigns that include implementation. Preserves product contracts while challenging weak layouts and components. Avoid for marketing or acquisition pages, audit-only critique, isolated cosmetic polish, PWA install mechanics, faithful Figma implementation, image generation, or backend-only work.
metadata:
  version: "0.1.0"
---

# UX Design

Design and ship application interfaces as working product flows. Preserve local product identity and
sound local patterns, challenge weak ones, implement the smallest solution that fixes the actual
failure, and prove it in the rendered UI.

## Source Boundary

The linked NotebookLM notebook is a draft research surface over five healthy book sources. Treat its
output as evidence to review, not as publication authority. `sources.yaml` and `grounding.yaml` record
the retained claims. Reject absolute style prescriptions when the product, platform, or sources make
them context-dependent.

Glanceable monitoring guidance draws on Stephen Few's dashboard pitfalls paper and Google PAIR's
People + AI Guidebook; [glanceable monitoring and trust](references/glanceable-monitoring.md)
records their bounded rules.

Application workbench guidance also draws on a recorded product field case. Treat it as a set of
transferable mechanisms to test in the current product, not proof of universal usability outcomes.

Apple HIG learning covers separate Foundations and Patterns pages. For Apple-platform work or HIG
reference adaptation, read [Apple HIG topic map](references/apple-hig.md), then consult the individual
pages relevant to the affected task, including their platform considerations. A single HIG page
does not stand in for the whole guide.

## Ownership Boundary

This skill owns application UX/UI design plus implementation, repository `DESIGN.md` authority,
component and flow improvements, accessibility, responsive behavior, and rendered validation.

Route adjacent work elsewhere:

- isolated cosmetic polish of a sound component -> the available focused visual UI skill;
- public landing, portfolio, hero, or marketing art direction -> out of scope unless the user explicitly asks this skill to cover it;
- screenshot-first audit with findings only -> product-design audit or the available UX audit skill;
- PWA installability, manifests, standalone mode, and safe-area mechanics -> `pwa-app-design`;
- Figma creation or design-to-code -> the relevant Figma skill;
- bitmap illustration or visual reference generation -> `imagegen`.

## Application utility default

Start with what the user needs to accomplish and the next meaningful action. An application serves
work: creating, inspecting, arranging, deciding, editing, or managing something. Do not default to
acquisition-page sections, promotional heroes, testimonials, feature slogans, or decorative content.
An onboarding explanation or commercial screen is appropriate when it serves the requested task.

Translate “thinkless” into useful defaults, recognizable choices, visible consequences, and recovery.
Keep precision and advanced capabilities available. Preserve product contracts and identity, not a
failing layout or component choice. Do not make users repeat audience, tone, or constraints already
established in the conversation or repository, or choose styling details the product already resolves.

For workflow redesigns and crowded app workspaces, read
[task-first application design](references/task-first-apps.md) before selecting the structure.
Use its control, workspace, preview-truth, action-priority, and completion-state guidance. Skip that
reference for a bounded visual defect that does not change the flow. Keep the pre-code direction
brief and concrete; process artifacts should resolve actual decisions, not become a second project.

For dashboards, inboxes, status boards, or any surface people scan to decide what needs attention,
and for surfaces that present AI or agent output, read
[glanceable monitoring and trust](references/glanceable-monitoring.md).

## Default Workflow

### 1. Resolve authority and scope

1. Read the active repository instructions and `DESIGN.md` when present.
2. Inspect the token owner, reusable components, relevant tests, and one representative rendered
   surface before proposing a new visual direction.
3. Identify users, job, business outcome, technical constraints, target inputs and viewports, and the
   observed failure.
4. Classify the task as greenfield, existing-product change, design-authority reconciliation, or
   reference adaptation.
5. Classify the affected pattern using the table in `references/workflow.md`. Existing code and
   `DESIGN.md` are evidence and constraints, not proof that the current element is good.

Follow the authority order in `references/design-authority.md`. Do not force a house style onto an
unrelated product, but do not preserve a documented or shipped pattern when rendered task evidence
shows that it fails its job.

Completion gate: name the local authority, target flow, supported surfaces, success evidence, and
the pattern classification.

### 2. Model the flow and structure before the shell

Map the primary task as entry -> decisions -> action -> feedback -> recovery -> completion. Include
navigation and information hierarchy only to the depth needed for that flow. Design core content
before global chrome; shell-first work constrains the solution before content needs are known.

When the task adds or restructures a screen or region with two or more content groups, or a layout
that must recompose across viewports, produce a short textual structure artifact before implementation
(a flow line, an ASCII wireframe, and an element inventory). Use `references/workflow.md` to choose the
artifact form (full, flow-only, or none) and to run its pre-code critique gate.
Resolve structural gaps in the artifact before writing code.

For greenfield work, use disposable low-fidelity structure before visual polish, then move quickly to
working code. Do not spend the delivery budget on static mockups that cannot prove interaction.

Completion gate: the artifact form and reason are explicit, and no unresolved grouping, placement, or
crowding question remains before implementation.

### 3. Establish or preserve the local system

- Existing product: consume current tokens, typography, dependencies, and sound interaction
  conventions where they support the target job. Preserve identity and stable contracts, but do not
  force a weak component or composition to survive as a cosmetic restyle. Do not introduce a palette,
  font, component library, or motion dependency unless the task explicitly changes the foundation.
- Greenfield product: create the smallest token and primitive set needed by the core flow, then record
  product-specific decisions in repository `DESIGN.md` using `assets/DESIGN.md`.
- Spacing, inset, radius, control-height, and elevation silence: do not invent values. Use
  [dimension defaults](references/dimension-defaults.md) and record the adopted values in the local
  token owner. Adopt dimensions only; colors and typography stay local.
- Drift: select one repository-local canonical token owner, convert duplicate surfaces into consumers,
  document bounded exceptions, and add a deterministic regression check.

Keep audience, product personality, information architecture, palette, typography, imagery,
components, and justified exceptions local. Cross-project rules may define quality gates and
ownership discipline, not a universal visual shell.

### 4. Choose repair or redesign deliberately

When step 1 classified the pattern as structurally weak, or a first repair still leaves the task
unclear, run the repair-versus-redesign procedure in `references/workflow.md` before implementing.
Building a bounded element from scratch is valid when existing primitives encode the failure;
promote it to a reusable primitive only after repeated need.

Completion gate: record why the element was preserved, repaired, or replaced and which rendered
evidence supports the choice.

### 5. Implement the smallest coherent flow

Do not begin implementation while the step 2 artifact, when required, has an unresolved element
placement, mixed-purpose region, missing state, or unanswered critique question.

Implement the smallest coherent solution that fixes the cause, even when that requires a new bounded
element rather than a smaller cosmetic patch. Build from reusable primitives and real content. Reuse
only primitives suitable for the target job. Each interactive component must cover the states
required by its behavior: default, hover where supported, focus, pressed or selected, disabled,
loading or progress, error, success, and destructive confirmation when relevant.

Use hierarchy to clarify sequence and action priority. Prefer de-emphasizing secondary content over
making every primary element larger, brighter, or boxed. Group by proximity: space between groups
must be visibly greater than space within a group. Empty states must explain the situation and offer
an appropriate next action. Treat visible copy as part of the interface, not filler: do not add visual text noise through generic helper text, repeated prompts, decorative labels, or per-item instructions when the control, placement, or state already makes the action clear. Before adding
visible supporting text, name the uncertainty, constraint, state, or recovery need it resolves; if
there is none, omit it. Keep accessible names, persistent form labels, actionable errors, status
messages, and necessary empty-state or recovery copy even when redundant coaching is removed.

For forms, keep a persistent accessible label for every control; placeholders may provide examples
but must not replace labels. Associate hints and errors with their controls, preserve entered data on
failure, focus the first actionable error when appropriate, and make recovery explicit.

For every styled native select, use the canonical pattern in `references/dimension-defaults.md`:
`appearance: none` on the select plus one positioned, `aria-hidden` SVG chevron in a wrapper. Never
combine it with `appearance: auto` or a `background-image` arrow.
End padding alone is not evidence that an arrow exists.

Check the rendered surface for the generated-default tells in `references/interface-rules.md`
(ALL-CAPS eyebrows, `→` in buttons, middle-dot meta strings, identical card kits) and keep each
only with a product reason.

Read `references/interface-rules.md` for the complete component, hierarchy, content, loading, search,
form-alignment, select-indicator, responsive, and accessibility rules. Read `references/design-authority.md`
only for `DESIGN.md`, token ownership, or reference-learning work.

### 6. Validate in code and the rendered product

Run targeted component or flow tests first, then the repository's lint, typecheck, and build checks
that cover the changed surface. For web CSS, run the deterministic helper from the loaded skill
directory when applicable. Do not assume the active repository owns this script; pass CSS files or
HTML templates that contain inline style blocks:

```bash
python3 <ux-design-skill-directory>/scripts/validate_delivery.py \
  --css <component.css> \
  --contrast 'label,#foreground,#background,4.5' \
  --spacing-scale 0,4,8,16,32,64 --radius-scale 0,4,8,16,50%,9999 --tells
```

Pass actual rendered foreground/background pairs, and the repository's own scales when it has them.
This helper validates explicit contrast pairs, styled native selects (one indicator, end clearance),
off-scale spacing and radius literals, vertical margins on form rows, and with `--tells` the
generated-default tells; it does not replace
browser inspection.

Verify the supported themes and representative small, medium, landscape, and desktop viewports.
Exercise keyboard flow, visible focus, touch or pointer input, 200% text, reduced motion, long content,
loading, empty, error, success, disabled, stale or offline, and destructive states when relevant.
Check that sticky or fixed UI does not hide content and that dialogs have an accessible name, initial
focus, focus containment, Escape behavior, and focus return.

Read `references/validation.md` for the full state matrix, the responsive/input matrix, and the
select-indicator and control-alignment rendered-proof requirements — a passing padding or no-overflow
check alone is insufficient visual proof for either — before final delivery.

Completion gate: tests pass, the core task completes in the rendered interface, critical states and
viewports are verified, and any untestable gap is explicit.

## Reference Adaptation

When learning from a product, screenshot, or research source:

1. Record the observed mechanism separately from the inferred benefit.
2. Extract the problem and transferable principle.
3. Reject palette, typography, copy, branding, exact dimensions, signature motifs, and distinctive
   composition unless they belong to the active product.
4. If the visual direction is genuinely uncertain, explore a small set of meaningfully different treatments against explicit task and emotional criteria. Select one, inspect it in context, and refine or discard it; do not equate more variants or novelty with a better result.
5. Re-express the principle with local tokens, content, and familiar interaction patterns. Use expressive color, shape, size, motion, or containment only when it clarifies hierarchy or supports the intended feeling without weakening task clarity, accessibility, or a familiar pattern.
6. Add a checkable acceptance criterion and critique inaccessible or fragile reference behavior.

Apply spatial-layout guidance only when the target is a spatial interface. In that context, use depth sparingly to communicate hierarchy, keep depth cues consistent with the represented space, and keep text readable; platform-specific guidance does not become a web or mobile default.

Use `references/research-boundary.md` for the evidence record, these source-specific boundaries, and
excluded NotebookLM absolutes.

## Output Contract

Open with this structured block, filled from the `references/workflow.md` decisions — a missing
field means the decision was skipped, not that it didn't apply:

```
authority: <repository DESIGN.md | shared defaults> — <one-line target flow>
pattern: <sound | repairable | structurally-weak>
artifact_form: <full | flow-only | none> — <one-line reason>
decision: <preserved | repaired | replaced> — <one-line rendered evidence>
```

Then, in prose:

- Separate observed evidence, product decisions, implementation, and verification.
- Report changed files and rendered states or viewports tested.
- Name deterministic, accessibility, test, and visual evidence plus any exact gap.
- Do not stop at a mood board, generic checklist, or unverified code diff.
