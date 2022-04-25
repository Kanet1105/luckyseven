from typing import Optional
from fastapi import FastAPI
from fastapi import WebSocket, WebSocketDisconnect
from pydantic import BaseModel
import nats


class ConnectionManager:
    def __init__(self):
        self.connections = {}

    async def onConnection(self, websocket: WebSocket, uid: str):
        if uid in self.connections:
            print("uid: {id} exists.".format(id=uid))
        else:
            await websocket.accept()
            self.connections[uid] = websocket
            print("-" * 50)
            print("A new connection has been made")
            print("uid: {id}".format(id=uid))
            print("socket: {sock}".format(sock=self.connections[uid]))

    def onDisconnection(self, uid: str):
        print("-" * 50)
        print("A client disconnected")
        print("uid: {id}".format(id=uid))
        print("socket: {sock}".format(sock=self.connections[uid]))
        del self.connections[uid]

    async def publish(self, uid: str):
        data = self.connections[uid].receive_json()
        print(data)


class MinimalData(BaseModel):
    index: int
    value0: Optional[list] = None
    value1: Optional[str] = None
    value2: Optional[int] = None
    value3: Optional[float] = None


app = FastAPI()
print("Starting the api server.")
manager = ConnectionManager()
print("Initializing the connection manager.")


@app.get("/")
async def root():
    return {"websocket uri": "/stream/$uid"}


@app.post("/post/")
async def minimalPublish(data: MinimalData):
    return data


@app.websocket("/websocket/{uid}")
async def streamPublish(websocket: WebSocket, uid: str):
    await manager.onConnection(websocket, uid)
    try:
        while True:
            await manager.publish(uid)
    except WebSocketDisconnect:
        manager.onDisconnection(uid)
