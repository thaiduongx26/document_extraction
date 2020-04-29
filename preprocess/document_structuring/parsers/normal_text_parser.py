from preprocess.document_structuring.node import Node


class NormalTextParser:
    """ Add the new node as a sibling of the current node.
    """

    @staticmethod
    def run(current_node: Node, new_node: Node):
        current_node.parent.add_child(new_node)
        new_node.parser_name = __class__.__name__
        return True
