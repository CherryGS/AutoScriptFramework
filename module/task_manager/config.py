from datetime import datetime
from enum import Enum
from typing import Literal

from pydantic import BaseModel
from rich import print


class SettingType(str, Enum):
    choice = "choice"
    itext = "inline_text"
    btext = "block_text"
    cbox = "check_box"


class _TemplateSetting(BaseModel):
    type: SettingType  # 类型
    name: str  # 设置名称
    text: datetime  # 设置默认文本
    mutable: bool = True  # 该设置是否可变
    Description: list[str] = []  # 设置说明


class TemplateNumSetting(_TemplateSetting):
    text: int | float  # 设置默认文本


class TemplateStrSetting(_TemplateSetting):
    text: str  # 设置默认文本


class TemplateDateSetting(_TemplateSetting):
    text: datetime  # 日期


class TemplateCheckSetting(_TemplateSetting):
    text: bool  # 是否确定


class TemplateChoiceSetting(_TemplateSetting):
    text: int  # 选择第几个
    args: list[str]  # 选项


TemplateSetting = (
    TemplateNumSetting
    | TemplateStrSetting
    | TemplateDateSetting
    | TemplateCheckSetting
    | TemplateChoiceSetting
)


class TemplateBlockConfig(BaseModel):
    title: str  # 名称
    cont: list[TemplateSetting]
    description: list[str] = []  # 描述


class TemplateGeneralConfig(BaseModel):
    title: str  # 名称
    cont: list[TemplateBlockConfig]


class TemplateTaskConfig(TemplateGeneralConfig):
    disable: bool = True  # 该任务是否启用
    nxt: datetime  # 任务下次执行时间


class TemplateInstanceConfig(BaseModel):
    idx: str  # 该实例的标识号 , 一般与实例名称相同
    cont: list[TemplateTaskConfig]
    conf: list[TemplateGeneralConfig]
