#!/usr/bin/env python3
"""Conservative deterministic checks for ux-design web UI delivery.

Validates explicit contrast pairs; catches styled native selects that omit an
explicit indicator strategy, end clearance, or a complete replacement
indicator, or that would render two arrows; and, when scales are given,
reports off-scale spacing and radius literals. Always flags vertical margins on
form-row selectors. It does not replace computed-style, semantic, interaction,
or visual QA in a browser.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


HEX_COLOR = re.compile(r"^#[0-9a-fA-F]{3}(?:[0-9a-fA-F]{3})?$")
COMMENT = re.compile(r"/\*.*?\*/", re.DOTALL)
CSS_BLOCK = re.compile(r"(?P<selector>[^{}]+)\{(?P<body>[^{}]*)\}", re.DOTALL)
DECLARATION = re.compile(
    r"(?P<name>-{0,2}[a-z][a-z0-9_-]*)\s*:\s*(?P<value>[^;]+)", re.IGNORECASE
)
VAR_REF = re.compile(r"var\(\s*(--[a-z0-9_-]+)\s*(?:,\s*([^()]*))?\)", re.IGNORECASE)
LENGTH = re.compile(r"^(-?[0-9]*\.?[0-9]+)(px|rem|%)?$", re.IGNORECASE)
SELECT_TYPE_SELECTOR = re.compile(
    r"(?:^|[\s>+~,(])select(?=[:.\[#\s>+~,)]|$)", re.IGNORECASE
)
SELECT_CLASS_SELECTOR = re.compile(
    r"\.[a-z0-9_-]*select(?=[:.\[#\s>+~,)]|$)", re.IGNORECASE
)
SELECT_INDICATOR_SELECTOR = re.compile(
    r"\.(?:select-indicator|select-chevron)(?=[:.\[#\s>+~,)]|$)", re.IGNORECASE
)
ROW_SELECTOR = re.compile(
    r"\.[a-z0-9_-]*(?:field|form-row|form-group|row)s?(?=[:.\[#\s>+~,)]|$)",
    re.IGNORECASE,
)
SPACING_PROPERTY = re.compile(r"^(?:padding|margin)(?:-[a-z-]+)?$|^(?:row-|column-)?gap$")
VERTICAL_MARGIN = re.compile(r"^margin(?:-top|-bottom|-block(?:-start|-end)?)?$")
SPACING_VAR = re.compile(r"^--[a-z0-9_-]*(?:space|gap|inset|pad|gutter)[a-z0-9_-]*$")
RADIUS_VAR = re.compile(r"^--[a-z0-9_-]*radius[a-z0-9_-]*$")
APPEARANCE = re.compile(
    r"(?:-webkit-)?appearance\s*:\s*(?P<value>[a-z-]+)", re.IGNORECASE
)
MIN_CONTROL_HEIGHT = 32
ARROW_IN_ACTION = re.compile(r"<(button|a)\b[^>]*>[^<]*(?:→|&rarr;)\s*</\1>", re.IGNORECASE)
SOFT_GREY_SHADOW = re.compile(r"rgba\(\s*0\s*,\s*0\s*,\s*0\s*,\s*0?\.1\s*\)")


def _relative_luminance(hex_color: str) -> float:
    value = hex_color.strip().lstrip("#")
    if len(value) == 3:
        value = "".join(character * 2 for character in value)
    if len(value) != 6 or not HEX_COLOR.match(f"#{value}"):
        raise ValueError(f"expected #RGB or #RRGGBB, got {hex_color!r}")
    channels = [int(value[index : index + 2], 16) / 255 for index in (0, 2, 4)]
    linear = [
        channel / 12.92
        if channel <= 0.04045
        else ((channel + 0.055) / 1.055) ** 2.4
        for channel in channels
    ]
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]


def contrast_ratio(foreground: str, background: str) -> float:
    lighter, darker = sorted(
        (_relative_luminance(foreground), _relative_luminance(background)),
        reverse=True,
    )
    return (lighter + 0.05) / (darker + 0.05)


def _declarations(body: str) -> dict[str, str]:
    return {
        match.group("name").casefold(): match.group("value").strip()
        for match in DECLARATION.finditer(body)
    }


def _resolve_px(value: str, variables: dict[str, str], depth: int = 0) -> float | None:
    """Resolve a px/rem literal, var() token, or additive calc() to px; else None."""
    if depth > 8:
        return None
    text = VAR_REF.sub(
        lambda match: variables.get(match.group(1), match.group(2) or "?"), value
    )
    if "var(" in text:
        return _resolve_px(text, variables, depth + 1)
    # ponytail: additive calc only (+/-); multiplication or min()/clamp() resolve to None.
    text = re.sub(r"calc\(|\(|\)", " ", text, flags=re.IGNORECASE).strip()
    total, sign = 0.0, 1.0
    for index, token in enumerate(re.split(r"\s+([+-])\s+", text)):
        if index % 2:
            sign = -1.0 if token == "-" else 1.0
            continue
        length = LENGTH.match(token)
        unit = (length.group(2) or "").casefold() if length else ""
        if not length or unit == "%" or (not unit and float(length.group(1)) != 0):
            return None
        number = float(length.group(1)) * (16 if unit == "rem" else 1)
        total += sign * number
    return total


def _px(number: float) -> str:
    return f"{number:g}px"


def _styled_select_findings(blocks, variables: dict[str, str]) -> list[str]:
    findings = []
    complete_indicator: dict[str, str] | None = None
    incomplete_indicator_reasons: list[str] = []
    for match in blocks:
        if not SELECT_INDICATOR_SELECTOR.search(match.group("selector")):
            continue
        declarations = _declarations(match.group("body"))
        missing = []
        if declarations.get("position", "").casefold() != "absolute":
            missing.append("position: absolute")
        if declarations.get("pointer-events", "").casefold() != "none":
            missing.append("pointer-events: none")
        if not any(key in declarations for key in ("inset-inline-end", "right", "inset")):
            missing.append("an explicit logical-end inset")
        if missing:
            incomplete_indicator_reasons.extend(missing)
        else:
            complete_indicator = declarations

    # ponytail: all select rules merge in source order (one select style per stylesheet);
    # split the check per selector if a product ships several deliberate select styles.
    select_blocks = [
        match for match in blocks
        if not SELECT_INDICATOR_SELECTOR.search(match.group("selector"))
        and (
            SELECT_TYPE_SELECTOR.search(match.group("selector"))
            or SELECT_CLASS_SELECTOR.search(match.group("selector"))
        )
    ]
    if select_blocks:
        selector = " / ".join(match.group("selector").strip() for match in select_blocks)
        body = ";".join(match.group("body") for match in select_blocks)
        declarations = _declarations(body)
        if not any(
            key.startswith(prefix)
            for key in declarations
            for prefix in ("border", "background", "box-shadow", "padding")
        ):
            return findings
        appearance_values = [
            appearance.group("value").casefold()
            for appearance in APPEARANCE.finditer(body)
        ]
        uses_custom_appearance = "none" in appearance_values
        has_background_indicator = "background-image" in declarations or "url(" in (
            declarations.get("background", "").casefold()
        )
        end_padding = declarations.get("padding-inline-end") or declarations.get(
            "padding-right"
        )
        if not end_padding:
            findings.append(
                f"{selector}: select end clearance is missing; add padding-inline-end "
                "for the value and indicator"
            )
        if not appearance_values:
            findings.append(
                f"{selector}: styled select indicator strategy is implicit; declare "
                "appearance:none with one wrapper chevron (or appearance:auto)"
            )
        elif uses_custom_appearance:
            if has_background_indicator:
                findings.append(
                    f"{selector}: background-image arrow is not the canonical indicator; "
                    "use one aria-hidden .select-indicator SVG in a wrapper"
                )
            elif complete_indicator is None:
                detail = ", ".join(dict.fromkeys(incomplete_indicator_reasons))
                suffix = f"; missing {detail}" if detail else ""
                findings.append(
                    f"{selector}: appearance:none requires a complete "
                    f".select-indicator/.select-chevron rule{suffix}"
                )
        elif any(value in {"auto", "menulist", "menulist-button"} for value in appearance_values):
            if complete_indicator is not None or has_background_indicator:
                findings.append(
                    f"{selector}: platform arrow plus a custom indicator renders two "
                    "arrows; set appearance:none"
                )
        else:
            findings.append(
                f"{selector}: unsupported native select appearance strategy "
                f"{appearance_values[-1]!r}; use appearance:none with a wrapper chevron"
            )

        if uses_custom_appearance and complete_indicator is not None and end_padding:
            padding = _resolve_px(end_padding, variables)
            inset = _resolve_px(
                complete_indicator.get("inset-inline-end")
                or complete_indicator.get("right", ""),
                variables,
            )
            size = _resolve_px(
                complete_indicator.get("inline-size")
                or complete_indicator.get("width", ""),
                variables,
            )
            if None not in (padding, inset, size) and padding < inset + size:
                findings.append(
                    f"{selector}: padding-inline-end {_px(padding)} is less than indicator "
                    f"inset + size ({_px(inset + size)}); long values overlap the arrow"
                )

        for key in ("min-height", "min-block-size", "height", "block-size"):
            height = _resolve_px(declarations.get(key, ""), variables)
            if height is not None and height < MIN_CONTROL_HEIGHT:
                findings.append(
                    f"{selector}: select {key} is {_px(height)}; require at least "
                    f"{MIN_CONTROL_HEIGHT}px (40px default, 44px touch)"
                )
    return findings


def _row_margin_findings(blocks, variables: dict[str, str]) -> list[str]:
    findings = []
    for match in blocks:
        selector = match.group("selector").strip()
        if not ROW_SELECTOR.search(selector):
            continue
        for name, value in _declarations(match.group("body")).items():
            if not VERTICAL_MARGIN.match(name):
                continue
            parts = value.split()
            vertical = parts if name != "margin" else [parts[0], parts[2 if len(parts) > 2 else 0]]
            if any(_resolve_px(part, variables) not in (0, None) for part in vertical):
                findings.append(
                    f"{selector}: {name}: {value} on a form row; let the parent stack "
                    "gap own row spacing"
                )
    return findings


def _scale_findings(
    blocks,
    variables: dict[str, str],
    spacing_scale: set[float] | None,
    radius_scale: set[str] | None,
) -> list[str]:
    findings = []

    def check(selector: str, name: str, value: str, scale, kind: str) -> None:
        if "var(" in value or "calc(" in value:
            return  # token references are checked where the token is defined
        for part in value.split():
            if kind == "radius" and part in scale:
                continue
            number = _resolve_px(part, {})  # keywords and % resolve to None
            if number is None:
                continue
            allowed = abs(number) in scale if kind == "spacing" else _px(number) in scale
            if not allowed:
                findings.append(f"{selector}: {name}: {value} is off the {kind} scale")
                return

    for match in blocks:
        selector = match.group("selector").strip()
        for name, value in _declarations(match.group("body")).items():
            if spacing_scale is not None and (
                SPACING_PROPERTY.match(name) or SPACING_VAR.match(name)
            ):
                check(selector, name, value, spacing_scale, "spacing")
            if radius_scale is not None and (
                name.endswith("radius") or RADIUS_VAR.match(name)
            ):
                check(selector, name, value, radius_scale, "radius")
    return findings


def _tell_findings(text: str, blocks) -> list[str]:
    """Generated-default tells; legitimate only when the product chooses them."""
    findings = []
    for match in blocks:
        selector = match.group("selector").strip()
        declarations = _declarations(match.group("body"))
        if declarations.get("text-transform", "").casefold() == "uppercase" and (
            "letter-spacing" in declarations
        ):
            findings.append(f"tell: {selector}: tracked ALL-CAPS label; keep only with a product reason")
        if "→" in declarations.get("content", "") or "\\2192" in declarations.get("content", ""):
            findings.append(f"tell: {selector}: arrow appended via content; let the label say the action")
    if ARROW_IN_ACTION.search(text):
        findings.append("tell: button or link text ends with an arrow; let the label say the action")
    shadowed = [
        match.group("selector").strip() for match in blocks
        if SOFT_GREY_SHADOW.search(_declarations(match.group("body")).get("box-shadow", ""))
    ]
    if len(shadowed) >= 3:
        findings.append(
            f"tell: the same soft grey shadow on {len(shadowed)} rules ({', '.join(shadowed[:3])}…); "
            "use an elevation step per surface"
        )
    return findings


def validate_css_text(
    css_text: str,
    *,
    contrast_pairs: list[tuple[str, str, str, float]] | None = None,
    spacing_scale: list[float] | None = None,
    radius_scale: list[str] | None = None,
    tells: bool = False,
) -> list[str]:
    blocks = list(CSS_BLOCK.finditer(COMMENT.sub("", css_text)))
    variables = {
        name: value
        for match in blocks
        for name, value in _declarations(match.group("body")).items()
        if name.startswith("--")
    }
    findings = _styled_select_findings(blocks, variables)
    findings += _row_margin_findings(blocks, variables)
    findings += _scale_findings(
        blocks,
        variables,
        set(spacing_scale) if spacing_scale is not None else None,
        set(radius_scale) if radius_scale is not None else None,
    )
    if tells:
        findings += _tell_findings(css_text, blocks)
    for label, foreground, background, threshold in contrast_pairs or []:
        try:
            ratio = contrast_ratio(foreground, background)
        except ValueError as error:
            findings.append(f"{label}: {error}")
            continue
        if ratio < threshold:
            findings.append(
                f"{label}: contrast {ratio:.4f}:1 is below required {threshold:.1f}:1 "
                f"({foreground} on {background})"
            )
    return findings


def parse_contrast_pair(value: str) -> tuple[str, str, str, float]:
    parts = [part.strip() for part in value.split(",")]
    if len(parts) != 4:
        raise argparse.ArgumentTypeError(
            "contrast must be label,#foreground,#background,threshold"
        )
    label, foreground, background, threshold_text = parts
    try:
        threshold = float(threshold_text)
        contrast_ratio(foreground, background)
    except ValueError as error:
        raise argparse.ArgumentTypeError(str(error)) from error
    return label, foreground, background, threshold


def parse_spacing_scale(value: str) -> list[float]:
    try:
        return [float(part.strip().removesuffix("px")) for part in value.split(",")]
    except ValueError as error:
        raise argparse.ArgumentTypeError(str(error)) from error


def parse_radius_scale(value: str) -> list[str]:
    items = [part.strip() for part in value.split(",") if part.strip()]
    return [item if item.endswith("%") else f"{float(item.removesuffix('px')):g}px" for item in items]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate contrast, styled-select indicators, and dimension scales."
    )
    parser.add_argument("--css", action="append", type=Path, default=[])
    parser.add_argument(
        "--contrast",
        action="append",
        type=parse_contrast_pair,
        default=[],
        metavar="LABEL,#FG,#BG,THRESHOLD",
    )
    parser.add_argument(
        "--spacing-scale",
        type=parse_spacing_scale,
        metavar="0,4,8,16,32,64",
        help="report padding, margin, and gap px literals outside this scale",
    )
    parser.add_argument(
        "--radius-scale",
        type=parse_radius_scale,
        metavar="0,4,8,16,50%,9999",
        help="report border-radius literals outside this scale",
    )
    parser.add_argument(
        "--tells",
        action="store_true",
        help="also report generated-default tells (ALL-CAPS eyebrows, arrow labels, one shadow everywhere)",
    )
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    css_text = "\n".join(path.read_text(encoding="utf-8") for path in args.css)
    findings = validate_css_text(
        css_text,
        contrast_pairs=args.contrast,
        spacing_scale=args.spacing_scale,
        radius_scale=args.radius_scale,
        tells=args.tells,
    )
    result = {"status": "invalid" if findings else "valid", "findings": findings}
    if args.json:
        print(json.dumps(result, indent=2))
    elif findings:
        print("FAILED: app UI delivery checks")
        for finding in findings:
            print(f"  - {finding}")
    else:
        print("OK: app UI delivery checks passed")
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
