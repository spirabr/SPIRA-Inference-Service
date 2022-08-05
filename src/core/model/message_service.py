from pydantic import BaseModel

from core.model.result import ResultUpdate


class RequestLetter(BaseModel):
    content: ResultUpdate
    publishing_channel: str
