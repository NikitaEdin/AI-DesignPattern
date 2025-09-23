from abc import ABC, abstractmethod
import copy

class SortingMethod(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def apply(self, data):
        pass

class BubbleSortingMethod(SortingMethod):
    def apply(self, data):
        if not isinstance(data, list):
            raise TypeError("Input must be a list")
        if data is None or len(data) == 0:
            return []
        if len(data) == 1:
            return copy.copy(data)
        result = copy.copy(data)
        n = len(result)
        swapped = True
        while swapped:
            swapped = False
            for i in range(1, n):
                if result[i-1] > result[i]:
                    result[i-1], result[i] = result[i], result[i-1]
                    swapped = True
                    n = i
        return result

class InsertionSortingMethod(SortingMethod):
    def apply(self, data):
        if not isinstance(data, list):
            raise TypeError("Input must be a list")
        if data is None or len(data) == 0:
            return []
        if len(data) == 1:
            return copy.copy(data)
        result = copy.copy(data)
        for i in range(1, len(result)):
            key = result[i]
            j = i - 1
            while j >= 0 and key < result[j]:
                result[j + 1] = result[j]
                j -= 1
            result[j + 1] = key
        return result

class SelectionSortingMethod(SortingMethod):
    def apply(self, data):
        if not isinstance(data, list):
            raise TypeError("Input must be a list")
        if data is None or len(data) == 0:
            return []
        if len(data) == 1:
            return copy.copy(data)
        result = copy.copy(data)
        n = len(result)
        for i in range(n):
            min_idx = i
            for j in range(i + 1, n):
                if result[min_idx] > result[j]:
                    min_idx = j
            result[i], result[min_idx] = result[min_idx], result[i]
        return result

class DataHandler:
    def __init__(self, method):
        if not isinstance(method, SortingMethod):
            raise ValueError("Must provide a valid sorting method")
        self.method = method

    def set_method(self, method):
        if not isinstance(method, SortingMethod):
            raise ValueError("Must provide a valid sorting method")
        self.method = method

    def get_current_method(self):
        return self.method.name

    def handle(self, data):
        if data is None:
            raise ValueError("Data cannot be None")
        try:
            return self.method.apply(data)
        except Exception as e:
            raise RuntimeError(f"Failed to process data: {str(e)}")

if __name__ == "__main__":
    test_data = [64, 34, 25, 12, 22, 11, 90]
    empty_data = []
    single_data = [5]

    handler = DataHandler(BubbleSortingMethod("Bubble"))
    print(f"Using {handler.get_current_method()}: {handler.handle(test_data)}")
    handler.set_method(InsertionSortingMethod("Insertion"))
    print(f"Using {handler.get_current_method()}: {handler.handle(test_data)}")
    handler.set_method(SelectionSortingMethod("Selection"))
    print(f"Using {handler.get_current_method()}: {handler.handle(test_data)}")

    print(f"Empty list with {handler.get_current_method()}: {handler.handle(empty_data)}")
    print(f"Single element with {handler.get_current_method()}: {handler.handle(single_data)}")