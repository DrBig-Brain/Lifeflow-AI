from pydantic import BaseModel, Field
from typing import List
import uuid

class DecideRequest(BaseModel):
    question: str
    context: str | None = None
    user_id: str | None = None  # for memory later

class ScenarioSummary(BaseModel):
    option: str
    outcome: str
    risk_level: str  # low / medium / high

class DecideResponse(BaseModel):
    decision_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    alternatives: List[str]
    scenarios: List[ScenarioSummary]
    debate_log: List[str]
    recommendation: str
    reasoning: str