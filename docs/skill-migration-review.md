# Shared helper migration

Authoring review on 2026-11-16. Imported from the author's mythosaur-tools
`skills/shared/` at source checkout HEAD `a846d5a5d3e9b6f08bf6211a03815a28f674761c`.
The source checkout was read, not changed. Existing local installer edits were preserved.

## Scope and package boundaries

Each helper keeps its name, source directory, trigger/evaluation fixtures and a
separate native plugin. New adapter versions start at `0.1.0`. The existing
`my-agent-skills` plugin remains the adapter for `what-to-ask` for compatibility;
none of these helpers installs or activates `your-turn-handoff`.

| Skill | Dependencies and effects | Migration work |
| --- | --- | --- |
| clean-cursor | Local filesystem, SQLite, optional OS process control; cleanup requires an exact approved plan | Removed nonportable origin frontmatter; retained read-only inspection and recovery gates |
| pii-precommit-check | Python 3 and Git; reads the target index, outputs redacted findings | Bundled scanner; replaced Mythosaur server clock import with stdlib; corrected unsupported whole-repo command and unsafe hook overwrite example |
| ask | Python 3, Git, selected authenticated Claude or Antigravity CLI; sends scoped prompt to provider, writes ignored audit artifacts | Bundled existing runner and tests; declared dependencies; requested concise advisor output |
| codex-image | Authenticated Codex CLI with actual image-generation capability, filesystem and visual inspection | Removed missing internal evidence link; limited automatic correction to one attempt |
| stop-slop | Instructions and focused prose references; no external runtime required | Retained pattern references, pinned source snapshots/checksums and upstream MIT notices |

The PII scanner skips binaries and files above 512 KiB and honors `pii:allow`.
It is a heuristic gate, not a proof that a repository contains no secrets. Scanner
success never authorizes staging, committing or pushing. Hooks are opt-in and must
preserve existing checks. No real Cursor data, external CLI session or user Git
hook was modified during this migration.

## NotebookLM consultation

Notebook: [DEV: Prompts](https://notebook.google.com/notebook/7eab7e5c-0f7c-4242-a2e2-b92be5839586).
Each skill received a separate consultation. Long requests rejected by the service
were replaced with bounded summaries. Notebook responses are advisory draft output,
not authority for CLI flags, Cursor database schemas or real execution evidence.

| Skill | Reviewed advice and disposition |
| --- | --- |
| clean-cursor | Applied explicit inspect/approve/execute/verify phases, compact metadata-only reporting, UUID validation, parameterized SQL and path/symlink checks. Cursor details still require local verification during use. |
| pii-precommit-check | Applied dependency checks, structured redacted findings, repository-specific remediation, explicit index rescan and preservation of existing hooks. Ordinary fixes stay within the user's authorized edit scope. |
| ask | Applied a Markdown findings/evidence/uncertainty contract, default prompt response budget, acceptance criteria and explicit escalation for unresolved high-impact disagreements or exhausted retries. Raw output stays intact. A JSON parser is unnecessary for the existing human-readable artifact. |
| codex-image | Removed unavailable local references, bounded correction to one attempt and made positive scene descriptions lead the prompt. Meaningful user exclusions remain supported. |
| stop-slop | Applied internal audit/edit/compare passes and separated original text, author instructions and output contract for delegated prompts. Audit-only mode still stops before rewriting; user-facing prose does not acquire mandatory XML markup. |

Relevant notebook sources include *Building Effective AI Agents* (Anthropic),
*a-practical-guide-to-building-agents.pdf*, *Prompt engineering overview*, and
*Context Engineering - Claude-Mem*. Their general prompting guidance does not
establish tool compatibility. Existing stop-slop normative source mappings remain
in its own `sources.yaml` and `grounding.yaml`.

## Verification and limits

- Repository manifest, provenance, private-content and snapshot checks run through `make test`.
- Existing trigger and behavior fixtures are preserved as rubrics; no live model
  baseline or multi-client activation evaluation is claimed.
- Existing ask runner tests pass (9 cases, mocked provider execution).
- A disposable Git repository confirmed clean staged data passes, indexed token
  data blocks even when the working tree is clean, and output redacts the token.
- The installer route tests cover every skill and all five client selections.
- No consumer installation, commit, push or deployment is part of this migration.

Rollback before publication: remove the five source folders and adapters plus
their marketplace/catalog entries, then regenerate snapshots. Preserve unrelated
local site edits when doing so.
