class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

class Tree:
    def __init__(self):
        self.root = None

    def insert(self, value):
        if self.root is None:
            self.root = Node(value)
            return
        current = self.root
        while True:
            if value < current.value:
                if current.left is None:
                    current.left = Node(value)
                    return
                current = current.left
            else:
                if current.right is None:
                    current.right = Node(value)
                    return
                current = current.right

    def __iter__(self):
        return TreeTraverser(self.root, reverse=False)

    def __reversed__(self):
        return TreeTraverser(self.root, reverse=True)

class TreeTraverser:
    def __init__(self, root, reverse=False):
        self.root = root
        self.reverse = reverse
        self.stack = []
        self.current = root

    def __iter__(self):
        return self

    def __next__(self):
        while self.current is not None or self.stack:
            while self.current is not None:
                self.stack.append(self.current)
                if self.reverse:
                    self.current = self.current.right
                else:
                    self.current = self.current.left
            if self.stack:
                self.current = self.stack.pop()
                val = self.current.value
                if self.reverse:
                    self.current = self.current.left
                else:
                    self.current = self.current.right
                return val
        raise StopIteration

if __name__ == "__main__":
    t = Tree()
    t.insert(5)
    t.insert(3)
    t.insert(7)
    t.insert(2)
    t.insert(4)
    print("Forward:")
    for v in t:
        print(v)
    print("Reverse:")
    for v in reversed(t):
        print(v)
    empty = Tree()
    print("Empty tree:")
    for v in empty:
        print(v)