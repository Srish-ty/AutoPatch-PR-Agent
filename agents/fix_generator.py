
# ADK imports
from google.adk.agents import Agent
from core.config import MODEL_NAME
from tools.repo_tool import clone_repository
from pydantic import BaseModel, Field


class file_fixing_status(BaseModel):
    is_file_updated: bool = Field(description="status of file update")
    massege: str = Field(description="details about file update")


def write_file(file_path: str, content: str) -> str:
    try:
        with open(file_path, "w", encoding="utf-8") as fh:
            fh.write(content)
        return f"Updated {file_path}"
    except Exception as e:
        return f"Error: {e}"
    
fixer = Agent(
    name="Fixer", model=MODEL_NAME, tools=[write_file],
    instruction=("Use the current file content and issues. Update the content according to issues. "
                    "When done, set is_file_updated true/false and add your massege."
                    "Note: if you feel updating file can cause problem then set is_file_updated to false and explain why in massege."),
    output_schema=file_fixing_status
)