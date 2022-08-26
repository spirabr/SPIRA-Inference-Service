from typing import List
from pydantic import BaseModel


class ResultUpdate(BaseModel):
    inference_id: str
    output: List[float]
    diagnosis: str
