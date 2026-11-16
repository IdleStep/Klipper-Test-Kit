# Contributing

Thank you for helping. Small, focused changes are easiest to review.

## Before you open a pull request

```sh
pip install -r requirements-test.txt
python -m unittest discover -s tests -v
```

The real-firmware tests (`tests/test_klippy.py`) run in CI against Klipper and Kalico;
[docs/TESTING.md](docs/TESTING.md) says how to run them locally and how the tests fit together.

- Keep the package general. It imports only the standard library and Jinja, and it names no
  repository that uses it. `tests/test_kit.py` fails when that changes.
- Three repositories use this one: Klipper-Hardware-Controls, Klipper-Chamber-Cooldown and
  Klipper-Configs. A change to a name that [docs/API.md](docs/API.md) lists is a major version.
- Add an entry to the CHANGELOG under "Unreleased".
- The Klipper and Kalico revisions in `.github/workflows/tests.yml` are also pinned in the
  workflows of the repositories that use this one. When you move them, change all of them
  together.

## Versions

Versions are annotated tags named `vMAJOR.MINOR.PATCH`. The repositories that use this one pin a
tag.

To release: in a pull request, rename `[Unreleased]` in the CHANGELOG to the version and date,
add the compare link at the bottom and a fresh `[Unreleased]` heading above it. After it is
merged, tag the merge commit.
