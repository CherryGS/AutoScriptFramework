import time
from multiprocessing import Pipe, Process, Queue
from multiprocessing.connection import PipeConnection
from pathlib import Path
from typing import Callable

from core.task.task import BaseTask
from utility.priority_queue import PriorityQueue

from ..executor import ThreadPoolExecutor
from ..scheduler import Scheduler
from .channel import *


class Adapter:
    def __init__(
        self,
        path: Path,
        pipe: PipeConnection,
        iq: Queue,
        oq: Queue,
        lq: Queue,
        name: str = "Default Adapter",
    ) -> None:
        self.name = name
        self.path = path
        self.pipe = pipe
        self.iq = iq
        self.oq = oq
        self.lq = lq

        self.heart_beat_interval = 0.2
        self.need_send_log = True
        self.close = False

        self.signal = None
        self.signal_queue = PriorityQueue[Signal]()
        self.signal_handler: dict[str, Callable[[Self, Signal], Any]] = dict()

        self.signal_handler[SignalType.close] = __close
        self.signal_handler[SignalType.info] = __get_worker_info
        self.signal_handler[SignalType.retask] = __reload_tasks

        self.sche = Scheduler()
        self.sche.reload_task(self.get_task())

    def _listen_signal(self):
        while not self.close:
            if not self.signal:
                recv = self.pipe.recv()
                self.signal = Signal(**recv)

    def _response_signal(self):
        o = self.signal
        while not self.close:
            if o:
                self.signal_queue.insert(o)
                resp = SignalResp(
                    signal_type=o.type,
                    status=True,
                    key=o.key,
                    body="Queued",
                )
                self.pipe.send(resp)
                self.signal = None

    def _send_log(self):
        while not self.close and self.need_send_log:
            log = ""
            self.lq.put(log)

    def _send_heart_beat(self):
        while not self.close:
            time.sleep(self.heart_beat_interval)
            msg = HeartbeatMsg()
            self.oq.put(msg)

    def _solve_signal(self):
        while not self.close:
            while not self.signal_queue.empty():
                s = self.signal_queue.pop()
                self.signal_handler[s.type](self, s)

    def run(self):
        with ThreadPoolExecutor() as exec:
            exec.submit(self._listen_signal)
            exec.submit(self._response_signal)
            exec.submit(self._send_log)
            exec.submit(self._send_heart_beat)
            exec.submit(self.sche.run)

    def get_task(self):
        return []

    def create_new_instance(self, name: str, folder: Path):
        pass


def __reload_tasks(self: Adapter, s: Signal):
    self.sche.reload_task(self.get_task())


def __close(self: Adapter, s: Signal):
    self.close = True


def __get_worker_info(self: Adapter, s: Signal):
    pass
