from sqlalchemy import Column, Integer, String
from src.app.db.db import Base
from pydantic import BaseModel

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    


class UserCreate(BaseModel):
    name: str
    email: str