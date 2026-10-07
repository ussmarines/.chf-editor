"""Guidance must distinguish observations from names and negative results."""
from copy import deepcopy
import unittest

from chflab.evidence import material_options, material_evidence, CATALOG, DNA_CATALOG
from gui import VALIDATION_LABELS


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

    def test_owner_acceptance_is_limited_to_six_capture_backed_effects(self):
        accepted = {item["id"] for item in CATALOG
                    if item["validation"]["visual_effect"] == "owner_validated_capture"}
        self.assertEqual(accepted, {
            "freckles-opacity-female", "female-hair-base-melanin",
            "male-hair-base-melanin", "male-beard-base-melanin",
            "male-brow-base-melanin", "female-hair-root-dye-red-channel",
        })
        self.assertIn("VALIDATED by owner", VALIDATION_LABELS["owner_validated_capture"])
        by_id = {item["id"]: item for item in CATALOG}
        root_dye = by_id["female-hair-root-dye-red-channel"]
        self.assertEqual(root_dye["validation"]["game_save"], "not_authenticated")
        self.assertEqual(root_dye["validation"]["ui_mapping"], "group_only")
        self.assertEqual(root_dye["tested_channels"], ["R"])
        for item_id in ("female-hair-dye-amount", "female-hair-variation"):
            self.assertEqual(by_id[item_id]["validation"]["visual_effect"], "not_isolated")
        self.assertEqual(by_id["female-secondary-hair-dye-copy-negative"]
                         ["validation"]["visual_effect"], "no_visible_change")
        self.assertFalse(any(item["validation"]["visual_effect"] == "owner_validated_capture"
                             for item in DNA_CATALOG))

    def test_owner_validated_effect_remains_in_guided_filter_and_counts(self):
        record = self.reference()
        match = material_options(record, "Observed visual changes")[0]["evidence"]
        self.assertEqual(match["validation"]["visual_effect"], "owner_validated_capture")
        self.assertIn("verify the effect on this file", match["scope"])
        counts = material_evidence(record)
        self.assertEqual(counts["historical_visual_change_matches"], 1)
        self.assertEqual(counts["historical_negative_matches"], 1)
