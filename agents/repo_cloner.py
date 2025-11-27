
# ADK imports
from google.adk.agents import Agent
from core.config import MODEL_NAME
from tools.repo_tool import clone_repository


repo_cloner = Agent(name="RepoCloner", model=MODEL_NAME, tools=[clone_repository], instruction="Clone the repo. return the local path.")