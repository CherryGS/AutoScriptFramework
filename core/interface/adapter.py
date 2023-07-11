from pathlib import Path
from pydantic import BaseModel

from .task import GeneralConfig, TaskConfig


class InstanceConfig(BaseModel):
    name: str  # 实例名称
    unique_id: str | int  # 该实例的标识号 , 一般与实例名称相同
    context: list[TaskConfig]
    config: list[GeneralConfig]


class _AdapterConfig(BaseModel):
    unique_id: int  # 唯一识别id
    name: str  # 用来展示


class AdapterConfig(_AdapterConfig):
    task_file: Path
