from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import secrets

router = APIRouter()

class User(BaseModel):
    username: str
    password: str


@router.post("/auth/login")
async def login(user: User):
    # Check user credentials (you can replace this with your own authentication logic)
    if user.username == "administrator" and user.password == "password":
        token = secrets.token_hex(16);
        return {"message": "Login successful", "username": user.username, "token": token}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")