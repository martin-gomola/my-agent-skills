# Apple HIG topic map

Read this for Apple-platform work or learning from Apple references. The HIG is a collection:
open the relevant topic and its platform considerations before adapting it. The links below record
18 Foundations and 25 Patterns topic pages reviewed in Chrome on 2026-10-30. This review covers their
written guidance; linked videos, SDK documentation, and every component page were not reviewed.

## Transfer boundary

Keep the user task, product identity, and repository contracts in charge. Apple system behavior is
platform authority for an Apple target; guidance applied to web or other platforms is a design
hypothesis to check locally. Do not import native point sizes, SF fonts, SF Symbols, Liquid Glass,
window placement, authentication requirements, or visionOS immersion rules as cross-platform defaults.
Preserve existing authorization and data contracts when simplifying account or permission flows.

Use the table to select a topic, not as a requirement to add every capability. Most established
hierarchy, labels, accessibility, and state guidance already lives in the skill's interface rules.

## Foundations

| Topic / source | Decision it informs |
| --- | --- |
| [Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility) | Adapt to sensory, mobility, and cognitive needs; preserve multiple ways to perceive and operate. |
| [App icons](https://developer.apple.com/design/human-interface-guidelines/app-icons) | Recognition at small sizes, appearance variants, and system-applied effects; follow current asset specifications. |
| [Branding](https://developer.apple.com/design/human-interface-guidelines/branding) | Express identity through content and voice while keeping familiar controls and task space. |
| [Color](https://developer.apple.com/design/human-interface-guidelines/color) | Use stable semantic roles and check actual backgrounds, contrast settings, and cultural meaning. |
| [Dark Mode](https://developer.apple.com/design/human-interface-guidelines/dark-mode) | Test adaptive appearances and assets; dark palettes are not simple inversions. |
| [Icons](https://developer.apple.com/design/human-interface-guidelines/icons) | Recognizable meaning, optical alignment, visual consistency, and accessible labels. |
| [Images](https://developer.apple.com/design/human-interface-guidelines/images) | Choose appropriate resolution, profiles, and formats; inspect device rendering and performance. |
| [Immersive experiences](https://developer.apple.com/design/human-interface-guidelines/immersive-experiences) | User-controlled immersion, predictable transitions, and physical comfort; visionOS-specific. |
| [Inclusion](https://developer.apple.com/design/human-interface-guidelines/inclusion) | Plain, welcoming language and representation without stereotypes or unnecessary jargon. |
| [Layout](https://developer.apple.com/design/human-interface-guidelines/layout) | Hierarchy, grouping, progressive disclosure, available space, and text-size adaptation. |
| [Materials](https://developer.apple.com/design/human-interface-guidelines/materials) | Semantic layering and readable separation; Liquid Glass is platform guidance, not a universal visual theme. |
| [Motion](https://developer.apple.com/design/human-interface-guidelines/motion) | Purposeful feedback and continuity; brief, optional, interruptible movement. |
| [Privacy](https://developer.apple.com/design/human-interface-guidelines/privacy) | Minimal data needs, contextual permission requests, clear purpose, and system protections. |
| [Right to left](https://developer.apple.com/design/human-interface-guidelines/right-to-left) | Reading-order layout and navigation; distinguish mirrored directions from preserved media and physical directions. |
| [SF Symbols](https://developer.apple.com/design/human-interface-guidelines/sf-symbols) | Symbol meaning, weight, rendering, and purposeful animation in supported Apple contexts. |
| [Spatial layout](https://developer.apple.com/design/human-interface-guidelines/spatial-layout) | Accurate depth, readable text, comfortable interaction spacing, and stable surroundings; visionOS-specific. |
| [Typography](https://developer.apple.com/design/human-interface-guidelines/typography) | Legible roles and custom fonts; recompose at large accessibility sizes while preserving hierarchy. |
| [Writing](https://developer.apple.com/design/human-interface-guidelines/writing) | Consistent action labels, contextual tone, clear errors, and useful next steps. |

## Patterns

| Topic / source | Decision it informs |
| --- | --- |
| [Charting data](https://developer.apple.com/design/human-interface-guidelines/charting-data) | Choose a chart for an analytical message; use familiar encodings, accessible descriptions, and progressive detail. |
| [Collaboration and sharing](https://developer.apple.com/design/human-interface-guidelines/collaboration-and-sharing) | Clear permissions, sharing scope, and visible collaboration state using supported platform affordances. |
| [Drag and drop](https://developer.apple.com/design/human-interface-guidelines/drag-and-drop) | Alternatives, predictable move/copy semantics, destination feedback, transfer states, and undo. |
| [Entering data](https://developer.apple.com/design/human-interface-guidelines/entering-data) | Reduce unnecessary input, allow paste, clarify requirements, and validate usefully. |
| [Feedback](https://developer.apple.com/design/human-interface-guidelines/feedback) | Contextual status, proportionate interruption, actionable failures, and significant completion signals. |
| [File management](https://developer.apple.com/design/human-interface-guidelines/file-management) | Confidence that work is preserved, visible unsaved state, and familiar open/save/export behavior. |
| [Going full screen](https://developer.apple.com/design/human-interface-guidelines/going-full-screen) | User control, access to essential tasks, and state continuity when leaving or returning. |
| [Launching](https://developer.apple.com/design/human-interface-guidelines/launching) | Fast access and restoration of previous work; platform launch screens are not advertising. |
| [Live-viewing apps](https://developer.apple.com/design/human-interface-guidelines/live-viewing-apps) | Clear live status, immediate playback feedback, and browsing without losing current content. |
| [Loading](https://developer.apple.com/design/human-interface-guidelines/loading) | Useful content early, visible progress, and continued access to independent tasks. |
| [Managing accounts](https://developer.apple.com/design/human-interface-guidelines/managing-accounts) | Explain account value, gate only necessary features, and make deletion consequences and status clear. |
| [Managing notifications](https://developer.apple.com/design/human-interface-guidelines/managing-notifications) | Honest urgency, interruption discipline, consent, and user control. |
| [Modality](https://developer.apple.com/design/human-interface-guidelines/modality) | Justified, focused modal tasks with a clear exit and protection against accidental work loss. |
| [Multitasking](https://developer.apple.com/design/human-interface-guidelines/multitasking) | Preserve work and resume sensibly; handle attention changes, background tasks, and interruptions. |
| [Offering help](https://developer.apple.com/design/human-interface-guidelines/offering-help) | Contextual, brief help for actual uncertainty; avoid teaching familiar controls redundantly. |
| [Onboarding](https://developer.apple.com/design/human-interface-guidelines/onboarding) | Learning through use, contextual tips, and deferred optional setup. |
| [Playing audio](https://developer.apple.com/design/human-interface-guidelines/playing-audio) | System playback expectations, routing, volume, and interruption handling. |
| [Playing haptics](https://developer.apple.com/design/human-interface-guidelines/playing-haptics) | Consistent optional event feedback that complements other channels. |
| [Playing video](https://developer.apple.com/design/human-interface-guidelines/playing-video) | Familiar playback controls, aspect ratio, resumption, and immediate exit. |
| [Printing](https://developer.apple.com/design/human-interface-guidelines/printing) | Discoverable availability, relevant options, and previews of setting consequences. |
| [Ratings and reviews](https://developer.apple.com/design/human-interface-guidelines/ratings-and-reviews) | Ask after meaningful engagement without interrupting work; platform prompts and policies apply. |
| [Searching](https://developer.apple.com/design/human-interface-guidelines/searching) | Visible scope, appropriate prominence, useful suggestions, and privacy-aware history. |
| [Settings](https://developer.apple.com/design/human-interface-guidelines/settings) | Useful defaults, few preferences, task-local options, and respect for system settings. |
| [Undo and redo](https://developer.apple.com/design/human-interface-guidelines/undo-and-redo) | Predictable named operations, visible results, and platform conventions. |
| [Workouts](https://developer.apple.com/design/human-interface-guidelines/workouts) | Legibility during movement, relevant session controls, and honest unavailable-sensor states; fitness-specific. |

## Evidence to seek in the product

Select only checks relevant to the change: complete the task with motion reduced or interrupted,
operate gesture actions through an alternative, recover after denied access, follow a translated
RTL flow, keep readable content over changing backgrounds, and return to intact work after an
interruption. Preference for an Apple example alone does not establish task success or accessibility.
