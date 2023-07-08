from utility.priority_queue import PriorityQueue
from typing import Self
from ..executor import ThreadPoolExecutor
from ..task import BaseTask


class Scheduler:
    # TODO : Single Pattern
    def __init__(self, tasks: list[BaseTask] = []) -> None:
        self.task: BaseTask | None = None
        self.task_hash: set[BaseTask] = set()
        self.task_queue = PriorityQueue[BaseTask]()
        self.reload_task(tasks)

        self.close = False

    def _assign_task(self, task: BaseTask):
        if task in self.task_hash:
            return

    def reload_task(self, tasks: list[BaseTask]):
        self.task_queue.clear()
        self.task_hash.clear()
        for task in tasks:
            if task not in self.task_hash:
                self.task_queue.insert(task)
                self.task_hash.add(task)

    def run(self):
        while not self.close:
            if self.task and self.task.finished:
                self._assign_task(self.task)
                self.task = None
            if not self.task and not self.task_queue.empty():
                self.task = self.task_queue.pop()
            if self.task:
                self.task.run()
