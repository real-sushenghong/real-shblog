#!/usr/bin/env python3
"""Fetch 48h GitHub activity for each project repo and reorder data/projects.yaml.

Sorts: commits DESC (most active first), then original yaml order for repos
with zero activity (stable fallback). Writes back in-place preserving all
existing fields — only the top-level item order changes.

Usage:
    GITHUB_TOKEN=xxx python3 scripts/sync_projects.py

Designed to run in GitHub Actions (GITHUB_TOKEN is auto-injected).
"""
from __future__ import annotations

import os
import sys
import datetime
import urllib.request
import urllib.error
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.stderr.write("pyyaml required: pip install pyyaml\n")
    sys.exit(1)


REPO_OWNER = "shenghongio"
SINCE_HOURS = int(os.environ.get("PROJECTS_ACTIVITY_HOURS", "48"))
YAML_PATH = Path(os.environ.get("PROJECTS_YAML", "data/projects.yaml"))


def _total_commits_from_link(headers) -> int | None:
    """Parse GitHub Link header to extract total page count when per_page=1."""
    link = headers.get("Link", "")
    for part in link.split(","):
        if 'rel="last"' in part:
            import re
            m = re.search(r'[?&]page=(\d+)', part)
            if m:
                return int(m.group(1))
    return None


def fetch_commit_count(repo: str, since: datetime.datetime, token: str | None) -> int:
    since_iso = since.strftime("%Y-%m-%dT%H:%M:%SZ")
    url = (
        f"https://api.github.com/repos/{REPO_OWNER}/{repo}/commits"
        f"?since={since_iso}&per_page=1"
    )
    req = urllib.request.Request(url)
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("User-Agent", "blogio-sync-projects")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            count = _total_commits_from_link(resp.headers)
            if count is None:
                body = resp.read().decode()
                import json
                count = len(json.loads(body))
            return count
    except urllib.error.HTTPError as e:
        sys.stderr.write(f"  [WARN] {repo}: HTTP {e.code}, treating as 0\n")
        return 0
    except Exception as e:
        sys.stderr.write(f"  [WARN] {repo}: {e}, treating as 0\n")
        return 0


def main() -> int:
    if not YAML_PATH.exists():
        sys.stderr.write(f"{YAML_PATH} not found\n")
        return 1

    with open(YAML_PATH, encoding="utf-8") as f:
        projects = yaml.safe_load(f) or []

    if not isinstance(projects, list):
        sys.stderr.write("projects.yaml must be a top-level list\n")
        return 1

    token = os.environ.get("GITHUB_TOKEN")
    since = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=SINCE_HOURS)
    sys.stderr.write(f"Syncing activity for last {SINCE_HOURS}h (since {since.isoformat()}Z)\n")

    original_positions = {item["title"]: i for i, item in enumerate(projects)}
    counts: dict[str, int] = {}
    for item in projects:
        title = item["title"]
        counts[title] = fetch_commit_count(title, since, token)
        sys.stderr.write(f"  {title}: {counts[title]} commits\n")

    def sort_key(item):
        t = item["title"]
        return (-counts.get(t, 0), original_positions.get(t, 999))

    projects.sort(key=sort_key)

    with open(YAML_PATH, "w", encoding="utf-8") as f:
        yaml.dump(projects, f, allow_unicode=True, sort_keys=False, default_flow_style=False)

    sys.stderr.write("Updated data/projects.yaml order:\n")
    for i, item in enumerate(projects, 1):
        sys.stderr.write(f"  {i}. {item['title']} ({counts.get(item['title'], 0)})\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())