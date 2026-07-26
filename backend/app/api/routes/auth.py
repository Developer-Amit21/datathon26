from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()


class LoginRequest(BaseModel):
    username: str
    password: str


@router.post("/login")
def login(payload: LoginRequest) -> dict:
    if payload.username == "admin" and payload.password == "admin":
        return {
            "access_token": "demo-token",
            "token_type": "bearer",
            "role": "Administrator",
            "user": payload.username,
        }
    raise HTTPException(status_code=401, detail="Invalid credentials")
