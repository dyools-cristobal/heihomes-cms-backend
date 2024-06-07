from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import secrets
import jwt
import datetime

router = APIRouter()

class User(BaseModel):
    username: str
    password: str

secret_key = 'livewithhei'
@router.post("/auth/login")
async def login(user: User):
    # Check user credentials (you can replace this with your own authentication logic)
    if user.username == "administrator" and user.password == "password":
        
        payload = {
            'user_id': 123,
            'username': 'john_doe',
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)  # Expiration time
        }
        token = jwt.encode(payload, secret_key, algorithm='HS256')
        return {"message": "Login successful", "username": user.username, "token": token}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")