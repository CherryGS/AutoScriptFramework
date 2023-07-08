from datetime import datetime
from typing import Any, Self
from pydantic import BaseModel, Field
from enum import Enum, IntEnum


class SignalType(Enum, str):
    resp = "response"  # 代表子进程的响应信号 , 特殊
    close = "process_need_close"  # 进程需要关闭
    info = "get_worker_info"  # 获取 worker 信息
    retask = "reload_task"  # 重载任务


class level(IntEnum):
    close = 1000
    retask = 900
    info = 0


class Signal(BaseModel):
    type: SignalType
    priority: level
    key: str | None = None
    create_time: datetime = Field(default_factory=datetime.now)

    def __lt__(self, o: Self):
        return (
            self.create_time < o.create_time
            if self.priority == o.priority
            else self.priority > o.priority
        )


class SignalResp(BaseModel):
    type: SignalType = SignalType.resp
    signal_type: SignalType
    status: bool
    key: str | None = None
    body: str | None = None
    create_time: datetime = Field(default_factory=datetime.now)


class MsgType(Enum, str):
    heart = "heart_beat"  # 心跳包
    info = "worker_info"  # worker 信息


class WorkerInfo(BaseModel):
    pass


class _Message(BaseModel):
    type: MsgType | None = None
    create_time: datetime = Field(default_factory=datetime.now)


class HeartbeatMsg(_Message):
    type: MsgType = MsgType.heart


class WorkerInfoMsg(_Message):
    type: MsgType = MsgType.info
    body: WorkerInfo
