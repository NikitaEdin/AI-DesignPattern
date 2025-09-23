import copy

class Item:
    def __init__(self, name, values):
        self.name = name
        self.values = values
    def clone(self):
        return copy.deepcopy(self)
    def __repr__(self):
        return f"Item(name={self.name!r}, values={self.values!r})"

if __name__ == "__main__":
    original = Item("Template", [1, 2, 3])
    copy1 = original.clone()
    copy2 = original.clone()
    copy1.name = "InstanceA"
    copy1.values.append(4)
    copy2.name = "InstanceB"
    copy2.values.append(5)
    print("original:", original)
    print("copy1   :", copy1)
    print("copy2   :", copy2)