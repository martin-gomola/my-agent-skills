---
name: delegate-code
metadata:
  version: "0.10.0"
description: Delegates a scoped implementation task to a local Codex, Claude Code or Antigravity CLI in its own git worktree, then reviews the diff and the returned Outcome and Next step. Use when the user asks to hand coding work to Codex, Claude or Antigravity from another agent. Avoid for read-only opinions, image generation, or work the current agent should do itself.
---

# Delegate Code

Use this workflow to give a write task to another local agent while the
calling agent keeps planning and review. The worker edits files in a separate
git worktree. The caller checks the diff before anything reaches the user's
branch. It needs a Git repository and an installed, already-authenticated
worker CLI. It installs nothing and never reads or prints credentials.

| Worker | Good for | Command |
| --- | --- | --- |
| `codex` | Routine implementation, tests, refactors; usually the largest quota | `codex exec` |
| `claude` | Hard design, tricky code, careful review fixes | `claude -p` |
| `agy` | Antigravity with Gemini models; a second opinion in code, or when the others are out of quota | `agy -p` |

Use the worker the user names. If they name none, ask, or pick `codex` for
routine work and `claude` for hard design. Never delegate to the agent you are
running in. Any of these agents, or Cursor, can be the caller; Cursor is never a
worker. Use `second-opinion` for a read-only second opinion and `codex-image` for
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
   - the files the worker may change, as a list of paths or globs, and what
     must not change; step 8 checks the diff against this list;
   - decisions already settled;
   - the exact check command that proves the change;
   - "Do not commit, push, or edit outside this directory.";
   - the required ending, quoted in full:

     ```text
     End your final message with these lines, each separated by a blank line:
     **Status:** DONE, DONE_WITH_CONCERNS, BLOCKED or NEEDS_CONTEXT.
     **Outcome:** one sentence: what changed and whether the check passed.
     **Next step:** none, or the one action left for a human.
     If the brief leaves a choice that would change the result, stop before
     editing and answer NEEDS_CONTEXT with your questions; do not guess.
     Never weaken, skip or delete a test to make the check pass.
     ```

   Leave out credentials, private data, and chat history the task does not need.

   Then reread the brief as the worker. For each item above, find what the
   worker would have to guess and fill it from the repository or this chat.
   If a guess would change the result, ask the user one question before you
   go on. If the brief still needs a step the worker must not take, such as a
   migration, a deletion, or a production or network side effect, take that
   step out or get the user's approval for it first.
3. **Preflight.**
   - Run `which -a <worker>`, `<worker> --version` and the command's `--help`
     (`codex exec --help`, `claude --help` or `agy --help`). Use only flags
     the help lists.
   - Run `git check-ignore -q .delegate-code/x`. If `.delegate-code/` is not
     ignored, ask the user once whether to ignore both working folders of these
     skills in this repository, so `second-opinion` will not ask again. On a
     yes, add the missing ones to the untracked exclude file (or to
     `.gitignore` if the user prefers):

     ```sh
     for d in .second-opinion .delegate-code; do
       git check-ignore -q "$d/x" || echo "$d/" >> "$(git rev-parse --git-path info/exclude)"
     done
     ```
   - Check `git status --short`. The worktree starts from `HEAD`, so
     uncommitted changes are not in it. Tell the user before you continue
     without them.
4. **Create the worktree** inside the ignored folder, so a caller limited to
   the repository can still write it:

   ```sh
   git worktree add -b delegate-code/<slug> .delegate-code/<slug> HEAD
   ```

   Run the brief's check command once in the new worktree before the worker
   starts:
   - If it cannot run, for example because of a missing dependency, a wrong
     path, or a missing script, fix the command in the brief or tell the user.
     Do not send a worker a check it cannot run.
   - If it already passes, it cannot prove the change. Add a test or an
     expected output that fails now, or say in the brief what the check must
     newly show.
   - Note the result as the baseline for step 8.
   - List the files the check depends on: the test files it runs, their
     fixtures, and the config or script that defines the command. Step 8
     needs this list.

5. **Choose the access mode.**
   - **Restricted** (default): the worker can edit files in the worktree and
     run only what it needs.
   - **Full access**: no approvals and no worker sandbox. Use it only when the
     user asks for it for this run, or has stated it as a standing preference
     in their agent instructions. The worktree is then the only boundary, so
     the brief's "do not edit outside this directory" rule and step 8's scope
     check matter more.
6. **Run the worker** from inside the worktree (`cd .delegate-code/<slug>`). Runs can
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
     --max-budget-usd <usd> \
     --output-format json < "$TASK/brief.md" > "$TASK/result.json" 2> "$TASK/worker.log"
   claude -p --permission-mode bypassPermissions --max-budget-usd <usd> \
     --output-format json < "$TASK/brief.md" > "$TASK/result.json" 2> "$TASK/worker.log"
   ```

   `result.json` holds the final message in `result` and the session id in
   `session_id`. In restricted mode, add one `--allowedTools` entry for each
   command the worker must run.

   **Spend cap.** Use the limit the user gives; without one, use `5`. Several
   delegations share one total: split it so the caps add up to no more than
   the user's limit. A run stopped by the cap is a failed run; report it as
   that and do not raise the cap without asking. Codex and Antigravity have no
   spend flag, so the watchdog's time limit below is their only cap; say so
   when the user asked for a spend limit.

   **Antigravity**, restricted, then full access. `agy` takes the prompt as the
   `-p` argument, not on stdin:

   ```sh
   agy --mode accept-edits --sandbox --print-timeout 1800s --output-format json \
     --settings '{"permissions":{"allow":["command(<program>)"]}}' \
     -p="$(cat "$TASK/brief.md")" > "$TASK/result.json" 2> "$TASK/worker.log"
   agy --dangerously-skip-permissions --print-timeout 1800s --output-format json \
     -p="$(cat "$TASK/brief.md")" > "$TASK/result.json" 2> "$TASK/worker.log"
   ```

   `result.json` holds the final message in `response` and the session id in
   `conversation_id`. In restricted mode, allow each program the worker must
   run, such as `command(npm)` for `npm test`; the rule matches the program name.
   A denied command shows in `denied_actions` and can leave `response` empty.

   **Watchdog.** A worker that writes only to files gives no sign of life:
   `claude -p` prints nothing until its final answer, so a hung run and a
   working one both look like an empty file. Give every run a hard limit by
   prefixing the command with `perl -e 'alarm shift; exec @ARGV' 1800`
   (seconds; `timeout 1800` works too where installed). Then classify the run:
   - `ok`: exit 0 and a non-empty final message;
   - `empty`: exit 0 but no final message;
   - `timeout`: exit 142 (`perl`) or 124 (`timeout`);
   - `failed`: any other exit code; read the tail of `worker.log`.

   Treat anything but `ok` as a failed run. Do not wait on an empty file past
   the limit.

   **Run note.** When the run starts, write `.delegate-code/<slug>.run` next to
   the worktree (not inside it, so the diff stays clean) with four lines:
   `worker=<name>`, `task=<$TASK>`, `started=<UTC time>` and `pid=<PID>`
   (from `$!` when you start it with `&`; leave it empty if the host does not
   show it). The status check below reads it. Delete it with the worktree.

   If the worker fails or hits its usage limit, report that and stop. Do not
   switch to another agent or API.

   - **Caller sandbox.** The worker writes its own state (`~/.codex`,
     `~/.claude` or `~/.gemini`) and needs network access to its service. Under a sandboxed
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
7. **Read the result** from `last.md` (Codex), `result` in `result.json`
   (Claude) or `response` in `result.json` (Antigravity). Take the `Status`,
   `Outcome` and `Next step` lines. If they are missing, treat the run as
   unverified rather than failed. Act on the status:
   - `DONE`: go on to step 8.
   - `DONE_WITH_CONCERNS`: go on to step 8 and check each concern there.
   - `NEEDS_CONTEXT`: answer the questions from the repository or this chat,
     or ask the user, then send the answers as the correction below. Do not
     resend the same brief unchanged.
   - `BLOCKED`: report the blocker to the user and stop. Do not retry the
     same worker with the same brief.
8. **Verify it yourself.** Do not rely on the worker's report:
   - check scope with `git -C .delegate-code/<slug> status --short` and
     `git -C .delegate-code/<slug> diff`, and confirm `git status --short` in the main
     checkout shows no new changes;
   - list every changed file outside the brief's list of files the worker may
     change; review each one and report it, even when the edit looks harmless;
   - run the brief's check command in the worktree and compare it with the
     baseline from step 4;
   - if the diff touches a file the check depends on (the list from step 4),
     review those edits first: a weakened, skipped or deleted test makes a
     passing check prove nothing. Say so in the report;
   - review the diff against the brief, since this review is what the caller is for.

   **Independent review.** The caller planned the task, so it is not a neutral
   reviewer. When the user asks for an independent review, or the change is
   risky (security, data, a public API), also run `second-opinion` with a provider that
   is neither the worker nor you. Save the diff with
   `git -C .delegate-code/<slug> add -A && git -C .delegate-code/<slug> diff --cached > "$TASK/diff.patch"`
   and give the reviewer three files: `brief.md`, the worker's final message
   and `diff.patch`. Ask for two separate answers:
   - **Brief:** met, not met, or cannot verify from the diff, for each done
     criterion;
   - **Findings:** each marked Critical, Important or Minor, with file and line.

   Treat its findings as input to your review, not a verdict. Correct only
   confirmed Critical and Important findings and unmet criteria; list Minor
   ones in the report.
   Plausible but wrong findings are the most common review failure, so
   confirm each one in the code, or with a failing test or command, before
   you put it in a correction or a report. Drop what you cannot confirm, or
   label it unverified.

   If something misses the brief, send one short correction to the same
   session from inside the worktree, so the worker keeps its context:

   ```sh
   codex exec resume <access flag> -o "$TASK/last.md" <thread_id> - < "$TASK/fix.md"
   claude -p <access flags> --resume <session_id> --output-format json \
     < "$TASK/fix.md" > "$TASK/result.json"
   agy --conversation <conversation_id> <access flags> --output-format json \
     -p="$(cat "$TASK/fix.md")" > "$TASK/result.json"
   ```

   Antigravity returns a new `conversation_id` after each resume; use the latest.

   For Codex, the restricted access flag is `-c 'sandbox_mode="workspace-write"'`,
   because `resume` has no `--sandbox` flag. Use the same access mode as the
   first run. If it still misses, stop and report what is left.

   **Fingerprint the reviewed state.** Once the worker has exited and your
   review is done, record a hash of the whole worktree, untracked files
   included:

   ```sh
   git -C .delegate-code/<slug> add -A && git -C .delegate-code/<slug> write-tree
   ```

   Staging in the worktree commits nothing.
9. **Report** the worker, access mode, branch, worktree path, the worker's Status and
   Outcome, your own check result, your review findings, and the fingerprint. Do not merge,
   commit, push, or remove the worktree until the user says so. When the user
   approves, run the fingerprint command again first. If the hash differs, the
   worktree changed after review: stop, show what changed, and review again
   before merging. Otherwise merge the branch or apply the diff, then run the
   brief's check command again in the main checkout: `HEAD` may have moved
   since the worktree was created, so the merged result is new code. If it
   fails, stop, keep the worktree and branch, and report the failure. If it
   passes, run `git worktree remove .delegate-code/<slug>`, delete the run note and the
   branch. Keep the task directory until the user is done with it.

## Check on delegations

When the user asks how a delegation is going, or what is left in
`.delegate-code/`, read each `.delegate-code/*.run` note and its worktree. Only
read; change nothing.

- **Progress.** Report the time since `started` and the files changed so far
  (`git -C .delegate-code/<slug> status --short`), which works for every
  worker. For Codex, also give the last step from the tail of
  `$TASK/events.jsonl` in plain words, such as "ran the tests" or "edited
  src/list.py". Claude and Antigravity write nothing until they finish.
- **State.**
  - `running`: `pid` is set and `kill -0 <pid>` succeeds;
  - `finished`: the final message exists (`last.md` or `result.json` in
    `task`) and is not yet reviewed or merged;
  - `abandoned`: no live process, no final message, and the time limit has
    passed;
  - `unknown`: anything else, including a worktree with no note. Never call
    it abandoned without that evidence.
- **Cleanup.** List what each finished or abandoned worktree holds (changes,
  commits, or nothing) and offer to review, keep, or remove it. Remove a
  worktree, its branch, and its note only after the user says so, and never one
  that is `running` or `unknown`.

## Several delegations

**Split only when it pays.** Keep a request as one delegation when one
worker can finish it within the watchdog limit and its parts share most of
their files. Split it when the parts touch separate files and can run in
parallel, or when one run would be too large to review as one diff. Each
extra task costs a brief, a worktree and a review, so do not split for
neatness.

When one request becomes more than one delegation, write `$TASK/plan.md`
before any worktree exists. List each task with its slug, its files (the
same list its brief carries) and the slugs it depends on.

- If two tasks list the same file, make one depend on the other. Never run
  them at the same time.
- A task with no dependencies starts from `HEAD`. A dependent task starts
  only after each task it depends on is reviewed and merged, from the branch
  that holds those merges, so it sees their code.
- Run independent tasks in parallel, each through steps 2 to 9 on its own.
- If a task fails or is blocked, do not start the tasks that depend on it.
  Report them as not started.
- **Progress notes.** When a task is merged, fails or is blocked, add one
  line under `## Done` in `plan.md`: the slug, its state, and what a later
  task must know, such as a new function name, a changed interface or a trap
  the worker hit. Before you write a dependent task's brief, read those lines
  and put the ones it needs into the brief. Its worker cannot see the earlier
  runs.

## Boundaries

- One task per worktree, each on its own branch.
- The worker edits only inside its worktree. The caller does all merging.
- Tools that scan the whole checkout, such as test discovery or linters, may
  also pick up `.delegate-code/`. Exclude it there if it gets in the way.
- Each worker's usage, quota, and data handling follow the user's account for
  that service. Delegating sends the brief and the repository files the worker
  reads to that service.
