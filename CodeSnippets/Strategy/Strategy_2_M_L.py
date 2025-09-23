# Sorting Algorithm interface
class SortAlgorithm:
    def sort(self, items):
        raise NotImplementedError("sort must be implemented")

# Bubble Sort algorithm
class BubbleSort(SortAlgorithm):
    def sort(self, items):
        for i in range(len(items)):
            for j in range(i+1, len(items)):
                if items[j] < items[i]:
                    items[i], items[j] = items[j], items[i]
        return items

# Merge Sort algorithm
class MergeSort(SortAlgorithm):
    def sort(self, items):
        if len(items) <= 1:
            return items
        mid = len(items) // 2
        left = self.sort(items[:mid])
        right = self.sort(items[mid:])
        return self.merge(left, right)

    def merge(self, left, right):
        result = []
        while len(left) > 0 and len(right) > 0:
            if left[0] <= right[0]:
                result.append(left.pop(0))
            else:
                result.append(right.pop(0))
        if len(left) > 0:
            result += left
        if len(right) > 0:
            result += right
        return result

# Testing code
def main():
    items = [5, 2, 9, 1, 3, 4, 7, 6, 8]
    print("Original list:", items)
    sorted_items = MergeSort().sort(items)
    print("Sorted list:", sorted_items)

if __name__ == "__main__":
    main()