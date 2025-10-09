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

@app.get(
    "/items",
    response_model=list[schemas.InventoryItemOut],
    tags=["inventory"],
    summary="Получить список ТМЦ с ответственными",
)
def list_items(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    items = (
        db.query(
            models.InventoryItem.id,
            models.InventoryItem.name,
            models.InventoryItem.serial_number,
            models.InventoryItem.brand,
            models.InventoryItem.status,
            models.InventoryItem.location_id,
            models.InventoryItem.location,
            models.User.username.label("responsible_name")
        )
        .outerjoin(models.User, models.InventoryItem.responsible_id == models.User.id)
        .all()
    )

    return [
        {
            "id": i.id,
            "name": i.name,
            "serial_number": i.serial_number,
            "brand": i.brand,
            "status": i.status,
            "location_id": i.location_id,
            "location": i.location,
            "responsible_name": i.responsible_name,
        }
        for i in items
    ]

@app.get("/items/{item_id}")
def get_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    item = db.query(InventoryItem).filter(InventoryItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    # Можно добавить проверку прав пользователя к объекту (если нужно)
    return item

@app.post("/items")
def add_item(
    item: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    location_obj = None
    if item.get("location_id"):
        location_obj = db.query(models.Location).filter(models.Location.id == item["location_id"]).first()
        if not location_obj:
            raise HTTPException(status_code=400, detail="Указанная локация не найдена")

    new_item = models.InventoryItem(
        name=item.get("name"),
        serial_number=item.get("serial_number"),
        brand=item.get("brand"),
        status=item.get("status", "Подтвердить ТМЦ"),
        responsible=item.get("responsible"),
        location_id=item.get("location_id"),
        location=location_obj.name if location_obj else None,
    )

    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item


@app.put("/items/{item_id}")
def update_item(
    item_id: int,
    item_data: schemas.TMCUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    item = db.query(InventoryItem).filter(InventoryItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    for key, value in item_data.dict(exclude_unset=True).items():
        setattr(item, key, value)
    db.commit()
    db.refresh(item)
    return item


@app.delete("/items/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_item = db.query(InventoryItem).filter(InventoryItem.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")

    db.delete(db_item)
    db.commit()
    return {"message": "Item deleted"}

@app.put("/api/tmc/{tmc_id}/edit", response_model=schemas.TMCOut)
def edit_tmc_item(tmc_id: int, tmc_in: schemas.TMCUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    obj = crud.update_tmc(db, tmc_id, tmc_in)
    if not obj:
        raise HTTPException(status_code=404, detail="TMC not found")
    return obj

@app.post("/api/tmc/{tmc_id}/transfer", response_model=schemas.TMCOut)
def transfer_tmc_item(tmc_id: int, new_responsible_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    obj = crud.transfer_tmc(db, tmc_id, new_responsible_id)
    if not obj:
        raise HTTPException(status_code=404, detail="TMC not found")
    return obj

@app.post("/api/tmc/{tmc_id}/send_to_service", response_model=schemas.TMCOut)
def send_tmc_to_service(tmc_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    obj = crud.send_to_service(db, tmc_id)
    if not obj:
        raise HTTPException(status_code=404, detail="TMC not found")
    return obj

@app.post("/api/tmc/{tmc_id}/return_from_service", response_model=schemas.TMCOut)
def return_tmc_from_service(tmc_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    obj = crud.return_from_service(db, tmc_id)
    if not obj:
        raise HTTPException(status_code=404, detail="TMC not found")
    return obj

@app.get("/locations", response_model=list[schemas.LocationOut])
def list_locations(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    locations = db.query(models.Location).all()
    # преобразуем Enum → строка
    return [{"id": loc.id, "location": loc.name} for loc in locations]