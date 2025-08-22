from fastapi import HTTPException, Depends
from fastapi import APIRouter
from common.verify_token import verify_token


router = APIRouter()


@router.get("/example")
async def protected_route(user_data=Depends(verify_token)):
    return {"message": "You are authenticated!", "user_id": user_data["uid"]}
