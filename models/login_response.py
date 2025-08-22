from pydantic import BaseModel
from typing import Optional

class LoginResponse(BaseModel):
    kind: str
    localId: str
    email: str
    displayName: Optional[str] = None
    idToken: str
    registered: bool
    refreshToken: str
    expiresIn: str
