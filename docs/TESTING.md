# Testing

The tests of this repository run the three tools on small examples, and check that the package
stays general.

| Test | What it covers |
|---|---|
| `tests/test_kit.py` | The simulator runs with devices the caller gives it. The package imports only the standard library and Jinja, and names no repository that uses it. |
| `tests/test_config_lint.py` | Each rule of the linter, the config files of this repository, and the length of the longest path. |
| `tests/test_klippy_batch.py` | The parts of the runner that need no firmware: the support folder, the environment and the log reader. |
| `tests/test_klippy.py` | The runner and the assert macros under real Klipper and Kalico. |
| `tests/test_api_doc.py` | `docs/API.md` lists the public names and the names exist. |

Run everything but the real-firmware tests:

```sh
pip install -r requirements-test.txt
python -m unittest discover -s tests -v
```

The real-firmware tests are skipped until `KLIPPER_DIR`, `KLIPPY_DICT` and `KLIPPY_PYTHON` are
set; `KLIPPY_REQUIRED=1` makes a skip an error. The `klippy` jobs of
[`.github/workflows/tests.yml`](../.github/workflows/tests.yml) show the steps: check out Klipper or
Kalico, copy `test/configs/linuxprocess.config` to `.config`, run `make olddefconfig` and `make`,
install `scripts/klippy-requirements.txt` into a virtual environment, and point the three
variables at the checkout, the dictionary `out/klipper.dict` and that environment's Python.

Klipper renders macros with Jinja 2.11 and Kalico with 3.1, so run the simulator tests with
both: `pip install Jinja2==2.11.3 MarkupSafe==2.0.1`.
