from typing import List
from models.chapter import Chapter
from models.project import Project


projects: List[Project] = [
    Project(1, 'You are in the world of the 3 little pigs, who all just moved out of their parents house and are about to build their own homes.', [
        Chapter(1, 'Pig 1 has built his house out of straw. Pig 1 does not believe in the Big Bad Wolf', 'Pig 1 house has been blown away by the Big Bad Wolf. He is now aware and afraif of the Big Bad Wolf. He will flee in fear anytime the Big Bad Wolf interacts with him')
    ])
]

class ProjectService:
    def get_project(self, project_id: int):
        return next(x for x in projects if x.project_id == project_id)
