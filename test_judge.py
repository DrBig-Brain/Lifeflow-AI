from app.agents.planner import run_planner
from app.agents.simulator import run_simulator
from app.agents.debate import run_debate
from app.agents.judge import run_judge

question = "Should I learn DSA or focus on ML projects this month?"
context = "I am a 2nd year ECE student preparing for placement OAs"

alternatives = run_planner(question, context)
scenarios = run_simulator(alternatives, context)
debate_log = run_debate(scenarios, context)
result = run_judge(scenarios, debate_log, context)

print("Recommendation:", result["recommendation"])
print()
print("Reasoning:", result["reasoning"])