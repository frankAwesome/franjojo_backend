from typing import List
from pydantic import BaseModel


class ChapterMilestone(BaseModel):
    milestoneId: int
    name: str
    matches: List[str]
    completed: bool
