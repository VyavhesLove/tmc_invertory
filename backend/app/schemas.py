# backend/app/schemas.py
from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict

# === Users ===
class UserBase(BaseModel):
    username: str
    email: Optional[EmailStr] = None

class UserCreate(UserBase):
    password: str
    is_admin: bool = False

class UserOut(UserBase):
    id: int
    username: str
    model_config = ConfigDict(from_attributes=True)

class UserIsAdmin(BaseModel):
    is_admin: bool


# === Inventory ===
class ItemBase(BaseModel):
    name: str
    serial_number: Optional[str] = None
    brand: Optional[str] = None
    status: Optional[str] = None
    responsible_id: Optional[int] = None
    location_id: Optional[int] = None
    # comment: Optional[str] = None

class ItemCreate(ItemBase):
    """Схема для создания нового ТМЦ"""
    pass

class ItemUpdate(ItemBase):
    """Схема для обновления существующего ТМЦ"""
    pass

class ItemOut(ItemBase):
    """Выходная схема для отображения ТМЦ в интерфейсе"""
    id: int
    location_name: Optional[str] = None
    responsible_name: Optional[str] = None

    class Config:
        orm_mode = True

# === Locations ===
class LocationBase(BaseModel):
    location: str

class LocationCreate(LocationBase):
    pass  # здесь можно добавить поля для создания, если нужно

class LocationOut(LocationBase):
    id: int
    location: str

    model_config = ConfigDict(from_attributes=True)