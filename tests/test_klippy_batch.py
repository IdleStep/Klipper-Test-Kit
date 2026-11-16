"""The parts of the real-firmware runner that need no firmware."""
import os
import pathlib
import tempfile
import unittest
from unittest import mock

from klipper_test_kit import klippy_batch
from klipper_test_kit.klippy_batch import SUPPORT_DIR, lay_out_support


class LayOutSupport(unittest.TestCase):
    def folders(self, tmp, **files):
        """Make a folder per keyword with the given {name: text} files; return their paths."""
        made = []
        for folder, contents in files.items():
            path = pathlib.Path(tmp) / folder
            path.mkdir()
            for name, text in contents.items():
                (path / name).write_text(text, encoding='utf-8')
            made.append(path)
        return made

    def test_the_assert_macros_of_this_package_are_always_there(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = pathlib.Path(tmp) / 'klippy-support'
            lay_out_support(target)
            self.assertEqual(sorted(path.name for path in target.iterdir()), ['assert.cfg'])
            self.assertEqual((target / 'assert.cfg').read_bytes(),
                             (SUPPORT_DIR / 'assert.cfg').read_bytes())

    def test_the_config_files_of_each_folder_are_added_and_nothing_else(self):
        with tempfile.TemporaryDirectory() as tmp:
            first, second = self.folders(tmp, one={'a.cfg': 'A', 'run.gcode': 'G'},
                                         two={'b.cfg': 'B'})
            target = pathlib.Path(tmp) / 'klippy-support'
            lay_out_support(target, [first, second])
            self.assertEqual(sorted(path.name for path in target.iterdir()),
                             ['a.cfg', 'assert.cfg', 'b.cfg'])

    def test_a_later_folder_replaces_a_file_of_the_same_name(self):
        with tempfile.TemporaryDirectory() as tmp:
            first, second = self.folders(tmp, one={'a.cfg': 'first'}, two={'a.cfg': 'second'})
            target = pathlib.Path(tmp) / 'klippy-support'
            lay_out_support(target, [first, second])
            self.assertEqual((target / 'a.cfg').read_text(encoding='utf-8'), 'second')

    def test_a_folder_of_the_caller_can_replace_the_assert_macros(self):
        with tempfile.TemporaryDirectory() as tmp:
            (own,) = self.folders(tmp, own={'assert.cfg': 'own'})
            target = pathlib.Path(tmp) / 'klippy-support'
            lay_out_support(target, [own])
            self.assertEqual((target / 'assert.cfg').read_text(encoding='utf-8'), 'own')


class Environment(unittest.TestCase):
    def test_a_run_without_the_firmware_is_skipped(self):
        with mock.patch.dict(os.environ, clear=True):
            with self.assertRaises(unittest.SkipTest) as raised:
                klippy_batch.skip_unless_configured(self)
        for name in klippy_batch.ENV:
            self.assertIn(name, str(raised.exception))

    def test_klippy_required_turns_the_skip_into_an_error(self):
        with mock.patch.dict(os.environ, {'KLIPPY_REQUIRED': '1'}, clear=True):
            with self.assertRaises(RuntimeError):
                klippy_batch.skip_unless_configured(self)

    def test_a_configured_run_is_not_skipped(self):
        with mock.patch.dict(os.environ, {name: 'x' for name in klippy_batch.ENV}, clear=True):
            klippy_batch.skip_unless_configured(self)


class Helpers(unittest.TestCase):
    def test_a_delayed_gcode_becomes_a_macro_with_the_same_body(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = pathlib.Path(tmp) / 'timer.cfg'
            path.write_text('[delayed_gcode LOOP]\ngcode:\n  M117 one\n  M117 two\n',
                            encoding='utf-8')
            self.assertEqual(klippy_batch.delayed_gcode_as_macro(path, 'LOOP', 'TICK'),
                             '[gcode_macro TICK]\ngcode:\n  M117 one\n  M117 two\n')

    def test_the_error_lines_are_the_ones_that_say_what_went_wrong(self):
        log = 'Starting\nConfig error: bad option\nLoaded\nUnknown command:"X"\n'
        self.assertEqual(klippy_batch.error_lines(log),
                         'Config error: bad option\nUnknown command:"X"\n---\n')


if __name__ == '__main__':
    unittest.main()
