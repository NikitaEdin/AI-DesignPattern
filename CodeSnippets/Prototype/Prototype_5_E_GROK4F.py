class Item:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def duplicate(self):
        return Item(self.name, self.value)

if __name__ == "__main__":
    original = Item("Book", 20)
    copy_item = original.duplicate()
    copy_item.value = 15
    print(f"Original: {original.name}, Value: {original.value}")
    print(f"Copy: {copy_item.name}, Value: {copy_item.value}")