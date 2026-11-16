# Authoring notes: prompt-writing principles

Reviewed on 2026-11-14. These paraphrased authoring notes identify the public source sections behind the skill's core principles. They are provenance, not a runtime reading requirement.

## Source themes used

- **Prompt Engineering, February 2025, pp. 55-62:** keep prompts clear and relevant; use a direct task verb; provide context that affects the answer; express the desired output; use positive instructions and retain negative constraints for real boundaries. The guide presents role, context, format, and task as useful components rather than mandatory boilerplate for every request.
- **Agents Companion, February 2025, contract data model, pp. 47-50:** define the task, deliverables, scope, input sources, acceptance conditions, and how a result will be checked.
- **Building Effective AI Agents, Anthropic:** use exact tool/file references where ambiguity causes navigation errors; code tasks benefit from tests and environment feedback because they are objectively verifiable.
- **Workspace with Gemini prompting guide:** include only the components that help a particular request, and refine prompts based on observed results.

## Synthesis boundary

The compact workflow and clarification policy are local design choices refined through drafting examples. The public PM Skills prompt-optimizer and prompt-debugging skills, inspected at commit `e0009a385c480fb0b5687e7412df67c7c64f7cee` in mohitagw15856/pm-claude-skills, informed the distinction between creating a new task prompt and diagnosing an existing failing prompt. No source templates or code were copied. Source documents retain their original licenses; the MIT license covers the original instructions and distribution code in this repository.
