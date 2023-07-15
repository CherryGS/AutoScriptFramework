from pathlib import Path
from pydantic import BaseModel

from .task import GeneralConfig, TaskConfig


class InstanceConfig(BaseModel):
    name: str  # 实例名称 , 唯一
    adapter_id: int  # 相关联的 adapter 的 id


class AdapterConfig(BaseModel):
    unique_id: int  # 唯一识别id
    name: str  # 用来展示
    task_pre_folder: Path = Path(".")  # 在相应实例文件夹下存放 task 的文件夹 , 默认是实例文件夹根目录
    task_files: list[str]  # 在相应实例文件夹下存放的需要载入的 task 的名字 , 包含 `.json`
