import logging
import time
from datetime import datetime
from multiprocessing import Pipe, Process, Queue
from multiprocessing.connection import PipeConnection
from pathlib import Path
from typing import Any, Callable, Self

from rich import print
from rich.console import Console

from utility import redatetime
from utility.logger import (
    RichCallbackHandler,
    RichFileHandler,
    file_formatter,
    getLogger,
    hook_exception,
    initialize_logger,
)
from utility.priority_queue import PriorityQueue

from ..executor import ThreadPoolExecutor
from ..interface import *
from ..scheduler import Scheduler

logger = getLogger()


class Adapter:
    # TODO: 添加关闭时 log
    # TODO: 添加异常与异常处理
    def __init__(
        self,
        instance_name: str,
        instance_path: Path,
        signal_pipe: PipeConnection,
        input_queue: Queue,
        output_queue: Queue,
        renderable_queue: Queue,
        need_response: bool = False,
        adapter_name: str = "Default Adapter",
    ) -> None:
        self.instance_name = instance_name
        self.instance_path = instance_path
        self.signal_pipe = signal_pipe
        self.input_queue = input_queue  # 从外接受
        self.output_queue = output_queue  # 向外输入
        self.renderable_queue = renderable_queue  # 传输 rich 美化后的 log renderable
        self.need_response = need_response  # 是否需要 response
        self.adapter_name = adapter_name

        self.unique_id = None  # 唯一id , 用来关联 instance

        self.heart_beat_interval = 0.2
        self.need_send_log = True
        self.close = False

        self.signal_queue_send = PriorityQueue[Signal]()
        self.signal_queue_receive = PriorityQueue[Signal]()
        self.signal_handler: dict[str, Callable[[Signal], Any]] = dict()
        self.signal_handler[SignalType.need_close] = self._need_close
        self.signal_handler[SignalType.heartbeat] = self._heartbeat

        self.sche = Scheduler()

    # signal tools

    def _add_signal(self, s: Signal):
        """
        将待发送的的 Signal 按 `priority` 属性从大到小加入优先队列 , 留待后面发送
        """
        self.signal_queue_send.insert(s)

    def _listen_signal(self):
        """
        监听 Signal
        """
        while not self.close:
            recv: Signal = self.signal_pipe.recv()
            if recv is None:  # 收到 None 关闭
                break
            self.signal_queue_receive.insert(recv)
            logger.debug(f"Receive signal '{recv.type}' created in {recv.create_time}")
        logger.info("Signal listener exits.")

    def _send_signal(self):
        """
        发送完所有 Signal 后才会退出
        """

        def _do(self: Self):
            while not self.signal_queue_send.empty():
                sig = self.signal_queue_send.pop()
                self.signal_pipe.send(sig)
                logger.debug(f"Send signal '{sig.type}' created in {sig.create_time}")

        if self.need_response:
            while not self.close:
                _do(self)
            _do(self)
        logger.info("Signal sender exits.")

    def _solve_signal(self):
        """
        处理完所有 Signal 后才会退出
        """

        def _do(self: Self):
            while not self.signal_queue_receive.empty():
                s = self.signal_queue_receive.pop()
                if s.type in self.signal_handler:
                    logger.debug(f"Solve signal '{s.type}' created in {s.create_time}")
                    self.signal_handler[s.type](s)
                    logger.debug(f"Finish signal '{s.type}' created in {s.create_time}")
                else:
                    logger.warning(f"Unknown signal : {s}")

        while not self.close:
            _do(self)
        _do(self)
        logger.info("Signal solver exits.")

    # task
    def _tmp_task(self):
        pass

    # main

    def _set_logger(self):
        """
        添加两个 handler : 加入队列和写入文件
        这里尽量不要修改全局的级别
        """
        logger.handlers.clear()  # * 因为是多进程 , 且是入口没有多线程的情况 , 所以这里可以直接清除
        h1 = RichCallbackHandler(callback=self.renderable_queue.put)
        # ! 这里要保证 `self.instance_path` 存在
        h2 = RichFileHandler.quick(
            self.instance_path / f"{redatetime.day_str()}_{self.instance_name}.log"
        )
        h2.setFormatter(file_formatter)
        initialize_logger([h1, h2])
        hook_exception(callback=self.renderable_queue.put_nowait)

        debug_logger = getLogger("core.adapter.debug")  # file only
        debug_logger.setLevel("DEBUG")
        debug_logger.propagate = False
        debug_logger.addHandler(h2)
        self.debug = debug_logger

    def _run(self):
        while not self.close:
            self.sche.run()

    def run(self):
        """
        adapter 的入口函数
        """
        self._set_logger()
        logger.info("Logger initialized.")
        with ThreadPoolExecutor() as exec:
            exec.submit(self._listen_signal)
            exec.submit(self._send_signal)
            exec.submit(self._solve_signal)
            # exec.submit(self._run)
        logger.info("Process is closing.")
        self.clear()

    def clear(self):
        # self.signal_pipe.close() 从主进程关闭即可
        lis = [self.input_queue, self.output_queue, self.renderable_queue]
        for i in lis:
            # 清空队列 , 防止 `close` 可能的死锁
            while not i.empty():
                i.get_nowait()
            i.close()
            # i.cancel_join_thread()
        for i in lis:
            i.join_thread()

    def create_new_instance(self, name: str, folder: Path):
        pass

    # handler

    def _need_close(self, s: Signal):
        assert s.type == SignalType.need_close
        self.close = True

    def _heartbeat(self, s: Signal):
        assert s.type == SignalType.heartbeat
        response = Response(priority=s.priority, body=s)
        self._add_signal(response)
