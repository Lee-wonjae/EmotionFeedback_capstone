from typing import List
from pydantic import BaseModel

class ScenarioData(BaseModel):
    scenarios: List[str]
    likeabilities: List[float]