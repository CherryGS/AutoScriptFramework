from enum import Enum, IntEnum, StrEnum
from typing import Any, Self, Type

from pydantic import BaseModel, Field

from utility import Annodate, redatetime


class SignalType(StrEnum):
    response = "response"  # 对上一个获得信号的响应信号
    need_close = "need_close"  # 进程需要结束
    heartbeat = "heartbeat"  # 心跳包


class Level(IntEnum):
    """
    使用 `IntEnum` 类使得 level 可以与整数比较
    """

    heartbeat = 1000
    need_close = 900


class Signal(BaseModel):
    """
    小根堆中的排序规则 :
    `priority` 相同时 , 时间更早的排在前面
    否则 `priority` 更大的排在前面
    """

    type: SignalType
    priority: Level | int
    body: Any | None = None
    create_time: Annodate = Field(default_factory=redatetime.now)

    def __lt__(self, o: Self):
        return (
            self.create_time < o.create_time
            if self.priority == o.priority
            else self.priority > o.priority
        )


class NeedClose(Signal):
    type: SignalType = SignalType.need_close
    priority: Level = Level.need_close


class Heartbeat(Signal):
    type: SignalType = SignalType.heartbeat
    priority: Level = Level.heartbeat


class Response(Signal):
    type: SignalType = SignalType.response
    body: Signal


class HeartbeatResponse(Response):
    priority: Level = Level.heartbeat
    body: Heartbeat


class MessageType(StrEnum):
    heart_beat = "heart_beat"


class Message(BaseModel):
    type: MessageType
    body: Any | None = None
    create_time: Annodate = Field(default_factory=redatetime.now)


if __name__ == "__main__":
    print(f"{Level.need_close}")
