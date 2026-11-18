---
name: relay
metadata:
  version: "0.2.0"
description: Delegates a scoped implementation task to a local Codex or Claude Code CLI in its own git worktree, then reviews the diff and the returned Outcome and Next step. Use when the user asks to hand coding work to Codex or Claude from another agent. Avoid for read-only opinions, image generation, or work the current agent should do itself.
---

# Relay

Use this workflow to give a write task to another local agent while the
calling agent keeps planning and review. The worker edits files in a separate
git worktree. The caller checks the diff before anything reaches the user's
branch. It needs a Git repository and an installed, already-authenticated
worker CLI. It installs nothing and never reads or prints credentials.

| Worker | Good for | Command |
| --- | --- | --- |
| `codex` | Routine implementation, tests, refactors; usually the largest quota | `codex exec` |
| `claude` | Hard design, tricky code, careful review fixes | `claude -p` |

Use the worker the user names. If they name none, ask, or pick `codex` for
routine work and `claude` for hard design. Never delegate to the agent you are
running in. Use `ask` for a read-only second opinion and `codex-image` for
images.

## Workflow

1. **Confirm the handoff.** Delegate only when the user asked another agent to
   do the work. Ask before delegating if the task is unclear, touches secrets or
   production, or needs decisions nobody has made yet.
2. **Write the brief** in `brief.md` in a new temporary directory outside the
   repository (`mktemp -d`, use its absolute path as `$TASK`). Use
   `what-to-ask` if it is installed. The brief must stand on its own, because
   the worker sees none of this chat. It states:
   - the goal and the done criteria;
   - the files or area in scope and what must not change;
   - decisions already settled;
   - the exact check command that proves the change;
   - "Do not commit, push, or edit outside this directory.";
   - the required ending, quoted in full:

     ```text
     End your final message with these lines, each separated by a blank line:
     **Outcome:** one sentence: what changed and whether the check passed.
     **Next step:** none, or the one action left for a human.
     ```

   Leave out credentials, private data, and chat history the task does not need.
3. **Preflight.**
   - Run `which -a <worker>`, `<worker> --version` and the command's `--help`
     (`codex exec --help` or `claude --help`). Use only flags the help lists.
   - Run `git check-ignore -q .relay/x`. If `.relay/` is not ignored, ask the
     user before adding it to `.gitignore` or the untracked
     `.git/info/exclude`.
   - Check `git status --short`. The worktree starts from `HEAD`, so
     uncommitted changes are not in it. Tell the user before you continue
     without them.
4. **Create the worktree** inside the ignored folder, so a caller limited to
   the repository can still write it:

   ```sh
   git worktree add -b relay/<slug> .relay/<slug> HEAD
   ```

5. **Choose the access mode.**
   - **Restricted** (default): the worker can edit files in the worktree and
     run only what it needs.
   - **Full access**: no approvals and no worker sandbox. Use it only when the
     user asks for it for this run, or has stated it as a standing preference
     in their agent instructions. The worktree is then the only boundary, so
     the brief's "do not edit outside this directory" rule and step 7's scope
     check matter more.
6. **Run the worker** from inside the worktree (`cd .relay/<slug>`). Runs can
   be long, so start them in the background when the host supports that.

   **Codex**, restricted, then full access:

   ```sh
   codex exec --sandbox workspace-write --json -o "$TASK/last.md" - \
     < "$TASK/brief.md" > "$TASK/events.jsonl" 2> "$TASK/worker.log"
   codex exec --dangerously-bypass-approvals-and-sandbox --json \
     -o "$TASK/last.md" - < "$TASK/brief.md" > "$TASK/events.jsonl" 2> "$TASK/worker.log"
   ```

   The session id is `thread_id` in the `thread.started` event of
   `events.jsonl`.

   **Claude**, restricted, then full access:

   ```sh
   claude -p --permission-mode acceptEdits --allowedTools "Bash(<check command>)" \
     --output-format json < "$TASK/brief.md" > "$TASK/result.json" 2> "$TASK/worker.log"
   claude -p --permission-mode bypassPermissions \
     --output-format json < "$TASK/brief.md" > "$TASK/result.json" 2> "$TASK/worker.log"
   ```

   `result.json` holds the final message in `result` and the session id in
   `session_id`. In restricted mode, add one `--allowedTools` entry for each
   command the worker must run.

   If the worker fails or hits its usage limit, report that and stop. Do not
   switch to another agent or API.

   - **Caller sandbox.** The worker writes its own state (`~/.codex` or
     `~/.claude`) and needs network access to its service. Under a sandboxed
     caller, such as Claude Code's sandbox or Codex in `workspace-write`
     without network, it fails with `Operation not permitted` or connection
     errors. Run it outside the caller's sandbox with the user's approval.
   - **Model.** `model_not_found` or "not supported with a ChatGPT account"
     usually means an outdated CLI, not a wrong model: an old binary earlier
     on `PATH` does not know the newer models. Compare the `which -a` results
     and their versions, run the newest one, and tell the user which old one
     shadows it. Keep the user's default model. Pass `-m` or `--model` only
     when the user names a model, and never edit the worker's config.
   - **Log noise.** Transport errors about unreachable MCP servers come from
     the worker's own config and do not fail the run. Judge the run by the
     exit code and the final message.
7. **Read the result** from `last.md` (Codex) or `result` in `result.json`
   (Claude). Take the `Outcome` and `Next step` lines. If they are missing,
   treat the run as unverified rather than failed.
8. **Verify it yourself.** Do not rely on the worker's report:
   - check scope with `git -C .relay/<slug> status --short` and
     `git -C .relay/<slug> diff`, and confirm `git status --short` in the main
     checkout shows no new changes;
   - run the brief's check command in the worktree;
   - review the diff against the brief, since this review is what the caller is for.

   If something misses the brief, send one short correction to the same
   session from inside the worktree, so the worker keeps its context:

   ```sh
   codex exec resume <access flag> -o "$TASK/last.md" <thread_id> - < "$TASK/fix.md"
   claude -p <access flags> --resume <session_id> --output-format json \
     < "$TASK/fix.md" > "$TASK/result.json"
   ```

   For Codex, the restricted access flag is `-c 'sandbox_mode="workspace-write"'`,
   because `resume` has no `--sandbox` flag. Use the same access mode as the
   first run. If it still misses, stop and report what is left.
9. **Report** the worker, access mode, branch, worktree path, the worker's
   Outcome, your own check result, and your review findings. Do not merge,
   commit, push, or remove the worktree until the user says so. When the user
   approves, merge the branch or apply the diff, then run
   `git worktree remove .relay/<slug>` and delete the branch. Keep the task
   directory until the user is done with it.

## Boundaries

- One task per worktree. Parallel relays get separate branches and must not
  touch the same files.
- The worker edits only inside its worktree. The caller does all merging.
- Tools that scan the whole checkout, such as test discovery or linters, may
  also pick up `.relay/`. Exclude it there if it gets in the way.
- Each worker's usage, quota, and data handling follow the user's account for
  that service. Delegating sends the brief and the repository files the worker
  reads to that service.
