#!/usr/bin/env python3
"""Assembles laws and pipeline parts into a single .md file for the orchestrator."""

import os
import sys
from pathlib import Path

ROOT = Path(__file__).parent
LAWS_DIR = ROOT / "laws"
PIPELINE_DIR = ROOT / "pipeline"
OUTPUT_FILE = ROOT / "orchestrator.md"


def read_md_files(directory: Path) -> list[tuple[str, str]]:
    files = sorted(directory.glob("*.md"))
    return [(f.stem, f.read_text().strip()) for f in files]


def assemble():
    sections = []

    laws = read_md_files(LAWS_DIR)
    if not laws:
        print("Warning: no files found in laws/", file=sys.stderr)
    for _, content in laws:
        sections.append(content)

    parts = read_md_files(PIPELINE_DIR)
    if not parts:
        print("Warning: no files found in pipeline/", file=sys.stderr)
    for _, content in parts:
        sections.append(content)

    output = "\n\n---\n\n".join(sections)
    OUTPUT_FILE.write_text(output + "\n")
    print(f"Assembled {len(laws)} law file(s) and {len(parts)} pipeline part(s) → {OUTPUT_FILE}")


if __name__ == "__main__":
    assemble()
