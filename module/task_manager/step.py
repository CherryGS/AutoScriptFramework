from typing import Self


class TemplateStep:
    def __init__(self, time_lim: int = 2, **kwargs) -> None:
        self.time_lim = time_lim  # 该步骤的执行时间上限
        self.finish: bool = False
        for i, j in kwargs.items():
            self.__setattr__(i, j)

    def run(self):
        # Todo : Add time limit
        raise NotImplementedError

    def is_finish(self) -> bool:
        return self.finish

    def when_finish(self, o: Self):
        raise NotImplementedError
