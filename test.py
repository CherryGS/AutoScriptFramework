import asyncio
from rich import print

a = list(range(1, 10))
b = list(range(10, 20))


async def run(a):
    for i in a:
        print(i, end=" ")
        await asyncio.sleep(0.2)


async def main1():
    await run(a)
    await run(b)


if __name__ == "__main__":
    asyncio.run(main1())
