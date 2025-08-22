from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from firebase_admin import auth

router = APIRouter()

class GoogleLoginRequest(BaseModel):
    id_token: str

@router.post("/google-login")
async def google_login(payload: GoogleLoginRequest):
    try:
        decoded_token = auth.verify_id_token(payload.id_token)
        return {"uid": decoded_token["uid"], "email": decoded_token.get("email")}
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid Google ID token")
