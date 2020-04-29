from preprocess.document_structuring.node import Node


def get_ol_index(node: Node) -> int:
    for tag in reversed(node.paragraph.layout['tags']):
        if 'ol_index' in tag:
            ol_index = int(tag.split(':')[-1])
            return ol_index


class HTMLOLParser:
    @staticmethod
    def run(current_node: Node, new_node: Node):
        ol_index = get_ol_index(new_node)
        if ol_index is not None:
            found = current_node.find_up(lambda node: get_ol_index(node) == ol_index)
            if not found.is_root():
                found.parent.add_child(new_node)
                new_node.parser_name = __class__.__name__
                return True

        return False
