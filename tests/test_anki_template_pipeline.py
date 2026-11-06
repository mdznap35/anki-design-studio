import base64
import json
import re
import unittest
from pathlib import Path
from unittest.mock import patch

import tts
from app import _resolve_design_fields


class TemplateFieldRegressionTests(unittest.TestCase):
    def test_real_design_41_declares_every_referenced_field(self):
        source = Path("public/designs_100.js").read_text(encoding="utf-8")
        payload = source.split("=", 1)[1].strip().rstrip(";")
        designs = json.loads(payload)
        design = next(item for item in designs if item.get("name") == "41")
        # The legacy browser payload omits fields; reproduce that exact path.
        fields = _resolve_design_fields(None, design.get("front", ""), design.get("back", ""))
        referenced = set(re.findall(r'{{\s*(?:[#\^/]\s*)?(?:text:|type:)?\s*([^{}]+?)\s*}}',
                                    design.get("front", "") + design.get("back", "")))
        for raw in referenced:
            field = raw.strip()
            if field not in {"FrontSide", "Tags", "Deck", "Subdeck", "Card", "CardFlag", "Note", "Template"}:
                self.assertIn(field, fields, "design 41 references an undeclared field: " + field)
        self.assertIn("Extras", fields)

    def test_declared_fields_are_preserved_without_duplicates(self):
        fields = _resolve_design_fields(["French", "Arabic", "Extras"], "{{French}}", "{{Extras}}")
        self.assertEqual(fields.count("French"), 1)
        self.assertEqual(fields.count("Extras"), 1)

    def test_combined_audio_contains_both_gap_boundaries(self):
        def silence(ms):
            return ("S%d" % int(ms)).encode("ascii") if ms else b""

        def concat(parts):
            return b"|".join(part for part in parts if part)

        cfg = {
            "frGapBefore": 100,
            "frGapAfter": 250,
            "arGapBefore": 400,
            "arGapAfter": 150,
        }
        with patch.object(tts, "_silence", side_effect=silence), patch.object(tts, "_concat_mp3", side_effect=concat):
            _fr, _ar, both = tts._build_clips(b"FR", b"AR", cfg)
        payload = both.split(",", 1)[1] if "," in both else both
        self.assertEqual(base64.b64decode(payload), b"S100|FR|S250|S400|AR|S150")


if __name__ == "__main__":
    unittest.main()
