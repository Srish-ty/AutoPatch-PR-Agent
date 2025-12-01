import json
import subprocess
from typing import List

from core.artifacts import store_issues

def run_ruff_on_path(path: str) -> List[dict]:
    # Example: ruff in JSON mode
    try:
        result = subprocess.run(
            ["ruff", "check", path, "--format", "json"],
            capture_output=True,
            text=True,
            check=True,
        )
        issues = json.loads(result.stdout or "[]")
        return issues
    except Exception:
        return []

def analyze_repo_for_issues(local_path: str) -> str:
    issues = run_ruff_on_path(local_path)
    if not issues:
        return "No issues found."
    report_id = store_issues(issues, local_path)
    return f"Issues stored. Reference ID: {report_id}"
