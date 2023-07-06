from datetime import datetime
from typing import Self

from .config import TaskConfig


class BaseTask:
    def __init__(self, config: TaskConfig) -> None:
        self.config = config

    def next_time(self):
        """
        该任务下一次的运行时间

        :raises NotImplementedError: _description_
        """
        raise NotImplementedError

    def __lt__(self, o: Self):
        return self.config.nxt < o.config.nxt


if __name__ == "__main__":
    now = datetime.today()
