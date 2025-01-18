from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.app.db.db import get_db
from src.app.users.models.user_model import User, UserCreate, TokenSchema, UserLogin
from src.app.libs.hash import hash_pass, verify_password, create_access_token, create_refresh_token
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

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(user:UserCreate, db: AsyncSession = Depends(get_db)):
    new_user = User(name=user.name, email=user.email, password=hash_pass(user.password))
    db.add(new_user)
    await db.commit()
    return {"message": "User created successfully"}

@router.post("/login", response_model=TokenSchema, status_code=status.HTTP_201_CREATED) 
async def login(form_data: UserLogin , db: AsyncSession = Depends(get_db)):
    query = await db.execute(select(User).where(User.email == form_data.email))
    user = query.scalar_one_or_none() 
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )

    hashed_pass = user.password
    if not verify_password(form_data.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )

    return {
        "access_token": create_access_token(user.email),
        "refresh_token": create_refresh_token(user.email),
    }  