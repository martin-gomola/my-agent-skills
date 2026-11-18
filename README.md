<div align="center">

# My Agent Skills

<p align="center"><strong>Reusable skills for the coding agents I use.</strong></p>

![Portable skills · SKILL.md](https://img.shields.io/badge/Portable%20skills-SKILL.md-56645f)
![No MCP required](https://img.shields.io/badge/No%20MCP-required-2f7a6b)

[Get started](#get-started) · [Skills](#skills) · [Help](#help)

</div>

Skills for developers who work with more than one AI coding agent. They help you
write a brief another agent can act on, delegate it, and get back a result with
a clear next step. Install only the behavior you need in each agent.

| I want to… | Choose |
| --- | --- |
| Turn notes, a screenshot, or another agent's result into a prompt | [what-to-ask](skills/what-to-ask/SKILL.md) |
| Ask an external model for a second opinion | [ask](skills/ask/SKILL.md) |
| Generate images through a local Codex CLI | [codex-image](skills/codex-image/SKILL.md) |
| Hand a coding task to Codex and review its diff | [relay](skills/relay/SKILL.md) |
| Get a clear result and next step after an answer | [your-turn-handoff](docs/handoff.md) |
| Inspect or clean Cursor storage safely | [clean-cursor](skills/clean-cursor/SKILL.md) |
| Check staged changes for private data | [pii-precommit-check](skills/pii-precommit-check/SKILL.md) |
| Edit or audit prose while preserving voice | [stop-slop](skills/stop-slop/SKILL.md) |
| Give a repository a GitHub Pages site people can understand | [github-repo-site](skills/github-repo-site/SKILL.md) |

[Work across agents](docs/across-agents.md) shows how the first four skills fit
together and which handoffs still need you to paste text.

## Get started

[Open the skill installer](https://martin-gomola.github.io/my-agent-skills/) to
choose skills, coding agents, and whether to install for this project or all your
projects. Copy one command and run it in your terminal. Installation uses the
[Skills CLI](https://github.com/vercel-labs/skills) and requires Node.js 22.20+
and Git. Codex, Claude Code, Cursor, Antigravity, and Gemini CLI are supported.
Generated commands disable Skills CLI telemetry for that run.

Install only the behavior you need. The standalone
[your-turn-handoff](docs/handoff.md) skill works with or without the separate
[Your Turn inbox](https://github.com/martin-gomola/your-turn).

## Skills

| Skill | Use it when |
| --- | --- |
| [what-to-ask](skills/what-to-ask/SKILL.md) | You need a clear prompt for another agent, or want to continue from another agent's result. |
| [ask](skills/ask/SKILL.md) | Request an opinion through an installed Claude or Antigravity CLI. |
| [codex-image](skills/codex-image/SKILL.md) | Hand off image creation to a Codex CLI with image generation available. |
| [relay](skills/relay/SKILL.md) | Have Codex implement a scoped task in its own worktree while your agent reviews the diff. |
| [your-turn-handoff](docs/handoff.md) | You want agent answers to end with a clear result and the next step. |
| [clean-cursor](skills/clean-cursor/SKILL.md) | Inspect Cursor storage and approve exact cleanup targets. |
| [pii-precommit-check](skills/pii-precommit-check/SKILL.md) | Scan staged Git changes using a bundled Python scanner. |
| [stop-slop](skills/stop-slop/SKILL.md) | Tighten a draft or audit prose without inventing authorship claims. |
| [github-repo-site](skills/github-repo-site/SKILL.md) | Build a GitHub Pages project page from repository facts, or a skill installer like this one. |

## Help

- [Update or remove your installation](docs/install.md)
- [Skill missing, duplicate, or unable to install?](docs/install.md#troubleshooting)
- [Development and validation](docs/development.md)
- [Installer page (local preview)](docs/development.md#installer-page)
- [MIT license](LICENSE)
