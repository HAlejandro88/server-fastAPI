from fastapi import FastAPI, Request
#from app.routes import router as user_router
#from app.db import init_db

from src.app.books.routes.books_route import router as books_router
from src.app.users.routes.user_route import router as user_router
from fastapi.exceptions import RequestValidationError
#from src.app.db.db import init_db


app = FastAPI()

@app.middleware("http")
async def custom_middleware(request: Request, call_next):
    print("Procesando solicitud:", request.url)
    response = await call_next(request)
    print("Procesando respuesta")
    return response

# Incluir rutas
app.include_router(user_router)
app.include_router(books_router)


# Ruta de prueba
@app.get("/")
async def root():
    return {"message": "Hello, FastAPI with SQLAlchemy!"}

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "body": exc.body},
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error"},
    )