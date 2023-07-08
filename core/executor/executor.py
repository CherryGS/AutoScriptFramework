"""
原子性(全部执行/全部不执行) , 可见性(对公共变量的修改是否会立即反应) , 有序性(代码重排)
"""
from concurrent.futures import ThreadPoolExecutor as _ThreadPoolExecutor
from concurrent.futures import ProcessPoolExecutor as _ProcessPoolExecutor


class ThreadPoolExecutor(_ThreadPoolExecutor):
    pass


class ProcessPoolExecutor(_ProcessPoolExecutor):
    pass
