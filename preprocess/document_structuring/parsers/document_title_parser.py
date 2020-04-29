from preprocess.document_structuring.node import Node


class DocumentTitleParser:
    def __init__(self):
        self.enable = True

    def run(self, current_node: Node, new_node: Node):
        if self.enable:
            self.enable = False

            if current_node.parent.is_root() and current_node.paragraph.text == '販売ニュース':
                current_node.add_child(new_node)
                new_node.is_document_title = True
                new_node.parser_name = __class__.__name__
            else:
                current_node.is_document_title = True
                return False

            return True

        return False
