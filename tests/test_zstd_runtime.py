import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from chflab.zstd_runtime import check_zstd, resolve_zstd


class ZstdRuntimeTest(unittest.TestCase):
    def test_bad_explicit_or_environment_path_never_falls_back(self):
        with tempfile.TemporaryDirectory() as tmp:
            absent = str(Path(tmp) / "missing.dll")
            with patch.dict(os.environ, {"CHF_ZSTD_DLL": absent}):
                with self.assertRaises(ValueError):
                    resolve_zstd()
                with self.assertRaises(ValueError):
                    resolve_zstd(absent)

    def test_not_a_native_library_has_actionable_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "not-a-library.dll"
            path.write_text("synthetic invalid library")
            with self.assertRaisesRegex(ValueError, "compatible Zstandard"):
                check_zstd(path)

    def test_real_library_roundtrip_and_environment_resolution(self):
        configured = os.environ.get("CHF_ZSTD_DLL")
        if not configured:
            self.skipTest("set CHF_ZSTD_DLL for the native-library roundtrip")
        result = check_zstd(configured)
        self.assertEqual(result["roundtrip"], "PASS")
        self.assertTrue(result["version"])
        self.assertEqual(resolve_zstd(), Path(configured).resolve())
