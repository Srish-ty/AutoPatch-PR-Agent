import re
from google.genai.agents import Runner
from core.agent_runtime import build_session_service, run_agent, ensure_dir
from core.config import TEMP_REPOS_DIR
from core.git_utils import clone_repo
from agents.analysis_agent import analyze_repo_for_issues
from agents.fix_agent import fix_issues_with_llm
from agents.publish_agent import create_pull_request, create_branch_and_push

async def run_pipeline(repo_url: str, gh_token: str, base_branch: str):
    ensure_dir(TEMP_REPOS_DIR)
    local_path = clone_repo(repo_url, TEMP_REPOS_DIR, base_branch or None)

    session_service = build_session_service()
    session_id = "session_main"

    # you would build separate runners in real code; here assume one Runner for simplicity
    runner_analyze = Runner(model="models/gemini-2.0-flash", app= "auto-patch-pr-agent", session_service=session_service)
    runner_fix = Runner(model="models/gemini-2.0-flash", app= "auto-patch-pr-agent", session_service=session_service)

    # Analyze
    print("\n[Analyzer]: Analyzing...")
    analysis_output = analyze_repo_for_issues(local_path)
    print("Analysis:", analysis_output)

    match = re.search(r"([a-f0-9\-]{36})", analysis_output)
    if not match:
        print("No Reference ID returned.")
        return
    report_id = match.group(1)
    print(f"Artifact ID: {report_id}")

    # Fix
    print("\n[Fixer]: Fixing...")
    await fix_issues_with_llm(runner_fix, session_id, report_id)

    # Publish
    print("\n[Publisher]: Publishing...")
    new_branch = "auto-style-fixes"
    created_branch = create_branch_and_push(local_path, new_branch, gh_token)
    pr_url = create_pull_request(
        repo_url=repo_url,
        new_branch=created_branch,
        base_branch=base_branch or "main",
        gh_token=gh_token,
        title="chore: auto style fixes",
        body="This PR was created by Auto Patch PR Agent.",
    )
    print("PR created:", pr_url)
