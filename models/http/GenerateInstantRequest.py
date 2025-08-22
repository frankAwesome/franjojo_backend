from pydantic import BaseModel


class GenerateInstantRequest(BaseModel):
    fromId: str
    toId: str
    fromInput: str
