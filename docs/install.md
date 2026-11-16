# Manage your installation

Need to install first? [Choose your agent in the README](../README.md#get-started).

Updates are explicit. After updating, start a new chat or session to use the new
instructions. If you edited an installed copy, save those changes before replacing it.

## Skills installed from the website

The website installs selected skills directly with the
[Skills CLI](https://github.com/vercel-labs/skills). Run project commands from the
same project folder where you installed them. Node.js 22.20+ and Git are required.

```bash
npx skills list
npx skills check
npx skills update what-to-ask
npx skills remove what-to-ask
```

Replace `what-to-ask` with the skill you want to manage. For skills installed for
all your projects, use `npx skills list --global` and
`npx skills remove what-to-ask --global`. Use `npx skills update --global` to update
global skills, or `npx skills update --project` for the current project.
Updates are explicit; review them before starting a new agent chat.

The Skills CLI collects telemetry; see its
[configuration documentation](https://github.com/vercel-labs/skills/blob/main/docs/troubleshooting.md#telemetry)
for what is sent and how to disable it.

## Existing native plugin installations

If you installed a plugin before using the skill selector, keep using the native
instructions below, or remove that plugin before installing the same skills
directly. This avoids duplicate skills.

### Codex

Update:

```bash
codex plugin marketplace upgrade my-agent-skills
codex plugin add my-agent-skills@my-agent-skills
```

Remove:

```bash
codex plugin remove my-agent-skills@my-agent-skills
```

To remove the marketplace entry too, run
`codex plugin marketplace remove my-agent-skills`.

### Claude Code

Update from Claude Code:

```text
/plugin marketplace update my-agent-skills
/plugin update my-agent-skills@my-agent-skills
```

Remove:

```text
/plugin uninstall my-agent-skills@my-agent-skills
```

### Cursor

Refresh the imported marketplace in **Customize > Plugins** and use its update
control when offered. Otherwise remove the plugin and
[repeat installation](../README.md#get-started).

To uninstall, remove **my-agent-skills** in Customize.

### Antigravity CLI

Update by removing and reinstalling the plugin:

```bash
agy plugin uninstall my-agent-skills
git -C my-agent-skills pull --ff-only
agy plugin install ./my-agent-skills/plugins/what-to-ask
```

To remove it without reinstalling:

```bash
agy plugin uninstall my-agent-skills
```

### Gemini CLI

Update by repeating installation with the same scope:

```bash
gemini skills install https://github.com/martin-gomola/my-agent-skills.git --path skills/what-to-ask --scope user
```

Remove:

```bash
gemini skills uninstall what-to-ask --scope user
```

If you chose a workspace installation, use `--scope workspace` for both commands.

## Troubleshooting

### The repository cannot be found

This repository is public. Check the repository name and client-specific install
steps; a GitHub login should not be required.

### The skill does not appear

Start a new session and check the installation in your client:

For website installations, first run `npx skills list` (add `--global` for an
installation across projects). Direct skills do not appear in plugin lists.
The table below checks existing native installations.

| Client | Check |
| --- | --- |
| Codex | `codex plugin list --marketplace my-agent-skills` |
| Claude Code | Open the `/plugin` menu |
| Cursor | Open Customize > Plugins |
| Antigravity CLI | `agy plugin list` |
| Gemini CLI | `gemini skills list --all` |

For workspace skills, the client may ask you to trust the project or approve
activation. Review that request in the client.

### The skill appears twice

Keep one installation per client. If another setup already manages this skill,
use that setup to update it.

Cursor also reads Claude and Codex skill directories, so a direct copy can appear
alongside a plugin installation. Remove only the duplicate copy you own.
Never delete an entire shared skill registry.

### I use the Antigravity App rather than its CLI

For a direct folder installation, copy the complete `skills/what-to-ask/` folder
from this repository to `~/.gemini/config/skills/what-to-ask/`. This includes its
license and resources. Start a new session.

Update by replacing only that skill folder after reviewing local changes.
Uninstall by removing that folder. Use this route instead of a second plugin
installation for the same skill.

## Sources and verification

Website installation uses the [Skills CLI](https://github.com/vercel-labs/skills).
Existing native installations follow these client mechanisms:
[Codex](https://developers.openai.com/plugins/build/plugins),
[Claude Code](https://code.claude.com/docs/en/discover-plugins),
[Cursor](https://cursor.com/docs/skills),
[Antigravity](https://antigravity.google/docs/skills) and
[Gemini CLI](https://geminicli.com/docs/cli/skills/).

[Verification coverage](development.md#verification-coverage) lists what was
checked locally and what still needs testing in the clients.
