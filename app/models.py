from typing import List, Literal, Optional, Dict, Any
from pydantic import BaseModel, Field

Priority = Literal["low", "medium", "high", "critical"]
Team = Literal["network", "hardware", "software", "security", "accounts"]
ActionType = Literal["classify", "assign", "request_info", "propose_fix", "resolve"]

class Ticket(BaseModel):
    id: str
    title: str
    description: str
    reporter: str
    system: str
    expected_priority: Priority
    expected_team: Team
    required_info: List[str] = Field(default_factory=list)
    resolution_keywords: List[str] = Field(default_factory=list)

class EnvAction(BaseModel):
    action_type: ActionType
    payload: Dict[str, Any]

class Observation(BaseModel):
    ticket_id: str
    title: str
    description: str
    reporter: str
    system: str
    known_info: Dict[str, Any]
    missing_info: List[str]
    history: List[str]
    step_count: int
    max_steps: int
    done: bool
    success: bool
    last_action_error: Optional[str] = None

class StepResult(BaseModel):
    observation: Observation
    reward: float
    done: bool
    info: Dict[str, Any] = Field(default_factory=dict)