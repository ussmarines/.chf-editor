"""Guidance must distinguish observations from names and negative results."""
from copy import deepcopy
import unittest

from chflab.evidence import material_options, material_evidence, CATALOG, DNA_CATALOG


class GuidedTest(unittest.TestCase):
    def reference(self):
        materials = [{"submaterials": []} for _ in range(6)]
        materials[3]["submaterials"] = [{"name_hash": "2b6fdea7", "floats": [],
            "colors": [{"name_hash": "unrelated", "rgba": [0, 0, 0, 255]},
                       {"name_hash": "09c9c7a2", "rgba": [0, 40, 66, 255]}]}]
        materials[5]["submaterials"] = [{"name_hash": "02176211", "floats": [],
            "colors": [{"name_hash": "09c9c7a2", "rgba": [254, 254, 254, 255]}]}]
        return {"material_definitions": materials}

    def test_negative_observation_is_not_an_observed_visual_change(self):
        record = self.reference()
        original = deepcopy(record)
        self.assertEqual(len(material_options(record)), 2)
        positive = material_options(record, "Observed visual changes")
        self.assertEqual(len(positive), 1)
        self.assertEqual(positive[0]["coordinates"], (3, 0, "color", 1))
        self.assertEqual(positive[0]["evidence"]["tested_channels"], ["R"])
        self.assertEqual(len(material_options(record, "All raw parameters")), 3)
        self.assertEqual(record, original)
        counts = material_evidence(record)
        self.assertEqual(counts["historical_negative_matches"], 1)
        self.assertEqual(counts["without_historical_visual_change"], 2)

    def test_hash_match_on_wrong_submaterial_does_not_qualify(self):
        record = self.reference()
        record["material_definitions"][3]["submaterials"][0]["name_hash"] = "different"
        self.assertEqual(material_options(record, "Observed visual changes"), [])

    def test_all_observations_report_separate_validation_axes(self):
        for item in CATALOG + DNA_CATALOG:
            self.assertEqual(set(item["validation"]),
                             {"ui_mapping", "game_load", "game_save", "visual_effect", "scope"})
            self.assertIn("historical", item["validation"]["scope"])
