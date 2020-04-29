from preprocess.document_structuring.node import Node


class RootParser:
    """ If the current node is the root node, then add the new node as a child of the current node.
    This parser should be presented as the first parser in the parser list.
    """

    @staticmethod
    def run(current_node: Node, new_node: Node):
        if current_node.is_root():
            current_node.add_child(new_node)
            new_node.parser_name = __class__.__name__
            return True

        return False
