from langchain_groq import ChatGroq
from langchain.messages import SystemMessage, HumanMessage
from dotenv import load_dotenv
from app.models import ScenarioSummary
import os
import json

load_dotenv()

llm = ChatGroq(
    model = "llama-3.3-70b-versatile",
    api_key = os.getenv("XAI_API_KEY"),
    temperature = 0.7
)

JUDGE_SYSTEM_PROMPT = """
You are a wise judge synthesizing a decision debate.
You will receive decesion scenarios and a debate log from three agents: optimist, pessimist and realist.
Your job is to read everything carefully and produce a final recommendation.

Rules:
- Pick exactly one option as your recommendation.
- Explain your reasoning clearly in 2-3 sentences.
- Return ONLY a json object, nothing else.
- No Markdown, no backticks

Example output: {
    "recommendation":"the exact option text here",
    "reasoning":"your reasoning here is 2-3 sentences"
}
"""

def run_judge(
        scenarios: list[ScenarioSummary],
        debate_log: list[str],
        context: str | None = None,
        past_decisions: list[dict]= [],
) -> dict:
    scenarios_text = "\n".join([
        f"-Option: {s.option}\nOutcome: {s.outcome}\nRisk:{s.risk_level}"
        for s in scenarios
    ])
    debate_text = "\n".join(debate_log)

    user_message = f"Scenarios:\n{scenarios_text}\nDebate:\n{debate_text}"
    
    if context:
        user_message += f"\nContext:\n{context}"

    if past_decisions:
        past_text = "\n".join([
            f"- Q: {p['question']} -> Recommendation: {p['recommendation']}"
            for p in past_decisions
        ])
        user_message += f"\n\nPast decisions by this user:\n{past_text}"
        
    message = [
        SystemMessage(content=JUDGE_SYSTEM_PROMPT),
        HumanMessage(content=user_message)
    ]
    response = llm.invoke(message)
    result = json.loads(response.content)
    return result