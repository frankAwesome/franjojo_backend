
from fastapi import HTTPException, Depends
from fastapi import APIRouter
from common.verify_token import verify_token
import logging


router = APIRouter()


@router.get("/example")
async def protected_route(user_data=Depends(verify_token)):
    logger = logging.getLogger("franjojo_backend")
    logger.info(f"/example accessed by user {user_data['uid']}")
    return {"message": "You are authenticated!", "user_id": user_data["uid"]}
