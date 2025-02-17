from cachetools import TTLCache
from datetime import datetime, timedelta
import pickle
import threading
from cachetools import TTLCache
import os

class Cache:
    def __init__(self,filename='cache.pkl'):
        self.filename = filename
        self.cache = {}
        self.lock = threading.Lock()  # For thread safety
        self.data = {}

        # Load existing cache from disk if available
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'rb') as f:
                    self.cache = pickle.load(f)
                print(f"Loaded cache with {len(self.cache)} entries from disk")
            except Exception as e:
                print(f"Error loading cache: {str(e)}")
                self.cache = {}

    def _save_to_disk(self):
        """Internal method to persist cache to disk"""
        with self.lock:
            try:
                # Clean expired entries before saving
                self._clean_expired()
                with open(self.filename, 'wb') as f:
                    pickle.dump(self.cache, f)
            except Exception as e:
                print(f"Error saving cache: {str(e)}")

    def _clean_expired(self):
        """Remove expired entries from cache"""
        now = datetime.now()
        expired_keys = [k for k, v in self.cache.items() if v['expiry'] < now]
        for k in expired_keys:
            del self.cache[k]

    def get(self, key):
        """Retrieve cached data if it exists and is not expired"""
        entry = self.cache.get(key)
        if entry:
            if datetime.now() < entry['expiry']:
                return entry['data']
            else:
                del self.cache[key]
                self._save_to_disk()
        return None

    def set(self, key, data, ttl):
        """Store data in cache with time-to-live (ttl) in seconds"""
        self.cache[key] = {
            'data': data,
            'expiry': datetime.now() + timedelta(seconds=ttl)
        }
        self._save_to_disk()
