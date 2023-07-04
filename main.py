import rich.traceback
from multiprocessing import Pool

# 注册 rich 的 traceback 为默认
rich.traceback.install(show_locals=True)

if __name__ == "__main__":
    # TODO: 更改实现
    import adapter.DestinyChild as ds

    with Pool() as pool:
        while True:
            comm = input("Please input the command. \n")
            if comm == "q":
                exit()
            instance = ds.DestinyChildManager()
            process = pool.apply(instance.run)
