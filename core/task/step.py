from distutils.log import Log
from itertools import chain
from typing import Any, Self, Awaitable, Callable, Type
from pydantic import BaseModel, ConfigDict


class _DataMixin(BaseModel):
    # 默认添加额外项
    model_config = ConfigDict(extra="allow")


class BaseData(_DataMixin):
    """
    维护在 Step DAG 上转移时获得的部分信息
    """

    now_name: str = ""  # 该 step 名字
    now_loop: int = 0  # 现在在第几次循环
    now_level: int = 0  # 现在在递归第几层


class Logic:
    def __init__(self, always_true: bool = False) -> None:
        self.always_true = always_true

    def __call__(self, ctx: BaseData) -> Any:
        return self.always_true


class BaseStep:
    """
    所有的 Step 应该构成 DAG , 并且在考虑 Logic 的情况下从起点开始应该至多只有一条有效路径
    """

    amount = 0

    def __init__(self) -> None:
        self.loop_max = 1
        self.loop_logic = Logic(always_true=True)
        self.nxt: list[Self] = list()
        self.nxt_logic: list[Logic] = list()
        self.name: str = f"{self.__class__.amount}"
        self.__class__.amount += 1

    def _add_next(self, o: Self, f: Logic):
        self.nxt.append(o)
        self.nxt_logic.append(f)

    def _copy(self):
        r = self.__class__()
        r.loop_max = self.loop_max
        r.loop_logic = self.loop_logic
        map(r.nxt.append, self.nxt)
        map(r.nxt_logic.append, self.nxt_logic)
        return r

    def set_loop(self, c: int, f: Logic):
        assert c > 0
        r = self._copy()
        r.loop_max = c
        r.loop_logic = f
        return r

    def add_next(self, o: Self, f: Logic):
        r = self._copy()
        r._add_next(o, f)
        return r

    def _run(self, ctx: BaseData):
        raise NotImplementedError

    def run(self, ctx: BaseData):
        ctx.now_name = self.name
        for loop in range(self.loop_max):
            ctx.now_loop = loop + 1
            if not self.loop_logic(ctx):
                break
            self._run(ctx)
