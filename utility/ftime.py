from datetime import datetime
from typing import Annotated
from tzlocal import get_localzone


class redatetime(datetime):
    """
    重写内置 datetime 使其默认采用 'T' 分隔和时区
    以防 json schema 波浪线
    """

    tz = get_localzone()

    def __str__(self) -> str:
        return self.isoformat("T")

    @classmethod
    def now(cls):
        return super().now(cls.tz)

    @classmethod
    def day_str(cls):
        return cls.strftime(cls.now(), "%Y-%m-%d")


Annodate = Annotated[datetime, redatetime]

if __name__ == "__main__":
    from rich import print

    print(redatetime.now())
