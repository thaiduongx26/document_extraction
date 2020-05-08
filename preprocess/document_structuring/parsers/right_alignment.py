from ..node import Node
from ...document_reader.pdf.style import ALIGNMENT


class RightAlignmentParser:
    """ Table row always take the direct above paragraph as parent
    """

    @staticmethod
    def run(current_node: Node, new_node: Node):
        node = current_node
        # print(" new_node.paragraph.is_table(): ", new_node.paragraph.is_table())
        # print("new_node.paragraph.layout['alignment']: ", new_node.paragraph.layout)
        if not new_node.paragraph.is_table() and new_node.paragraph.layout['alignment'] == ALIGNMENT.RIGHT:
            if not node.paragraph.is_table() and node.paragraph.layout['alignment'] == ALIGNMENT.RIGHT:
                node = current_node.parent

            if not node.can_has_child():
                node = node.parent

            node.add_child(new_node)
            new_node.parser_name = __class__.__name__
            return True
        else:
            return False
