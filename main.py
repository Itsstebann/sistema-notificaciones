from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine
from app.models import Usuario, Notificacion
from app.database import Base
from app.routers import auth_router, notificaciones_router, websocket_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Sistema de Notificaciones en Tiempo Real",
    description="API con WebSockets y Redis para notificaciones instantáneas",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(notificaciones_router)
app.include_router(websocket_router)


@app.get("/", tags=["General"])
def root():
    return {"mensaje": "Sistema de Notificaciones activo"}
