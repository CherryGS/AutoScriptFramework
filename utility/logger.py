import logging
from logging import LogRecord
from pathlib import Path
from types import ModuleType, TracebackType
from typing import Any, Callable, Iterable, List, Type

from rich._log_render import FormatTimeCallable
from rich.console import Console, ConsoleRenderable
from rich.highlighter import Highlighter
from rich.logging import RichHandler
from rich.traceback import LOCALS_MAX_LENGTH, LOCALS_MAX_STRING, Traceback

# from AzurlaneAutoScript , thx
console_formatter = logging.Formatter(
    fmt="%(asctime)s.%(msecs)03d │ %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)
file_formatter = logging.Formatter(
    fmt="%(asctime)s.%(msecs)03d | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

_console = Console(record=True)


class RichRecordHandler(RichHandler):
    """
    用来进行主进程中的控制台输出和记录
    """

    def __init__(
        self,
        level: int | str = logging.NOTSET,
    ) -> None:
        super().__init__(
            level,
            console=_console,
            show_time=False,
            rich_tracebacks=True,
            tracebacks_show_locals=True,
        )


class RichCallbackHandler(RichHandler):
    """
    用来进行子进程中 log 的传递
    简单的将原代码中 `emit` 部分的直接输出变成以 `log_renderable` 为参数的 `callback` 调用, 大概是不支持 `jupter` 了
    """

    def __init__(
        self,
        level: int | str = logging.NOTSET,
        console: Console | None = None,
        *,
        callback: Callable[[ConsoleRenderable], Any],
        show_time: bool = True,
        omit_repeated_times: bool = True,
        show_level: bool = True,
        show_path: bool = True,
        enable_link_path: bool = True,
        highlighter: Highlighter | None = None,
        markup: bool = False,
        rich_tracebacks: bool = False,
        tracebacks_width: int | None = None,
        tracebacks_extra_lines: int = 3,
        tracebacks_theme: str | None = None,
        tracebacks_word_wrap: bool = True,
        tracebacks_show_locals: bool = False,
        tracebacks_suppress: Iterable[str | ModuleType] = ...,
        locals_max_length: int = 10,
        locals_max_string: int = 80,
        log_time_format: str | FormatTimeCallable = "[%x %X]",
        keywords: List[str] | None = None,
    ) -> None:
        """
        callback : 回调函数 , 在 `emit` 最后获取到拼接好的 log 后执行 , 要求瞬间完成 , 否则会阻塞函数
        对于 `Queue` 可以考虑使用 `put_nowait`
        ! 此处的代码尤其是参数是基于 `RichHandler` 的方法修改而得到 , 可能会因原代码的微小改变而失效 .
        """
        self.callback = callback
        super().__init__(
            level,
            console,
            show_time=show_time,
            omit_repeated_times=omit_repeated_times,
            show_level=show_level,
            show_path=show_path,
            enable_link_path=enable_link_path,
            highlighter=highlighter,
            markup=markup,
            rich_tracebacks=rich_tracebacks,
            tracebacks_width=tracebacks_width,
            tracebacks_extra_lines=tracebacks_extra_lines,
            tracebacks_theme=tracebacks_theme,
            tracebacks_word_wrap=tracebacks_word_wrap,
            tracebacks_show_locals=tracebacks_show_locals,
            tracebacks_suppress=tracebacks_suppress,
            locals_max_length=locals_max_length,
            locals_max_string=locals_max_string,
            log_time_format=log_time_format,
            keywords=keywords,
        )

    def emit(self, record: LogRecord) -> None:
        """
        由 `logging` 模块自动调用
        ! 此处的代码是基于 `RichHandler` 的方法修改而得到 , 可能会因原代码的微小改变而失效 .
        """
        message = self.format(record)
        traceback = None
        if (
            self.rich_tracebacks
            and record.exc_info
            and record.exc_info != (None, None, None)
        ):
            exc_type, exc_value, exc_traceback = record.exc_info
            assert exc_type is not None
            assert exc_value is not None
            traceback = Traceback.from_exception(
                exc_type,
                exc_value,
                exc_traceback,
                width=self.tracebacks_width,
                extra_lines=self.tracebacks_extra_lines,
                theme=self.tracebacks_theme,
                word_wrap=self.tracebacks_word_wrap,
                show_locals=self.tracebacks_show_locals,
                locals_max_length=self.locals_max_length,
                locals_max_string=self.locals_max_string,
                suppress=self.tracebacks_suppress,
            )
            message = record.getMessage()
            if self.formatter:
                record.message = record.getMessage()
                formatter = self.formatter
                if hasattr(formatter, "usesTime") and formatter.usesTime():
                    record.asctime = formatter.formatTime(record, formatter.datefmt)
                message = formatter.formatMessage(record)

        message_renderable = self.render_message(record, message)
        log_renderable = self.render(
            record=record, traceback=traceback, message_renderable=message_renderable
        )

        try:
            # * 调用 callback
            self.callback(log_renderable)
        except Exception:
            self.handleError(record)


class RichFileHandler(RichHandler):
    """
    用来进行文件的写入
    `RichHandler` 本身并没有有关文件的设置 , 重定向到文件需要一个设定了文件输出的 `Console` 作为 console 参数传入
    """

    def __init__(
        self,
        level: int | str = logging.NOTSET,
        console: Console | None = None,
        **kwargs,
    ) -> None:
        assert (
            console and console._file is not None
        ), "文件 `RichHandler` 需要设置了 `file` 属性的 `Console` 实例"
        super().__init__(
            level,
            console,
            show_time=False,
            show_level=False,
            rich_tracebacks=True,
            tracebacks_show_locals=True,
            **kwargs,
        )

    @classmethod
    def quick(cls, log_file: Path):
        """
        快速创建一个 FileHandler , console 应该不会被 gc 干掉的吧
        """
        f = open(log_file, "a+", encoding="utf8")
        console = Console(file=f)
        return cls(console=console)


def hook_exception(
    *,
    callback: Callable[[Traceback], Any],
    console: Console | None = None,
    width: int | None = 100,
    extra_lines: int = 3,
    theme: str | None = None,
    word_wrap: bool = False,
    show_locals: bool = False,
    locals_max_length: int = LOCALS_MAX_LENGTH,
    locals_max_string: int = LOCALS_MAX_STRING,
    locals_hide_dunder: bool = True,
    locals_hide_sunder: bool | None = None,
    indent_guides: bool = True,
    suppress: Iterable[str | ModuleType] = (),
    max_frames: int = 100,
) -> Callable[[Type[BaseException], BaseException, TracebackType | None], Any]:
    """
    hook 未捕获异常并调用 callback
    ! 此处的代码是基于 `rich.traceback` 中的 `install` 修改而得到 , 可能会因原代码的微小改变而失效 .
    """
    traceback_console = Console(stderr=True) if console is None else console

    locals_hide_sunder = (
        True
        if (traceback_console.is_jupyter and locals_hide_sunder is None)
        else locals_hide_sunder
    )

    def excepthook(
        type_: Type[BaseException],
        value: BaseException,
        traceback: TracebackType | None,
    ) -> None:
        renderable = Traceback.from_exception(
            type_,
            value,
            traceback,
            width=width,
            extra_lines=extra_lines,
            theme=theme,
            word_wrap=word_wrap,
            show_locals=show_locals,
            locals_max_length=locals_max_length,
            locals_max_string=locals_max_string,
            locals_hide_dunder=locals_hide_dunder,
            locals_hide_sunder=bool(locals_hide_sunder),
            indent_guides=indent_guides,
            suppress=suppress,
            max_frames=max_frames,
        )
        try:
            callback(renderable)
            sys.__excepthook__(type_, value, traceback)
        except Exception:
            info = sys.exc_info()
            sys.__excepthook__(info[0], info[1], info[2])  # type: ignore

    import sys

    old_excepthook = sys.excepthook
    sys.excepthook = excepthook
    return old_excepthook


class BetterLogger(logging.getLoggerClass()):
    # TODO : Finish
    def title(self, *arg, title: str, **kwargs):
        self.info(title, arg, kwargs)


logging.setLoggerClass(BetterLogger)


# 前面已经调用 `setLoggerClass` , 这里是为了方便 type hint
def getLogger(name: str | None = None):
    """
    TODO: 使得可以区分 `name` 是否为 `None` 时的类型
    即使调用 `logging.setLoggerClass(CustomLogger)` 之后 , 如果 `getLogger` 没有指定参数 `name` , 返回的还是 `RootLogger`
    只有指定了 `name` 之后 , 返回的才是 `CustomLogger`
    """
    f = logging.getLogger(name)
    if name:
        assert isinstance(f, BetterLogger)
        return f
    else:
        assert isinstance(f, logging.RootLogger)
        return f


def initialize_logger(handlers: list, level: int):
    """
    初始化根记录器
    """
    # * level 是根记录器的等级
    # ! 启用了 `force=True` 会强制覆盖原有的配置
    logging.basicConfig(level=level, handlers=handlers, force=True)
    # * 使得 log 的 `emit` 中的 `handle` 可以抛出异常 , 这可能会打断程序
    logging.raiseExceptions = True


if __name__ == "__main__":
    import logging

    f = getLogger("")
    f.warning("test")
