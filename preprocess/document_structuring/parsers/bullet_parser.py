# All bullet lines are sibling
from preprocess.document_structuring.node import Node


class BulletParser:
    @staticmethod
    def run(current_node: Node, new_node: Node):
        node = current_node
        if new_node.paragraph.has_bullet() and node.paragraph.has_bullet() \
                and node.paragraph.bullet == new_node.paragraph.bullet:
            if node.paragraph.has_numbering():
                node.add_child(new_node)
            else:
                node.parent.add_child(new_node)
            new_node.parser_name = 'BulletParser'
            return True

        return False
