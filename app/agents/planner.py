from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from dotenv import load_dotenv
import os
import json
from typing import List

load_dotenv()

llm = ChatGroq(
    model = "llama-3.3-70b-versatile",
    groq_api_key = os.getenv("XAI_API_KEY"),
    temperature = 0.7
)

PLANNER_SYSTEM_PROMPT = """
You are a decision planning assistant.
Given a question or decision, your job is to generate exactly 3 concrete,
meaningful alternatives that the user could realistically persue.

Rules:
-Each alternative must be specific and actionable
-Do not use generic label like "option A"
-Return only a json array of 3 strings, nothing else
-No markdown, no explanation, no backticks

Example output:
["Alternative one here","Alternative two here","Alternative three here"]
"""

def run_planner(question:str,context : str | None = None) -> List[str]:
    user_message = f"Decision: {question}"
    if context:
        user_message += f"\nContext: {context}"
    
    message = [
        SystemMessage(content=PLANNER_SYSTEM_PROMPT),
        HumanMessage(content=user_message)
    ]

    response = llm.invoke(message)

    alternatives = json.loads(response.content)
    return alternatives
