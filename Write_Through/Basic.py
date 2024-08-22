class DummyDB:
    def __init__(self) :
        self.db={}

    def getData(self, key):
        return self.db[key]

    def setData(self, key, value):
        print("DATABASE UPDATED!")
        self.db[key]=value

class WriteThrough:
    def __init__(self, DB) :
        self.cache={}
        self.db=DB
    
    def getData(self, key):
        cache_entry=self.cache.get(key)
        if cache_entry:
            print("CACHE HIT!")
            return cache_entry
        
        print("CACHE MISS!")
        data=self.db.getData(key)
        self.cache[key]=data
        return data

    def setData(self, key, value):
        self.cache[key]=value
        self.db.setData(key, value)

db=DummyDB()
cache=WriteThrough(db)

cache.setData("name","Daemon Targaryen")
db.setData("Alias","The Rogue Prince")

print(cache.getData("name"))        
print(cache.getData("Alias"))        
