# backend/app/crud.py
from sqlalchemy.orm import Session
from . import models, schemas

# --- USERS ---
def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user_in: schemas.UserCreate, hashed_password: str):
    db_user = models.User(
        username=user_in.username,
        email=user_in.email,
        hashed_password=hashed_password,
        is_admin=user_in.is_admin
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# --- INVENTORY ---
def get_all_items(db: Session):
    return db.query(models.InventoryItem).all()

def get_item(db: Session, item_id: int):
    return db.query(models.InventoryItem).filter(models.InventoryItem.id == item_id).first()

def create_item(db: Session, item_data: dict):
    new_item = models.InventoryItem(**item_data)
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item

def update_item(db: Session, item_id: int, item_data: dict):
    item = get_item(db, item_id)
    if not item:
        return None
    for key, value in item_data.items():
        setattr(item, key, value)
    db.commit()
    db.refresh(item)
    return item

def delete_item(db: Session, item_id: int):
    item = get_item(db, item_id)
    if not item:
        return None
    db.delete(item)
    db.commit()
    return item

# --- LOCATIONS ---
def get_all_locations(db: Session):
    return db.query(models.Location).all()
