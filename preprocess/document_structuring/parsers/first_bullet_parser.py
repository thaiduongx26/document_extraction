# All bullet lines are sibling
from preprocess.document_structuring.node import Node


class FirstBulletParser:
    @staticmethod
    def run(current_node: Node, new_node: Node):
        node = current_node
        if new_node.paragraph.has_bullet():
            node.parent.add_child(new_node)
            new_node.parser_name = 'BulletParser'
            return True

        return False
