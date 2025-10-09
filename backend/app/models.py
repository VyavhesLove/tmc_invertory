from sqlalchemy import Boolean, Column, Integer, String, Enum, ForeignKey, Text
from sqlalchemy.orm import relationship
from .database import Base
import enum
# from enum import IntEnum

class TMCStatus(str, enum.Enum):
    at_work = "В работе"
    in_repair = "В ремонте"
    issued = "Выдано"
    available = "Доступно"
    confirm = "Подтвердить ТМЦ"
    confirm_repair = "Подтвердить ремонт"

# DEV
class InventoryItem(Base):
    __tablename__ = "inventory_items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    serial_number = Column(String, unique=True, nullable=True)
    brand = Column(String, nullable=True)
    status = Column(Enum(TMCStatus), default=TMCStatus.confirm)
    responsible = Column(String, nullable=True)
    location = Column(String, nullable=True)
    location_id = Column(Integer, nullable=True)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True) # (Integer, default=1)
    is_admin = Column(Boolean, default=False) # (Integer, default=0)

    tmc_items = relationship("TMC", back_populates="responsible")

class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    #location = Column(Enum(LocationEnum), unique=True, index=True, nullable=False)
    name = Column(String, unique=True, nullable=False)

    # Связь с таблицей InventoryItem / TMC (один ко многим)
    tmc_items = relationship("TMC", back_populates="location_obj")

    # При отладке или в логах print(location_obj) покажет "Кампус", а не <Location object at ...>
    def __str__(self):
        return self.name