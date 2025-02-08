import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Ler a URL do banco do arquivo .env
DATABASE_URL = os.getenv("DATABASE_URL")

# 🚨 Garantir que estamos usando 'asyncpg'
if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")

# Criar engine assíncrona
engine = create_async_engine(DATABASE_URL, echo=True)

# Criar sessão de banco de dados
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

# Dependência para injetar sessão no FastAPI
async def get_db():
    async with SessionLocal() as session:
        yield session
