#!/usr/bin/env python3
"""Assembles per-agent .zip bundles for the SnaKt pipeline.

Each zip contains:
  - instructions.md   (agent-specific; solver instructions expanded from templates)
  - agents/<sub>.zip  (subordinate bundles, for agents that spawn others)
  - tools/<tool>.py   (for agents that need specific tools)

Inline comments in .md source files are stripped before bundling.
A comment starts with %% and runs to the end of the line.

Run: python3 assemble.py
Output: dist/<slug>.zip for every agent in the pipeline.
"""

import io
import re
import zipfile
from pathlib import Path

# Inline comment marker for .md source files.
# Everything from this token to the end of the line is stripped before bundling.
COMMENT_MARKER = "%%"

ROOT = Path(__file__).parent
AGENTS_DIR = ROOT / "agents"
DIST_DIR = ROOT / "dist"

# Number of solver instances per method.
# Slot 1 runs on Opus; all subsequent slots run on Sonnet.
SOLVER_SLOTS = 3

# Tools bundled into specific agent zips, keyed by agent slug.
AGENT_TOOLS: dict[str, list[str]] = {
    "orchestrator": ["tools/artifacts.py", "agents/shared/standing-rules.md"],
    "planner":      ["tools/search.py"],
    "repo-setup":   ["tools/artifacts.py"],
}


# ---------------------------------------------------------------------------
# Discovery
# ---------------------------------------------------------------------------

def slug_from_folder(folder: Path) -> str:
    """Strip numeric ordering prefix: '04-strategist' → 'strategist'."""
    return re.sub(r"^\d+-", "", folder.name)


def is_solver_template(slug: str) -> bool:
    """True for template-only folders like 'solver-v' (not instances like 'solver-v-1')."""
    return bool(re.fullmatch(r"solver-[a-z]+", slug))


def discover_agent_folders() -> dict[str, Path]:
    """Return {slug: folder} for all agent folders, in ordering-prefix order."""
    return {
        slug_from_folder(f): f
        for f in sorted(AGENTS_DIR.iterdir())
        if f.is_dir() and f.name != "shared"
    }


def discover_solver_methods(folders: dict[str, Path]) -> list[str]:
    """Return method letters inferred from solver template folders, in discovery order."""
    return [
        m.group(1)
        for slug in folders
        if (m := re.fullmatch(r"solver-([a-z]+)", slug))
    ]


def solver_instance_slugs(methods: list[str]) -> list[str]:
    return [
        f"solver-{method}-{i}"
        for method in methods
        for i in range(1, SOLVER_SLOTS + 1)
    ]


def slot_model(index: int) -> str:
    return "Opus" if index == 1 else "Sonnet"


# ---------------------------------------------------------------------------
# Comment stripping
# ---------------------------------------------------------------------------

def strip_comments(text: str) -> str:
    """Strip inline %% comments (marker + everything after) from each line."""
    lines = []
    for line in text.splitlines():
        idx = line.find(COMMENT_MARKER)
        if idx != -1:
            line = line[:idx].rstrip()
        lines.append(line)
    return "\n".join(lines)


def read_md(path: Path) -> str:
    return strip_comments(path.read_text())


# ---------------------------------------------------------------------------
# Zip construction
# ---------------------------------------------------------------------------

def expand_solver_template(slug: str, folders: dict[str, Path]) -> str:
    m = re.fullmatch(r"solver-([a-z]+)-(\d+)", slug)
    method, index = m.group(1), int(m.group(2))
    template = (folders[f"solver-{method}"] / "instructions_template.md").read_text()
    return strip_comments(
        template
        .replace("{index}", str(index))
        .replace("{model}", slot_model(index))
        .replace("{slug}", slug)
    )


def build_zip(
    slug: str,
    folders: dict[str, Path],
    built: dict[str, bytes],
    subordinates: dict[str, list[str]],
) -> bytes:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:

        # instructions.md — expand template for solver instances, read directly for others
        if re.fullmatch(r"solver-[a-z]+-\d+", slug):
            zf.writestr("instructions.md", expand_solver_template(slug, folders))
        else:
            zf.writestr("instructions.md", read_md(folders[slug] / "instructions.md"))

        # tools and shared .md files — strip comments from .md, copy others as-is
        for tool_rel in AGENT_TOOLS.get(slug, []):
            path = ROOT / tool_rel
            if path.suffix == ".md":
                zf.writestr(tool_rel, read_md(path))
            else:
                zf.write(path, tool_rel)

        # agents/<sub>.zip
        for sub in subordinates.get(slug, []):
            zf.writestr(f"agents/{sub}.zip", built[sub])

    return buf.getvalue()


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def assemble() -> None:
    DIST_DIR.mkdir(exist_ok=True)

    folders = discover_agent_folders()
    methods = discover_solver_methods(folders)
    instances = solver_instance_slugs(methods)

    # All buildable step agents (solver template folders are sources, not outputs).
    agent_slugs = [s for s in folders if not is_solver_template(s)]

    # Subordinate relationships derived from discovered slugs — no hardcoding.
    subordinates: dict[str, list[str]] = {
        "orchestrator": [s for s in agent_slugs if s != "orchestrator"],
        "strategist":   instances,
    }

    # Build leaves before parents; solver instances before strategist; all before orchestrator.
    leaf_slugs = [s for s in agent_slugs if s not in ("orchestrator", "strategist")]
    build_order = leaf_slugs + instances + ["strategist", "orchestrator"]

    built: dict[str, bytes] = {}
    for slug in build_order:
        zip_bytes = build_zip(slug, folders, built, subordinates)
        built[slug] = zip_bytes
        (DIST_DIR / f"{slug}.zip").write_bytes(zip_bytes)
        print(f"  built  dist/{slug}.zip")

    print(f"\nAssembled {len(build_order)} bundle(s) → dist/")


if __name__ == "__main__":
    assemble()
