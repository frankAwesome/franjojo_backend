from pydantic import BaseModel


class GenerateInstantRequest(BaseModel):
    fromId: str
    toId: str
    fromInput: str
    story_id: str
    chapter: int
    action: str  # e.g. "story_progressed", "idle", "annoyed", "chapter_info"
