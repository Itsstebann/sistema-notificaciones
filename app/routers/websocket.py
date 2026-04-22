from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.redis_client import redis_client
import asyncio
import json

router = APIRouter(tags=["WebSocket"])


@router.websocket("/ws/{usuario_id}")
async def websocket_endpoint(websocket: WebSocket, usuario_id: int):
    await websocket.accept()
    pubsub = redis_client.pubsub()
    pubsub.subscribe(f"notificaciones:{usuario_id}")

    try:
        while True:
            mensaje = pubsub.get_message(ignore_subscribe_messages=True)
            if mensaje:
                await websocket.send_text(mensaje["data"].decode("utf-8"))
            await asyncio.sleep(0.1)
    except WebSocketDisconnect:
        pubsub.unsubscribe(f"notificaciones:{usuario_id}")
