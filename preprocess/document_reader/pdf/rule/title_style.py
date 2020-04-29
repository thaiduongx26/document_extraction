from typing import List

from . import PositiveBaseRule
from ..line import Line
from ..paragraph import Paragraph


class TitleStyle(PositiveBaseRule):
    def __init__(self, font_size_threshold=13):
        self.font_size_threshold = font_size_threshold

    def run(self, paragraph: Paragraph, lines: List[Line], index: int, **kwargs):
        """ Lines with identical strong style(big font, bold) usually is title and should be in the same paragraph
        """
        if paragraph.get_last_char_font().size > self.font_size_threshold \
                and paragraph.get_last_char_font() == lines[index].get_first_char_font():
            return True
