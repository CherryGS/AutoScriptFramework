from fastapi import APIRouter, WebSocket
from utility import getLogger

test_router = APIRouter()


@test_router.get("/test/1")
def test_raise_exception():
    raise Exception("Test raise exception.")


@test_router.get("/test/2")
def test_raise_exception_log():
    getLogger("uvicorn").exception(Exception("Test raise exception."))
