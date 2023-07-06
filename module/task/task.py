from datetime import datetime
from typing import Self

from .config import TemplateTaskConfig


class BaseTask:
    """
    默认以下次执行时间为 key 比较大小
    """

    def __init__(self, config: TemplateTaskConfig) -> None:
        self.config = config

    def next_time(self):
        """
        该任务下一次的运行时间

        Raises:
            NotImplementedError: _description_
        """
        raise NotImplementedError

    def __lt__(self, o: Self):
        return self.config.nxt < o.config.nxt


if __name__ == "__main__":
    now = datetime.today()
