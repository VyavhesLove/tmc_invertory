# backend/app/routers/items.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app import models, schemas
from app.deps import get_db
from app.auth import get_current_user
from app.models import User

router = APIRouter(
    prefix="/items",
    tags=["ТМЦ"]
)

@router.get(
    "/",
    response_model=List[schemas.ItemOut],
    summary="Получить список всех ТМЦ",
    description="""
    Возвращает список всех объектов ТМЦ (inventory_items).  
    Поля `responsible_name` и `location_name` формируются из связанных таблиц `users` и `locations`.
    """
)
def list_items(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Основной эндпоинт для получения списка всех ТМЦ.
    Возвращает готовый список JSON-объектов без обёрток.
    """
    # Получаем все объекты
    items = db.query(models.InventoryItem).all()
    if not items:
        return []

    # Собираем данные вручную (лучше, чем ORM.join для dev)
    result = []
    for it in items:
        responsible_name = (
            db.query(models.User.username)
            .filter(models.User.id == it.responsible_id)
            .scalar()
        )
        location_name = (
            db.query(models.Location.name)
            .filter(models.Location.id == it.location_id)
            .scalar()
        )

        result.append({
            "id": it.id,
            "name": it.name,
            "serial_number": it.serial_number,
            "brand": it.brand,
            "status": it.status,
            "responsible_id": it.responsible_id,
            "responsible_name": responsible_name or "",
            "location_id": it.location_id,
            "location_name": location_name or "",
            "comment": getattr(it, "comment", None),
        })

    return result

@router.get("/{item_id}", response_model=schemas.ItemOut, summary="Получить информацию о ТМЦ по ID")
def get_item(item_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Возвращает подробную информацию об объекте ТМЦ по его ID.
    """
    item = db.query(models.InventoryItem).filter(models.InventoryItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="ТМЦ не найден")

    responsible_name = (
        db.query(models.User.username)
        .filter(models.User.id == item.responsible_id)
        .scalar()
    )
    location_name = (
        db.query(models.Location.name)
        .filter(models.Location.id == item.location_id)
        .scalar()
    )
    return {
        "id": item.id,
        "name": item.name,
        "serial_number": item.serial_number,
        "brand": item.brand,
        "status": item.status,
        "responsible_id": item.responsible_id,
        "responsible_name": responsible_name,
        "location_id": item.location_id,
        "location": location_name,
        "comment": item.comment,
    }


@router.post(
    "/",
    response_model=schemas.ItemOut,
    status_code=status.HTTP_201_CREATED,
    summary="Создать новый объект ТМЦ"
)
def create_item(item_in: schemas.ItemCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Добавляет новый объект ТМЦ в базу данных.
    Проверяет, существует ли указанная локация и ответственный пользователь.
    """
    if item_in.location_id:
        location = db.query(models.Location).filter(models.Location.id == item_in.location_id).first()
        if not location:
            raise HTTPException(status_code=400, detail="Указанная локация не найдена")

    if item_in.responsible_id:
        responsible = db.query(models.User).filter(models.User.id == item_in.responsible_id).first()
        if not responsible:
            raise HTTPException(status_code=400, detail="Указанный ответственный не найден")

    new_item = models.InventoryItem(**item_in.dict())
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item


@router.put(
    "/{item_id}",
    response_model=schemas.ItemOut,
    summary="Обновить данные существующего ТМЦ"
)
def update_item(item_id: int, item_in: schemas.ItemUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Обновляет данные объекта ТМЦ.
    Можно изменить любые поля: статус, бренд, ответственного и т.д.
    """
    db_item = db.query(models.InventoryItem).filter(models.InventoryItem.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="ТМЦ не найден")

    for key, value in item_in.dict(exclude_unset=True).items():
        setattr(db_item, key, value)

    db.commit()
    db.refresh(db_item)
    return db_item


@router.delete(
    "/{item_id}",
    status_code=status.HTTP_200_OK,
    summary="Удалить объект ТМЦ"
)
def delete_item(item_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Удаляет объект ТМЦ из базы данных по его ID.
    Возвращает сообщение об успешном удалении.
    """
    db_item = db.query(models.InventoryItem).filter(models.InventoryItem.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="ТМЦ не найден")

    db.delete(db_item)
    db.commit()
    return {"message": f"ТМЦ (ID {item_id}) успешно удалён"}