# Runtime-choice attribution correction

Recorded **2026-10-23 23:37:47 UTC / 2026-10-24 01:37:47 Europe/Madrid**.

The frozen plan's `runtime_choice`, its frozen source template (`freeze.py`),
and frozen README incorrectly state or imply that the human explicitly selected
Python 3.13.14, NumPy 2.4.6 and SciPy 1.18.0. The **parent assistant** selected
that existing system runtime as an implementation choice within the human's
general authorization for project work and subagents. The human did not expressly
authorize those particular versions. No software installation was performed.

The current README now makes this distinction and links here. The frozen plan,
source snapshots (including the old README), results and seeds remain byte-for-byte
unchanged. This is a provenance-attribution correction, with **no change to the
statistical design, synthetic parameters, implementation executed, inputs or
results**. No reseeding or execution was done to erase the metadata error.

- Preserved plan SHA256: `2ae9beb9e7fd4fdbeec875feef481466d2e047c9e59682f84d4ff08956d006be`.
- Preserved primary result SHA256: `17af80b5f5fddc7d553003a47223dfff57cada96ea40636e2c31145cd16a9314`.
- A full deterministic reproduction run had already been launched before this
  correction was requested. Its scientific outputs match exactly; timestamps
  and runtime differ. See `reproduction-verification.json`.

Interpret the original attribution language in the preserved records with this
erratum. The runtime and numerical package versions themselves are correctly
recorded and remain pinned for reproduction.
