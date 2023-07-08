from datetime import datetime as _datetime
from tzlocal import get_localzone


class datetime(_datetime):
    """
    重写内置 datetime 使得默认采用 'T' 分隔和时区
    以防 json schema 波浪线
    """

    tz = get_localzone()

    def __str__(self) -> str:
        return self.isoformat("T")

    @classmethod
    def now(cls):
        return super().now(cls.tz)


if __name__ == "__main__":
    from rich import print

    print(datetime.now())
