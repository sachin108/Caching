import time
import threading
import sched

class DummyDB:
    def __init__(self):
        self.data = {}

    def getData(self, key):
        return self.data.get(key)

    def setData(self, key, value):
        self.data[key] = value

class WriteThroughCacheWithTTL:
    def __init__(self, db, ttl, cleanup_interval):
        self.db = db
        self.cache = {}
        self.ttl = ttl
        self.cleanup_interval = cleanup_interval
        self.scheduler = sched.scheduler(time.time, time.sleep)

        self.cleanup_thread = threading.Thread(target=self._start_scheduler)
        self.cleanup_thread.daemon = True
        self.lock = threading.Lock()

        self.cleanup_thread.start()

    def _start_scheduler(self):
        while True:
            # Schedule the next cleanup event
            self.scheduler.enter(self.cleanup_interval, 1, self._cleanup_expired_cache)
            self.scheduler.run(blocking=True)
            '''
            self.scheduler.run(): This method processes events in the event queue.

            blocking=True: When set to True, the method will block the execution and wait until 
            all scheduled events have been executed. 
            '''

    def _cleanup_expired_cache(self):
        with self.lock:
            current_time = time.time()
            expired_keys = [key for key, value in self.cache.items()
                            if (current_time - value['timestamp']) >= self.ttl]
            for key in expired_keys:
                del self.cache[key]
            
            print("CLEANUP DONE!")


    def _start_cleanup_thread(self):
        self.cleanup_timer = threading.Timer(self.cleanup_interval, self._cleanup_expired_cache)
        self.cleanup_timer.start()

    def getData(self, key):
        with self.lock:
            if key in self.cache:
                print("Cache hit!")
                return self.cache[key]['value']

            print("Cache miss!")
            value = self.db.getData(key)
            if value is not None:
                self.cache[key] = {'value': value, 'timestamp': time.time()}
            return value

    def setData(self, key, value):
        with self.lock:
            self.cache[key] = {'value': value, 'timestamp': time.time()}
            self.db.setData(key, value)

db = DummyDB()
cache = WriteThroughCacheWithTTL(db, ttl=10, cleanup_interval=5)

cache.setData("name","Daemon Targaryen")
time.sleep(5)

print(cache.getData("name"))        

db.setData("Alias","The Rogue Prince")
time.sleep(6)

print(cache.getData("name"))        
print(cache.getData("Alias"))   
print(cache.getData("Alias"))   