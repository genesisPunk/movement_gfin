from cachetools import TTLCache
from datetime import datetime


class Cache:
    def __init__(self, ttl):
        self.data = {}
        self.ttl = ttl
        
    def set(self, key, value):
        self.data[key] = {
            'value': value,
            'expiry': datetime.now().timestamp() + self.ttl
        }
        
    def get(self, key):
        item = self.data.get(key)
        if item and item['expiry'] > datetime.now().timestamp():
            return item['value']
        return None