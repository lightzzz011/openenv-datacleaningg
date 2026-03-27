from pydantic import BaseModel
from typing import Dict, List, Any


class Action(BaseModel):
    action: str


class Observation(BaseModel):
    data: Dict[str, List[Any]]


class StepResult(BaseModel):
    observation: Observation
    reward: float
    done: bool
    info: Dict[str, Any]