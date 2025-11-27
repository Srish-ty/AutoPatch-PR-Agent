import asyncio

from dotenv import load_dotenv
load_dotenv()

from agents.orchestrator import agent_workflow

if __name__ == "__main__":
    asyncio.run(agent_workflow())
