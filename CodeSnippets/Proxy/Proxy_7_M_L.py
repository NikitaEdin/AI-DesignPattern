class Proxy:
    def __init__(self, target):
        self.target = target

    def __getattr__(self, name):
        return getattr(self.target, name)

    def __setattr__(self, name, value):
        setattr(self.target, name, value)

class RealObject:
    def __init__(self):
        self.data = []

    def add_item(self, item):
        self.data.append(item)

    def get_items(self):
        return self.data

# Usage example
real_object = RealObject()
proxy = Proxy(real_object)
proxy.add_item("item1")
proxy.add_item("item2")
print(proxy.get_items()) # Output: ['item1', 'item2']