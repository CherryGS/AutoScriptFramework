import os
from pathlib import Path

from utility.logger import RichRecordHandler

# 设置工作目录为当前文件对应目录
os.chdir(Path(__file__).parent)

import logging

import rich.traceback
import uvicorn

# 注册 rich 的 traceback 为默认
rich.traceback.install(show_locals=True)

if __name__ == "__main__":
    import uvicorn.server

    from global_config import basic_config
    from server import app
    from utility import redatetime
    from utility.logger import (
        RichFileHandler,
        console_formatter,
        file_formatter,
        getLogger,
        initialize_logger,
    )

    # 配置 rootLogger
    log_path = basic_config.main_log_path
    level = logging.DEBUG if basic_config.debug else logging.INFO
    if not log_path.is_dir():
        os.makedirs(log_path)
    file_handler = RichFileHandler.quick(log_path / f"{redatetime.day_str()}_main.log")
    file_handler.setFormatter(file_formatter)
    console_handler = RichRecordHandler()
    console_handler.setFormatter(console_formatter)
    initialize_logger([console_handler, file_handler], level)
    getLogger().info(f"Program starts with log level {getLogger().getEffectiveLevel()}")

    """ --- log level ---
    CRITICAL 50
    ERROR 40
    WARNING 30
    INFO 20
    DEBUG 10
    Trace 5 (uvicorn)
    NOTSET 0
    """

    # 配置并运行服务器
    # ? 好像 uvicorn 的 logrecord 不会传到 rootlogger
    # ? 但 `getLogger("uvicorn").propagate = True` , 其余的 `uvicorn.error` 等类似
    # * uvicorn 利用 config 在运行时修改 logger , 所以在修改前 `propagate = True`
    # * 简单的在设置中配置 `log_config=None` 来禁止 uvicorn 进行任何修改
    # * 同时不设置 `log_level` 使得所有的记录器从 `getLogger('uvicorn')` 获取等级
    server_config = uvicorn.Config(app, port=5000, log_config=None)
    server = uvicorn.Server(server_config)
    uvicorn_file_handler = RichFileHandler.quick(
        log_path / f"{redatetime.day_str()}_uvicorn.log"
    )
    uvicorn_file_handler.setFormatter(file_formatter)
    uvicorn_logger = getLogger("uvicorn")
    uvicorn_logger.setLevel(level)
    uvicorn_logger.propagate = False
    uvicorn_logger.addHandler(uvicorn_file_handler)
    uvicorn_logger.addHandler(console_handler)
    server.run()
