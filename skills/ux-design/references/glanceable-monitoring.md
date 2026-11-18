# Glanceable monitoring and trust

Read for dashboards, inboxes, status boards, queues, and any surface people scan to decide what
needs their attention; and for surfaces that present output from AI models or agents. Skip it for a
single-task form or editor with nothing to monitor.

Keep the user task, product identity, and repository contracts in charge. These rules sharpen
hierarchy for monitoring and trust; they do not replace local tokens, components, or `DESIGN.md`.

## Monitoring at a glance

Source: Stephen Few, *Common Pitfalls in Dashboard Design* (Perceptual Edge, 2006). Few defines a
dashboard as the most important information consolidated on one screen so it can be monitored at a
glance, used in three steps: see the big picture, focus on what needs attention, drill in to act.

- Support the monitoring sequence: overview first, then the items that need attention, then a short path to the detail needed to act.
- Keep the overview needed for monitoring visible together; do not split items people compare into separate tabs, selectors, or screens.
  Long histories and drill-down detail may scroll or open elsewhere; the summary that says what
  needs attention may not.
- Give every key status or measure its comparison: what it is compared with, whether it is good or bad, and whether it changed.
- Place the most important, attention-needing items in the most prominent position, and group related items next to each other.
- Make only what needs attention visually prominent; subdue chrome, logos, navigation, and routine items.
  When everything is emphasized, nothing stands out.
- Do not let decoration take prime position or compete with the data; decorative art must stay visually quieter than any status.
- Keep color subdued and neutral by default, reserve strong color for meaning or exceptions, and never encode status by color alone.
- Show only the precision needed to decide; round numbers and times to what the decision needs.

## Trust in AI or agent output

Source: Google PAIR, *People + AI Guidebook*, chapters Explainability + Trust and Errors + Graceful
Failure. Apply this only to probabilistic or generated output (models, agents, recommendations); do
not add confidence displays to deterministic data.

- Help people calibrate trust: show what the output is based on and its known limits, so they know when to rely on it and when to check.
- Name the data sources behind an AI result, especially data people may not expect the system to use.
- Show confidence or verification evidence only when it changes the decision, in terms people understand.
- Treat a low-confidence or unverified result as a possible error state, and give a path forward from every failure.

## Acceptance checks

- In a few seconds on the rendered surface, a new viewer can name which items need them and why.
- The most prominent position holds attention-needing content, not chrome or decoration.
- Every status or measure that drives a decision shows its comparison or evidence beside it.
- Status remains distinguishable in grayscale and with color-vision deficiency simulation.
- For AI or agent output, the evidence behind a result (checks, sources, confidence) is reachable
  from the result itself, and every failure state names a next action.
