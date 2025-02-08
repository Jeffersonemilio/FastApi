from fastapi import FastAPI, HTTPException, Depends

from sqlalchemy.ext.asyncio import AsyncSession
from models import User
from database import get_db

from passlib.context import CryptContext

app = FastAPI()

async def startup():
    await init_db()

@app.get("/")
async def root():
    return {"greeting": "Hello, World!", "message": "Welcome to ok FastAPI!"}

@app.get("/add")
def add(a: float, b: float):
    return {"operation": "addition", "a": a, "b": b, "result": a + b}

@app.get("/subtract")
def subtract(a: float, b: float):
    return {"operation": "subtraction", "a": a, "b": b, "result": a - b}

@app.get("/multiply")
def multiply(a: float, b: float):
    return {"operation": "multiplication", "a": a, "b": b, "result": a * b}

@app.get("/divide")
def divide(a: float, b: float):
    if b == 0:
        raise HTTPException(status_code=400, detail="Divisão por zero não é permitida")
    return {"operation": "division", "a": a, "b": b, "result": a / b}


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@app.post("/register")
async def register_user(username: str, full_name: str, password: str, db: AsyncSession = Depends(get_db)):
    hashed_password = pwd_context.hash(password)
    new_user = User(username=username, full_name=full_name, hashed_password=hashed_password)
    
    db.add(new_user)
    await db.commit()
    
    return {"message": "Usuário cadastrado com sucesso"}