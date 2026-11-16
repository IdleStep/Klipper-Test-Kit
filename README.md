# Klipper Test Kit

[![Test kit checks](https://github.com/IdleStep/Klipper-Test-Kit/actions/workflows/tests.yml/badge.svg)](https://github.com/IdleStep/Klipper-Test-Kit/actions/workflows/tests.yml)

Test tools for repositories of Klipper and Kalico config files. A repository says which devices
its printer has and which config files to load; this one runs the macros, lints the files and
loads them in real firmware, with no printer.

It has three tools, which share no state and can be used one at a time:

| Tool | What it does |
|---|---|
| `klipper_test_kit.Printer` | A macro simulator. It renders the real `gcode_macro` and `delayed_gcode` templates with Klipper's Jinja delimiters and executes the commands they emit against an in-memory printer. Tests then check the state, the commands that ran and the messages. |
| `klipper_test_kit.config_lint` | Static checks for config files: files Klipper would fail to parse, broken includes, indentation, trailing whitespace, CRLF endings, malformed `RESPOND` messages, public macros without a description and macro options that stock Klipper rejects. |
| `klipper_test_kit.klippy_batch` | A runner that gives a printer configuration and a gcode script to real Klipper or Kalico in batch mode. A script checks macro variables, heater targets and status fields with the macros of `klippy/assert.cfg`. |

The simulator is fast and runs anywhere, but it is not Klipper. The runner is Klipper, but it
cannot fire timers or read a fan's speed back. The linter reads the text. Use all three: each
catches what the others cannot.

The major version is the version of the public interface. Only a major release renames or
removes a name that [docs/API.md](docs/API.md) lists, and the [changelog](CHANGELOG.md) lists
every release.

## Requirements

- Python 3 and Jinja2. Klipper renders macros with Jinja 2.11 and Kalico with 3.1. CI runs the
  tests of this repository on Python 3.12 with both.
- For the runner: a Klipper or Kalico checkout, its linux process MCU built, and Python with
  the firmware's `scripts/klippy-requirements.txt` installed.

## Use

Check this repository out beside yours, or at a path of your choice, and add it to `sys.path`
in your tests:

```python
import pathlib
import sys

sys.path.append(str(pathlib.Path(__file__).resolve().parents[2] / 'Klipper-Test-Kit'))
from klipper_test_kit import Printer, wrap

printer = Printer(wrap({'heater_generic chamber': {'target': 0.}}))
printer.load('chamber.cfg')
printer.run('CHAMBER', TEMP=60)
assert printer.state['heater_generic chamber'].target == 60
```

A command the simulator has no effect for goes to `Printer.handle`. A subclass overrides it to
give that command an effect.

[docs/API.md](docs/API.md) lists every name, [docs/TESTING.md](docs/TESTING.md) says how to
run the real-firmware tests, and the tests of this repository are the examples.

## Used by

- [Klipper-Hardware-Controls](https://github.com/IdleStep/Klipper-Hardware-Controls)
- [Klipper-Chamber-Cooldown](https://github.com/IdleStep/Klipper-Chamber-Cooldown)
- [Klipper-Configs](https://github.com/IdleStep/Klipper-Configs)

## License

GPL-3.0, like Klipper. See [LICENSE](LICENSE).
