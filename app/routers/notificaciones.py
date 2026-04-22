from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.notificacion import Notificacion
from app.models.usuario import Usuario
from app.schemas.notificacion import NotificacionCreate, NotificacionResponse
from app.routers.auth import get_current_user
from app.redis_client import redis_client
import json

router = APIRouter(prefix="/notificaciones", tags=["Notificaciones"])


@router.post("/", response_model=NotificacionResponse)
def crear_notificacion(notif: NotificacionCreate, db: Session = Depends(get_db), usuario=Depends(get_current_user)):
    usuario_destino = db.query(Usuario).filter(
        Usuario.id == notif.usuario_id).first()
    if not usuario_destino:
        raise HTTPException(
            status_code=404, detail="Usuario destino no encontrado")

    nueva = Notificacion(**notif.model_dump())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)

    redis_client.publish(f"notificaciones:{notif.usuario_id}", json.dumps({
        "id": nueva.id,
        "titulo": nueva.titulo,
        "mensaje": nueva.mensaje,
        "creada_en": nueva.creada_en.isoformat()
    }))

    return nueva


@router.get("/", response_model=list[NotificacionResponse])
def mis_notificaciones(db: Session = Depends(get_db), usuario=Depends(get_current_user)):
    return db.query(Notificacion).filter(Notificacion.usuario_id == usuario.id).all()


@router.patch("/{notif_id}/leer", response_model=NotificacionResponse)
def marcar_leida(notif_id: int, db: Session = Depends(get_db), usuario=Depends(get_current_user)):
    notif = db.query(Notificacion).filter(
        Notificacion.id == notif_id,
        Notificacion.usuario_id == usuario.id
    ).first()
    if not notif:
        raise HTTPException(
            status_code=404, detail="Notificación no encontrada")
    notif.leida = True
    db.commit()
    db.refresh(notif)
    return notif
