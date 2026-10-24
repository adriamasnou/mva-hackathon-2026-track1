# Optional verification workflow

[verify.yml](verify.yml) preserves the reviewed CI workflow as an inactive example.
To enable it manually, copy it to `.github/workflows/verify.yml` and commit it
using credentials with permission to create or update workflows (the `workflow`
scope for an OAuth token). It is optional for this publication package.

The offline verification commands remain valid from the repository root:

```sh
python3 tools/check_package.py
python3 -m unittest discover -s tests -v
python3 canary/run_canary.py --self-test
python3 analysis/exposure_check.py
```

The example also includes citation verification, which requires access to the
public NCBI service and is separate from these offline checks.
