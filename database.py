import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Modificar a URL para usar asyncpg corretamente
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL.startswith("postgres://"):  # Railway pode fornecer com "postgres://"
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+asyncpg://")

# Criar engine assíncrona
engine = create_async_engine(DATABASE_URL, echo=True)

# Criar sessão de banco de dados
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

# Dependência para injetar sessão no FastAPI
async def get_db():
    async with SessionLocal() as session:
        yield session
