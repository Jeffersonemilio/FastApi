import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Carregar variáveis do .env
load_dotenv()

# Ler a URL do banco do arquivo .env
DATABASE_URL = os.getenv("DATABASE_URL")

# Criar engine assíncrona para PostgreSQL
engine = create_async_engine(DATABASE_URL, echo=True)

# Criar sessão de banco de dados
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

# Dependência para injetar sessão no FastAPI
async def get_db():
    async with SessionLocal() as session:
        yield session


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
