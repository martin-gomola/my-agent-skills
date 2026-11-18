# Alignment and inset field case

Recorded on 2026-10-31 in the your-turn local agent inbox (web, Chrome), on synthetic fixture data.
User reports during review, each followed by a rendered measurement and a repair.

| Report | Measured cause | Repair | Rendered proof after |
| --- | --- | --- | --- |
| Theme and Live controls "too far from the right side" | The 44px icon-only toggle ended on the content edge, but its centered 18px glyph ended 13px inside it | Bleed the edge control by (44 - 18) / 2 so the glyph meets the edge | Glyph right gap 0px at 1440px; menu glyph gap 0px at 375px |
| Sidebar leaf "lower than" the top bar | Sidebar content started 32px down; top bar sat 8px down | Same top-inset token for both rows | All three centered at y=30 on inbox, pane, chat page, phone drawer |
| Select arrow "stuck to the side" | `appearance: auto` with 36px end padding; Chrome's native arrow ignored the padding | `appearance: none` plus one positioned chevron at a named end inset | One chevron, 12px from the border, vertical offset 0 |
| Load more not centered | `justify-self: start` under a full-width list | Center under the list it extends | 582px left and right at 1440px |
| Status card looked clipped under the pane title | Sticky opaque header with no bottom edge or padding | Hairline bottom edge and padding on the sticky header | Content scrolls under a visible boundary |
| Agent pill not vertically aligned with metadata | Mixed-size flex items aligned by box center | `align-items: baseline` | Baselines 136.8 vs 137.6 before; 137.6 for all items after |
| Wrapped metadata line started with "·" | Separator rendered before each item | Separator trails its item | Wrapped line ends with "·", next line starts with text |
| "No unified padding system" | Text controls mixed 12/16px starts and ad-hoc ends | Named tokens: control text inset, trailing indicator inset, icon bleed | Controls share 16px start and 12px indicator end |

Measurement methods that caught these, where box rectangles of the containers did not:

- glyph rectangles (the `svg`), not button rectangles, for edge alignment;
- a zero-size `inline-block` probe with `vertical-align: baseline` inserted in each item for baselines;
- element center y for controls that share a row across separate containers (sidebar and top bar);
- zoomed rendered screenshots at desktop and phone widths in both themes.
