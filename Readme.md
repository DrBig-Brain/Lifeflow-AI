# LifeFlowAI

LifeFlowAI is a modular decision-making service that composes specialised agents (planner, simulator, debate, judge) to evaluate alternatives and produce explainable recommendations. It provides a FastAPI backend and a React + Vite frontend client.

Live demo
---------
- Deployment: https://life-flow-ai-sigma.vercel.app/

Key features
------------
- Planner: generate concrete alternatives for a decision using an LLM.
- Simulator: synthesize scenario outcomes for each alternative.
- Debate: create a structured debate between perspectives on scenarios.
- Judge: produce a final recommendation and reasoning, optionally using past decisions from memory.
- Simple auth and memory layers for per-user persistence.

Repository layout
-----------------
- `app/` — Backend FastAPI service and agents
	- `main.py` — FastAPI application and `/decide` endpoint
	- `models.py` — Pydantic request/response models
	- `agents/` — Agent implementations: `planner.py`, `simulator.py`, `debate.py`, `judge.py`
	- `auth/` — Authentication routes and utilities
	- `memory/` — Persistent decision store helpers
- `client/` — React + Vite frontend
- Top-level tests: `test_planner.py`, `test_simulator.py`, `test_judge.py`, `test_debate.py`

Getting started
---------------

Prerequisites
- Python 3.10+
- Node.js 16+ and npm or yarn
- An LLM API key (set as environment variables; see Notes)

Backend (API)
1. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install Python dependencies:

```bash
pip install -r requirements.txt
```

3. Set required environment variables (example):

```bash
export XAI_API_KEY="your-api-key-here"
```

4. Run the API server (development):

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000` by default.

API endpoints
- `GET /` — health/status ping
- `POST /decide` — decision endpoint. Accepts a `DecideRequest` JSON and returns a `DecideResponse` with alternatives, scenarios, debate log, and a recommendation.

Example request
```json
{
	"question": "Should I take a job offer in another city?",
	"context": "I have young kids and a mortgage.",
	"user_id": "user-123"
}
```

Frontend (client)
1. Install and run the client:

```bash
cd client
npm install
npm run dev
```

Testing
-------
Run the Python tests from the repository root:

```bash
pytest -q
```

Notes & configuration
---------------------
- The agents call external LLM services; set API keys (for example, `XAI_API_KEY`) in your environment before running.
- `app/models.py` defines `DecideRequest` and `DecideResponse` used by the API.
- Ensure `requirements.txt` pins the dependencies you need for reproducible installs.

Contributing
------------
- Add agent strategies under `app/agents/` and wire them into `app/main.py`.
- Add tests for new behavior and run `pytest`.

License
-------
This repository does not include a license file. Add a `LICENSE` if you plan to open source the project.

Contact
-------
Open issues or feature requests on the repository tracker.

