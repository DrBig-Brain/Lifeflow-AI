from app.agents.planner import run_planner 

result = run_planner(
    question = "Shoudl i learn DSA or focus on ML projects this month",
    context = "I am going to be 3rd year engineering student preparing for placement and OAs"
)

print(result)