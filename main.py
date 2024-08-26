from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine
import models
from apis.rooms import router as rooms_router
from apis.roles import router as roles_router
from apis.properties import router as properties_router
from apis.amenities import router as amenities_router
from apis.upload import router as upload_router
from apis.auth import router as auth_router
from apis.users import router as user_router


app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(rooms_router)
app.include_router(roles_router)
app.include_router(properties_router)
app.include_router(amenities_router)
app.include_router(upload_router)
app.include_router(auth_router)
app.include_router(user_router)

origins = [
    'http://localhost:4200',
    'https://localhost:4200',
    'https://heihomes.sg',
    'http://heihomes.sg',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["POST", "GET", "PUT", "DELETE"],
    allow_headers=["*"]
)