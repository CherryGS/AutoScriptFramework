from fastapi import APIRouter, WebSocket
from manager import manager

my_router = APIRouter()


@my_router.get("/workers_info")
def get_workers_info():
    pass


@my_router.get("/status/{worker_id}")
def get_worker_status(worker_id: str):
    pass


@my_router.websocket("/log/ws")
async def ws_main_log(ws: WebSocket):
    await ws.accept()
    while True:
        await ws.send_text("some html")


@my_router.websocket("/log/{worker_id}/ws")
async def ws_worker_log(ws: WebSocket, worker_id: str):
    await ws.accept()
    while True:
        data = await ws.receive_text()
        await ws.send_text("some html")


@my_router.get("/run/{instance_name}")
def run_instance(instance_name: str):
    # TODO : 阻塞监听成功信号
    manager.run_instance(instance_name)
    return {"status": "OK"}


@my_router.get("/close/{instance_name}")
def close_instance(instance_name: str):
    # TODO : 阻塞监听成功信号
    manager.close_instance(instance_name)
    return {"status": "OK"}
