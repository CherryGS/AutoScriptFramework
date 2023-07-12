from contextlib import contextmanager
from fastapi import FastAPI
from .router import my_router, test_router
from .interface import InstanceMethod


@contextmanager
def lifespan(app: FastAPI):
    yield


app = FastAPI()
app.include_router(my_router)
app.include_router(test_router)


@app.post("/instance")
def instance_method(method: InstanceMethod):
    ...
