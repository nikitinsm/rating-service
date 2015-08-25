


class MemoryStorage(object):

    key_value_storage = None

    def __init__(self):
        self.key_value_storage = {}

    def get(self, key):
        return self.key_value_storage.get(key) or None

    def set(self, key, value):
        self.key_value_storage[key] = value

    def increment(self, key, value):
        self.key_value_storage.setdefault(key, 0)
        self.key_value_storage[key] += value

    def decrement(self, key, value):
        self.key_value_storage.setdefault(key, 0)
        self.key_value_storage[key] -= value

    def delete(self, key):
        self.key_value_storage.pop(key)



default_storage = MemoryStorage()