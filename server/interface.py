from pydantic import BaseModel
from enum import StrEnum


class InstanceMethodType(StrEnum):
    start = "start"
    kill = "kill"
    restart = "restart"
    list = "list"


class InstanceMethod(BaseModel):
    type: InstanceMethodType
    name: str


class InstanceMethodResult(BaseModel):
    ...
