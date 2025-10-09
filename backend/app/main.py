from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import crud
from . import schemas
from .deps import get_db
from .database import engine, SessionLocal, Base
from . import models
from .models import User
from .auth import (
    authenticate_user,
    create_access_token,
    get_current_user,
    hash_password,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)
from datetime import timedelta

# ========================
# FastAPI приложение
# ========================
app = FastAPI(
    title="TMC Inventory API",
    #переключить в None на проде!
    docs_url="/docs",       # Swagger UI
    redoc_url="/redoc",     # ReDoc
    openapi_url="/openapi.json"  # JSON-схема
)

from .routers import items
app.include_router(items.router)

# 02.10.2025 start
origins = ["http://localhost:8000", "http://127.0.0.1:8000", "http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# 02.10.2025 end

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
    # Создадим дефолтного пользователя (admin:admin), если БД пуста
    db = SessionLocal()
    if not db.query(User).first():
        user = User(username="admin", hashed_password=get_password_hash("admin"))
        db.add(user)
        db.commit()
    db.close()

# ========================
# Auth endpoints
# ========================

@app.post("/auth/login", tags=["Auth"], summary="Авторизация и получение токена")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Неверное имя пользователя или пароль")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": token, "token_type": "bearer"}

# ========================
# Регистрация нового пользователя (только admin)
# ========================
@app.post("/auth/register", tags=["Auth"], response_model=schemas.UserOut)
def register_user(
    new_user: schemas.UserCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Недостаточно прав")

    existing = crud.get_user_by_username(db, new_user.username)
    if existing:
        raise HTTPException(status_code=400, detail="Такой пользователь уже существует")

    hashed = hash_password(new_user.password)
    db_user = crud.create_user(db, new_user, hashed)
    return db_user

@app.get("/locations", response_model=list[schemas.LocationOut])
def list_locations(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    locations = db.query(models.Location).all()
    # преобразуем Enum → строка
    return [{"id": loc.id, "location": loc.name} for loc in locations]