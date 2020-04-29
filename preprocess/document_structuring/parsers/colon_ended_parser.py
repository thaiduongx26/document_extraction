# This one is a context parser
from preprocess.document_structuring.node import Node


class ColonEndedParser:
    @staticmethod
    def run(current_node: Node, new_node: Node):
        if current_node.is_root():
            return False

        if current_node.paragraph.text.strip().endswith(':'):
            current_node.add_child(new_node)
            new_node.parser_name = __class__.__name__
            return True

        return False
