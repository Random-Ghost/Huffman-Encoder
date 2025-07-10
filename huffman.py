from tree import Node


def to_char_dict(sentence: str) -> dict[str, float]:
    n: int = len(sentence)
    per: float = 1 / n
    char_dict: dict[str, float] = {}
    for char in sentence:
        if char in char_dict.keys():
            char_dict[char] += per
        else:
            char_dict[char] = per
    return char_dict


def create_tree(node_list: list[Node]) -> Node:
    # this is used to create the node tree from the node list.
    # here we use the standard Huffman algorithm to arrange the tree.
    n = len(node_list)
    char_list = node_list
    for i in range(n - 1):
        # first we sort to make sure the lowest two are at the back of the list
        char_list = sorted(char_list, reverse=True)
        # we combine them to make a parent node
        temp_node = Node(leaf=False, left=char_list[-2], right=char_list[-1])
        # we remove the last two
        char_list.pop()
        char_list.pop()
        # then we add the new node to the list
        char_list.append(temp_node)
    # at the end, there will be one node left which should be the root node.
    return char_list[0]


class Huffman:
    root: Node

    def __init__(self, sentence: str = None, char_dict: dict[str, float] = None):
        self.encode_dict: dict[str, str] = {}  # this is initialized here as it is a mutable object.

        # if char_dict is none, we have to find the frequency of the characters.
        if char_dict is None:
            char_dict: dict[str, float] = to_char_dict(sentence)

        # we convert it to a node list.
        node_list: list[Node] = []
        for key, value in char_dict.items():
            node_list.append(Node(leaf=True, key=key, value=value))

        # now we can create the tree.
        self.root = create_tree(node_list)

        # now we can create the code dictionary.
        self.bin()

    def bin(self) -> None:  # this is just to create the binary dictionary for encoding.
        # it creates the encoding bits from the node tree.
        # now we have the tree, but we do not know where anything is on the tree
        # I will be using a BFS algorithm to do this.
        # we have a dictionary that we append nodes to when we reach them. We pop them when we scan them.
        # everything is saved to a dictionary.
        # we also have a dictionary we save root node values to.
        # we use 0 for left values and 1 for right values
        # we are assuming there are more than 2 characters in the encoder.
        char_dict: dict[Node, str] = {self.root.left: "0", self.root.right: "1"}
        while len(char_dict) >= 1:
            temp = next(iter(char_dict))  # this gives us the first key in the dictionary.
            # we should note that temp is a Node object.
            # if it is a leaf node, we remove it from the dictionary and add it to encode_dict.
            if temp.leaf:
                self.encode_dict[temp.key] = char_dict[temp]  # the value will be the binary representation
                char_dict.pop(temp)
            else:
                char_dict[temp.left] = char_dict[temp] + "0"
                char_dict[temp.right] = char_dict[temp] + "1"
                char_dict.pop(temp)

    def encode(self, sentence: str) -> str:
        # we only need to iterate through the characters and find their code in encode_dict.
        code: str = ""
        for char in sentence.lower():
            code += self.encode_dict[char]
        return code

    def decode(self, code: str) -> str:
        # we iterate through the characters. 0 moves to the left of the current node. 1 to the right.
        pos = self.root  # we start at the root node and move down the tree.
        sentence: str = ""
        for char in code:
            if char == "0":
                pos = pos.left
            else:
                pos = pos.right
            # if we do not end up on a root node, we just move on to the next character.
            # but if we end up on a leaf node, we reset pos and add the key to the sentence.
            if pos.leaf:
                sentence += pos.key
                pos = self.root
        return sentence
