import copy

class Component:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def duplicate(self):
        return copy.deepcopy(self)

    def display(self, indent=0):
        print("  " * indent + f"Component: {self.name} = {self.value}")

class Assembly:
    def __init__(self, name):
        self.name = name
        self.components = []

    def add_component(self, component):
        self.components.append(component)

    def duplicate(self):
        new_assembly = copy.copy(self)
        new_assembly.components = [comp.duplicate() for comp in self.components]
        return new_assembly

    def display(self, indent=0):
        print("  " * indent + f"Assembly: {self.name}")
        for comp in self.components:
            comp.display(indent + 1)

class Product:
    def __init__(self, model):
        self.model = model
        self.assemblies = []

    def add_assembly(self, assembly):
        self.assemblies.append(assembly)

    def duplicate(self):
        new_product = copy.copy(self)
        new_product.assemblies = [asm.duplicate() for asm in self.assemblies]
        return new_product

    def display(self, indent=0):
        print("  " * indent + f"Product: {self.model}")
        for asm in self.assemblies:
            asm.display(indent + 1)

def main():
    # Build original product
    comp1 = Component("CPU", 100)
    comp2 = Component("RAM", 50)
    assembly1 = Assembly("Motherboard")
    assembly1.add_component(comp1)
    assembly1.add_component(comp2)
    product = Product("PC-Original")
    product.add_assembly(assembly1)

    print("Original Product:")
    product.display()

    # Clone the product
    cloned_product = product.duplicate()

    # Modify clone
    cloned_product.model = "PC-Cloned"
    if cloned_product.assemblies:
        cloned_product.assemblies[0].components[0].value = 200

    print("\nAfter modifying clone:")
    print("Original Product:")
    product.display()
    print("Cloned Product:")
    cloned_product.display()

    # Edge case: Shared mutable reference
    shared_assembly = Assembly("Shared")
    shared_comp = Component("GPU", 75)
    shared_assembly.add_component(shared_comp)
    product.add_assembly(shared_assembly)
    cloned_product.add_assembly(shared_assembly)  # Same instance

    print("\nAfter adding shared assembly to both:")
    print("Original Product:")
    product.display()
    print("Cloned Product:")
    cloned_product.display()

    # Modify shared component
    shared_comp.value = 150

    print("\nAfter modifying shared component:")
    print("Original Product:")
    product.display()
    print("Cloned Product:")
    cloned_product.display()

if __name__ == "__main__":
    main()