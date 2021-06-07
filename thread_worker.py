import time
import threading


class ThreadWorker:
    def thread_worker(self, number: int):
        rst = 0
        for idx in range(number):
            rst += idx
            pass
        print(rst)
        pass


def supervisor():
    obj = ThreadWorker()
    thread_worker = threading.Thread(target=obj.thread_worker, args=(99999999,))
    thread_worker.start()
    while thread_worker.is_alive():
        time.sleep(1)  # 每一秒询问一次
        print(thread_worker.is_alive())
        pass
    pass


if __name__ == '__main__':
    supervisor()
    pass
