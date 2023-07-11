from dataclasses import dataclass
from multiprocessing import Pipe, Process, Queue
from multiprocessing.connection import PipeConnection
from pathlib import Path
from typing import Any, Callable, Type

from global_config import basic_config
from core.adapter import Adapter
from core.interface import *


class Worker:
    def __init__(
        self, Adapter: Type[Adapter], instance_name: str, instance_path: Path
    ) -> None:
        signal_pipe = Pipe()

        # ipc & adapter
        self.input_queue = Queue()
        self.output_queue = Queue()
        self.renderable_queue = Queue()  # 与 `rich` 耦合
        self.ipc_args = (
            signal_pipe[1],
            self.input_queue,
            self.output_queue,
            self.renderable_queue,
        )
        self.adapter = Adapter(instance_name, instance_path, *self.ipc_args)
        self.process = Process(target=self.adapter.run)

        # self
        self.signal_pipe = signal_pipe[0]
        self._close: bool = False

    # ipc tools

    def _send_close(self):
        self.signal_pipe.send(NeedClose())

    # main

    def start(self):
        self.process.start()

    def is_alive(self):
        return self.process.is_alive()

    def close(self, force: bool = False):
        self._close = True
        if force:
            self.process.terminate()
        else:
            self._send_close()

        self.clear()

    def clear(self, timeout: int = 5):
        self.process.join(timeout)
        self.signal_pipe.close()
        self.input_queue.close()
        self.output_queue.close()
        self.renderable_queue.close()
        self.process.close()


def fake_get_adapter_by_instance_name(instance_name: str) -> Type[Adapter]:
    return Adapter


class Manager:
    def __init__(self) -> None:
        self.workers: dict[str, Worker] = dict()

    def create_instance(self, instance_name: str, adapter: Adapter):
        adapter.create_new_instance(instance_name, basic_config.instance_folder)

    def run_instance(self, instance_name: str):
        fake_instance_path = Path(r"E:\CherryGS\Project\AutoScriptFramework\log")
        fake_Adapter = fake_get_adapter_by_instance_name(instance_name)
        worker = Worker(fake_Adapter, instance_name, fake_instance_path)
        self.workers[instance_name] = worker
        worker.start()

    def close_instance(self, instance_name: str, force: bool = False):
        if instance_name not in self.workers:
            raise ValueError()
        self.workers[instance_name].close(force)


manager = Manager()
