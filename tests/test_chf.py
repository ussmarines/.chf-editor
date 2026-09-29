"""Focused container and single-change checks; no private fixture is stored here."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


class ChfCliTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture = os.environ.get("CHF_TEST_SOURCE")
        cls.dll = os.environ.get("CHF_ZSTD_DLL")
        if not cls.fixture or not cls.dll:
            raise unittest.SkipTest("set CHF_TEST_SOURCE and CHF_ZSTD_DLL to run local tests")

    def cli(self, *args):
        return subprocess.run([sys.executable, str(ROOT / "chf.py"), "--zstd-dll", self.dll,
                               *map(str, args)], cwd=ROOT, capture_output=True, text=True)

    def test_rejects_corrupted_crc_and_length(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.chf"
            raw = bytearray(Path(self.fixture).read_bytes())
            raw[64] ^= 1
            path.write_bytes(raw)
            self.assertNotEqual(self.cli("inspect", path).returncode, 0)
            path.write_bytes(raw[:-1])
            self.assertNotEqual(self.cli("inspect", path).returncode, 0)

    def test_balanced_dna_change_and_no_overwrite(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(self.fixture)
            before_bytes = source.read_bytes()
            info = json.loads(self.cli("inspect", source).stdout)
            weights = [entry[0] for entry in info["face_parts"]["Nose"]]
            slot = next(i for i, weight in enumerate(weights) if weight < 65535)
            balance_slot = next(i for i, weight in enumerate(weights) if i != slot and weight > 0)
            new = weights[slot] + 1
            target = Path(directory) / "variant.chf"
            args = ("variant", source, target, "--part", "Nose", "--slot", str(slot),
                    "--balance-slot", str(balance_slot), "--value", str(new),
                    "--game-version", "test", "--control", "unit test")
            without_balance = list(args)
            del without_balance[without_balance.index("--balance-slot"):without_balance.index("--balance-slot") + 2]
            self.assertNotEqual(self.cli(*without_balance).returncode, 0)
            result = self.cli(*args)
            self.assertEqual(result.returncode, 0, result.stderr)
            manifest = json.loads(result.stdout)
            logical = [c for c in manifest["structured_diff"] if c["path"] != "compressed_size"]
            self.assertEqual({c["path"] for c in logical},
                             {f"face_parts.Nose[{slot}][0]", f"face_parts.Nose[{balance_slot}][0]"})
            reread = json.loads(self.cli("inspect", target).stdout)
            self.assertEqual(sum(weights), sum(value for value, _ in reread["face_parts"]["Nose"]))
            self.assertEqual([entry[1] for entry in info["face_parts"]["Nose"]],
                             [entry[1] for entry in reread["face_parts"]["Nose"]])
            self.assertEqual(source.read_bytes(), before_bytes)
            self.assertNotEqual(self.cli(*args).returncode, 0)
            self.assertEqual(target.read_bytes().__len__(), 4096)
            self.assertTrue(target.with_suffix(".experiment.json").exists())
            blocked = Path(directory) / "manifest_taken.chf"
            blocked_manifest = blocked.with_suffix(".experiment.json")
            blocked_manifest.write_text("existing record", encoding="utf-8")
            blocked_args = list(args)
            blocked_args[blocked_args.index(target)] = blocked
            self.assertNotEqual(self.cli(*blocked_args).returncode, 0)
            self.assertFalse(blocked.exists())
            self.assertEqual(blocked_manifest.read_text(encoding="utf-8"), "existing record")
            invalid = Path(directory) / "invalid.chf"
            invalid_args = list(args)
            invalid_args[invalid_args.index(target)] = invalid
            invalid_args[invalid_args.index("--balance-slot") + 1] = str(slot)
            self.assertNotEqual(self.cli(*invalid_args).returncode, 0)
            self.assertFalse(invalid.exists())
            impossible_value = weights[slot] + weights[balance_slot] + 1
            if impossible_value <= 65535:
                insufficient = list(args)
                insufficient[insufficient.index(target)] = invalid
                insufficient[insufficient.index("--value") + 1] = str(impossible_value)
                self.assertNotEqual(self.cli(*insufficient).returncode, 0)
                self.assertFalse(invalid.exists())

    def test_raw_material_single_change_and_stale_source(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(self.fixture)
            original = source.read_bytes()
            info = json.loads(self.cli("inspect", source).stdout)
            selected = next(
                (mi, si, kind, pi, entry)
                for mi, material in enumerate(info["material_definitions"])
                for si, sub in enumerate(material["submaterials"])
                for kind in ("floats", "colors")
                for pi, entry in enumerate(sub[kind])
                if kind == "colors" or -1000 < entry["value"] < 1000)
            mi, si, kind, pi, entry = selected
            color = kind == "colors"
            old = entry["rgba"][0] if color else entry["value"]
            value = (old + 1 if old < 255 else old - 1) if color else old + 0.125
            target = Path(directory) / "param.chf"
            args = ("variant-param", source, target, "--expected-source-sha256", info["sha256"],
                    "--material-index", mi, "--submaterial-index", si,
                    "--kind", "color" if color else "float", "--param-index", pi,
                    "--name-hash", entry["name_hash"], "--value", value,
                    "--game-version", "test", "--control", "raw unit test")
            if color:
                args += ("--channel", "R")
            stale = list(args)
            stale[stale.index("--expected-source-sha256") + 1] = "0" * 64
            self.assertNotEqual(self.cli(*stale).returncode, 0)
            self.assertFalse(target.exists())
            result = self.cli(*args)
            self.assertEqual(result.returncode, 0, result.stderr)
            manifest = json.loads(result.stdout)
            logical = [c for c in manifest["structured_diff"] if c["path"] != "compressed_size"]
            self.assertEqual(len(logical), 1)
            self.assertEqual(logical[0]["path"],
                             f"material_definitions[{mi}].submaterials[{si}].{kind}[{pi}]"
                             + (".rgba[0]" if color else ".value"))
            self.assertEqual(source.read_bytes(), original)
            self.assertEqual(target.stat().st_size, 4096)
            self.assertEqual(json.loads(self.cli("inspect", target).stdout)["sha256"],
                             manifest["output_sha256"])


if __name__ == "__main__":
    unittest.main()
