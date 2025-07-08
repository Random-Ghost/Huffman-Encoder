from typing import Self


class Node:
    # this is a binary tree implementation so each node only has two children.
    # since it is a Huffman tree, it has a char if it is a leaf node.
    # when each node is created, we will already know if its children.
    # we do not need to know a node's parent since we will only be traversing from the root down.
    leaf: bool
    key: str
    value: int
    left: Self
    right: Self

    def __init__(self, leaf: bool = False, key: str = None, value: int = None, left: Self = None, right: Self = None):
        self.leaf = leaf
        self.key = key
        self.value = value
        if not leaf:
            self.left = left
            self.right = right
            self.key = "in"
            self.value = left.value + right.value

    def __repr__(self):
        if self.leaf:
            return self.key + " : " + str(self.value)
        return (self.left.key + " : " + str(self.left.value) + " <- " + self.key + " : " + str(self.value) + " -> "
                + self.right.key + " : " + str(self.right.value))

    def __lt__(self, other):
        return self.value < other.value
