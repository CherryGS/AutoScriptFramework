from dataclasses import dataclass
from multiprocessing import Pipe, Process, Queue
from multiprocessing.connection import PipeConnection
from pathlib import Path
from typing import Any

from core.adapter import Adapter
from core.adapter.channel import *

from ..config import asf_cofig


@dataclass(eq=False, slots=True)
class WorkerCollection:
    process: Process
    pipe: PipeConnection
    inque: Queue
    outque: Queue
    logque: Queue


class Manager:
    def __init__(self) -> None:
        self.worker_collections: dict[str, WorkerCollection] = dict()
        self.all_instance: dict[str, Any] = dict()

    def _get_all_instance(self):
        return {"NO": "NotImplement"}

    def get_all_instance(self):
        if not self.all_instance:
            self.all_instance = self._get_all_instance()
        return self.all_instance

    def create_instance(self, instance_name: str, adapter: Adapter):
        adapter.create_new_instance(instance_name, asf_cofig.instance_folder)

    def run_instance(self, instance_name: str):
        # some code to get adapter worker
        path = Path()
        conns = Pipe()
        inque = Queue()
        outque = Queue()
        logque = Queue()

        worker = Adapter(path=path, pipe=conns[1], iq=inque, oq=outque, lq=logque)
        run_args = ()
        run_kwargs = {}
        process = Process(target=worker.run, args=run_args, kwargs=run_kwargs)

        self.worker_collections[instance_name] = WorkerCollection(
            process=process, pipe=conns[0], inque=inque, outque=outque, logque=logque
        )
        process.start()

    def close_instance(self, instance_name: str):
        p = self.worker_collections[instance_name]
        p.inque.close()
        p.outque.close()


manager = Manager()
