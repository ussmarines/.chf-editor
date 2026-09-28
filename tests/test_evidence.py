"""Evidence matching must not expose private fingerprints or overstate effects."""
import unittest

from chflab.evidence import dna_evidence, material_evidence


class EvidenceTest(unittest.TestCase):
    def test_eye_evidence_requires_both_regions_and_uses_cautious_scope(self):
        eye = [[5970, 17], [59564, 32], [0, 33], [0, 40]]
        record = {
            "sha256": "not-published",
            "body_guid": "ad4cb0ef944a79d053c2d3b4582538ad",
            "dna": {"gender_hash": "54ebf49e", "variant_hash": "6e5bd869"},
            "face_parts": {"EyeLeft": eye, "EyeRight": eye, "Jaw": [[1, 2]]},
        }
        result = dna_evidence(record)
        self.assertEqual(len(result["matched_evidence"]), 1)
        self.assertEqual(result["unknown_regions"], ["Jaw"])
        self.assertEqual(result["unknown_region_count"], 1)
        self.assertIn("verify the effect", result["matched_evidence"][0]["scope"])
        self.assertNotIn("reference_sha256", result["matched_evidence"][0])
        self.assertEqual(set(result["matched_evidence"][0]["raw_slots"]),
                         {"EyeLeft", "EyeRight"})
        del record["face_parts"]["EyeRight"]
        self.assertEqual(dna_evidence(record)["matched_evidence"], [])

    def test_mouth_evidence_is_scoped_to_matching_signature_only(self):
        record = {
            "sha256": "private-fingerprint-not-used",
            "body_guid": "ad4cb0ef944a79d053c2d3b4582538ad",
            "dna": {"gender_hash": "54ebf49e", "variant_hash": "6e5bd869"},
            "face_parts": {"Mouth": [[5553, 11], [43144, 27], [11712, 36], [5125, 38]]},
        }
        result = dna_evidence(record)
        self.assertEqual(len(result["matched_evidence"]), 2)
        self.assertEqual(result["unknown_region_count"], 0)
        self.assertTrue(all("verify the effect" in item["scope"]
                            for item in result["matched_evidence"]))

        record["dna"]["gender_hash"] = "different-signature"
        self.assertEqual(dna_evidence(record)["matched_evidence"], [])
        self.assertEqual(dna_evidence(record)["unknown_region_count"], 1)

    def test_material_evidence_uses_structure_without_returning_file_hashes(self):
        materials = [{"submaterials": []} for _ in range(6)]
        materials[3]["submaterials"] = [{"name_hash": "420b2ed3", "floats": [
            {"name_hash": "unknown", "value": 0.0} for _ in range(5)] + [
            {"name_hash": "a300fab9", "value": 0.9995}], "colors": []}]
        materials[4]["submaterials"] = [{"name_hash": "unrelated", "floats": [
            {"name_hash": "unknown", "value": 0.0} for _ in range(5)] + [
            {"name_hash": "a300fab9", "value": 0.9995}], "colors": []}]
        record = {"sha256": "private-fingerprint-not-used", "material_definitions": materials}
        result = material_evidence(record)
        self.assertEqual(len(result["matched_fields"]), 1)
        self.assertEqual(result["matched_fields"][0]["control"],
                         "Hair > Color > Natural Color (hair)")
        self.assertIn("verify the effect", result["matched_fields"][0]["scope"])
        self.assertNotIn("reference_sha256", result["matched_fields"][0])
        self.assertEqual(result["unknown_field_occurrences"], 11)


if __name__ == "__main__":
    unittest.main()
