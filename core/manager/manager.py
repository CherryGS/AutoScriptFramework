import time
from dataclasses import dataclass
from multiprocessing import Pipe, Process, Queue
from multiprocessing.connection import PipeConnection
from pathlib import Path
from typing import Any, Callable, Type

from core.adapter import Adapter
from core.interface import *
from global_config import basic_config
from utility import getLogger

logger = getLogger()


class Worker:
    def __init__(
        self, Adapter: Type[Adapter], instance_name: str, instance_path: Path
    ) -> None:
        signal_pipe = Pipe()
        self.instance_name = instance_name
        self.instance_path = instance_path

        # ipc & adapter
        self.input_queue = Queue(-1)
        self.output_queue = Queue(-1)
        self.renderable_queue = Queue(-1)  # 与 `rich` 耦合
        self.ipc_args = (
            signal_pipe[1],
            self.input_queue,
            self.output_queue,
            self.renderable_queue,
        )

        self.adapter = Adapter(instance_name, instance_path, *self.ipc_args)
        self.process = Process(target=self.adapter.run, name=instance_name)

        # self
        self.signal_pipe = signal_pipe[0]
        self._close: bool = False

    # ipc tools

    def _send_close(self):
        self.signal_pipe.send(NeedClose())
        self.signal_pipe.send(None)  # 发送 None 当作关闭信息

    # main

    def start(self):
        logger.info(f"Instance '{self.instance_name}' will start")
        self.process.start()

    def is_alive(self):
        return self.process.is_alive()

    def close(self, force: bool = False, timeout: float | None = None):
        logger.info(
            f"Try to close instance '{self.instance_name}' with force '{force}' and timeout '{timeout}'"
        )
        self._close = True
        if force:
            logger.info(f"Instance '{self.instance_name}' will be terminated.")
            self.process.terminate()
        else:
            logger.info(f"Instance '{self.instance_name}' will close selfly.")
            self._send_close()

        self.clear(timeout=timeout)
        logger.info(f"Instance '{self.instance_name}' closed.")

    def clear(self, timeout: float | None):
        self.process.join(timeout=timeout)
        if self.process.is_alive():
            logger.info(
                f"Instance '{self.instance_name}' will be terminated because timeout."
            )
            self.process.terminate()
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
        try:
            fake_instance_path = Path(r"E:\CherryGS\Project\AutoScriptFramework\log")
            fake_Adapter = fake_get_adapter_by_instance_name(instance_name)
            worker = Worker(fake_Adapter, instance_name, fake_instance_path)
            self.workers[instance_name] = worker
            worker.start()
        except Exception as e:
            ...

    def close_instance(
        self, instance_name: str, force: bool = False, timeout: float | None = None
    ):
        if instance_name not in self.workers:
            raise ValueError()
        self.workers[instance_name].close(force)


manager = Manager()
