from pydantic import BaseModel


class ResultUpdate(BaseModel):
    inference_id: str
    output: float
    diagnosis: str
