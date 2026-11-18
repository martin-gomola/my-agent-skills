<div align="center">

# My Agent Skills

<p align="center"><strong>A handoff protocol for working across AI coding agents.</strong></p>

![Portable skills · SKILL.md](https://img.shields.io/badge/Portable%20skills-SKILL.md-56645f)
![No MCP required](https://img.shields.io/badge/No%20MCP-required-2f7a6b)

[Get started](#get-started) · [Cross-agent loop](#cross-agent-loop) · [Help](#help)

</div>

For developers who work with more than one AI coding agent. Write a brief
another agent can act on, delegate it, and get back a result that ends with the
same two lines in every agent:

```text
**Outcome:** The CSV export includes only the filtered rows; relevant tests passed.

**Next step:** none
```

That [your-turn-handoff](docs/handoff.md) format is the protocol. Paste it into
any agent and the next brief starts from a settled result, not a retold chat.

## Cross-agent loop

| Step | Skill | Use it when |
| --- | --- | --- |
| Brief | [what-to-ask](skills/what-to-ask/SKILL.md) | Turn notes, a screenshot, or another agent's result into a self-contained prompt. |
| Delegate | [ask](skills/ask/SKILL.md) | Get a read-only second opinion through an installed Claude or Antigravity CLI. |
| Delegate | [relay](skills/relay/SKILL.md) | Have Codex or Claude implement a scoped task in its own worktree while your agent reviews the diff. |
| Delegate | [codex-image](skills/codex-image/SKILL.md) | Hand off image creation to a Codex CLI with image generation available. |
| Result | [your-turn-handoff](docs/handoff.md) | End every answer with a clear Outcome and Next step, plus Recap and Decision in longer chats. |

[Work across agents](docs/across-agents.md) walks through the loop and lists the
handoffs that still need you to paste text.

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

## Help

- [Update or remove your installation](docs/install.md)
- [Skill missing, duplicate, or unable to install?](docs/install.md#troubleshooting)
- [Development and validation](docs/development.md)
- [Installer page (local preview)](docs/development.md#installer-page)
- [MIT license](LICENSE)
