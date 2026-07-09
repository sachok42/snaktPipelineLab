#!/usr/bin/env python3
"""Assembles per-agent .zip bundles for the SnaKt pipeline.

Each zip contains:
  - instructions.md   (agent-specific; solver instructions are expanded from templates)
  - agents/<sub>.zip  (subordinate agent bundles, for agents that spawn others)
  - tools/<tool>.py   (for agents that need specific tools)

Run: python3 assemble.py
Output: dist/<agent-slug>.zip for every agent in the pipeline.
"""

import io
import zipfile
from pathlib import Path

ROOT = Path(__file__).parent
AGENTS_DIR = ROOT / "agents"
DIST_DIR = ROOT / "dist"

# ---------------------------------------------------------------------------
# Solver roster: (slug, name, method, index, model)
# ---------------------------------------------------------------------------
SOLVERS = [
    ("solver-v-1", "Aleksei", "v", 1, "Opus"),
    ("solver-v-2", "Selin",   "v", 2, "Sonnet"),
    ("solver-v-3", "Nikos",   "v", 3, "Sonnet"),
    ("solver-a-1", "Finn",    "a", 1, "Opus"),
    ("solver-a-2", "Priya",   "a", 2, "Sonnet"),
    ("solver-a-3", "Lior",    "a", 3, "Sonnet"),
    ("solver-b-1", "Ingrid",  "b", 1, "Opus"),
    ("solver-b-2", "Jae",     "b", 2, "Sonnet"),
    ("solver-b-3", "Mei",     "b", 3, "Sonnet"),
    ("solver-n-1", "Tariq",   "n", 1, "Opus"),
    ("solver-n-2", "Zara",    "n", 2, "Sonnet"),
    ("solver-n-3", "Mateus",  "n", 3, "Sonnet"),
    ("solver-m-1", "Sofía",   "m", 1, "Opus"),
    ("solver-m-2", "Kwame",   "m", 2, "Sonnet"),
    ("solver-m-3", "Linh",    "m", 3, "Sonnet"),
]

# ---------------------------------------------------------------------------
# Direct subordinates (whose zips are bundled inside the parent's zip)
# ---------------------------------------------------------------------------
AGENT_SUBORDINATES = {
    "soren": [
        "mira", "tomas", "yuki", "amara",
        "dawa", "ren", "valentina", "marcus", "ebele",
    ],
    "amara": [slug for slug, *_ in SOLVERS],
}

# ---------------------------------------------------------------------------
# Tools bundled into specific agent zips
# ---------------------------------------------------------------------------
AGENT_TOOLS = {
    "soren": ["tools/artifacts.py"],
    "mira":  ["tools/search.py"],
    "tomas": ["tools/artifacts.py"],
}


def _expand_solver_template(method: str, name: str, index: int, model: str, slug: str) -> str:
    template_path = AGENTS_DIR / f"solver-{method}" / "instructions_template.md"
    text = template_path.read_text()
    return (
        text
        .replace("{name}", name)
        .replace("{method}", method.upper())
        .replace("{index}", str(index))
        .replace("{model}", model)
        .replace("{slug}", slug)
    )


def build_zip(slug: str, built_zips: dict) -> bytes:
    """Build the zip for one agent, assuming all subordinate zips are already built."""
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:

        # instructions.md — expand solver templates, read others directly
        if slug.startswith("solver-"):
            entry = next(e for e in SOLVERS if e[0] == slug)
            s_slug, name, method, index, model = entry
            instructions = _expand_solver_template(method, name, index, model, slug)
            zf.writestr("instructions.md", instructions)
        else:
            instructions_path = AGENTS_DIR / slug / "instructions.md"
            zf.write(instructions_path, "instructions.md")

        # tools/
        for tool_rel in AGENT_TOOLS.get(slug, []):
            tool_path = ROOT / tool_rel
            zf.write(tool_path, tool_rel)

        # agents/<sub>.zip — subordinate bundles
        for sub_slug in AGENT_SUBORDINATES.get(slug, []):
            zf.writestr(f"agents/{sub_slug}.zip", built_zips[sub_slug])

    return buf.getvalue()


def assemble():
    DIST_DIR.mkdir(exist_ok=True)

    built_zips = {}

    # Build order: leaves first, then amara (needs solver zips), then soren (needs all).
    all_slugs = (
        ["mira", "tomas", "yuki", "dawa", "ren", "valentina", "marcus", "ebele"]
        + [slug for slug, *_ in SOLVERS]
        + ["amara"]
        + ["soren"]
    )

    for slug in all_slugs:
        zip_bytes = build_zip(slug, built_zips)
        built_zips[slug] = zip_bytes
        out_path = DIST_DIR / f"{slug}.zip"
        out_path.write_bytes(zip_bytes)
        print(f"  built  {out_path.relative_to(ROOT)}")

    print(f"\nAssembled {len(all_slugs)} agent bundle(s) → {DIST_DIR.relative_to(ROOT)}/")


if __name__ == "__main__":
    assemble()
