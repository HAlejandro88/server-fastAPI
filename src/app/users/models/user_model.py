from sqlalchemy import Column, Integer, String
from src.app.db.db import Base
from pydantic import BaseModel

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    


class UserCreate(BaseModel):
    name: str
    email: str
    password: str

class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    
class UserLogin(BaseModel):
    email: str
    password: str