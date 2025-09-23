class Operation():
    def __init__(self):
        pass
    
    def execute(self, a, b):
        raise NotImplementedError("execute() is not implemented in the base class")

class Addition(Operation):
    def execute(self, a, b):
        return a + b

class Subtraction(Operation):
    def execute(self, a, b):
        return a - b

class Multiplication(Operation):
    def execute(self, a, b):
        return a * b

class Division(Operation):
    def execute(self, a, b):
        return a / b

def main():
    operations = [Addition(), Subtraction(), Multiplication(), Division()]
    numbers = [10, 20, 30, 40]

    for operation in operations:
        for num in numbers:
            result = operation.execute(num, num)
            print(f"{operation.__class__.__name__}: {result}")

if __name__ == "__main__":
    main()