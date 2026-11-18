---
name: relay
metadata:
  version: "0.1.0"
description: Delegates a scoped implementation task from Claude or Cursor to a local Codex CLI in its own git worktree, then reviews the diff and the returned Outcome and Next step. Use when the user asks to hand coding work to Codex. Avoid for read-only opinions, image generation, or work the current agent should do itself.
---

# Relay

Use this workflow to give Codex a write task while the calling agent keeps
planning and review. Codex does the edits in a separate git worktree. The
caller checks the diff before anything reaches the user's branch. It needs an
installed, already-authenticated `codex` CLI and a Git repository. It installs
nothing and never reads or prints credentials.

Use `ask` for a read-only second opinion and `codex-image` for images.

## Workflow

1. **Confirm the handoff.** Delegate only when the user asked for Codex to do
   the work. Ask before delegating if the task is unclear, touches secrets or
   production, or needs decisions nobody has made yet.
2. **Write the brief** in `brief.md` in a new temporary directory outside the
   repository (`mktemp -d`). Use `what-to-ask` if it is installed. The brief
   must stand on its own, because Codex sees none of this chat. It states:
   - the goal and the done criteria;
   - the files or area in scope and what must not change;
   - decisions already settled;
   - the exact check command that proves the change;
   - "Do not commit, push, or edit outside this worktree.";
   - the required ending, quoted in full:

     ```text
     End your final message with these lines, each separated by a blank line:
     **Outcome:** one sentence: what changed and whether the check passed.
     **Next step:** none, or the one action left for a human.
     ```

   Leave out credentials, private data, and chat history the task does not need.
3. **Preflight.** Run `which -a codex`, `codex --version` and `codex exec --help`. Use only the
   flags the help lists. Check `git status --short`. The worktree starts from
   `HEAD`, so uncommitted changes in the caller's tree are not in it. Tell the
   user before you continue without them.
4. **Create the worktree** next to the repository on a new branch:

   ```sh
   git worktree add -b relay/<slug> ../<repo>-relay-<slug> HEAD
   ```

5. **Run Codex** with its root set to the worktree and the least access needed:

   ```sh
   codex exec --sandbox workspace-write -C ../<repo>-relay-<slug> \
     -o "$TASK/last.md" - < "$TASK/brief.md" > "$TASK/codex.log" 2>&1
   ```

   Runs can be long, so start it in the background when the host supports
   that. Never add `--dangerously-bypass-approvals-and-sandbox` or broader
   filesystem access. If Codex fails or hits its usage limit, report that and
   stop. Do not switch to another agent or API.

   - **Caller sandbox.** Codex must write its own state under `~/.codex` and
     reach its service. Under a sandboxed host shell, such as Claude Code's,
     it fails with `Operation not permitted`. Run the command outside the host
     sandbox with the user's approval. Codex's own `workspace-write` sandbox
     still limits it to the worktree. Use absolute paths for `$TASK`, because
     the temporary directory can differ outside the sandbox.
   - **Model.** `model_not_found` or "not supported with a ChatGPT account"
     usually means an outdated CLI, not a wrong model: an old binary earlier
     on `PATH` does not know the newer models. Compare
     `which -a codex` with each binary's `--version`, run the newest one, and
     tell the user which old one shadows it. Keep the user's default model.
     Pass `-m` only when the user names a model, and never edit their Codex
     config.
   - **Log noise.** `rmcp` transport errors about unreachable MCP servers come
     from the user's Codex config and do not fail the run. Judge the run by the
     exit code and `last.md`.
6. **Read the result** from `last.md`. Take the `Outcome` and `Next step`
   lines. If they are missing, treat the run as unverified rather than failed.
   Use `codex.log` only to diagnose a failure.
7. **Verify it yourself.** Do not rely on Codex's report:
   - check scope with `git -C <worktree> status --short` and `git -C <worktree> diff`;
   - run the brief's check command in the worktree;
   - review the diff against the brief, since this review is what the caller is for.

   If something misses the brief, run Codex once more in the same worktree
   with a short correction brief. If it still misses, stop and report what is
   left.
8. **Report** the branch, the worktree path, Codex's Outcome, your own check
   result, and your review findings. Do not merge, commit, push, or remove the
   worktree until the user says so. When the user approves, merge the branch
   or apply the diff, then run `git worktree remove` on the worktree. Keep the
   task directory until the user is done with it.

## Boundaries

- One task per worktree. Parallel relays get separate branches and must not
  touch the same files.
- Codex works only inside its worktree sandbox. The caller does all merging.
- Codex's usage, quota, and data handling follow the user's Codex account.
  Delegating sends the brief and the repository files Codex reads to that
  service.
