from pydantic import BaseModel


class ChapterMilestone(BaseModel):
    name: str
    completed: bool
