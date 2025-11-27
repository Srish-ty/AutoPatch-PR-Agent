import os
import json
import uuid
import subprocess

from core.config import ARTIFACT_STORE


def run_linter_and_store(local_path: str) -> str:
    """
    Run 'ruff check' on the given path. Store issues in ARTIFACT_STORE and return a reference id.
    Returns human-readable error strings on failure.
    """
    try:
        proc = subprocess.run(
            ["ruff", "check", local_path, "--output-format=json"],
            capture_output=True, text=True, check=False
        )
    except FileNotFoundError:
        return "Error: Ruff linter not installed."
    except Exception as e:
        return f"Error running linter: {e}"

    raw = proc.stdout.strip() or "[]"
    try:
        issues = json.loads(raw)
    except json.JSONDecodeError:
        return "Error: Linter output not valid JSON."

    if not issues:
        return "No issues found."

    report_id = str(uuid.uuid4())
    ARTIFACT_STORE[report_id] = {"issues": issues, "count": len(issues), "repo_path": local_path}
    return f"Issues stored. Reference ID: {report_id}"