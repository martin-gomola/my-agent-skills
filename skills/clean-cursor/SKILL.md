---
name: clean-cursor
metadata:
  version: "0.1.0"
description: Safely inspects and cleans Cursor IDE storage, including caches, agent CLI downloads, workspace state, SQLite data, and a specific chat by ID. Use for Cursor disk cleanup or when a broken Cursor chat still appears in Cursor or the Your Turn inbox; avoid unrelated application or project cleanup.
---

# Clean Cursor storage

Ported from the author's mythosaur-tools shared skill. Requires local filesystem and SQLite access; OS application control is needed only for approved cleanup. No MCP is required.

Run this workflow when the user asks how to free Cursor disk space, inspect Cursor storage, or clean Cursor files. The user may invoke it as `$clean-cursor`.

An informational question (for example, “how do I clean Cursor?”) authorizes read-only inspection and advice, not deletion. Before any deletion, inspect the relevant paths and present the exact targets, sizes, expected space reclaimed, and effects; get explicit confirmation immediately before closing Cursor or changing files. A request to create or install this skill is not authorization to inspect or clean the user's Cursor installation.

## Remove one chat by ID

Use this branch when the user names a Cursor chat/composer UUID or says a broken Cursor chat still appears in the Your Turn inbox.

Validate the composer ID as one complete UUID before resolving paths or building queries. Resolve the target directory under the inspected transcript root and stop if it escapes that root, is a symlink to another location, or matches more than one candidate. Bind UUIDs as SQLite parameters rather than interpolating SQL.

- First distinguish the requested outcome: hide the item from Your Turn while retaining the Cursor chat, or remove the chat and its local transcript. Do not treat “remove from the UI” as permission to delete Cursor history.
- Your Turn discovers Cursor sessions from `~/.cursor/projects/*/agent-transcripts/<composerId>/<composerId>.jsonl`, with related files potentially nested below that composer directory. Removing only the `composerHeaders` row from `state.vscdb` does not remove this transcript source, so Your Turn can continue to list the chat.
- Locate the exact composer directory by UUID and inspect its file count and total bytes without printing transcript contents. Also check whether `composerHeaders` has the UUID. Report the exact paths and which source records exist; do not print stored values.
- If the user wants only the Your Turn item hidden, preserve Cursor's `state.vscdb` entry. Use a Your Turn hide/archive action if the current app provides one. Otherwise explain that moving the transcript directory out of Cursor's discovery path also moves the local transcript source; offer a recoverable move to the OS Trash, or ask whether the user instead wants permanent local chat deletion. Do not delete the transcript to simulate a reversible hide.
- If the user explicitly wants the chat deleted from Cursor's local history, include both the matching `composerHeaders` row and the exact transcript directory in the approved plan. State that deleting the transcript can remove local conversation history and may affect tools that read Cursor agent transcripts. Leave `ItemTable` rows untouched unless their schema identifies a precise, approved target; an ID match inside a value alone is not sufficient.
- Before approval, show the UUID, exact database and transcript paths, database/sidecar sizes, composer-header match count, transcript file count/bytes, backup files, temporary-space estimate, and whether the action is recoverable. Do not close Cursor or move/delete either source until the user approves that specific plan.
- After approval, close Cursor cleanly, verify no Cursor process holds the target files, and move only the exact composer directory to the OS Trash when the user chose a recoverable hide. For permanent deletion, remove only the approved UUID-matched records and directory. Preserve unrelated files and transcripts outside that exact directory.
- Verify the composer ID is absent from the intended source(s), then verify the Your Turn inbox no longer returns it if that app is running. If Cursor or Your Turn is open, refresh it only after source verification. Report any opaque `ItemTable` reference left behind.

## Inventory and classify

Keep the phases explicit: inspect metadata → present exact targets and recovery plan → obtain approval → execute → verify. If the schema differs from the expected layout, Cursor still holds the files, or any integrity/backup check fails, stop before mutation. Return a compact inventory of paths, byte counts, row counts and candidate effects; never load raw transcripts merely to populate the report.

- Detect the OS and resolve Cursor's user-data root. Common roots are macOS `~/Library/Application Support/Cursor`, Windows `%APPDATA%/Cursor`, and Linux `~/.config/Cursor`. If Cursor is installed elsewhere, search only likely Cursor configuration roots and report the selected path.
- Inventory sizes for the root's `Cache`, `CachedData`, `User/workspaceStorage`, and `User/globalStorage`. Within `globalStorage`, identify the largest immediate subdirectories. In particular, `anysphere.cursor-agent-worker/agent-cli` can contain downloaded CLI releases and temporary extraction directories; treat these as managed runtime files, not generic cache.
- Classify `Cache` and `CachedData` as generally rebuildable. Explain that clearing them can cause cache rebuilds or downloads. Do not claim every file in `globalStorage` is disposable.
- Treat `workspaceStorage` as editor/workspace state; do not recommend deleting it wholesale. Inspect and report its largest entries only when useful, without exposing workspace contents.
- For downloaded agent CLI versions, inspect version and `.tmp-*` directory sizes and dates. Do not delete version directories or temporary downloads based only on their names or age; list exact proposed paths and get explicit approval first. Never remove the whole `anysphere.cursor-agent-worker` directory as a generic cleanup step.
- For `User/globalStorage/state.vscdb`, confirm it exists and is SQLite. Inspect its schema with `PRAGMA table_info` and count rows in `cursorDiskKV` and `ItemTable` when present. Do not print stored values; keys or values may contain private prompts or workspace data.
- Report sizes of `state.vscdb`, `state.vscdb-wal`, `state.vscdb-shm`, `state.vscdb.bak`, and `state.vscdb.backup` if present. Do not assume backups are disposable.
- Do not infer that `ItemTable` rows are old from key names or values. Delete rows only when the schema has a clear timestamp/age field and the user approved a specific cutoff; otherwise leave `ItemTable` intact and state that its age cannot be safely determined.

Present a concise inventory and rank cleanup candidates by likely space reclaimed and risk. Do not clean the database merely because the user asked to clean caches, or clean caches merely because the user asked about the database.

## Clean rebuildable caches

After the user approves the exact cache paths, close Cursor cleanly and recheck it has exited before deleting. Remove only the approved `Cache` or `CachedData` contents; do not use broad wildcards over the Cursor user-data root. Report sizes before and after and note that Cursor may rebuild or download these files.

## Clean agent CLI downloads

After the user approves an exact list of agent CLI paths, close Cursor and confirm it has exited. Remove only those listed version or temporary directories. Do not infer which release is active, and do not remove a version directory merely because a newer-looking version exists. Report exact paths and bytes removed. If active-use status cannot be established, leave version directories in place and explain the uncertainty.

## Clean the SQLite state database

After the user approves the displayed plan:

1. Close Cursor cleanly where possible. If processes remain, identify them and ask for confirmation before terminating them. On macOS, the requested `killall Cursor "Cursor Helper"` may be used after confirmation; handle the no-processes-found result normally. Use the corresponding process manager on other operating systems. Recheck that Cursor has exited before opening the database for writes.
2. Open the database with SQLite and run an integrity check before mutation. If it fails, stop and preserve all files.
3. In a transaction, delete a `composerHeaders` row only with `WHERE composerId = <approved UUID>` and only if that row was included in the approved plan. Require the affected row count to match the inspected count. Clear `cursorDiskKV` only if it exists and the user approved deleting its contents. Delete `ItemTable` rows only under the approved timestamp cutoff described above. Commit only after the statements and affected row counts match the approved plan; otherwise roll back.
4. Create a uniquely named temporary database in the same directory using SQLite `VACUUM INTO`. Do not overwrite an existing file. Run `PRAGMA integrity_check` on the output and stop without replacing the original if it does not return `ok`.
5. Replace the original database only after the vacuumed copy passes validation. Keep the original recoverable until the replacement is verified; restore it if replacement verification fails. Close every SQLite connection before handling `-wal` or `-shm` files. Remove sidecars only after confirming Cursor is stopped and SQLite has safely consolidated committed data.
6. Remove `state.vscdb.bak` and `state.vscdb.backup` only after the replacement passes validation and the user approved their deletion. Never delete unrelated files or wildcard-matched backups.
7. Report database sizes before and after, total bytes reclaimed (including deleted backup/sidecar files when measurable), which tables were changed, and the validation result. If free space prevents creating the temporary copy, stop and explain the required space; do not delete the original to make room.

Prefer SQLite's backup API or an explicitly named recovery copy when making a separate backup. Do not place a full extra copy in globalStorage without explaining the temporary disk-space cost. Never run cleanup commands on a database path that has not been shown to and confirmed by the user.
