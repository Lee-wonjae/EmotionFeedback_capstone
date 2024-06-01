from typing import List
from pydantic import BaseModel

class profileData(BaseModel):
    interests: List[str]
