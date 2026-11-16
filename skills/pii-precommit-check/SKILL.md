---
name: pii-precommit-check
metadata:
  version: "0.1.0"
description: Runs the PII pre-commit scan on staged changes or diffs for hardcoded credentials, emails, home paths, and auth files. Use before commits, when about to push, or checking leaked creds.
---

# pii-precommit-check

## Workflow

1. Resolve this installed skill's directory and the target Git repository. Check Python 3 and Git exist. Run `python3 <skill-dir>/scripts/pii_scan.py --repo <repo-root> --staged` using the bundled [scanner](scripts/pii_scan.py). Missing dependencies or scanner errors are not a clean result.
2. If findings exist:
   - stop the commit and list each affected file, line and finding type without its sensitive value
   - propose the repository's existing environment/configuration mechanism or a clearly synthetic test fixture as the replacement; preserve unrelated code
   - apply fixes only within the authorized edit scope, then rescan the Git index after authorized staging; report unresolved findings and scanner errors explicitly
3. The bundled CLI supports staged scans only, skipping binary and over-512-KiB files. For repository-wide validation, use the target repository's established scanner or report that this CLI cannot provide that coverage.
4. Report findings without secret values. A clean scan is not authorization to stage, commit or push. If the user requests automatic protection, inspect the existing hook and `core.hooksPath` first; preserve existing checks and install only the explicitly requested invocation.

## Design

This skill stays intentionally small.

The local scan script owns:

- scanning
- matching and severity rules
- structured findings

The skill owns:

- when to trigger
- which command to run
- how to react to findings

## Hook Installation

To install a pre-commit hook that runs PII scanning automatically:

```bash
python3 <skill-dir>/scripts/pii_scan.py --repo <repo-root> --staged
```

Use the repository's existing hook mechanism if available. Never overwrite a hook. Resolve the installed script path first and explain how to remove only the added invocation.

## Dependencies and provenance

Ported from the author's mythosaur-tools shared skill. The scanner needs only Python 3 and Git; it reads the Git index and emits redacted findings without network access or file changes. Exit codes are 0 for no matches, 1 for findings and 2 for usage/runtime errors. Review the indexed content after authorized staging; a working-tree fix alone does not change the index.
