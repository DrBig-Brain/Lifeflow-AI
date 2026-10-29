import os
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from dotenv import load_dotenv
from app.models import ScenarioSummary
import json

load_dotenv()

llm = ChatGroq(
    model = "llama-3.3-70b-versatile",
    api_key = os.getenv("XAI_API_KEY"),
    temperature = 0.7
)

SIMULATOR_SYSTEM_PROMPT = """
You are a future simulation assisstant.
Given a decision alternative, simulate a realistic future outcome for it.

Rules:
-Be specific and realistic, not generic
-risk_level must be exactly one of: low, medium, high
-Return ONLY a JSON object, nothing else
-No markdown, no explanation, no backticks
Example_output : 
{
    "option":"the alternative text here",
    "outcome":"a realistic description of how this plays out in future",
    "risk_level":"medium"
}
"""

def run_simulator(alternatives: list[str], context: str | None = None) -> list[ScenarioSummary]:
    scenarios = []
    for alternative in alternatives:
        user_message = f"Alternative: {alternative}"
        if context:
            user_message += f"\nContext: {context}"

        message = [
            SystemMessage(content=SIMULATOR_SYSTEM_PROMPT),
            HumanMessage(content=user_message)
        ]

        response = llm.invoke(message)

        data = json.loads(response.content)

        scenarios.append(ScenarioSummary(
            option=data["option"],
            outcome=data["outcome"],
            risk_level=data["risk_level"],
        ))

    return scenarios
