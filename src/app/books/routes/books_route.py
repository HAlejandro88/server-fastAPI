from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.app.db.db import get_db
from src.app.books.models.book_model import Book, BookeCreate

#router = APIRouter()

router = APIRouter(
    prefix="/books",
    tags=["books"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def get_books(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Book))
    books = result.scalars().all()
    return books

@router.post("/")
async def create_book(book:BookeCreate, db: AsyncSession = Depends(get_db)):
    new_book = Book(title=book.title, author=book.author, description=book.description)
    db.add(new_book)
    await db.commit()
    return {"message": "Book created successfully"}
