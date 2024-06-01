from pydantic import BaseModel

class stt_Result(BaseModel):
    content: str
    millisec: int