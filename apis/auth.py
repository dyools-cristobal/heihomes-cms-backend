from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

class User(BaseModel):
    username: str
    password: str


@router.post("/auth/login")
async def login(user: User):
    # Check user credentials (you can replace this with your own authentication logic)
    if user.username == "administrator" and user.password == "password":
        return {"message": "Login successful"}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")