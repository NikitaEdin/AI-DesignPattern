class TreeNode:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

class TreeTraverser:
    def __init__(self, root, strategy='inorder'):
        self._root = root
        self._strategy = strategy
        self._current_index = 0
        self._values = []
        self._visited = set()
        self._generate_sequence()
    
    def _generate_sequence(self):
        if self._strategy == 'inorder':
            self._inorder_traversal(self._root)
        elif self._strategy == 'preorder':
            self._preorder_traversal(self._root)
        elif self._strategy == 'postorder':
            self._postorder_traversal(self._root)
        elif self._strategy == 'levelorder':
            self._levelorder_traversal(self._root)
    
    def _inorder_traversal(self, node):
        if node:
            self._inorder_traversal(node.left)
            self._values.append(node.value)
            self._inorder_traversal(node.right)
    
    def _preorder_traversal(self, node):
        if node:
            self._values.append(node.value)
            self._preorder_traversal(node.left)
            self._preorder_traversal(node.right)
    
    def _postorder_traversal(self, node):
        if node:
            self._postorder_traversal(node.left)
            self._postorder_traversal(node.right)
            self._values.append(node.value)
    
    def _levelorder_traversal(self, node):
        if not node:
            return
        queue = [node]
        while queue:
            current = queue.pop(0)
            self._values.append(current.value)
            if current.left:
                queue.append(current.left)
            if current.right:
                queue.append(current.right)
    
    def __iter__(self):
        self._current_index = 0
        return self
    
    def __next__(self):
        if self._current_index >= len(self._values):
            raise StopIteration
        value = self._values[self._current_index]
        self._current_index += 1
        return value
    
    def __len__(self):
        return len(self._values)
    
    def reset(self):
        self._current_index = 0
    
    def peek(self):
        if self._current_index < len(self._values):
            return self._values[self._current_index]
        return None
    
    def has_next(self):
        return self._current_index < len(self._values)
    
    def change_strategy(self, strategy):
        self._strategy = strategy
        self._values = []
        self._current_index = 0
        self._generate_sequence()

if __name__ == "__main__":
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.left.left = TreeNode(4)
    root.left.right = TreeNode(5)
    root.right.left = TreeNode(6)
    root.right.right = TreeNode(7)
    
    traverser = TreeTraverser(root, 'inorder')
    
    print("Inorder traversal:")
    for value in traverser:
        print(value, end=' ')
    print()
    
    traverser.change_strategy('preorder')
    print("Preorder traversal:")
    while traverser.has_next():
        print(traverser.__next__(), end=' ')
    print()
    
    traverser.change_strategy('levelorder')
    print("Level order traversal:")
    traverser.reset()
    for value in traverser:
        print(value, end=' ')
    print()
    
    print(f"Total nodes: {len(traverser)}")