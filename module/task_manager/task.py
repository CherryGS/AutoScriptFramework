from datetime import datetime

from .config import TemplateTaskConfig


class TemplateTask:
    def __init__(self, config: TemplateTaskConfig) -> None:
        self.config = config

    def next_time(self):
        """
        该任务下一次的运行时间

        Raises:
            NotImplementedError: _description_
        """
        raise NotImplementedError


if __name__ == "__main__":
    now = datetime.today()
