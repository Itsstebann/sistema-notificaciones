from pydantic import BaseModel
from datetime import datetime

class NotificacionCreate(BaseModel):
    titulo: str
    mensaje: str
    usuario_id: int

class NotificacionResponse(BaseModel):
    id: int
    titulo: str
    mensaje: str
    leida: bool
    creada_en: datetime
    usuario_id: int

    class Config:
        from_attributes = True
