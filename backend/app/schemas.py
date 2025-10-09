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
    is_admin: bool
    model_config = ConfigDict(from_attributes=True)


# === TMC / Inventory ===
class TMCBase(BaseModel):
    name: str
    serial_number: Optional[str] = None
    brand: Optional[str] = None
    type: Optional[str] = None
    model: Optional[str] = None
    # location: Optional[str] = None
    location_id: Optional[int] = None

class TMCCreate(TMCBase):
    # дополнительные поля для создания можно добавить здесь
    pass

class TMCUpdate(BaseModel):
    name: Optional[str] = None
    serial_number: Optional[str] = None
    brand: Optional[str] = None
    type: Optional[str] = None
    model: Optional[str] = None
    status: Optional[str] = None
    responsible_id: Optional[int] = None
    # location: Optional[str] = None
    location_id: Optional[int] = None
    comment: Optional[str] = None

class TMCOut(TMCBase):
    id: int
    status: str
    responsible_id: Optional[int] = None
    comment: Optional[str] = None
    location_name: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

# === Locations ===
class LocationBase(BaseModel):
    location: str

class LocationCreate(LocationBase):
    pass  # здесь можно добавить поля для создания, если нужно

class LocationOut(LocationBase):
    id: int
    location: str

    model_config = ConfigDict(from_attributes=True)