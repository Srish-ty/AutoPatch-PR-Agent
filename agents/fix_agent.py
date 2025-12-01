import json
import os

from google.genai.agents import Runner
from core.agent_runtime import run_agent
from core.artifacts import get_artifact
from core.git_utils import write_file

async def fix_issues_with_llm(runner_fix: Runner, session_id: str, report_id: str):
    artifact = get_artifact(report_id)
    if not artifact:
        print(f"Report id {report_id} not found.")
        return

    for issue in artifact.get("issues", []):
        filename = issue.get("filename") or issue.get("file")
        if not filename:
            continue

        if not os.path.exists(filename):
            continue

        with open(filename, "r", encoding="utf-8") as fh:
            current_content = fh.read()

        prompt = (
            "Here is the current file content and suggestion by ruff. "
            "Fix the code according to suggestions.\n\n"
            f"File Content:\n{current_content}\n\n"
            f"suggestion:\n{json.dumps(issue, default=str)}"
        )
        fix_resp = await run_agent(runner_fix, session_id, prompt)
        if fix_resp.strip():
            write_file(filename, fix_resp)
            print(f"Updated {filename}")
