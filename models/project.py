from typing import List
from models.chapter import Chapter


class Project:
    def __init__(self, project_id, lore, chapters):
        self.project_id = project_id
        self.lore = lore
        self.chapters: List[Chapter] = chapters