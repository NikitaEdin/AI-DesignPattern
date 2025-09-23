from abc import ABC, abstractmethod

class TextOperation(ABC):
    @abstractmethod
    def transform(self, text):
        pass

class UpperCaseOperation(TextOperation):
    def transform(self, text):
        if not isinstance(text, str):
            raise TypeError("Input must be a string")
        return text.upper()

class ReverseOperation(TextOperation):
    def transform(self, text):
        if not isinstance(text, str):
            raise TypeError("Input must be a string")
        return text[::-1]

class ReplaceOperation(TextOperation):
    def __init__(self, old, new):
        self.old = old
        self.new = new

    def transform(self, text):
        if not isinstance(text, str):
            raise TypeError("Input must be a string")
        return text.replace(self.old, self.new)

class TextProcessor:
    def __init__(self, operation: TextOperation):
        if not isinstance(operation, TextOperation):
            raise TypeError("operation must implement TextOperation")
        self._operation = operation

    def process(self, text):
        return self._operation.transform(text)

    def set_operation(self, operation: TextOperation):
        if not isinstance(operation, TextOperation):
            raise TypeError("operation must implement TextOperation")
        self._operation = operation

def get_operation_by_name(name, **kwargs):
    registry = {
        "upper": UpperCaseOperation,
        "reverse": ReverseOperation,
        "replace": ReplaceOperation,
    }
    try:
        cls = registry[name]
    except KeyError:
        raise ValueError(f"Unknown operation '{name}'")
    return cls(**kwargs) if kwargs else cls()

if __name__ == "__main__":
    processor = TextProcessor(get_operation_by_name("upper"))
    print(processor.process("Hello World"))
    processor.set_operation(get_operation_by_name("reverse"))
    print(processor.process("Hello World"))
    processor.set_operation(get_operation_by_name("replace", old="l", new="x"))
    print(processor.process("Hello World"))
    try:
        get_operation_by_name("nonexistent")
    except ValueError as err:
        print("Error:", err)