"""The runner and the assert macros under real Klipper (or Kalico); see klippy_batch.py for setup.

Every script in tests/klippy runs on the test printer in tests/klippy/printer.cfg. A script whose
name ends in _fails must make klippy exit with an error: those show that each assert macro, and
an unknown command, can fail a run.
"""
import pathlib
import unittest

from klipper_test_kit.klippy_batch import run_script, run_script_files, skip_unless_configured

TESTS = pathlib.Path(__file__).resolve().parent
SCRIPTS = TESTS / 'klippy'
PRINTER = (SCRIPTS / 'printer.cfg').read_text(encoding='utf-8')
EXTRA = TESTS / 'klippy_support'


class RealKlipper(unittest.TestCase):
    def test_scripts(self):
        run_script_files(self, SCRIPTS, PRINTER, {})

    def test_the_config_files_of_a_support_folder_can_be_included(self):
        skip_unless_configured(self)
        code, log = run_script(PRINTER + '[include klippy-support/extra.cfg]\n',
                               'ASSERT_VAR MACRO=EXTRA VARIABLE=seen VALUE=1\n', {},
                               support=[EXTRA])
        self.assertEqual(code, 0, log[-3000:])

    def test_a_folder_of_links_can_be_included(self):
        skip_unless_configured(self)
        code, log = run_script(PRINTER + '[include linked/extra.cfg]\n',
                               'ASSERT_VAR MACRO=EXTRA VARIABLE=seen VALUE=1\n',
                               {'linked': EXTRA})
        self.assertEqual(code, 0, log[-3000:])


if __name__ == '__main__':
    unittest.main()
