from app.agents.planner import run_planner
from app.agents.simulator import run_simulator

question = "Should i learn DSA or focus on ML projects this month"
context = "I am a 2nd year ECE student preparing for placement OAs"

alternatives = run_planner(question,context)
print("alternatives: ",alternatives)
scenarios = run_simulator(alternatives,context)
for s in scenarios:
    print(s)