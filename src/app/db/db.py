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
"""
echo=True
Descripción: Cuando se establece en True, este parámetro activa el modo "echo" del motor de SQLAlchemy. Esto significa que todas las consultas SQL que se envían a la base de datos se imprimirán en la consola. Es útil para la depuración, ya que te permite ver qué consultas se están ejecutando.
Uso: Puedes establecerlo en False en producción para evitar la salida de consultas en la consola.
future=True
Descripción: Este parámetro habilita el modo futuro de SQLAlchemy, lo que significa que el motor se comportará de acuerdo con las futuras versiones de SQLAlchemy. Esto es útil si deseas utilizar características que se introducirá en versiones posteriores de SQLAlchemy.
Uso: Al establecer future=True, puedes asegurarte de que tu código sea compatible con las futuras versiones de SQLAlchemy y que puedas aprovechar nuevas características y mejoras.
"""

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