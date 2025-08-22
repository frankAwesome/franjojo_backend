from fastapi import HTTPException, Depends, Header
from common.verify_token import verify_token
from models.user import User
from models.login_response import LoginResponse
from firebase_admin import auth
from fastapi import APIRouter
import requests
import json
import os


router = APIRouter()


@router.post("/login", response_model=LoginResponse)
async def login(user: User):
    # Load API key from firebase-api-key.json
    key_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "firebase-api-key.json")
    with open(key_path, "r") as f:
        api_key = json.load(f)["api_key"]
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}"
    payload = {
        "email": user.email,
        "password": user.password,
        "returnSecureToken": True
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        return LoginResponse(**response.json())
    else:
        raise HTTPException(status_code=400, detail=response.json().get("error", {}).get("message", "Login failed"))
