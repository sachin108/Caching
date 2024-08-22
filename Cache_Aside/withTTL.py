import time
import sched
from threading import Thread, Lock

class CacheAside:
    def __init__(self, ttl, cleanup_interval):
        self.cache = {}
        self.ttl = ttl 
        self.cleanup_interval = cleanup_interval 
        self.scheduler = sched.scheduler(time.time, time.sleep)
        # Start the cleanup scheduler in a separate thread
        self.cleanup_thread = Thread(target=self._start_scheduler)
        self.cleanup_thread.daemon = True  
        self.lock=Lock()
        # A daemon thread in Python is a type of thread that runs in the background and does not prevent 
        # the program from exiting. 
        
        self.cleanup_thread.start()

    def _start_scheduler(self):
        while True:
            # Schedule the next cleanup event
            self.scheduler.enter(self.cleanup_interval, 1, self._cleanup_expired_cache)
            self.scheduler.run(blocking=True)

    def get_data(self, key):
        current_time = time.time()

        #lock ensures that only one thread can update the cache at a time, preventing 
        #concurrent updates that could lead to inconsistent or corrupted cache states
        with self.lock:      
            cache_entry=self.cache.get(key)
            if cache_entry:
                print("Cache hit")
                return cache_entry['data']
        
        print("Cache miss")
        data = self.fetch_from_db(key)
        
        with self.lock:  
            self.cache[key] = {
                'data': data,
                'expiry': current_time + self.ttl
            }
        
        return data

    def fetch_from_db(self, key):
        db={
            "name":"Arthur",
            "familyName":"Dayne",
            "title":["ser", "Sword of the Morning"],
            "culture": "Donishmen",
            "allegiances":["House Dayne", "Kingsguard"]
        }
        return db.get(key, None)

    def _cleanup_expired_cache(self):
        with self.lock:  
            current_time = time.time()
            keys_to_delete = [key for key, value in self.cache.items() if value['expiry'] <= current_time]
            
            for key in keys_to_delete:
                del self.cache[key]

        print("Cache cleanup done")

cache = CacheAside(ttl=10, cleanup_interval=5)

print(cache.get_data("name"))  # Cache miss
time.sleep(4)
print(cache.get_data("name"))  # Cache hit
time.sleep(7)
print(cache.get_data("name"))  # Cache miss (expired, should trigger cleanup)
