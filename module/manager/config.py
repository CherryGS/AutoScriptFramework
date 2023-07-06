from pydantic import BaseModel
from rich import print

from module.task import GeneralConfig, TaskConfig


class TemplateInstanceConfig(BaseModel):
    idx: str  # 该实例的标识号 , 一般与实例名称相同
    cont: list[TaskConfig]
    conf: list[GeneralConfig]
