from pydantic import BaseModel
from rich import print

from core.task import GeneralConfig, TaskConfig


class InstanceConfig(BaseModel):
    name: str  # 实例名称
    unique_id: str | int  # 该实例的标识号 , 一般与实例名称相同
    context: list[TaskConfig]
    config: list[GeneralConfig]
