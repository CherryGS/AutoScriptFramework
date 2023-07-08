import os
from pathlib import Path

from pydantic import BaseModel, Field


class Config(BaseModel):
    instance_folder: Path = Field(default=Path(os.getcwd()) / "config")


asf_cofig = Config()
