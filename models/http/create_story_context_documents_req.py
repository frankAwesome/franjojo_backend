from typing import List

from pydantic import BaseModel


class StoryContextDocumentReq(BaseModel):
    documents: List[str]