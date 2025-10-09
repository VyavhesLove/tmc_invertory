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