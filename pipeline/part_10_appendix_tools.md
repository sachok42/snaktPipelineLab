# Appendix — Tool Scripts

This orchestrator prompt is designed to be self-contained. The two Python tools referenced
throughout the pipeline are embedded below. If the execution environment does not already
have them on disk at `tools/artifacts.py` and `tools/search.py`, the first agent that needs
either script must write it to disk before invoking it.

---

## tools/artifacts.py

Creates and validates the artifact repository directory layout.

```python
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
```

---

## tools/search.py

Queries GitHub Issues (JetBrains/Kotlin), Stack Overflow ([kotlin]), and JetBrains YouTrack
in parallel and writes a ranked Markdown candidate list.

Optional environment variables: `GITHUB_TOKEN`, `STACKEXCHANGE_KEY`.

```python
#!/usr/bin/env python3
"""
Oracle problem search — queries GitHub Issues, Stack Overflow, and JetBrains YouTrack
for community-reported problems related to a given Kotlin feature.

Usage:
    python tools/search.py "sealed interfaces exhaustive when" [--limit 10] [--out results.md]

Environment variables (optional, improve rate limits):
    GITHUB_TOKEN      — GitHub personal access token
    STACKEXCHANGE_KEY — Stack Exchange API key
"""

import argparse
import gzip
import json
import os
import ssl
import sys
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path


def _ssl_context(insecure: bool) -> ssl.SSLContext | None:
    if insecure:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        return ctx
    try:
        import certifi
        return ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        return None


GITHUB_API        = "https://api.github.com/search/issues"
STACKOVERFLOW_API = "https://api.stackexchange.com/2.3/search/advanced"
YOUTRACK_API      = "https://youtrack.jetbrains.com/api/issues"


def search_github(keywords: str, limit: int) -> list[dict]:
    query = f"{keywords} repo:JetBrains/kotlin is:issue"
    params = urllib.parse.urlencode({"q": query, "sort": "reactions", "order": "desc", "per_page": limit})
    url = f"{GITHUB_API}?{params}"
    headers = {"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    data = _get_json(url, headers)
    results = []
    for item in data.get("items", []):
        results.append({
            "title":   item["title"],
            "url":     item["html_url"],
            "score":   item.get("reactions", {}).get("total_count", 0),
            "meta":    f"{item.get('comments', 0)} comments",
            "date":    item["created_at"][:7],
            "excerpt": _truncate(item.get("body") or ""),
        })
    return results


def search_stackoverflow(keywords: str, limit: int) -> list[dict]:
    params = {"order": "desc", "sort": "votes", "tagged": "kotlin",
              "q": keywords, "site": "stackoverflow", "pagesize": limit}
    key = os.environ.get("STACKEXCHANGE_KEY")
    if key:
        params["key"] = key
    url = f"{STACKOVERFLOW_API}?{urllib.parse.urlencode(params)}"

    raw = _get_raw(url, {"Accept-Encoding": "gzip"})
    try:
        raw = gzip.decompress(raw)
    except Exception:
        pass
    data = json.loads(raw)

    results = []
    for item in data.get("items", []):
        results.append({
            "title":   item["title"],
            "url":     item["link"],
            "score":   item.get("score", 0),
            "meta":    f"{item.get('answer_count', 0)} answers",
            "date":    _ts(item["creation_date"]),
            "excerpt": "",
        })
    return results


def search_youtrack(keywords: str, limit: int) -> list[dict]:
    query = f"project: KT {keywords} sort by: votes desc"
    params = urllib.parse.urlencode({
        "query":  query,
        "fields": "id,summary,votes,created,description",
        "$top":   limit,
    })
    url = f"{YOUTRACK_API}?{params}"

    data = _get_json(url, {"Accept": "application/json"})
    results = []
    for item in data:
        issue_id = item.get("id", "?")
        results.append({
            "title":   f"{issue_id} — {item.get('summary', '')}",
            "url":     f"https://youtrack.jetbrains.com/issue/{issue_id}",
            "score":   item.get("votes", 0),
            "meta":    f"{item.get('votes', 0)} votes",
            "date":    _ts(item["created"] / 1000) if item.get("created") else "unknown",
            "excerpt": _truncate(item.get("description") or ""),
        })
    return results


_CTX: ssl.SSLContext | None = None


def _get_raw(url: str, headers: dict) -> bytes:
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=12, context=_CTX) as resp:
        return resp.read()


def _get_json(url: str, headers: dict):
    return json.loads(_get_raw(url, headers))


def _ts(epoch) -> str:
    return datetime.fromtimestamp(float(epoch), tz=timezone.utc).strftime("%Y-%m")


def _truncate(text: str, length: int = 220) -> str:
    text = text.replace("\n", " ").strip()
    return text[:length] + "…" if len(text) > length else text


def render_section(title: str, items: list[dict], error: str | None) -> str:
    lines = [f"## {title}\n"]
    if error:
        lines.append(f"_Search failed: {error}_\n")
        return "\n".join(lines)
    if not items:
        lines.append("_No results._\n")
        return "\n".join(lines)
    for i, r in enumerate(items, 1):
        lines.append(f"{i}. **[{r['title']}]({r['url']})** — score {r['score']} · {r['meta']} · {r['date']}")
        if r["excerpt"]:
            lines.append(f"   > {r['excerpt']}")
        lines.append("")
    return "\n".join(lines)


def render_report(keywords: str, sections: list[tuple]) -> str:
    today = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d")
    header = f"# Problem Search: `{keywords}`\n_Generated {today}_\n\n---\n\n"
    body = "\n---\n\n".join(render_section(title, items, err) for title, items, err in sections)
    totals = "  ".join(
        f"{title.split('—')[0].strip()}: {len(items) if not err else 'error'}"
        for title, items, err in sections
    )
    footer = f"\n---\n\n_Sources — {totals}_\n"
    return header + body + footer


def main():
    parser = argparse.ArgumentParser(description="Oracle problem search for pipeline Step 0.")
    parser.add_argument("keywords",   help="Feature keywords to search for")
    parser.add_argument("--limit",    type=int, default=10, help="Max results per source (default 10)")
    parser.add_argument("--out",      help="Write output to this file instead of stdout")
    parser.add_argument("--insecure", action="store_true", help="Disable SSL certificate verification")
    args = parser.parse_args()

    global _CTX
    _CTX = _ssl_context(args.insecure)

    sources = [
        ("GitHub Issues — JetBrains/Kotlin", search_github),
        ("Stack Overflow — [kotlin]",        search_stackoverflow),
        ("YouTrack — KT project",            search_youtrack),
    ]

    sections = []
    with ThreadPoolExecutor(max_workers=3) as pool:
        futures = {pool.submit(fn, args.keywords, args.limit): title for title, fn in sources}
        results_map = {}
        for future in as_completed(futures):
            title = futures[future]
            try:
                results_map[title] = (future.result(), None)
            except Exception as exc:
                results_map[title] = ([], str(exc))

    for title, _ in sources:
        items, err = results_map[title]
        sections.append((title, items, err))

    report = render_report(args.keywords, sections)

    if args.out:
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        with open(args.out, "w") as f:
            f.write(report)
        print(f"Written to {args.out}", file=sys.stderr)
    else:
        print(report)


if __name__ == "__main__":
    main()
```
