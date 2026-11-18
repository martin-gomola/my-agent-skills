import unittest

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "validate_delivery.py"
SPEC = spec_from_file_location("validate_delivery", SCRIPT)
assert SPEC and SPEC.loader
MODULE = module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class StyledSelectIndicatorTests(unittest.TestCase):
    def test_rejects_implicit_native_indicator_strategy(self):
        findings = MODULE.validate_css_text(
            "select { border: 1px solid #ccc; padding: 12px; padding-inline-end: 40px; }"
        )
        self.assertTrue(any("indicator strategy is implicit" in finding for finding in findings))

    def test_accepts_explicit_native_indicator_strategy(self):
        findings = MODULE.validate_css_text(
            "select { appearance: auto; border: 1px solid #ccc; padding: 12px; padding-inline-end: 40px; }"
        )
        self.assertEqual(findings, [])

    def test_accepts_complete_custom_svg_indicator_strategy(self):
        css = """
        .select-control select {
          appearance: none;
          border: 1px solid #ccc;
          padding: 12px;
          padding-inline-end: 48px;
        }
        .select-indicator {
          position: absolute;
          inset-inline-end: 16px;
          pointer-events: none;
        }
        """
        self.assertEqual(MODULE.validate_css_text(css), [])

    def test_rejects_custom_indicator_that_can_intercept_clicks(self):
        css = """
        .select-control select {
          appearance: none;
          border: 1px solid #ccc;
          padding-inline-end: 48px;
        }
        .select-indicator { position: absolute; inset-inline-end: 16px; }
        """
        findings = MODULE.validate_css_text(css)
        self.assertTrue(any("pointer-events: none" in finding for finding in findings))

    def test_rejects_platform_arrow_with_custom_indicator(self):
        css = """
        .select-control select { appearance: auto; border: 1px solid #ccc; padding-inline-end: 40px; }
        .select-indicator { position: absolute; inset-inline-end: 16px; pointer-events: none; }
        """
        findings = MODULE.validate_css_text(css)
        self.assertTrue(any("two arrows" in finding for finding in findings))

    def test_rejects_background_image_arrow(self):
        css = """
        select { appearance: none; border: 1px solid #ccc; padding-inline-end: 40px;
                 background-image: url(chevron.svg); background-position: right 16px center; }
        """
        findings = MODULE.validate_css_text(css)
        self.assertTrue(any("background-image" in finding for finding in findings))

    def test_rejects_end_padding_smaller_than_indicator(self):
        css = """
        :root { --indicator-size: 16px; }
        .select-control select { appearance: none; border: 1px solid #ccc; padding-inline-end: 24px; }
        .select-indicator { position: absolute; inset-inline-end: 16px;
                            inline-size: var(--indicator-size); pointer-events: none; }
        """
        findings = MODULE.validate_css_text(css)
        self.assertTrue(any("overlap the arrow" in finding for finding in findings))


    def test_merges_select_rules_split_across_blocks(self):
        css = """
        input, .select-control select { border: 1px solid #ccc; padding-inline-end: 16px; }
        .select-control select { appearance: none; padding-inline-end: 40px; }
        .select-indicator { position: absolute; inset-inline-end: 16px; pointer-events: none; }
        """
        self.assertEqual(MODULE.validate_css_text(css), [])


class DimensionScaleTests(unittest.TestCase):
    SCALES = {
        "spacing_scale": [0, 4, 8, 16, 32, 64],
        "radius_scale": ["0px", "4px", "8px", "16px", "50%", "9999px"],
    }

    def test_canonical_select_passes_scale_checks(self):
        css = (Path(__file__).parents[1] / "references" / "dimension-defaults.md").read_text()
        block = css.split("```css", 1)[1].split("```", 1)[0]
        self.assertEqual(MODULE.validate_css_text(block, **self.SCALES), [])

    def test_reports_off_scale_spacing_and_radius_literals(self):
        css = ".card { padding: 12px 16px; gap: 10px; border-radius: 6px; } :root { --space-x: 20px; }"
        findings = MODULE.validate_css_text(css, **self.SCALES)
        self.assertEqual(len(findings), 4, findings)

    def test_scale_checks_are_opt_in(self):
        self.assertEqual(MODULE.validate_css_text(".card { padding: 12px; border-radius: 6px; }"), [])

    def test_rejects_vertical_margin_on_form_rows(self):
        findings = MODULE.validate_css_text(".form-field { margin-bottom: 16px; }")
        self.assertTrue(any("parent stack" in finding for finding in findings))
        self.assertEqual(MODULE.validate_css_text(".form-row { margin: 0 auto; }"), [])


class GeneratedDefaultTellTests(unittest.TestCase):
    def test_reports_tells_only_when_requested(self):
        css = """
        .eyebrow { text-transform: uppercase; letter-spacing: 0.12em; }
        .a, .b, .c { box-shadow: 0 2px 4px rgba(0,0,0,.1); }
        .card { box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); }
        .panel { box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        <button class="cta">Get started →</button>
        """
        self.assertEqual(MODULE.validate_css_text(css), [])
        findings = MODULE.validate_css_text(css, tells=True)
        self.assertEqual(len(findings), 3, findings)

    def test_plain_labels_have_no_tells(self):
        css = ".label { text-transform: none; } <button>Save changes</button>"
        self.assertEqual(MODULE.validate_css_text(css, tells=True), [])

if __name__ == "__main__":
    unittest.main()
