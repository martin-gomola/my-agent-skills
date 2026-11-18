# your-turn-handoff

Add a consistent result and next step to agent replies.

```text
**Outcome:** The CSV export includes only the filtered rows; relevant tests passed.

**Next step:** none
```

The skill ends final answers with **Outcome** and **Next step**, adding **Recap**
in longer chats and **Decision** for settled trade-offs. It works without the inbox.
The [handoff protocol spec](https://martin-gomola.github.io/your-turn-loop/spec.html)
defines the format for agents and for tools that read it.

## Install

[Open the skill installer](https://martin-gomola.github.io/your-turn-loop/),
select **your-turn-handoff** and your coding agents, then copy and run the command.
You can install it alone; no other skill is required. Installation requires
Node.js 22.20+ and Git.

**Already using Your Turn?** Its setup may already manage this skill. Keep one
installation and use that setup to update it. The separate
[Your Turn repository](https://github.com/martin-gomola/your-turn) provides the
optional inbox and setup across chats.

## Try it

Start a new chat and ask:

```text
Use your-turn-handoff for the final answers in this chat.
```

Your agent controls when skills load. Installation and an example request do not
prove activation in every future chat.

To continue in another agent, paste the block into a chat with
[what-to-ask](../skills/what-to-ask/SKILL.md) and ask for the follow-up prompt.
See [Work across agents](across-agents.md).

## Update or remove

Follow [Manage your installation](install.md). The editable source is
[the complete skill](../skills/your-turn-handoff/SKILL.md).
