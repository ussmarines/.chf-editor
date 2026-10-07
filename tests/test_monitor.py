import json
from copy import deepcopy
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from chf import variant_param
from chflab.inspector import inspect
from chflab.monitor import SaveMonitor, classify


class MonitorTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture = os.environ.get('CHF_TEST_SOURCE')
        cls.dll = os.environ.get('CHF_ZSTD_DLL')
        if not cls.fixture or not cls.dll:
            raise unittest.SkipTest('Set CHF_TEST_SOURCE and CHF_ZSTD_DLL for monitoring integration tests')

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.watch = self.root/'watched'
        self.watch.mkdir()
        self.source = self.watch/'baseline.chf'
        self.original = Path(self.fixture).read_bytes()
        self.source.write_bytes(self.original)
        record = inspect(self.source, self.dll, True)
        entry = record['material_definitions'][0]['submaterials'][0]['floats'][0]
        self.candidate = self.root/'candidate.chf'
        variant_param(self.source, self.candidate, self.dll, record['sha256'], 0, 0, 'float', 0,
                      entry['name_hash'], str(entry['value']+0.125), None, 'synthetic test', 'isolated float')

    def monitor(self, folder=False):
        return SaveMonitor(self.source, self.dll, self.root/'sessions', 'Synthetic control', 'test build', folder, 1)

    def test_stable_single_change_is_archived_but_not_visually_validated(self):
        monitor = self.monitor()
        self.source.write_bytes(self.candidate.read_bytes())
        self.assertEqual(monitor.poll(0), [])
        self.assertEqual(monitor.poll(0.5), [])
        event, = monitor.poll(1)
        self.assertEqual(event['status'], 'candidate_association')
        self.assertEqual(len(event['categories']), 1)
        self.assertEqual(event['visual_effect'], 'not observed')
        self.assertEqual(event['mapping_validation'], 'not confirmed')
        self.assertEqual((monitor.session/'0000.chf').read_bytes(), self.original)
        self.assertEqual((monitor.session/'0001.chf').read_bytes(), self.candidate.read_bytes())
        self.assertEqual(monitor.poll(3), [])
        self.assertEqual(self.source.read_bytes(), self.candidate.read_bytes())

    def test_partial_and_bad_crc_are_retried_without_advancing_baseline(self):
        monitor = self.monitor()
        self.source.write_bytes(self.original[:100])
        self.assertEqual(monitor.poll(0), [])
        self.assertTrue(monitor.error)
        bad = bytearray(self.candidate.read_bytes())
        bad[64] ^= 1
        self.source.write_bytes(bad)
        monitor.poll(1)
        self.assertEqual(monitor.poll(2), [])
        self.assertTrue(monitor.error)
        self.assertEqual(monitor.sequence, 0)
        self.assertFalse((monitor.session/'0001.chf').exists())
        self.source.write_bytes(self.candidate.read_bytes())
        self.assertEqual(monitor.poll(3), [])
        self.assertEqual(len(monitor.poll(4)), 1)

    def test_new_name_duplicate_is_ignored_then_changed_save_is_detected(self):
        monitor = self.monitor(True)
        duplicate = self.watch/'duplicate.chf'
        duplicate.write_bytes(self.original)
        monitor.poll(0)
        self.assertEqual(monitor.poll(1), [])
        changed = self.watch/'new-save.chf'
        changed.write_bytes(self.candidate.read_bytes())
        monitor.poll(2)
        event, = monitor.poll(3)
        self.assertEqual(event['observed_file'], str(changed))
        self.assertEqual(self.source.read_bytes(), self.original)

    def test_multiple_changed_files_pause_without_guessing(self):
        monitor = self.monitor(True)
        self.source.write_bytes(self.candidate.read_bytes())
        (self.watch/'other.chf').write_bytes(self.candidate.read_bytes())
        event, = monitor.poll(0)
        self.assertEqual(event['status'], 'multiple_files_changed')
        self.assertFalse(monitor.active)
        self.assertEqual(monitor.sequence, 0)

    def test_return_to_baseline_records_a_second_gesture(self):
        monitor = self.monitor()
        self.source.write_bytes(self.candidate.read_bytes())
        monitor.poll(0)
        forward, = monitor.poll(1)
        self.source.write_bytes(self.original)
        monitor.poll(2)
        reverse, = monitor.poll(3)
        self.assertEqual(reverse['after_sha256'], forward['before_sha256'])
        self.assertEqual(reverse['before_sha256'], forward['after_sha256'])
        monitor.stop()
        self.assertEqual(monitor.poll(4), [])

    def test_session_cannot_write_into_watched_directory(self):
        with self.assertRaises(ValueError):
            SaveMonitor(self.source, self.dll, self.watch/'sessions', 'control', 'build')

    def test_dna_region_group_and_identity_change_have_distinct_verdicts(self):
        before = inspect(self.source, self.dll, True)
        after = deepcopy(before)
        after['face_parts']['Nose'][0][0] += 1
        after['face_parts']['Nose'][1][0] -= 1
        event = classify(before, after)
        self.assertEqual(event['categories'], ['DNA/Nose'])
        self.assertEqual(event['status'], 'candidate_association')
        after['voice_guid'] = 'synthetic different identity'
        self.assertEqual(classify(before, after)['status'], 'incompatible_reference')

    def test_material_change_with_unrelated_metadata_is_ambiguous(self):
        before = inspect(self.source, self.dll, True)
        after = inspect(self.candidate, self.dll, True)
        after['flags'] = before['flags'] ^ 1
        self.assertEqual(classify(before, after)['status'], 'ambiguous_group')


class ScreenMetricTest(unittest.TestCase):
    def test_pixel_metric_is_not_an_anatomical_verdict(self):
        try:
            from PIL import Image
        except ImportError:
            self.skipTest('Optional Pillow dependency is not installed')
        from chflab.screen import pixel_change
        black = Image.new('RGB', (4, 4), 'black')
        white = Image.new('RGB', (4, 4), 'white')
        self.assertEqual(pixel_change(black, black), 0)
        self.assertEqual(pixel_change(black, white), 100)
        self.assertIsNone(pixel_change(black, Image.new('RGB', (5, 4))))

    def test_other_foreground_application_never_falls_back_to_desktop(self):
        try:
            from PIL import ImageGrab
        except ImportError:
            self.skipTest('Optional Pillow dependency is not installed')
        from chflab.screen import capture_game
        with patch('chflab.screen.game_window', side_effect=ValueError('not the game')):
            with patch.object(ImageGrab, 'grab') as grab:
                with self.assertRaises(ValueError):
                    capture_game()
                grab.assert_not_called()

    def test_native_uniform_capture_is_rejected_with_synthetic_image(self):
        try:
            from PIL import Image, ImageGrab
        except ImportError:
            self.skipTest('Optional Pillow dependency is not installed')
        from chflab.screen import capture_game
        with patch('chflab.screen.game_window', return_value=123):
            with patch.object(ImageGrab, 'grab', return_value=Image.new('RGB', (4, 4))):
                with self.assertRaisesRegex(ValueError, 'Empty/uniform'):
                    capture_game()
