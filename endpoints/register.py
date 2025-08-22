from fastapi import requests, HTTPException
from models.user import User
from firebase_admin import auth
from fastapi import APIRouter


router = APIRouter()


@router.post("/register")
async def register(user: User):
    try:
        user_record = auth.create_user(
            email=user.email,
            password=user.password
        )
        return {"uid": user_record.uid, "email": user_record.email}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))