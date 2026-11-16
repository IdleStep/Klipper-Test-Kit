# Public interface

What this package promises. The major version changes when anything listed here is renamed or
removed; the [changelog](../CHANGELOG.md) says how the other kinds of change are versioned.

A repository finds a checkout of this one beside itself, adds the checkout's folder to
`sys.path` and imports the package:

```python
import pathlib
import sys

sys.path.append(str(pathlib.Path(__file__).resolve().parents[2] / 'Klipper-Test-Kit'))
from klipper_test_kit import Printer, wrap
```

| Module | Names |
|---|---|
| `klipper_test_kit` | `State`, `wrap`, `Printer` |
| `klipper_test_kit.config_lint` | `config_files`, `lint_file`, `lint` |
| `klipper_test_kit.klippy_batch` | `ENV`, `SUPPORT_DIR`, `skip_unless_configured`, `delayed_gcode_as_macro`, `lay_out_support`, `run_script`, `error_lines`, `run_script_files` |

## The simulator

- `Printer(state=None, idle_timeout=600.)` renders the gcode macros and delayed gcodes of the
  config files it loads, with Klipper's Jinja delimiters, and executes the commands they emit
  against an in-memory printer. The caller gives the printer's devices as `state` (a copy is
  kept) and calls `load(path)` for each config file.
- `run(name, **params)` runs a macro. It gives the macro its own variables as plain names, as
  Klipper does (`{park}` as well as `printer["gcode_macro X"].park`). `execute(line)` runs one
  gcode line.
- The attributes are `state`, `templates`, `commands`, `messages`, `delays` and `idle_timeout`.
  `commands` lists every command that ran and `messages` what the macros sent to the console.
- `execute` gives these commands an effect on the state a macro reads: `SET_GCODE_VARIABLE`,
  `UPDATE_DELAYED_GCODE` (recorded in `delays`), `SET_IDLE_TIMEOUT`, `SET_GCODE_OFFSET` with
  `Z_ADJUST` when the state has a `gcode_move`, `SET_HEATER_TEMPERATURE`, `SET_FAN_SPEED`, `M106`
  and `SET_FILAMENT_SENSOR`. A macro's own name runs the macro. Every command is recorded in
  `commands`, and `action_respond_info` calls are recorded in `messages`. `execute` passes any
  other command to `handle(name, args, tokens)`, which does nothing. A subclass overrides
  `handle` to give a command an effect.
- `State` is a dict with attribute access, as Klipper's status objects are. `wrap` converts the
  dicts inside a value to `State`.

## The linter

- `lint_file(path, check_includes=True, max_columns=100)` returns the problems of one config
  file. `max_columns=None` turns the width check off.
- `lint(root, skip=())` lints every `.cfg` under a folder and returns `{relative path:
  [problems]}` for the files that have any. Includes under `tests/` are not resolved.
- `config_files(root, skip=())` yields the paths `lint` checks: every `.cfg` under a folder,
  except in a folder that starts with a dot or is named in `skip`.

## The real-firmware runner

- `run_script_files(test_case, script_dir, printer_cfg, links, support=())` runs every `*.gcode`
  in a folder as a subtest, on the printer configuration text `printer_cfg`. A script whose name
  ends in `_fails` must make klippy exit with an error; any other must succeed.
- `run_script(printer_cfg, gcode, links, support=())` runs one script and returns the exit code
  and the log. `links` maps a name to a folder that the configuration can include from, beside
  `printer.cfg`.
- The configuration includes `klippy-support/assert.cfg`, which defines `ASSERT_VAR`,
  `ASSERT_HEATER` and `ASSERT_STATUS`. `klippy-support/` also holds the `*.cfg` files of each
  folder in `support`, and a file of the same name replaces an earlier one. `SUPPORT_DIR` is the
  folder of this package's own files.
- The runner reads `KLIPPER_DIR`, `KLIPPY_DICT` and `KLIPPY_PYTHON` (`ENV`). With one of them
  missing the tests are skipped, and `KLIPPY_REQUIRED=1` turns a skipped run into an error.
- `skip_unless_configured(test_case)` skips a test the same way. `delayed_gcode_as_macro(path,
  delayed, macro)` returns the config text of a macro with the body of a delayed gcode, so a
  script can run one tick of a timer. `lay_out_support(folder, support=())` fills the support
  folder, and `error_lines(log)` picks the lines of a klippy log that say what went wrong.
