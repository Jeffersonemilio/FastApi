from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from models import User
from database import get_db
from auth import (
    authenticate_user,
    create_access_token,
    get_current_user,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    pwd_context,
)

app = FastAPI()

async def startup():
    await get_db()

@app.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    user = await authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return {
        "username": current_user.username,
        "full_name": current_user.full_name
    }

@app.post("/register")
async def register_user(username: str, full_name: str, password: str, db: AsyncSession = Depends(get_db)):
    hashed_password = pwd_context.hash(password)
    new_user = User(username=username, full_name=full_name, hashed_password=hashed_password)
    
    db.add(new_user)
    await db.commit()
    
    return {"message": "Usuário cadastrado com sucesso"}

# Rotas protegidas que requerem autenticação
@app.get("/", dependencies=[Depends(get_current_user)])
async def root():
    return {"greeting": "Hello, World!", "message": "Welcome to ok FastAPI!"}

@app.get("/add", dependencies=[Depends(get_current_user)])
def add(a: float, b: float):
    return {"operation": "addition", "a": a, "b": b, "result": a + b}

@app.get("/subtract", dependencies=[Depends(get_current_user)])
def subtract(a: float, b: float):
    return {"operation": "subtraction", "a": a, "b": b, "result": a - b}

@app.get("/multiply", dependencies=[Depends(get_current_user)])
def multiply(a: float, b: float):
    return {"operation": "multiplication", "a": a, "b": b, "result": a * b}

@app.get("/divide", dependencies=[Depends(get_current_user)])
def divide(a: float, b: float):
    if b == 0:
        raise HTTPException(status_code=400, detail="Divisão por zero não é permitida")
    return {"operation": "division", "a": a, "b": b, "result": a / b}

@app.get("/imc", dependencies=[Depends(get_current_user)])
def calculate_imc(peso: float, altura: float):
    if peso <= 0:
        raise HTTPException(status_code=400, detail="O peso deve ser maior que zero")
    if altura <= 0:
        raise HTTPException(status_code=400, detail="A altura deve ser maior que zero")
    
    imc = peso / (altura * altura)
    
    classificacao = ""
    if imc < 18.5:
        classificacao = "Abaixo do peso"
    elif imc < 25:
        classificacao = "Peso normal"
    elif imc < 30:
        classificacao = "Sobrepeso"
    else:
        classificacao = "Obesidade"
    
    return {
        "peso": peso,
        "altura": altura,
        "imc": round(imc, 2),
        "classificacao": classificacao
    }
