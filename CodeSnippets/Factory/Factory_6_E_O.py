from abc import ABC, abstractmethod
class Item(ABC):
    @abstractmethod
    def use(self): pass
class Widget(Item):
    def use(self): return "Widget in use"
class Gadget(Item):
    def use(self): return "Gadget in use"
class Creator:
    def make(self, kind: str) -> Item:
        if kind == "widget": return Widget()
        if kind == "gadget": return Gadget()
        raise ValueError("Unknown kind")
if __name__ == "__main__":
    creator = Creator()
    print(creator.make("widget").use())
    print(creator.make("gadget").use())