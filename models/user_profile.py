from pydantic import BaseModel

class UserProfile(BaseModel):
    email: str
    name: str
    age: int
    bio: str = ""
