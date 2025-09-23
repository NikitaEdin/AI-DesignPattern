import copy

class Item:
    def __init__(self, name, data):
        self.name = name
        self.data = data
    def clone(self):
        return copy.deepcopy(self)

class Example(Item):
    def __init__(self, name, data, value):
        super().__init__(name, data)
        self.value = value
    def __repr__(self):
        return f"Example(name={self.name!r}, data={self.data!r}, value={self.value!r})"

if __name__ == "__main__":
    original = Example("orig", {"a": 1}, [10])
    copy1 = original.clone()
    copy1.name = "copy"
    copy1.data["a"] = 2
    copy1.value.append(20)
    print(original)
    print(copy1)