"""docs/API.md lists the names other repositories import, and the names it lists exist.

Run with: python -m unittest discover -s tests -v
"""
import importlib
import inspect
import pathlib
import re
import unittest

API = (pathlib.Path(__file__).resolve().parents[1] / 'docs' / 'API.md').read_text(encoding='utf-8')
TOOLS = {
    'klipper_test_kit': ['State', 'wrap', 'Printer'],
    'klipper_test_kit.config_lint': ['config_files', 'lint_file', 'lint'],
    'klipper_test_kit.klippy_batch': [
        'ENV', 'SUPPORT_DIR', 'skip_unless_configured', 'delayed_gcode_as_macro',
        'lay_out_support', 'run_script', 'error_lines', 'run_script_files'],
}
PRINTER_METHODS = ['load', 'run', 'execute', 'handle']


class PublicInterface(unittest.TestCase):
    def mentioned(self, name):
        return re.search(r'`%s`|`[^`]*\b%s\b[^`]*`' % (name, name), API) is not None

    def test_the_listed_names_exist_and_are_in_the_text(self):
        for module, names in TOOLS.items():
            tool = importlib.import_module(module)
            for name in names:
                with self.subTest(module=module, name=name):
                    self.assertTrue(hasattr(tool, name), '%s.%s does not exist' % (module, name))
                    self.assertTrue(self.mentioned(name), '%s is not in docs/API.md' % name)

    def test_every_public_name_of_a_module_is_listed(self):
        for module, names in TOOLS.items():
            tool = importlib.import_module(module)
            if module == 'klipper_test_kit':
                public = set(tool.__all__)
            else:
                # The functions the module defines, and the two settings of the runner.
                public = {name for name, value in vars(tool).items()
                          if inspect.isfunction(value) and value.__module__ == module
                          and not name.startswith('_')}
                public |= {name for name in ('ENV', 'SUPPORT_DIR') if hasattr(tool, name)}
            with self.subTest(module=module):
                self.assertEqual(sorted(public - set(names)), [])

    def test_the_methods_of_the_printer_exist_and_are_listed(self):
        from klipper_test_kit import Printer
        for name in PRINTER_METHODS:
            with self.subTest(method=name):
                self.assertTrue(callable(getattr(Printer, name)))
                self.assertTrue(self.mentioned(name))

    def test_the_environment_variables_of_the_runner_are_listed(self):
        from klipper_test_kit.klippy_batch import ENV
        for name in ENV + ['KLIPPY_REQUIRED']:
            with self.subTest(variable=name):
                self.assertTrue(self.mentioned(name))


if __name__ == '__main__':
    unittest.main()
