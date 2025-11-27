
# ADK imports
from google.adk.agents import Agent
from core.config import MODEL_NAME
from tools.lint_tool import run_linter_and_store


analyzer = Agent(name="Analyzer", model=MODEL_NAME, tools=[run_linter_and_store], instruction="Run linter. It returns a Reference ID. Output ONLY that ID.")