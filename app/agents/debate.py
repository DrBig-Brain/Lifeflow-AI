from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from dotenv import load_dotenv
from app.models import ScenarioSummary
import os

load_dotenv()

llm = ChatGroq(
    model = "llama-3.3-70b-versatile",
    api_key = os.getenv("XAI_API_KEY"),
    temperature = 0.7
)

OPTIMIST_PORMPT = """
You are an optimistic debate agent.
Given a list of decision Scenarios, argue for the best possible outcomes.
Focus on opportunities, upsides, and what could go really well
Be enthusiastic but not unrealistic.
Return ONLY a single string with your argument, no labels, no markdown.
keep it under 3 sentences.
"""

PESSIMIST_PROMPT = """
You are a pessimistic debate agent.
Given a list of decision scenarios, highlight the risks, downside, and what could go wrong.
Be critical but not catastrophic.
Return ONLY a single string with your argument, no labels, no markdown.
keep it under 3 sentences.
"""

REALIST_PROMPT = """
You are a pessimistic debate agent.
Given a list of decision scenarios, give a balanced, grounded take.
Ackowledge both upside and downside without leaning either way.
Return ONLY a single string with your argument, no labels, no markdown.
keep it under 3 sentences.
"""

def _run_agent(system_prompt:str, scenarios: list[ScenarioSummary], context: str | None = None) -> str:
    scenario_text = "\n".join([
        f"- Option {s.option}\n Outcome: {s.outcome}\n Risk: {s.risk_level}"
        for s in scenarios
    ])

    user_message = f"Scenarios:\n{scenario_text}"
    if context:
        user_message += context
    
    message = [
        SystemMessage(content = system_prompt),
        HumanMessage(content = user_message)
    ]

    response = llm.invoke(message)
    return response.content.strip()

def run_debate(scenarios: list[ScenarioSummary],context: str | None = None) -> str:
    optimist = _run_agent(OPTIMIST_PORMPT,scenarios,context)
    pessimist = _run_agent(PESSIMIST_PROMPT, scenarios,context)
    realist = _run_agent(REALIST_PROMPT, scenarios, context)

    return [
        f"optimist: {optimist}",
        f"pessimist: {pessimist}",
        f"realist: {realist}"
    ]

