from sqlalchemy import Boolean, Column, Integer, String, Enum, ForeignKey, Text
from sqlalchemy.orm import relationship
from .database import Base
import enum


class TMCStatus(str, enum.Enum):
    at_work = "В работе"
    in_repair = "В ремонте"
    issued = "Выдано"
    available = "Доступно"
    confirm = "Подтвердить ТМЦ"
    confirm_repair = "Подтвердить ремонт"


# === DEV MODEL: InventoryItem ===
class InventoryItem(Base):
    __tablename__ = "inventory_items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    serial_number = Column(String, unique=True, nullable=True)
    brand = Column(String, nullable=True)
    status = Column(Enum(TMCStatus), default=TMCStatus.confirm)

    # --- Ключ на пользователя ---
    responsible_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    # --- Ключ на локацию ---
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=True)

    # --- Человеко-читаемое название локации ---
    # location = Column(String, nullable=True)

    # --- Relationships ---
    responsible = relationship("User", back_populates="inventory_items")
    location_obj = relationship("Location", back_populates="inventory_items")


# === USERS ===
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)

    # связь с инвентарём (один-ко-многим)
    inventory_items = relationship("InventoryItem", back_populates="responsible")


# === LOCATIONS ===
class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    # связь с инвентарём
    inventory_items = relationship("InventoryItem", back_populates="location_obj")

    def __str__(self):
        return self.name
