from pydantic import BaseModel


class GenerateDialogTree(BaseModel):
    projectId: int
    dialogTreeId: int
    currentChapterId: int
    currentDialogTreeNodeId: int
    toDialogAgentId: int