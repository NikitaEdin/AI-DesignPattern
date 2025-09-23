class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None

class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def append(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node
        self.size += 1

    def is_empty(self):
        return self.head is None

class Cursor:
    def __init__(self, lst):
        self.lst = lst
        self.reset()

    def reset(self):
        self.current = None
        self.last_accessed = None
        self.last_direction = None

    def __iter__(self):
        self.reset()
        return self

    def __next__(self):
        return self.forward()

    def forward(self):
        if self.current is None:
            if self.lst.is_empty():
                raise StopIteration
            self.current = self.lst.head
        else:
            if self.current.next is None:
                raise StopIteration
            self.current = self.current.next
        self.last_accessed = self.current
        self.last_direction = 'forward'
        return self.current.data

    def prev(self):
        if self.current is None:
            if self.lst.is_empty():
                raise ValueError("Cannot traverse backward: list is empty")
            self.current = self.lst.tail
        else:
            if self.current.prev is None:
                raise ValueError("Cannot traverse backward: at the beginning")
            self.current = self.current.prev
        self.last_accessed = self.current
        self.last_direction = 'backward'
        return self.current.data

    def remove(self):
        if self.last_accessed is None:
            raise ValueError("No last accessed element to remove")
        node = self.last_accessed
        prev_n = node.prev
        next_n = node.next
        if prev_n is not None:
            prev_n.next = next_n
        else:
            self.lst.head = next_n
        if next_n is not None:
            next_n.prev = prev_n
        else:
            self.lst.tail = prev_n
        self.lst.size -= 1
        if self.last_direction == 'forward':
            self.current = prev_n
        elif self.last_direction == 'backward':
            self.current = next_n
        self.last_accessed = None

if __name__ == "__main__":
    lst = LinkedList()
    lst.append("A")
    lst.append("B")
    lst.append("C")
    cursor = Cursor(lst)
    print("Forward traversal:")
    for item in cursor:
        print(item)
    cursor.reset()
    print("Backward traversal:")
    try:
        while True:
            print(cursor.prev())
    except ValueError:
        pass
    cursor.reset()
    print("Forward with removal of B:")
    for item in cursor:
        print(item)
        if item == "B":
            cursor.remove()
    cursor.reset()
    print("Backward with removal of B:")
    try:
        while True:
            item = cursor.prev()
            print(item)
            if item == "B":
                cursor.remove()
    except ValueError:
        pass
    empty_lst = LinkedList()
    empty_cursor = Cursor(empty_lst)
    try:
        next(empty_cursor)
    except StopIteration:
        print("Empty list handled correctly for forward.")
    try:
        empty_cursor.prev()
    except ValueError:
        print("Empty list handled correctly for backward.")