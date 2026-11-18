# Dimension defaults field case

Recorded on 2026-11-18 from user review of UI generated with this skill.

| Report | Cause in the skill | Repair |
| --- | --- | --- |
| Uneven padding between rows and components | `DESIGN.md` left "Spacing and density" blank and the rules said "follow the repository scale"; with no repository scale, agents invented one-off values and mixed row margins with container gaps | Concrete default scale, inset roles, control heights, and radius by component in `references/dimension-defaults.md`; parent `gap` owns row rhythm |
| Dropdown arrow wrong, doubled, or missing on selects | Three accepted indicator paths (`appearance: auto`, `background-image`, wrapper SVG); combinations rendered two arrows, and Chrome ignores end padding for the platform arrow | One canonical pattern: `appearance: none` plus one wrapper SVG chevron; validator rejects mixed paths and end padding smaller than inset + indicator size |
| Random radii and gaps | No radius or control-height default | Radius per component (controls 8, icon-only circular, tags 4, cards 16) and 32/40/44 control heights; validator `--spacing-scale` / `--radius-scale` |

Dimensions come from a verified production product UI token set (spacing 4/8/16/32/64, button 16 px
inline padding, 8 px radius, 8 px icon gap, alert 8/16 padding, elevation 1-4, breakpoints). Its
colors, typography, logo, and voice are excluded.
