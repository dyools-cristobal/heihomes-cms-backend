from fastapi import APIRouter, FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Annotated

from sqlalchemy import select
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

router = APIRouter()

class RoleBase(BaseModel):
    name: str
    description: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
#get all roles
@router.get("/roles/", status_code=status.HTTP_200_OK)
async def get_roles(db: db_dependency):
    stmt = select(models.Role)
    result = db.execute(stmt)
    roles = result.scalars().all()
    return roles

#create role
@router.post("/roles/", status_code=status.HTTP_201_CREATED)
async def create_role(role:RoleBase, db: db_dependency):
    db_role = models.Role(**role.dict())
    db.add(db_role)
    db.commit()

# delete role
@router.delete("/roles/{role_id}",status_code=status.HTTP_200_OK)
async def delete_role(role_id: int, db:db_dependency):
    db_role = db.query(models.Role).filter(models.Role.id == role_id).first()
    if db_role is None:
        raise HTTPException(status_code=404, detail='Role not found')
    db.delete(db_role)
    db.commit()