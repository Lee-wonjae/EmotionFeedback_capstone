from pydantic import BaseModel

class emotion_Result(BaseModel):
    image: int
    voice: int