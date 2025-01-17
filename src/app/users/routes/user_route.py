from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.app.db.db import get_db
from src.app.users.models.user_model import User, UserCreate
#from sqlalchemy import text

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={
        404: {"description": "Not found"},
        400: {"description": "Bad Request"},
        422: {"description": "Validation Error"},
        500: {"description": "Internal Server Error"},
    },
)

@router.get("/")
async def get_users(db: AsyncSession = Depends(get_db)):
    #result = await db.execute(text("SELECT * FROM users"))
    #print(result, "<----result_here")
    #users = result.fetchall()
    result = await db.execute(select(User))
    users = result.scalars().all() 
    return users

@router.post("/")
async def create_user(user:UserCreate, db: AsyncSession = Depends(get_db)):
    new_user = User(name=user.name, email=user.email)
    db.add(new_user)
    await db.commit()
    return {"message": "User created successfully"}