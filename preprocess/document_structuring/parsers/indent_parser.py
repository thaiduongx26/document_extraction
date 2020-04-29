from preprocess.document_structuring.node import Node


class IndentParser:
    """ Find the parent base on indentation of the nodes.
    """

    @staticmethod
    def run(current_node: Node, new_node: Node):

        node = current_node
        while not node.is_document_title and not node.is_root():
            if not node.paragraph.is_table():
                if node.paragraph.indentation < new_node.paragraph.indentation - 1:
                    break

                if abs(node.paragraph.indentation - new_node.paragraph.indentation) < 1:
                    if node.paragraph.has_numbering():
                        break
                    node = node.parent
                    break

            node = node.parent

        if not node.can_has_child():
            node = node.parent

        node.add_child(new_node)
        new_node.parser_name = __class__.__name__

        return True
