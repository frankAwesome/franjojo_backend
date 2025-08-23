from typing import List
from pydantic import BaseModel


class GenerateInstantRequest(BaseModel):
    projectId: int
    fromId: int
    toId: int
    fromInput: str
    current_chapter_id: int
    completed_chapter_ids: List[int]
