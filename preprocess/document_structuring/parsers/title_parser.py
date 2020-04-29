from preprocess.document_structuring.node import Node


class TitleParser:
    def run(self, current_node: Node, new_node: Node):
        """ Title will be in all UPPERCASE
        :param current_node:
        :param new_node:
        """

        text = new_node.content.text_block
        if text.is_uniform() and any(fmt in text.font_name().lower() for fmt in ('bold', 'italic')):
            new_node.content.is_title = True
            # Find the closet title which have smaller indent or bigger in font
            # TODO: consider alignment as well
            node = current_node
            while not node.is_root():
                if node.content.is_title:
                    # TODO: add more criteria: indentation, alignment
                    if node.content.text_block.font_size() > new_node.content.text_block.font_size():
                        node.add_child(new_node)
                        break
                node = node.parent
            else:
                node.add_child(new_node)

            new_node.parser_name = self.__class__.__name__
            return True

        return False
