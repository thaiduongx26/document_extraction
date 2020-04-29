from preprocess.document_structuring.node import Node


class TableParser:
    """ Table row always take the direct above paragraph as parent
    """

    @staticmethod
    def run(current_node: Node, new_node: Node):
        if new_node.paragraph.is_table():
            node = current_node
            if not node.can_has_child():
                node = node.parent

            node.add_child(new_node)
            new_node.parser_name = __class__.__name__
            return True

        return False
