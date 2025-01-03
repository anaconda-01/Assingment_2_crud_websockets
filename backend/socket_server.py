import socketio
import asyncio
origins = [
    "http://localhost:8000",  
    "http://127.0.0.1:8000",  
]
sio=socketio.AsyncServer(async_mode="asgi",cors_allowed_origins=origins)
counter=0
@sio.event
async def connect(sid,environ):
    global counter
    counter+=1
    await sio.emit("counter",counter,to=sid)
@sio.event
async def disconnect(sid):
    global counter
    counter-=1
    await sio.emit("counter",counter,to=sid)