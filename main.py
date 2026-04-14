import json
from contextlib import suppress
from pathlib import Path
from typing import Literal

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from pydantic import BaseModel, ValidationError


app = FastAPI(title="RideFlow AI Tracker")
INDEX_FILE = Path(__file__).with_name("index.html")


class LocationUpdate(BaseModel):
    user_id: str
    role: Literal["driver", "rider"]
    lat: float
    lng: float


class ConnectionManager:
    def __init__(self) -> None:
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket) -> None:
        # Step 1 of the WebSocket lifecycle:
        # accept the handshake and store the client so it can receive broadcasts.
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket) -> None:
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast_to_others(
        self, message: dict[str, str | float], sender: WebSocket
    ) -> None:
        disconnected_clients: list[WebSocket] = []

        # Step 3 of the lifecycle:
        # forward one user's location update to every other connected client.
        for connection in self.active_connections:
            if connection is sender:
                continue

            try:
                await connection.send_json(message)
            except Exception:
                # If a client is gone, mark it for cleanup so the server keeps running.
                disconnected_clients.append(connection)

        for connection in disconnected_clients:
            self.disconnect(connection)


manager = ConnectionManager()


@app.get("/")
async def serve_frontend() -> FileResponse:
    return FileResponse(INDEX_FILE)


@app.websocket("/ws/locations")
async def websocket_location_tracker(websocket: WebSocket) -> None:
    await manager.connect(websocket)

    try:
        while True:
            # Step 2 of the lifecycle:
            # wait for the next location message from this browser/client.
            raw_message = await websocket.receive_text()

            try:
                payload = LocationUpdate.model_validate(json.loads(raw_message))
            except (json.JSONDecodeError, ValidationError):
                await websocket.send_json(
                    {
                        "type": "error",
                        "message": (
                            "Expected JSON with user_id, role, lat, and lng fields."
                        ),
                    }
                )
                continue

            await manager.broadcast_to_others(payload.model_dump(), sender=websocket)

    except WebSocketDisconnect:
        # Final lifecycle step:
        # remove the client cleanly when the browser tab closes or loses connection.
        manager.disconnect(websocket)
    except Exception:
        manager.disconnect(websocket)
        with suppress(Exception):
            await websocket.close()
