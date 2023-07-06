from datetime import datetime
from enum import IntEnum

from pydantic import BaseModel


class SettingType(IntEnum):
    choice = 0
    inline_text = 1
    block_text = 2
    check_box = 3


class _Setting(BaseModel):
    type: SettingType  # 类型
    name: str  # 设置名称
    mutable: bool = True  # 该设置是否可变
    Description: list[str] = []  # 设置说明


class NumSetting(_Setting):
    value: int | float  # 默认值


class StrSetting(_Setting):
    value: str  # 默认值


class DateSetting(_Setting):
    value: datetime  # 默认值-日期


class CheckboxSetting(_Setting):
    value: bool  # 默认值-是否确定


class ChoiceSetting(_Setting):
    value: int  # 默认值-选择第几个
    args: list[str]  # 选项


Setting = NumSetting | StrSetting | DateSetting | CheckboxSetting | ChoiceSetting


class BlockConfig(BaseModel):
    title: str  # 名称
    cont: list[Setting]
    description: list[str] = []  # 描述


class GeneralConfig(BaseModel):
    title: str  # 名称
    cont: list[BlockConfig]


class TaskConfig(GeneralConfig):
    disable: bool = True  # 该任务是否启用
    nxt: datetime  # 任务下次执行时间
