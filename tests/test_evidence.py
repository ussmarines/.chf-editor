"""Evidence matching must not infer an effect from a hash alone."""
import unittest

from chflab.evidence import dna_evidence, material_evidence


class EvidenceTest(unittest.TestCase):
    def test_eye_evidence_requires_both_regions_and_counts_each_once(self):
        eye = [[5970, 17], [59564, 32], [0, 33], [0, 40]]
        record = {
            "sha256": "3b622248ee9e0dd38b8ee8b731d670081104697fcbce1cdeb238f121054769db",
            "body_guid": "ad4cb0ef944a79d053c2d3b4582538ad",
            "dna": {"gender_hash": "54ebf49e", "variant_hash": "6e5bd869"},
            "face_parts": {"EyeLeft": eye, "EyeRight": eye, "Jaw": [[1, 2]]},
        }
        result = dna_evidence(record)
        self.assertEqual(len(result["matched_evidence"]), 1)
        self.assertEqual(result["unknown_regions"], ["Jaw"])
        self.assertEqual(result["unknown_region_count"], 1)
        self.assertIn("fichier testé", result["matched_evidence"][0]["scope"])
        self.assertEqual(set(result["matched_evidence"][0]["raw_slots"]),
                         {"EyeLeft", "EyeRight"})
        del record["face_parts"]["EyeRight"]
        self.assertEqual(dna_evidence(record)["matched_evidence"], [])

    def test_mouth_negative_result_is_scoped_to_tested_file(self):
        record = {
            "sha256": "320d8ac838967ade855667a4f5a2b46b4a50aa8644d43f2be21c91a920fbb90f",
            "body_guid": "ad4cb0ef944a79d053c2d3b4582538ad",
            "dna": {"gender_hash": "54ebf49e", "variant_hash": "6e5bd869"},
            "face_parts": {"Mouth": [[5553, 11], [43144, 27], [11712, 36], [5125, 38]]},
        }
        result = dna_evidence(record)
        self.assertEqual(len(result["matched_evidence"]), 2)
        self.assertEqual(result["unknown_region_count"], 0)
        negative = next(item for item in result["matched_evidence"]
                        if "aucune différence nette" in item["observed_effect"])
        self.assertIn("fichier testé", negative["scope"])
        self.assertIn("à vérifier", next(item for item in result["matched_evidence"]
                                         if item is not negative)["scope"])

    def test_dna_scope_requires_female_signature_and_leaves_other_regions_unknown(self):
        record = {
            "sha256": "65c3fa90cb1d8655e2b1209ae5053f7e7e2151225f04f67f3beb35e77076ca70",
            "body_guid": "ad4cb0ef944a79d053c2d3b4582538ad",
            "dna": {"gender_hash": "54ebf49e", "variant_hash": "6e5bd869"},
            "face_parts": {"Nose": [[13530, 25], [22186, 27], [5308, 44], [24510, 45]],
                           "Jaw": [[1, 2]]},
        }
        result = dna_evidence(record)
        self.assertEqual(len(result["matched_evidence"]), 2)
        self.assertEqual(result["unknown_regions"], ["Jaw"])
        self.assertEqual(result["unknown_region_count"], 1)
        self.assertTrue(all("référence" in item["scope"] for item in result["matched_evidence"]))
        self.assertTrue(all(item["raw_slots"] == record["face_parts"]["Nose"]
                            for item in result["matched_evidence"]))

        record["sha256"] = "f" * 64
        self.assertTrue(all("à vérifier" in item["scope"]
                            for item in dna_evidence(record)["matched_evidence"]))
        record["sha256"] = "6b4847de0a5b2e48e237df354a0f2b00c4361f04c9a1cd6433504a1562bd2fcd"
        scopes = [item["scope"] for item in dna_evidence(record)["matched_evidence"]]
        self.assertEqual(sum("fichier testé" in scope for scope in scopes), 1)
        self.assertEqual(sum("à vérifier" in scope for scope in scopes), 1)
        record["dna"]["gender_hash"] = "f6676cdd"
        self.assertEqual(dna_evidence(record)["matched_evidence"], [])
        self.assertEqual(dna_evidence(record)["unknown_region_count"], 2)

    def test_scope_and_unknown_duplicate_hash(self):
        materials = [{"submaterials": []} for _ in range(6)]
        materials[3]["submaterials"] = [{"name_hash": "420b2ed3", "floats": [
            {"name_hash": "unknown", "value": 0.0} for _ in range(5)] + [
            {"name_hash": "a300fab9", "value": 0.9995}], "colors": []}]
        materials[4]["submaterials"] = [{"name_hash": "unrelated", "floats": [
            {"name_hash": "unknown", "value": 0.0} for _ in range(5)] + [
            {"name_hash": "a300fab9", "value": 0.9995}], "colors": []}]
        record = {"sha256": "0a167f3cc96fd79d850cf386d74c4cb9335bc0d645fa0257631390aa3a658597",
                  "material_definitions": materials}
        result = material_evidence(record)
        self.assertEqual(len(result["matched_fields"]), 1)
        self.assertEqual(result["matched_fields"][0]["control"],
                         "Hair > Color > Natural Color (cheveux)")
        self.assertEqual(result["matched_fields"][0]["scope"], "fichier de référence de cet essai")
        self.assertEqual(result["unknown_field_occurrences"], 11)

        record["sha256"] = "f" * 64
        self.assertIn("effet à vérifier", material_evidence(record)["matched_fields"][0]["scope"])

        record["sha256"] = "4c520e124eba4b5c19f7ab6043bebd71ead7f45888ceb99ae172a759cadf34b2"
        self.assertIn("hair_36_m", material_evidence(record)["record_caveats"][0])


if __name__ == "__main__":
    unittest.main()
