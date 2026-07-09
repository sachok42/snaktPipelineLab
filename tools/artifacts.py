#!/usr/bin/env python3
"""Initialise and validate the pipeline artifact repository layout."""

import argparse
import json
import sys
from pathlib import Path


ARTIFACT_DIRS = [
    "debug",
    "handoffs",
    "incidents",
    "intake",
    "complete",
    "meta",
    "reviews",
    "salvage",
    "search",
    "surface",
    "temp",
    "testing",
]

MANIFEST = ".pipeline-artifacts.json"


def _is_relative_to(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def _resolved(path: str) -> Path:
    return Path(path).expanduser().resolve()


def _validate_separate_root(artifact_root: Path, feature_repo: Path | None) -> None:
    if feature_repo is None:
        return
    if artifact_root == feature_repo or _is_relative_to(artifact_root, feature_repo):
        raise SystemExit(
            f"Artifact root must not be inside the feature repository: {artifact_root}"
        )


def init_artifacts(root: Path, feature_repo: Path | None) -> None:
    _validate_separate_root(root, feature_repo)
    root.mkdir(parents=True, exist_ok=True)
    for name in ARTIFACT_DIRS:
        (root / name).mkdir(exist_ok=True)

    manifest = {
        "artifact_root": str(root),
        "feature_repo": str(feature_repo) if feature_repo else None,
        "directories": ARTIFACT_DIRS,
    }
    (root / MANIFEST).write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"Artifact repository initialised at {root}")


def validate_artifacts(root: Path, feature_repo: Path | None) -> None:
    _validate_separate_root(root, feature_repo)
    missing = [name for name in ARTIFACT_DIRS if not (root / name).is_dir()]
    if missing:
        raise SystemExit(f"Artifact repository is missing directories: {', '.join(missing)}")
    if not (root / MANIFEST).is_file():
        raise SystemExit(f"Artifact repository is missing {MANIFEST}")
    print(f"Artifact repository valid at {root}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Manage pipeline artifact repository layout.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    for command in ("init", "validate"):
        sub = subparsers.add_parser(command)
        sub.add_argument("--root", required=True, help="Artifact repository root")
        sub.add_argument(
            "--feature-repo",
            help="Feature repository path; used to reject artifact roots inside the feature repo",
        )

    args = parser.parse_args()
    root = _resolved(args.root)
    feature_repo = _resolved(args.feature_repo) if args.feature_repo else None

    if args.command == "init":
        init_artifacts(root, feature_repo)
    else:
        validate_artifacts(root, feature_repo)
    return 0


if __name__ == "__main__":
    sys.exit(main())
