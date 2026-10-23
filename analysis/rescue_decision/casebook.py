"""Load frozen synthetic inputs without deriving expected labels from the evaluator."""

from copy import deepcopy
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def load_casebook():
    raw = (ROOT / "expected-cases.json").read_bytes()
    receipt = json.loads((ROOT / "expected-cases.freeze.json").read_text())
    if hashlib.sha256(raw).hexdigest() != receipt["sha256"]:
        raise ValueError("Frozen expected cases changed; do not regenerate labels to match code")
    book = json.loads(raw)
    if len(book["cases"]) != receipt["case_count"]:
        raise ValueError("Frozen case count disagrees with receipt")
    return book, receipt


def pointer_parent(document, pointer):
    if not pointer.startswith("/"):
        raise ValueError("Expected an absolute JSON pointer")
    keys = [key.replace("~1", "/").replace("~0", "~") for key in pointer[1:].split("/")]
    current = document
    for key in keys[:-1]:
        current = current[int(key)] if isinstance(current, list) else current[key]
    return current, int(keys[-1]) if isinstance(current, list) else keys[-1]


def set_pointer(document, pointer, value):
    parent, key = pointer_parent(document, pointer)
    # Require an existing key/index so a mistyped fixture does not silently add data.
    parent[key]
    parent[key] = deepcopy(value)


def materialize(book, case):
    data = deepcopy(book["baseline"])
    for path, value in case["set"].items():
        set_pointer(data, path, value)
    for path in case.get("remove", []):
        parent, key = pointer_parent(data, path)
        del parent[key]
    for values in case.get("append_contrasts", []):
        contrast = deepcopy(book["baseline"]["contrasts"][0])
        for path, value in values.items():
            set_pointer(contrast, path, value)
        data["contrasts"].append(contrast)
    for path, value in case.get("nonfinite", {}).items():
        if value not in ("NaN", "Infinity", "-Infinity"):
            raise ValueError("Unknown nonfinite fixture")
        set_pointer(data, path, float(value))
    return data
