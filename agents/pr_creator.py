
# ADK imports
from google.adk.agents import Agent
from core.config import MODEL_NAME
from tools.repo_tool import create_github_pr


publisher = Agent(name="Publisher", model=MODEL_NAME, tools=[create_github_pr], instruction="Create a GitHub PR.")