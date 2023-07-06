import heapq
from typing import TypeVar, Generic

T = TypeVar("T")


class PriorityQueue(Generic[T]):
    """
    小根堆
    """

    def __init__(self, lis: list[T] = list()) -> None:
        self.lis = lis
        heapq.heapify(self.lis)

    def insert(self, o: T):
        heapq.heappush(self.lis, o)

    def top(self):
        return self.lis[0]

    def pop(self):
        return heapq.heappop(self.lis)

    def empty(self):
        return not self.lis

    def clear(self):
        while not self.empty():
            self.pop()


if __name__ == "__main__":
    q = PriorityQueue[int](list(range(10, 1, -1)))
    print(q.top())
    q.insert(1)
    print(q.top())
