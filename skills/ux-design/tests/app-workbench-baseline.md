# Application workbench field baseline

Recorded from the JumpStart 3D panel redesign on 2026-10-25, before changing this skill.

The user wanted a reusable application-design workflow for ordinary people doing useful work,
without repeating a brief about low effort, fewer tabs, visual sizing, meaningful space, working
controls, and avoiding marketing filler.

## Observed failures

- The supplied screens grouped connection setup, creation workflows, and preferences around
  implementation features. Three AI clients' setup instructions competed with making an object.
- Settings occupied a narrow strip of a wide window. A large model area remained blank until an
  explicit preview. Beginners first encountered similar numeric fields and domain-specific units.
- A generic design-system search returned a Product Demo + Features marketing-page pattern. A
  narrower UX search still failed to retrieve the needed workflow guidance. This is a routing and
  recommendation failure observed in this session, not proof that every general UI skill fails.
- A rendered implementation exposed a footer covering help text and controls. Moving actions into
  a reserved footer and allowing the canvas to fit the remaining space corrected that layout.
- A manual create, apply, return, undo sequence exposed a success message that outlived its object.
  The correction invalidated that success state when the document changed.
- A body-height choice did not include its optional stacking rim. The UI needed to distinguish
  the editable body height from the total physical height and explain the difference.

The retained mechanisms are task-based navigation, optional setup separation, progressive
construction options, immediate dimensional guides, truthful inspected previews, a reserved action
area, action priority that follows the workflow, and state validation beyond the success click.
Do not turn this product's sidebar dimensions, grid pitch, colors, terminology, native-select ban,
preview engine, or manual-apply contract into universal application rules.

## Evidence limits

These are field observations from screenshots, source inspection, and rendered interaction. The
workshop redesign used a running application as well as a production-UI harness. Its build, full
tests, subsequent workflow checks, preview layout regressions, and panel gates passed in that
session. These results are product evidence, not a measured evaluation of this revised skill.
No isolated skill-on versus skill-off model trial was run. New trigger and behavior fixtures record
what the revised skill must demonstrate before claiming that it improves agent behavior.

## Neighbor boundaries

| Request | Owner |
| --- | --- |
| Make an application workflow easier to use and implement it | ux-design |
| Improve the type, icon alignment, or visual finish of a bounded component | existing visual UI or focused polish skill |
| Create a public acquisition, campaign, or marketing page | out of scope unless explicitly requested |
| Produce UX findings without implementation | available product UX audit skill |
| Repair installability or standalone PWA viewport mechanics | pwa-app-design |
| Faithfully implement a supplied Figma design | relevant Figma implementation skill |

Use the active request to settle mixed or ambiguous cases. A customer-facing application is still
an application; public audience alone does not make its working screens marketing pages.

## Revision validation

The canonical update passed the repository's `make skill-check` and the Skill Creator package
validator. The UX skill has no source-grounding errors; its existing remote sources retain nine
warnings because they are mutable and have no content checksums.

Six focused live Codex description-routing cases passed: implicit app redesign, explicit invocation,
public operational app, marketing exclusion, audit-only exclusion, and cosmetic-only exclusion.
These are targeted routing checks, not the entire fixture suite or a cross-client result. The
keyword-overlap stub failed its thresholds; it is a harness self-test that cannot understand the
negative boundary language and is not evidence of semantic routing quality. The manual behavior
harness is generated but has no captured outputs, so behavior, execution, and blind A/B comparisons
remain unverified. Coexistence ownership was reviewed against neighboring skill descriptions; no
live portfolio-wide selection score is claimed.

The change adds instructions, UI metadata, references, and evaluation data. It adds no executable
helper, package dependency, credential access, network endpoint, or hidden external write. Application
implementation and browser checks use tools already available in the active product environment.
Canonical changes are reviewable in Git. Consumer refresh is a separate, scoped deployment step;
other installed skills must not be updated merely because the exporter reports newer sources.
