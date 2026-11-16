# Manage your installation

Install directly from [the skill installer](https://martin-gomola.github.io/my-agent-skills/).
Choose skills, agents, and project or global scope, then run its command.
Installation uses the [Skills CLI](https://github.com/vercel-labs/skills) and
requires Node.js 22.20+ and Git.

## List, update or remove

Run project commands from the same project folder where you installed the skills:

```bash
DISABLE_TELEMETRY=1 npx skills list
DISABLE_TELEMETRY=1 npx skills check
DISABLE_TELEMETRY=1 npx skills update --project
DISABLE_TELEMETRY=1 npx skills remove what-to-ask
```

For skills installed across your projects:

```bash
DISABLE_TELEMETRY=1 npx skills list --global
DISABLE_TELEMETRY=1 npx skills update --global
DISABLE_TELEMETRY=1 npx skills remove what-to-ask --global
```

Replace `what-to-ask` with the skill you want to remove. Updates are explicit;
review them and save any changes to an installed copy before updating. Start a
new agent chat after installation or updates.

These commands set `DISABLE_TELEMETRY=1` for that CLI process. The variable is
not saved to your shell configuration. `DO_NOT_TRACK=1` is also supported.
In the current Skills CLI, this opt-out also disables fetching its remote skill
security audit results. Installation still needs network access to fetch skills.
See the [telemetry implementation](https://github.com/vercel-labs/skills/blob/main/src/telemetry.ts).

## Troubleshooting

### The repository cannot be found

Check the repository name: `martin-gomola/my-agent-skills`. It is public, so a
GitHub login should not be required.

### The skill does not appear

Run `DISABLE_TELEMETRY=1 npx skills list` from the project folder, or `DISABLE_TELEMETRY=1 npx skills list --global` for
a global installation. Confirm the command targeted your coding agent, then
start a new session. Your client may ask you to trust the project or approve
activation; review that request in the client.

### The skill appears twice

Keep one installation per agent. Check both project and global installations.
If another setup already manages the skill, use that setup to update it.
Remove only the duplicate skill you own, never an entire shared skill directory.

## Verification limits

Local checks validate skill sources, the catalog and generated command text.
They do not prove installation or activation in every supported client. See
[Development and validation](development.md#validate) for the checks available here.
