class DataContainer:
    def __init__(self, items=None):
        self._items = list(items) if items else []
        self._filters = []
        self._transforms = []
    
    def add_item(self, item):
        self._items.append(item)
    
    def add_filter(self, filter_func):
        self._filters.append(filter_func)
        return self
    
    def add_transform(self, transform_func):
        self._transforms.append(transform_func)
        return self
    
    def __iter__(self):
        return DataTraverser(self._items, self._filters, self._transforms)


class DataTraverser:
    def __init__(self, items, filters=None, transforms=None):
        self._items = items
        self._filters = filters or []
        self._transforms = transforms or []
        self._index = 0
        self._processed_items = None
        self._prepare_items()
    
    def _prepare_items(self):
        self._processed_items = list(self._items)
        
        for filter_func in self._filters:
            self._processed_items = [item for item in self._processed_items if filter_func(item)]
        
        for transform_func in self._transforms:
            self._processed_items = [transform_func(item) for item in self._processed_items]
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self._index >= len(self._processed_items):
            raise StopIteration
        
        item = self._processed_items[self._index]
        self._index += 1
        return item
    
    def __len__(self):
        return len(self._processed_items)
    
    def reset(self):
        self._index = 0
        return self


class ReversibleContainer(DataContainer):
    def __init__(self, items=None):
        super().__init__(items)
        self._reverse = False
    
    def set_reverse(self, reverse=True):
        self._reverse = reverse
        return self
    
    def __iter__(self):
        return ReversibleTraverser(self._items, self._filters, self._transforms, self._reverse)


class ReversibleTraverser(DataTraverser):
    def __init__(self, items, filters=None, transforms=None, reverse=False):
        super().__init__(items, filters, transforms)
        self._reverse = reverse
        if self._reverse:
            self._processed_items.reverse()


class BatchTraverser(DataTraverser):
    def __init__(self, items, batch_size, filters=None, transforms=None):
        super().__init__(items, filters, transforms)
        self._batch_size = max(1, batch_size)
    
    def __next__(self):
        if self._index >= len(self._processed_items):
            raise StopIteration
        
        batch = self._processed_items[self._index:self._index + self._batch_size]
        self._index += self._batch_size
        return batch


def create_batch_sequence(container, batch_size):
    return BatchTraverser(container._items, batch_size, container._filters, container._transforms)


if __name__ == "__main__":
    numbers = DataContainer([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    
    filtered_numbers = numbers.add_filter(lambda x: x % 2 == 0).add_transform(lambda x: x * 2)
    
    print("Filtered and transformed:")
    for item in filtered_numbers:
        print(item, end=" ")
    print()
    
    words = ReversibleContainer(["apple", "banana", "cherry", "date"])
    words.add_filter(lambda x: len(x) > 4).set_reverse(True)
    
    print("Reversed filtered words:")
    for word in words:
        print(word, end=" ")
    print()
    
    data = DataContainer(range(1, 11))
    batch_processor = create_batch_sequence(data, 3)
    
    print("Batched processing:")
    for batch in batch_processor:
        print(f"Batch: {batch}")
    
    traverser = DataTraverser([10, 20, 30])
    print(f"Length: {len(traverser)}")
    
    for item in traverser:
        print(f"Item: {item}")
    
    traverser.reset()
    print("After reset:")
    for item in traverser:
        print(f"Item: {item}")