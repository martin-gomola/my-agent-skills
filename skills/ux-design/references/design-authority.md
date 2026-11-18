# Design Authority

Load this reference only when creating or revising `DESIGN.md`, reconciling token ownership, or
promoting a durable design decision.

## Authority model

1. Accessibility, safety, and platform requirements.
2. Repository `DESIGN.md` and documented feature exceptions.
3. Canonical repository tokens, primitives, and content contracts.
4. Existing implementation as evidence to reconcile.
5. Shared defaults where local authority is silent.

Product identity remains local. Shared guidance may own minimum quality, evidence, and single-owner
discipline, but not a universal palette, typography, density, navigation, or component inventory.

Authority is not quality certification. When a documented token, component, or composition conflicts
with observed task failure, accessibility, content fit, or rendered evidence, classify it as stale
guidance, implementation debt, or a bounded exception. Preserve the product identity and stable
contracts, not the failing expression.

## Creating a local contract

Copy `assets/DESIGN.md`, remove irrelevant sections, and fill it from inspected repository and product
evidence. Mark unknowns as open questions. Do not invent user research, supported devices,
accessibility results, brand assets, or runtime constraints.

Record:

- users, jobs, product goals, non-goals, and trust signals;
- information architecture and core flows;
- visual roles, density, typography, motion, and content voice;
- token, primitive, shell, and generated-output owners;
- states, responsive behavior, accessibility, and validation evidence;
- bounded exceptions with rationale, owner, verification, and removal condition.

## Reconciling drift

Classify a mismatch as implementation drift, stale documentation, or intentional exception. Choose
one canonical repository token owner. Preserve product values there, replace duplicate declarations
with token consumption, document necessary literals, and add a deterministic regression check that
rejects competing owners or raw brand values outside bounded exceptions.

Verify all affected themes, responsive surfaces, generated outputs, and fallbacks. Update the local
contract when ownership or supported behavior changes.

## Promotion boundary

Promote a rule across products only when the user establishes it as shared or it repeatedly protects
a cross-project invariant. Promote the portable principle and acceptance check, not a product's
values or visual expression. Do not rewrite unrelated repositories while updating shared guidance.
