from langchain_core.messages import BaseMessage
from pydantic import BaseModel


class GenerateInstantResponse(BaseModel):
    response: BaseMessage
