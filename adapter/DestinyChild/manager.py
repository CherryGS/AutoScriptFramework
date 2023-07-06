from module.manager import TemplateTaskManager
from utility.priority_queue import PriorityQueue
from utility.ftime import now

from .config import DestinyChildConfig
from .task import DestinyChildTask


class DestinyChildManager(TemplateTaskManager):
    def __init__(self, inst: str = "ds", **kwargs) -> None:
        super().__init__(**kwargs)
        self.config = self.read_config(inst)
        self.task: DestinyChildTask | None = None  # 当前正在执行的 Task
        self.nxtq: list[DestinyChildTask] = list()
        self.queue = PriorityQueue[DestinyChildTask]()

    def reload(self):
        raise NotImplementedError

    def read_config(self, inst: str) -> DestinyChildConfig:
        raise NotImplementedError

    def reload_task(self):
        self.task = None
        self.nxtq.clear()
        self.queue.clear()
        for i in self.config.cont:
            self.queue.insert(DestinyChildTask(i))
        while not self.queue.empty():
            if self.queue.top().config.nxt <= now():
                self.nxtq.append(self.queue.pop())
        if self.nxtq:
            self.task = self.nxtq.pop()

    def run(self):
        self.reload_task()
        while self.task is not None:
            self.task.run()
