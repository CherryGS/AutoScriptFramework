from contextlib import contextmanager
from fastapi import FastAPI
from manager import manager
from .router import my_router


@contextmanager
def lifespan(app: FastAPI):
    yield


app = FastAPI()
app.include_router(my_router)
