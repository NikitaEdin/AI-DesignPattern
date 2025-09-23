class Component:
    def __init__(self):
        self.elements = []

    def include(self, element):
        self.elements.append(element)

class AssemblyGuide:
    def __init__(self):
        self.component = Component()

    def add_base(self):
        self.component.include("Base Layer")

    def add_topping(self):
        self.component.include("Topping")

    def retrieve(self):
        return self.component

class ProductionManager:
    def __init__(self, guide):
        self.guide = guide

    def oversee(self):
        self.guide.add_base()
        self.guide.add_topping()

if __name__ == "__main__":
    guide = AssemblyGuide()
    manager = ProductionManager(guide)
    manager.oversee()
    component = guide.retrieve()
    print(component.elements)