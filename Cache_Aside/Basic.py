class Cache_Aside:
    def __init__(self):
        self.cache={}

    def getData(self, key):
        if key in self.cache:
            #cache hit
            print("Cache hit")
            return self.cache.get(key)
    
        print("Cache miss")
        #cache miss
        self.cache[key]=self.dummy_DB(key)
        return self.cache[key]

    
    def dummy_DB(self, key):
        db={
            "name":"Arthur",
            "familyName":"Dayne",
            "title":["ser", "Sword of the Morning"],
            "culture": "Donishmen",
            "allegiances":["House Dayne", "Kingsguard"]
        }

        return db.get(key)

    
    def invalidate_cache(self, key):
        del self.cache[key]


cache=Cache_Aside()
print(cache.getData("name"))    #cache miss
print(cache.getData("name"))    #cache hit

print(cache.getData("culture"))    #cache miss
print(cache.getData("culture"))    #cache hit

print(cache.invalidate_cache("culture"))    #data will be deleted from cache

print(cache.getData("culture"))    #cache miss

