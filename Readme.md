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
- Node.js 20.19+ and npm
- Docker Compose (for the included local MongoDB service)
- A Groq API key (the current agents read it from `XAI_API_KEY`)

Backend and database
1. Copy the local environment template and start MongoDB:

```bash
cp .env.example .env
docker compose up -d mongodb
```

Add your Groq API key to `.env` as `XAI_API_KEY` before using `/decide`. If you already have a MongoDB instance, set `MONGODB_CONNECT_URI` in `.env` to its connection URI instead; set `MONGODB_TLS=true` if that server requires TLS.

2. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

3. Install Python dependencies:

```bash
pip install -r requirements.txt
```

4. Run the API server (development):

```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

The API will be available at `http://127.0.0.1:8000` and its interactive docs at `http://127.0.0.1:8000/docs`.

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
In a second terminal, install and run the client:

```bash
cd client
npm install
npm run dev
```

Open the local URL printed by Vite (normally `http://localhost:5173`). Requests are proxied to the local API by `vite.config.js`; set `VITE_API_URL` only when using a different API origin.

Testing
-------
Run the Python tests from the repository root:

```bash
pytest -q
```

Notes & configuration
---------------------
- The agents call Groq's API using `XAI_API_KEY` (retained for compatibility) and default to `openai/gpt-oss-120b`. Set `GROQ_MODEL` in `.env` to select another model available to your Groq account.
- MongoDB data is stored in the `lifeflowai-mongodb` Docker volume. Stop the local database with `docker compose down`; `docker compose down -v` also deletes its data.
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

