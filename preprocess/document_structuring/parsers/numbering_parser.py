from preprocess.document_reader import Numbering

from preprocess.document_structuring.node import Node


def find_numbering_parent(leaf: Node, numbering: Numbering):
    node = leaf
    while not node.is_root():
        if node.paragraph.has_numbering():
            if numbering.is_subsequence_of(node.paragraph.numbering):
                return node.parent

            if numbering.is_subitem_of(node.paragraph.numbering):
                return node

        node = node.parent

    return node


class NumberingParser:
    @staticmethod
    def run(current_node: Node, new_node: Node):
        if not new_node.paragraph.has_numbering() \
                or new_node.paragraph.numbering.is_initial():
            return False

        node = find_numbering_parent(current_node, new_node.paragraph.numbering)
        if not node.is_root() \
                and node.paragraph.has_numbering() \
                and node.paragraph.indentation > new_node.paragraph.indentation + 3:
            return False

        if node.is_root():
            return False

        node.add_child(new_node)
        new_node.parser_name = 'NumberingParser'
        return True
