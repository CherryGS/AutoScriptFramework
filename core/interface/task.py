from typing import Annotated
from utility import redatetime, Annodate
from enum import IntEnum

from pydantic import BaseModel, field_validator, ConfigDict


class ScopeType(IntEnum):
    inline = 0
    block = 1


class SettingType(IntEnum):
    check = 0
    text = 1
    choice = 2


base = str | int | bool


class _Setting(BaseModel):
    scope: ScopeType
    type: SettingType  # 类型
    name: str  # 设置名称
    mutable: bool = True  # 该设置是否可变
    description: list[str] = []  # 设置说明
    args: list[str] = []  # choice 的参数

    model_config = ConfigDict(extra="forbid")


class InlineSetting(_Setting):
    scope: ScopeType = ScopeType.inline
    value: base

    @field_validator("scope")
    def validate_scope(cls, v):
        if v != ScopeType.inline:
            raise ValueError(
                "InlineSetting must let the value of 'scope' to be the same as 'ScopeType.inline'."
            )
        return v


class BlockSetting(_Setting):
    scope: ScopeType = ScopeType.block
    value: list[base]

    @field_validator("scope")
    def validate_scope(cls, v):
        if v != ScopeType.block:
            raise ValueError(
                "BlockSetting must let the value of 'scope' to be the same as 'ScopeType.block'."
            )
        return v


Setting = InlineSetting | BlockSetting


class BlockConfig(BaseModel):
    name: str  # 名称
    unique_id: str | int
    content: list[Setting]
    description: list[str] = []  # 描述


class GeneralConfig(BaseModel):
    name: str  # 名称
    unique_id: str | int
    content: list[BlockConfig]
    description: list[str] = []  # 描述


class TaskConfig(GeneralConfig):
    disable: bool = True  # 该任务是否启用
    nxt: Annodate  # 任务下次执行时间
