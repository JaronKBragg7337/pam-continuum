from __future__ import annotations

import json
import os
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parent
PRIVATE = ROOT / "private"

EXCLUDED_NAMES = {".git", "node_modules", "__pycache__", "site", "private", "codex-pam-sandbox", "pam-continuum"}
MAX_DEPTH = 3

CLUSTERS = {
    "ai-infrastructure": {"ai", "orchestra", "observer", "omnilocal", "codex"},
    "creative-3d": {"threejs", "blender", "unreal", "unity", "game", "asset", "facing", "necklace", "space"},
    "simulation-worlds": {"heartbeat", "sim", "circuit", "biosphere", "organism", "world"},
    "strategy-and-intelligence": {"market", "war", "defender", "architect", "current"},
    "web-and-product": {"site", "hub", "studio", "exports", "independence", "ink"},
}


def iso_timestamp(path: Path) -> str | None:
    try:
        return datetime.fromtimestamp(path.stat().st_mtime, timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    except OSError:
        return None


def inventory_project(path: Path) -> dict:
    file_count = 0
    directory_count = 0
    extensions = Counter()
    deepest_observed = 0

    for current, directories, files in os.walk(path):
        current_path = Path(current)
        try:
            depth = len(current_path.relative_to(path).parts)
        except ValueError:
            depth = MAX_DEPTH
        deepest_observed = max(deepest_observed, depth)
        if depth >= MAX_DEPTH:
            directories[:] = []
        directories[:] = [name for name in directories if name not in EXCLUDED_NAMES]
        directory_count += len(directories)
        file_count += len(files)
        for name in files:
            suffix = Path(name).suffix.lower() or "[no-extension]"
            extensions[suffix] += 1

    normalized = path.name.lower()
    matches = [cluster for cluster, keywords in CLUSTERS.items() if any(keyword in normalized for keyword in keywords)]
    return {
        "name": path.name,
        "path_scope": "workspace-child",
        "last_modified": iso_timestamp(path),
        "file_count_observed": file_count,
        "directory_count_observed": directory_count,
        "scan_depth": deepest_observed,
        "top_extensions": dict(extensions.most_common(8)),
        "name_derived_clusters": matches,
        "interpretation_confidence": "low",
        "interpretation_basis": "directory name and metadata only; no project content opened",
    }


def build_assessment(inventory: dict) -> str:
    lines = [
        "# Protected Workspace Reconnaissance",
        "",
        f"Generated: `{inventory['generated_at']}`",
        "",
        "This is a local-only assessment. It records directory metadata and bounded file-extension counts. It does not publish project names and does not modify any existing project.",
        "",
        f"Observed workspace children: **{inventory['project_count']}** directories and **{inventory['top_level_file_count']}** top-level files.",
        "",
        "## Candidate clusters",
        "",
        "These are hypotheses derived from names and require confirmation before any project is treated as related:",
        "",
    ]
    if not inventory["candidate_clusters"]:
        lines.append("No candidate clusters detected.")
    else:
        for cluster in inventory["candidate_clusters"]:
            lines.append(f"- **{cluster['cluster']}** — {', '.join(cluster['projects'])} _(low confidence; name-derived)_")
    lines.extend([
        "",
        "## Safe next moves",
        "",
        "1. Confirm which project clusters are active before opening project contents.",
        "2. Compare public architecture documents before importing any code or data.",
        "3. Keep private workspace findings outside the public repository unless explicitly approved.",
        "4. Turn confirmed relationships into missions with evidence and verification criteria.",
        "",
    ])
    return "\n".join(lines)


def main() -> None:
    generated_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    projects = []
    top_level_file_count = 0

    for child in sorted(WORKSPACE.iterdir(), key=lambda item: item.name.lower()):
        if child.name in EXCLUDED_NAMES or child.name.startswith("."):
            continue
        if child.is_dir():
            projects.append(inventory_project(child))
        elif child.is_file():
            top_level_file_count += 1

    cluster_projects: dict[str, list[str]] = {cluster: [] for cluster in CLUSTERS}
    for project in projects:
        for cluster in project["name_derived_clusters"]:
            cluster_projects[cluster].append(project["name"])

    inventory = {
        "schema_version": 1,
        "generated_at": generated_at,
        "scope": str(WORKSPACE),
        "protected": True,
        "content_read": False,
        "project_count": len(projects),
        "top_level_file_count": top_level_file_count,
        "projects": projects,
        "candidate_clusters": [
            {"cluster": cluster, "projects": names, "confidence": "low", "basis": "directory names only"}
            for cluster, names in cluster_projects.items()
            if names
        ],
    }

    PRIVATE.mkdir(exist_ok=True)
    (PRIVATE / "workspace-inventory.json").write_text(json.dumps(inventory, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (PRIVATE / "initial-assessment.md").write_text(build_assessment(inventory), encoding="utf-8")
    print(json.dumps({"project_count": len(projects), "top_level_file_count": top_level_file_count, "output": str(PRIVATE)}, indent=2))


if __name__ == "__main__":
    main()

