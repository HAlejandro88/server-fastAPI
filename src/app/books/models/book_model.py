from sqlalchemy import Column, Integer, String
from pydantic import BaseModel
from src.app.db.db import Base
from typing import Optional


class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    author = Column(String, index=True)
    description = Column(String, index=True)
    
class BookeCreate(BaseModel):
    title: str
    author: str
    description: Optional[str] = None 