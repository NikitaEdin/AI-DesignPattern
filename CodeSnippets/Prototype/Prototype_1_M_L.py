import copy

class LinkedList():
    def __init__(self, value):
        self.value = value
        self.next = None

    def clone(self):
        new_list = LinkedList(self.value)
        current = self.next
        while current:
            new_node = LinkedList(current.value)
            new_list.next = new_node
            new_list = new_node
            current = current.next
        return new_list


if __name__ == "__main__":
    linked_list = LinkedList("head")
    node1 = LinkedList("first")
    node2 = LinkedList("second")
    node3 = LinkedList("third")
    linked_list.next = node1
    node1.next = node2
    node2.next = node3

    cloned_list = linked_list.clone()
    print(cloned_list)  # prints "head"
    print(linked_list is cloned_list)  # prints "False"