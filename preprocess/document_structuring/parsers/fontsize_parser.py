from ..node import Node
from ...document_reader.pdf.style import ALIGNMENT


class FontSizeParser:
    """ Find the parent base on indentation of the nodes.
    """

    @staticmethod
    def run(current_node: Node, new_node: Node):

        node = current_node
        if not node.paragraph.is_table() and node.paragraph.layout['alignment'] != ALIGNMENT.RIGHT:
            if node.paragraph.layout['font_size'] > new_node.paragraph.layout['font_size'] + 1:
                if not node.can_has_child():
                    node = node.parent

                node.add_child(new_node)
                new_node.parser_name = __class__.__name__
                return True

        return False
