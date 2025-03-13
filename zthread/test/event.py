import threading
import time

"""
模拟 事件的同步.
"""

class Counter:
    def __init__(self):
        self.value = 0
        self.event = threading.Event()

    def increment(self):
        self.value += 1
        print(f"Value is now {self.value}")
        # 模拟耗时操作
        time.sleep(1)


# 使用
counter = Counter()


def worker():
    counter.event.wait()  # 等待事件
    counter.increment()
    counter.event.clear()  # 清除事件，使后续线程等待


def worker2():
    time.sleep(2)
    print(" work 2 ......")
    counter.event.set()


thread1 = threading.Thread(target=worker)
thread2 = threading.Thread(target=worker2)

thread1.start()
thread2.start()

thread1.join()
thread2.join()
