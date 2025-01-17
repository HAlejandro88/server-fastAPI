from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData
from dotenv import load_dotenv
from pathlib import Path
import os

# Carga las variables de entorno del archivo .env
dotenv_path = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(dotenv_path=dotenv_path)

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/foo"
#DATABASE_URL = os.getenv("DATABASE_URL","postgresql+asyncpg://postgres:postgres@localhost:5432/foo")

# Crear el motor asincrónico
engine = create_async_engine(DATABASE_URL, echo=True, future=True)

# Crear la clase Base que utilizarán los modelos
Base = declarative_base()

# Crear la sesión asincrónica
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

# Función para obtener una sesión
async def get_session():
    async with async_session() as session:
        yield session
        
async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session
        
async def init_db():
    async with engine.begin() as conn:
        # Opcional: elimina tablas existentes
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)