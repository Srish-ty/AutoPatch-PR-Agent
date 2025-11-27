import os
import json
import shutil
import asyncio
import git
import uuid
import subprocess
import re
from typing import List, Optional
from urllib.parse import quote, urlparse, urlunparse
from datetime import datetime

# ADK imports
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from core.config import APP_NAME, TEMP_REPOS_DIR, ARTIFACT_STORE

from agents.repo_cloner import repo_cloner
from agents.style_analysis import analyzer
from agents.fix_generator import fixer
from agents.pr_creator import publisher



def display_artifact_changes(report_id: str) -> None:
    """Print a concise, human-friendly summary grouped by filename."""
    data = ARTIFACT_STORE.get(report_id)
    if not data:
        print(f"\n\033[1;31mNo artifact found for ID: {report_id}\033[0m\n")
        return
    issues = data.get("issues", [])
    if not issues:
        print("\n\033[1;32mNo issues recorded in artifact.\033[0m\n")
        return

    # Group issues by filename
    files = {}
    for it in issues:
        fname = it.get("filename") or it.get("path") or "<unknown>"
        files.setdefault(fname, []).append(it)

    print(f"\n\033[1;36mPlanned changes (report: {report_id})\033[0m\n")
    for fname, its in files.items():
        print(f"\033[1;35m--- {fname} ---\033[0m")
        for i, issue in enumerate(its, start=1):
            code = issue.get("code") or issue.get("rule") or issue.get("type") or ""
            msg = issue.get("message") or issue.get("description") or ""
            line = issue.get("line") or (issue.get("location") or {}).get("start", {}).get("line")
            col = issue.get("col") or (issue.get("location") or {}).get("start", {}).get("col")
            suggestion = issue.get("fix") or issue.get("suggestion") or issue.get("replacement")

            loc = f" (line:{line}" + (f", col:{col}" if col else "") + ")" if line else ""
            head = f"[{code}]{loc}" if code or loc else f"[{i}]"
            print(f" {head} {msg}")
            if suggestion:
                # pretty print small fixes inline; otherwise show placeholder
                if isinstance(suggestion, dict):
                    s = suggestion.get("content") or suggestion.get("patch") or suggestion.get("replacement") or str(suggestion)
                else:
                    s = str(suggestion)

                print(f"    \033[1;32mSuggestion:\033[0m {s}")
        print("")  # blank line between files
    print("")  # trailing newline





# # async runner helper
async def run_agent(runner: Runner, session_id: str, prompt: str) -> str:
    content = types.Content(role="user", parts=[types.Part(text=prompt)])
    final_text = ""
    async for event in runner.run_async(session_id=session_id, user_id="user_1", new_message=content):
        try:
            if getattr(event, "content", None) and event.content.parts:
                for part in event.content.parts:
                    if part.text:
                        final_text += part.text
        except Exception:
            continue
    return final_text


# Main workflow (cleaner and easier to follow)
async def agent_workflow():
    print("=== Google ADK Scalable Multi-Agent Tool ===")
    # repo_url = input("Repo URL: ").strip()
    # gh_token = input("GitHub Token: ").strip()

    repo_url = input("Repo URL: ")
    gh_token = input("GitHub Token: ")

        # Prompt branch before invoking the clone tool so we can pass it in the prompt when present
    branch = input("Branch to analyze (leave empty to use default/current branch): ").strip()

    session_service = InMemorySessionService()
    session_id = "session_main"
    await session_service.create_session(session_id=session_id, user_id="user_1", app_name=APP_NAME)

    runner_scan = Runner(agent=repo_cloner, app_name=APP_NAME, session_service=session_service)
    runner_analyze = Runner(agent=analyzer, app_name=APP_NAME, session_service=session_service)
    runner_fix = Runner(agent=fixer, app_name=APP_NAME, session_service=session_service)
    runner_pub = Runner(agent=publisher, app_name=APP_NAME, session_service=session_service)

    print("\n[repo_cloner]: Cloning...")
    # Build prompt — include branch only if provided
    clone_prompt = f"Clone {repo_url} (token: {gh_token})"
    if branch:
        clone_prompt += f" branch: {branch}"
    # clone_prompt += " and scan."
    scan_out = await run_agent(runner_scan, session_id, clone_prompt)

    # The repo_cloner tool returns the local path directly in normal flow. Fall back to predictable path.
    repo_name = repo_url.rstrip("/").split("/")[-1].replace(".git", "")
    local_path = scan_out if os.path.exists(scan_out) else os.path.abspath(os.path.join(TEMP_REPOS_DIR, repo_name))

    print("\n[Analyzer]: Analyzing...")
    analysis_resp = await run_agent(runner_analyze, session_id, f"Run linter on {local_path}")
    print(f"Agent Output: {analysis_resp}")

    match = re.search(r"([a-f0-9\-]{36})", analysis_resp)
    if not match:
        print("No Reference ID returned.")
        return

    report_id = match.group(1)
    print(f"Artifact ID: {report_id}")
    display_artifact_changes(report_id)

    if input("Fix issues? (y/n): ").lower() != 'y':
        return

    print("\n[Fixer]: Fixing...")
    artifact = ARTIFACT_STORE.get(report_id)
    if not artifact:
        print(f"report id {report_id} not found. No issues to fix.")
        return

    # Process a small number of issues for demo (preserve original behavior of slicing)
    for issue in artifact.get("issues", []):
        filename = issue.get("filename")
        if not filename or not os.path.exists(filename):
            print(f"Skipping invalid file: {filename}")
            continue
        with open(filename, "r", encoding="utf-8") as fh:
            current_content = fh.read()
        prompt = (
            "Here is the current file content and suggestion by ruff. Fix the code according to suggestions.\n\n"
            f"File Content:\n{current_content}\n\nsuggestion:\n{json.dumps(issue, default=str)}"
        )
        fix_resp = await run_agent(runner_fix, session_id, prompt)
        print("Fixer response:", fix_resp)

    print("\n[Publisher]: Publishing...")
    pub_resp = await run_agent(runner_pub, session_id, f"Create PR for {local_path} repo {repo_url}. use git token {gh_token} if required")
    print("Publish result:", pub_resp)