# Changelog

Versions follow the public interface listed in [docs/API.md](docs/API.md).

- Major: a listed name is renamed or removed, or a listed function stops taking an argument it
  took.
- Minor: something is added, or a check changes in a way that can change what another
  repository's tests fail on. The entry says what to check.
- Patch: a fix that makes a tool do what its documentation says.

## [Unreleased]

## [1.0.0] - 2026-11-15

### Added
- `klipper_test_kit.Printer`, the macro simulator of Klipper-Hardware-Controls without anything
  particular to that package: `Printer(state, idle_timeout)` takes the printer's devices from its
  caller, and a subclass gives a command the simulator has no effect for one by overriding
  `handle`.
- `klipper_test_kit.config_lint`, the static checks for config files, as they were in
  Klipper-Hardware-Controls.
- `klipper_test_kit.klippy_batch`, the real-firmware runner, as it was in
  Klipper-Hardware-Controls except for the support files. `run_script` and `run_script_files` take
  `support`, a list of folders whose `*.cfg` files `klippy-support/` holds besides the package's
  own, and a file of the same name replaces an earlier one. They copy the files, not link them,
  so a Windows checkout works. `lay_out_support` is the function that does it.
- `klippy/assert.cfg` holds `ASSERT_VAR`, `ASSERT_HEATER` and `ASSERT_STATUS`. The macros that
  record a fan, pin or LED stay with the repository whose printer has those devices.
- Tests for each tool, for the public interface and for the package staying general, and a CI
  workflow that runs them on Jinja 2.11 and 3.1 and runs the real-firmware tests on Klipper and
  Kalico.

[Unreleased]: https://github.com/IdleStep/Klipper-Test-Kit/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/IdleStep/Klipper-Test-Kit/tree/v1.0.0
