from abc import ABC, abstractmethod

class SortingMethod(ABC):
    @abstractmethod
    def sort(self, data):
        pass

class BubbleSortingMethod(SortingMethod):
    def sort(self, data):
        data = data[:]
        n = len(data)
        for i in range(n):
            for j in range(0, n - i - 1):
                if data[j] > data[j + 1]:
                    data[j], data[j + 1] = data[j + 1], data[j]
        return data

class InsertionSortingMethod(SortingMethod):
    def sort(self, data):
        data = data[:]
        for i in range(1, len(data)):
            key = data[i]
            j = i - 1
            while j >= 0 and key < data[j]:
                data[j + 1] = data[j]
                j -= 1
            data[j + 1] = key
        return data

class DataSorter:
    def __init__(self, method):
        self.method = method

    def set_method(self, method):
        self.method = method

    def perform_sort(self, data):
        if not isinstance(data, list):
            raise ValueError("Data must be a list")
        if not data:
            return []
        return self.method.sort(data)

if __name__ == "__main__":
    data = [64, 34, 25, 12, 22, 11, 90]
    sorter = DataSorter(BubbleSortingMethod())
    sorted_data = sorter.perform_sort(data)
    print("Bubble sorted:", sorted_data)
    sorter.set_method(InsertionSortingMethod())
    sorted_data = sorter.perform_sort(data)
    print("Insertion sorted:", sorted_data)