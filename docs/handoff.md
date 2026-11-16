# your-turn-handoff

Add a consistent result and next step to agent replies.

```text
**Outcome:** The CSV export includes only the filtered rows; relevant tests passed.

**Next step:** none
```

The skill ends final answers with **Outcome** and **Next step**, adding **Recap**
in longer chats and **Decision** for settled trade-offs. It works without the inbox.

**Already using Your Turn?** Keep its installation. You already have the handoff;
adding another plugin can load it twice. The full installer also sets up the
client-specific global rules and the optional inbox:

```bash
uvx your-turn@latest install
```

## Get started

For the standalone skill, choose your agent. This installs the handoff separately
from what-to-ask. The public repository does not require GitHub authentication.

<details>
<summary>Codex</summary>

```bash
codex plugin marketplace add martin-gomola/my-agent-skills
codex plugin add your-turn-handoff@my-agent-skills
```

</details>

<details>
<summary>Claude Code</summary>

Run inside Claude Code:

```text
/plugin marketplace add martin-gomola/my-agent-skills
/plugin install your-turn-handoff@my-agent-skills
```

Use `/your-turn-handoff:your-turn-handoff` in a new session.

</details>

<details>
<summary>Cursor</summary>

Open **Customize > Plugins > From GitHub Repository**, enter
`martin-gomola/my-agent-skills`, and select **your-turn-handoff**.

</details>

<details>
<summary>Antigravity CLI</summary>

From a directory where you want a new repository checkout:

```bash
git clone https://github.com/martin-gomola/my-agent-skills.git
agy plugin install ./my-agent-skills/plugins/your-turn-handoff
```

</details>

<details>
<summary>Gemini CLI</summary>

```bash
gemini skills install https://github.com/martin-gomola/my-agent-skills.git --path skills/your-turn-handoff --scope user
```

</details>

## Try it

Start a new chat and ask:

```text
Use your-turn-handoff for the final answers in this chat.
```

Your agent controls when skills load. Installation and an example request do not
prove activation in every future chat. Use the full Your Turn installer for its
client-specific setup across chats.

## Update or remove

For Codex:

```bash
codex plugin marketplace upgrade my-agent-skills
codex plugin add your-turn-handoff@my-agent-skills
```

Remove it with `codex plugin remove your-turn-handoff@my-agent-skills`.
For Claude Code, update or uninstall `your-turn-handoff@my-agent-skills` in the
`/plugin` menu. In Cursor, use the plugin's controls in Customize. For
Antigravity CLI, pull the checkout and reinstall its handoff plugin directory;
remove with `agy plugin uninstall your-turn-handoff`. For Gemini, repeat the
installation command to update; remove with
`gemini skills uninstall your-turn-handoff --scope user`.

See [installation help](install.md#troubleshooting) or
[the complete skill](../skills/your-turn-handoff/SKILL.md).
