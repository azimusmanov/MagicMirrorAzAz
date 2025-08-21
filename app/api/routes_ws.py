from fastapi import APIRouter, WebSocket

router = APIRouter()

@router.websocket("/ws/events")
async def events_ws(ws: WebSocket):
    # Accept connection from browser
    await ws.accept()
    # Stage 0: just send a confirmation message
    await ws.send_text("connected")
    # Close connection (later keep it open to stream events)
    await ws.close()
