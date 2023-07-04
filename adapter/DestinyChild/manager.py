from module.task_manager.manager import TemplateTaskManager

from .config import DestinyChildConfig
from .task import DestinyChildTask


class DestinyChildManager(TemplateTaskManager):
    def __init__(self, inst: str = "ds", **kwargs) -> None:
        super().__init__(**kwargs)
        self.config = self.read_config(inst)
        self.task: DestinyChildTask | None = None
        self.nxt: list[DestinyChildTask] = list()
        self.queue = None

    def reload(self):
        raise NotImplementedError

    def read_config(self, inst: str) -> DestinyChildConfig:
        raise NotImplementedError

    def load_task(self):
        res = list()
        for i in self.config.cont:
            res.append(DestinyChildTask(i))
        self.tasks = res

    def run(self):
        self.load_task()
