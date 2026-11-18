# Work across agents

Three skills cover one loop: write the brief, delegate it, and bring the result
back as the next step. Install each one only in the agents where you need it.

| Step | Skill | What moves | Who moves it |
| --- | --- | --- | --- |
| Brief | [what-to-ask](../skills/what-to-ask/SKILL.md) | Rough notes or another agent's result become a self-contained prompt. | The agent drafts it. |
| Delegate a read-only opinion | [ask](../skills/ask/SKILL.md) | The prompt goes to the local `claude` or `agy` CLI. | The agent runs the CLI. |
| Delegate an image | [codex-image](../skills/codex-image/SKILL.md) | An image brief goes to the local `codex exec`. | The agent runs the CLI. |
| Delegate implementation to Codex | [relay](../skills/relay/SKILL.md) | The prompt goes to `codex exec` in a new git worktree; the caller reviews the diff. | The agent runs the CLI. |
| Delegate implementation elsewhere | none | The prompt goes into another agent's chat. | You paste it. |
| Result | [your-turn-handoff](handoff.md) | The recipient ends with `Outcome` and `Next step`. | The recipient writes it. |
| Next step | what-to-ask | The pasted result becomes the next prompt. | You paste it back. |

## Example

1. In Cursor: "Use what-to-ask to write a prompt for Codex that adds the CSV
   export button in Atlas." The prompt asks Codex to end with a short report.
2. Paste the prompt into Codex. With your-turn-handoff installed there, its
   answer ends with `Outcome`, `Next step`, and later `Recap` and `Decision`.
3. Paste that block into any agent and ask what-to-ask for the follow-up prompt.
   Settled decisions and unverified results carry over without retelling the chat.
4. For a second opinion before merging, ask `$ask claude` to review the change.
   The calling agent receives the result and an audit file under `.ask/`,
   with no copy and paste. The runner writes there only when Git ignores it.

## What still needs you

- Only `relay` sends a write task, and only to Codex, in a separate worktree
  that you merge yourself. No skill types into another chat. `ask` runs its
  advisor read-only, and `codex-image` only produces images.
- Each `ask` call starts a new CLI process. For Claude, a follow-up can continue
  the same conversation with `--resume <session_id>` from the earlier result;
  Antigravity calls always start fresh.
- No skill reads another agent's chat history. Results travel only as text you
  paste, a file the runner writes, or the CLI output returned to the caller.
- The [Your Turn inbox](https://github.com/martin-gomola/your-turn) shows which
  chats wait on you. These skills do not use it to pass messages between agents.
- Approving consequential steps, choosing what to delegate, and judging the
  advisor's claims stay with you and the calling agent.
