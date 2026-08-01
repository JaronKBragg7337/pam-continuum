from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
CONFIG = ROOT / "config"

REQUIRED_JSON = [
    DATA / "state.json",
    DATA / "missions.json",
    DATA / "signals.json",
    DATA / "connections.json",
    DATA / "sources.json",
    DATA / "activity.json",
    DATA / "heartbeat.json",
    CONFIG / "system.json",
    CONFIG / "domains.json",
    CONFIG / "sources.json",
]

SECRET_PATTERNS = [
    re.compile(r"ghp_[A-Za-z0-9_]+"),
    re.compile(r"github_pat_[A-Za-z0-9_]+"),
    re.compile(r"sk-[A-Za-z0-9_-]{12,}"),
    re.compile(r"AIza[0-9A-Za-z_-]{20,}"),
]


def load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"missing JSON file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON in {path}: {exc}") from exc


def walk_strings(value, location=""):
    if isinstance(value, str):
        yield location, value
    elif isinstance(value, dict):
        for key, item in value.items():
            yield from walk_strings(item, f"{location}.{key}")
    elif isinstance(value, list):
        for index, item in enumerate(value):
            yield from walk_strings(item, f"{location}[{index}]")


def main() -> int:
    errors: list[str] = []
    documents = {}
    for path in REQUIRED_JSON:
        try:
            documents[path] = load_json(path)
        except ValueError as exc:
            errors.append(str(exc))

    for path, document in documents.items():
        for location, value in walk_strings(document):
            if any(pattern.search(value) for pattern in SECRET_PATTERNS):
                errors.append(f"credential-like value found in {path}:{location}")

    state = documents.get(DATA / "state.json")
    if isinstance(state, dict):
        for key in ("schema_version", "system", "mode", "runtime", "metrics", "protection"):
            if key not in state:
                errors.append(f"state.json missing required key: {key}")

    for name in ("missions.json", "signals.json"):
        items = documents.get(DATA / name)
        if not isinstance(items, list):
            errors.append(f"{name} must contain an array")
            continue
        required = ("id", "title", "status")
        for index, item in enumerate(items):
            if not isinstance(item, dict):
                errors.append(f"{name}[{index}] must be an object")
                continue
            for key in required:
                if not item.get(key):
                    errors.append(f"{name}[{index}] missing {key}")
            if name == "signals.json":
                for key in ("claim", "confidence", "basis", "falsifier", "horizon"):
                    if key not in item or item[key] in (None, "", []):
                        errors.append(f"{name}[{index}] missing {key}")

    if errors:
        print("PAM Continuum validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"PAM Continuum validation passed ({len(REQUIRED_JSON)} JSON documents checked; secrets scan clean).")
    return 0


if __name__ == "__main__":
    sys.exit(main())

