import copy
class ItemBase:
    def clone(self):
        raise NotImplementedError
class Widget(ItemBase):
    def __init__(self, name, data):
        self.name = name
        self.data = data
    def clone(self):
        return copy.deepcopy(self)
class Registry:
    def __init__(self):
        self._items = {}
    def register(self, key, item):
        self._items[key] = item
    def create(self, key):
        return self._items[key].clone()
if __name__ == '__main__':
    reg = Registry()
    original = Widget('w1', {'x': 1})
    reg.register('one', original)
    copy1 = reg.create('one')
    copy1.data['x'] = 2
    print(original.name, original.data)
    print(copy1.name, copy1.data)