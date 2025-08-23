from pydantic import BaseModel
from typing import List
from datetime import datetime

class Milestone(BaseModel):
    id: int
    name: str
    completed: bool
    timestamp: datetime = None

class GetNPCDialogRequest(BaseModel):
    dialogText: str
    storyId: str
    protagonistId: str
    npcId: str
    chapterId: str
    milestones: List[Milestone]
    timestamp: datetime = None


class Character(BaseModel):
    id: int
    name: str
    subtitle: str = ""  # e.g. 'protagonist', 'antagonist', etc.
    image: str = ""  # Direct URL to the character's image
    description: str = ""
    type: str = "npc"  # or "protagonist"
    timestamp: datetime = None

# For backward compatibility, NPCInfo is an alias for Character
NPCInfo = Character

class ChapterInfo(BaseModel):
    id: int
    title: str
    image: str = ""
    milestones: List[Milestone]
    description: str = ""
    timestamp: datetime = None


class GameStoryModel(BaseModel):
    storyId: int
    title: str
    lore: str = ""  # Story background/lore
    characters: List[Character]
    chapters: List[ChapterInfo]
    timestamp: datetime = None

class GetGameStoryParamsResponse(BaseModel):
    endpoint: str
    method: str
    response: dict
    timestamp: datetime = None
