class Sorter:
    def sort(self, data):
        pass

class BubbleSort(Sorter):
    def sort(self, data):
        n = len(data)
        for i in range(n):
            for j in range(0, n-i-1):
                if data[j] > data[j+1]:
                    data[j], data[j+1] = data[j+1], data[j]
        return data

class QuickSort(Sorter):
    def sort(self, data):
        if len(data) <= 1:
            return data
        pivot = data[len(data) // 2]
        left = [x for x in data if x < pivot]
        middle = [x for x in data if x == pivot]
        right = [x for x in data if x > pivot]
        return self.sort(left) + middle + self.sort(right)

class DataProcessor:
    def __init__(self, sorter):
        self.sorter = sorter
    
    def process(self, data):
        return self.sorter.sort(data)

if __name__ == "__main__":
    data = [64, 34, 25, 12, 22, 11, 90]
    processor = DataProcessor(BubbleSort())
    print(processor.process(data.copy()))
    
    processor = DataProcessor(QuickSort())
    print(processor.process(data.copy()))