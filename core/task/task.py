from utility import redatetime

from core.interface import *
from .step import BaseStep, BaseData


class BaseTask:
    def __init__(self, config: TaskConfig, step: BaseStep) -> None:
        self.finished = False
        self.config = config
        self.step = step
        self.data = BaseData()

    def run(self):
        data = self.data
        now = self.step
        enable = True
        while enable:
            enable = False
            data.now_level += 1
            now.run(data)
            for i, j in zip(now.nxt, now.nxt_logic):
                if j(data):
                    enable = True
                    now = i
                    break

    def __hash__(self) -> int:
        return hash(self.config.unique_id)


if __name__ == "__main__":
    now = redatetime.today()
