# backend/app/crud.py
from sqlalchemy.orm import Session
from . import models, schemas

# Подключим get_password_hash из auth (если у тебя хеширование в auth.py)
# Если функция называется иначе, поправь импорт.
try:
    from .auth import get_password_hash
except Exception:
    # Если auth.get_password_hash не доступен, пробрасываем - лучше хешировать заранее
    get_password_hash = None

# ----------------------
# Users
# ----------------------
def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user_in: schemas.UserCreate):
    """
    Создает нового пользователя.
    Если в проекте хеширование вынесено в другое место, можно заменить логику,
    чтобы принимать уже захешированный пароль.
    """
    if get_password_hash is None:
        raise RuntimeError("get_password_hash is not available. Please provide hashed password or import hashing function.")

    hashed = get_password_hash(user_in.password)
    db_user = models.User(
        username=user_in.username,
        email=getattr(user_in, "email", None),
        hashed_password=hashed,
        is_admin=getattr(user_in, "is_admin", False)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# ----------------------
# TMC / Inventory CRUD
# ----------------------
def list_tmc(db: Session, status: str | None = None):
    q = db.query(models.TMC)
    if status:
        q = q.filter(models.TMC.status == status)
    return q.all()

def create_tmc(db: Session, tmc_in: schemas.TMCCreate):
    obj = models.TMC(**tmc_in.model_dump()) if hasattr(tmc_in, "model_dump") else models.TMC(**tmc_in.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def update_tmc(db: Session, tmc_id: int, tmc_in: schemas.TMCUpdate):
    # Используем session.get если доступно, либо fallback к query.filter
    obj = db.get(models.TMC, tmc_id) if hasattr(db, "get") else db.query(models.TMC).filter(models.TMC.id == tmc_id).first()
    if not obj:
        return None

    # Обновляем только переданные поля
    data = tmc_in.model_dump(exclude_unset=True) if hasattr(tmc_in, "model_dump") else tmc_in.dict(exclude_unset=True)
    for k, v in data.items():
        if hasattr(obj, k):
            setattr(obj, k, v)

    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def transfer_tmc(db: Session, tmc_id: int, new_responsible_id: int):
    obj = db.get(models.TMC, tmc_id) if hasattr(db, "get") else db.query(models.TMC).filter(models.TMC.id == tmc_id).first()
    if not obj:
        return None
    obj.responsible_id = new_responsible_id
    db.commit()
    db.refresh(obj)
    return obj

def send_to_service(db: Session, tmc_id: int):
    obj = db.get(models.TMC, tmc_id) if hasattr(db, "get") else db.query(models.TMC).filter(models.TMC.id == tmc_id).first()
    if not obj:
        return None
    obj.status = models.TMCStatus.in_repair
    db.commit()
    db.refresh(obj)
    return obj

def return_from_service(db: Session, tmc_id: int):
    obj = db.get(models.TMC, tmc_id) if hasattr(db, "get") else db.query(models.TMC).filter(models.TMC.id == tmc_id).first()
    if not obj:
        return None
    obj.status = models.TMCStatus.available
    db.commit()
    db.refresh(obj)
    return obj