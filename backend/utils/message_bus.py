from collections import defaultdict
from cachetools import TTLCache


class MessageBus:
    def __init__(self):
        self.channels = defaultdict(list)
        self.cache = TTLCache(maxsize=100, ttl=300)

    def publish(self, channel, message):
        self.cache[channel] = message
        for callback in self.channels[channel]:
            callback(message)

    def subscribe(self, channel, callback):
        self.channels[channel].append(callback)