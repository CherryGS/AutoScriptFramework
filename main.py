import os
import rich.traceback
import uvicorn

from server import app
from manager import manager

# 注册 rich 的 traceback 为默认
rich.traceback.install(show_locals=True)

# 设置工作目录为当前文件对应目录
os.chdir(os.path.abspath(__file__))

if __name__ == "__main__":
    server_config = uvicorn.Config(app, port=5000, log_level="info")
    server = uvicorn.Server(server_config)
    server.run()
