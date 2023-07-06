from datetime import datetime
from enum import IntEnum

from pydantic import BaseModel


class SettingType(IntEnum):
    choice = 0
    inline_text = 1
    block_text = 2
    check_box = 3


class _TemplateSetting(BaseModel):
    type: SettingType  # 类型
    name: str  # 设置名称
    mutable: bool = True  # 该设置是否可变
    Description: list[str] = []  # 设置说明


class TemplateNumSetting(_TemplateSetting):
    value: int | float  # 默认值


class TemplateStrSetting(_TemplateSetting):
    value: str  # 默认值


class TemplateDateSetting(_TemplateSetting):
    value: datetime  # 默认值-日期


class TemplateCheckSetting(_TemplateSetting):
    value: bool  # 默认值-是否确定


class TemplateChoiceSetting(_TemplateSetting):
    value: int  # 默认值-选择第几个
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
