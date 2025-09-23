# The Director class is responsible for constructing complex objects.
class Director:
    def __init__(self, builder):
        self.builder = builder
    
    def build(self):
        return self.builder.construct()

# The Builder interface declares the methods for creating the complex object step by step.
class Builder:
    def construct(self):
        raise NotImplementedError("Subclasses must implement this method")
    
    def add_part(self, part):
        raise NotImplementedError("Subclasses must implement this method")
    
    def add_feature(self, feature):
        raise NotImplementedError("Subclasses must implement this method")
    
    def get_result(self):
        raise NotImplementedError("Subclasses must implement this method")

# The ConcreteBuilder class implements the Builder interface and provides an extension point for creating complex objects.
class ConcreteBuilder:
    def __init__(self, name):
        self.name = name
        self.parts = []
    
    def construct(self):
        return Product(self.name, self.parts)
    
    def add_part(self, part):
        self.parts.append(part)
    
    def add_feature(self, feature):
        self.parts.append(f"{self.name} has {feature}")
    
    def get_result(self):
        return self.construct()

# The Product class represents the complex object built by the Builder classes.
class Product:
    def __init__(self, name, parts):
        self.name = name
        self.parts = parts
    
    def get_name(self):
        return self.name
    
    def get_parts(self):
        return self.parts
    
    def __str__(self):
        return f"{self.name} has {len(self.parts)} parts."

# Usage example of the Builder pattern:
def main():
    # Create an instance of the Director class and pass a ConcreteBuilder instance to it.
    director = Director(ConcreteBuilder("Product"))
    
    # Call the build method of the Director object to construct a Product object.
    product = director.build()
    
    # Print the result of the construction process.
    print(product)

# Output: Product has 3 parts.