from fastapi import APIRouter, HTTPException
from models.user_profile import UserProfile
from firebase_admin import firestore
from common.firestore_utils import get_db

router = APIRouter()


@router.post("/profile")
async def add_profile(profile: UserProfile):
    try:
        db = get_db()
        doc_ref = db.collection("profiles").document(profile.email)
        doc_ref.set(profile.dict())
        return {"message": "Profile saved successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/profile/{email}")
async def get_profile(email: str):
    try:
        db = get_db()
        doc_ref = db.collection("profiles").document(email)
        doc = doc_ref.get()
        if doc.exists:
            return doc.to_dict()
        else:
            raise HTTPException(status_code=404, detail="Profile not found.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
