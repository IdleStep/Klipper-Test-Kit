# Security

This package only runs in tests: it reads config files and, for the real-firmware runner, starts
a Klipper process on a test configuration. It never connects to a printer. A bug that makes a
test pass when the code under test is wrong is still worth reporting, because other repositories
rely on those results for macros that switch heaters and fans.

Report it in a public issue on this repository. Reports are public on purpose: anyone who uses
the tests should be able to see the problem and the fix. Give the version, the firmware (Klipper
or Kalico) and a minimal example.

Supported: the latest release and `main`.
