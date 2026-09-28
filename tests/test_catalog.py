"""Source-name and CIG byte-order checks for the local inspector UI."""
import unittest

from gui import KNOWN_GUIDS, KNOWN_NAMES, annotate_hashes, cig_display


class CatalogTest(unittest.TestCase):
    def test_starbreaker_name_hash(self):
        self.assertEqual(KNOWN_NAMES["970753bd"], "BodyColor")
        self.assertEqual(KNOWN_NAMES["e22777e8"], "FrecklesAmount")

    def test_starchar_guid_matches_game_record(self):
        raw = "894d688ce913909a29aaf8c4009a34b2"
        display = cig_display(raw)
        self.assertEqual(display, "9a9013e9-8c68-4d89-b234-9a00c4f8aa29")
        self.assertEqual(KNOWN_GUIDS["itemPortGuids"][display], "hair_36")
        record = annotate_hashes([{"port_hash": "951a6013", "item_guid": raw}])[0]
        self.assertEqual(record["port_hash_name"], "hair_itemport")
        self.assertEqual(record["item_guid_name"], "hair_36")


if __name__ == "__main__":
    unittest.main()
