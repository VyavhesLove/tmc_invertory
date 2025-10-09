from sqlalchemy.orm import Session
from . import models, schemas

# не используются в коде, но оставлены для возможного будущего использования

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