from sqlalchemy import Boolean, Column, Integer, String, Enum, ForeignKey, Text
from sqlalchemy.orm import relationship
from .database import Base

class TMC(Base):
    __tablename__ = "tmc"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    serial_number = Column(String, unique=True, index=True, nullable=True)
    brand = Column(String, index=True)
    type = Column(String)
    model = Column(String)
    status = Column(Enum(TMCStatus), default=TMCStatus.confirm)
    responsible_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=True)
    location = Column(String, nullable=True) # Текстовое поле для локации DEV
    # location = Column(Enum(LocationEnum), nullable=True)
    comment = Column(Text, nullable=True)

    responsible = relationship("User", back_populates="tmc_items")
    location_obj = relationship("Location", back_populates="tmc_items")