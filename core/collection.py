from abc import ABCMeta
from typing import Any, Callable

from utility import PriorityQueue

from .interface import *


class IPCBase:
    def __init__(self) -> None:
        self.signal_queue_send = PriorityQueue[Signal]()
        self.signal_queue_receive = PriorityQueue[Signal]()
        self.signal_handler: dict[str, Callable[[Signal], Any]] = dict()
