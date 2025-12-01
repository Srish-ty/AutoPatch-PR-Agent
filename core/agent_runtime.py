import os
import json
from google.genai import types
from google.genai.agents import Runner, InMemorySessionService  # adjust import to real API

from .config import MODEL_NAME, APP_NAME

def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)

async def run_agent(runner: Runner, session_id: str, prompt: str) -> str:
    content = types.Content(role="user", parts=[types.Part(text=prompt)])
    final_text = ""
    async for event in runner.stream_input_content(session_id=session_id, content=content):
        if event.type == "response.delta":
            for part in event.delta.parts:
                if part.text:
                    final_text += part.text
    return final_text

def build_session_service() -> InMemorySessionService:
    return InMemorySessionService()
