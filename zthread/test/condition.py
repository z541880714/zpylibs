import threading


class Counter:
    def __init__(self):
        self.value = 0
        self.condition = threading.Condition()

    def increment(self):
        with self.condition:
            self.value += 1
            print(f"Value is now {self.value}")
            # 模拟耗时操作
            import time
            time.sleep(1)
            self.condition.notify_all()  # 通知所有等待的线程


# 使用
counter = Counter()


def worker():
    with counter.condition:
        counter.condition.wait()  # 等待条件
        counter.increment()


threads = [threading.Thread(target=worker) for _ in range(2)]
for thread in threads:
    thread.start()
for thread in threads:
    thread.join()
