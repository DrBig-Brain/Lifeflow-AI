from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.models import DecideRequest, ScenarioSummary, DecideResponse
from app.agents.planner import run_planner
from app.agents.simulator import run_simulator
from app.agents.debate import run_debate
from app.agents.judge import run_judge
from app.memory.store import save_decision, get_past_decision
from app.auth.routes import router as auth_router
from app.auth.utils import get_current_user
from app.auth.database import client
import os
load_dotenv()

app = FastAPI(title = "LifeFlowAI", version = "0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://life-flow-ai-sigma.vercel.app","http://localhost:5173"],  # we'll restrict this after deployment
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.on_event("startup")
async def startup():
    try:
        await client.admin.command("ping")
        print("Mongo connected")
    except Exception as e:
        print(repr(e))
    
app.include_router(auth_router)

@app.get("/")
def root():
    return{"status":"LifeFlowAI is running"}

@app.post("/decide", response_model = DecideResponse)
async def decide(request: DecideRequest, current_user: str = Depends(get_current_user)):
    
    past = await get_past_decision(current_user)

    try:
        alternatives = run_planner(request.question,request.context)
    except Exception as e:
        raise HTTPException(status_code = 500, detail = f"planner agent failed: {str(e)}")
    
    try:
        scenarios = run_simulator(alternatives,request.context)
    except Exception as e:
        raise HTTPException(status_code = 500, detail = f"simulator agent failed: {str(e)}")
    
    try:
        debate_log = run_debate(scenarios,request.context)
    except Exception as e:
        raise HTTPException(status_code = 500, detail = f"debate agent failed: {str(e)}")
    
    try:
        verdict = run_judge(scenarios,debate_log,request.context,past)
    except Exception as e:
        raise HTTPException(f"Judge agent failed: {str(e)}")

    
    response = DecideResponse(
        alternatives = alternatives,
        scenarios = scenarios,
        debate_log = debate_log,
        recommendation = verdict['recommendation'],
        reasoning = verdict["reasoning"]
    )

    await save_decision(
        decision_id = response.decision_id,
        user_id = request.user_id,
        question = request.question,
        recommendation = verdict["recommendation"],
        reasoning = verdict["reasoning"]
    )

    return response
