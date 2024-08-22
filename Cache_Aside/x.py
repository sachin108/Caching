from threading import Thread, Lock
import time

class CacheAside:
    def __init__(self):
        self.cache = {}
        self.lock = Lock()

    def function_x(self):
        print("Thread X acquiring lock")
        time.sleep(2)  # Simulate a long operation
        self.cache['x'] = 'value_x'
        print("Thread X updating cache")

    def function_y(self):
        print("Thread Y acquiring lock")
        time.sleep(2)  # Simulate a long operation
        self.cache['y'] = 'value_y'
        print("Thread Y updating cache")

cache = CacheAside()

thread_x = Thread(target=cache.function_x)
thread_y = Thread(target=cache.function_y)

thread_x.start()
thread_y.start()

thread_x.join()
thread_y.join()

print(cache.cache)
