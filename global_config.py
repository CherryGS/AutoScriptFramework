import os
from pathlib import Path

from pydantic import BaseModel, Field


class Config(BaseModel):
    instance_folder: Path = Field(default=Path(os.getcwd()) / "config")
    main_log_path: Path = Field(default=Path(os.getcwd()) / "log")
    debug: bool = True
    passwd: str | None = None


try:
    import json

    f = open("./global_config.json", "r")
    basic_config = Config(**json.loads(f.read()))
except Exception as e:
    basic_config = Config()
