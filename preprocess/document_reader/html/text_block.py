from typing import List


class TextBlock:
    def __init__(self, text: str, tags: List):
        """ Represents a block of text under a certain tag.
        Typically, one paragraph may consists of one or more text block.
        :param text: text under certain tag.
        :param tags: stack of tags of the current text.
        """
        self.text = text
        self.tags = tags
