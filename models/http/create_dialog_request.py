from typing import List
from pydantic import BaseModel

from models.http.chapter_milestone import ChapterMilestone


class CreateDialogRequest(BaseModel):
    activeChapterId: int
    playerQuestion: str
    completedChapterIds: List[int]
    milestones: List[ChapterMilestone]
