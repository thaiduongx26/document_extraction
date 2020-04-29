from typing import List

from . import NegativeBaseRule
from ..line import Line
from ..paragraph import Paragraph


class LineLength(NegativeBaseRule):
    def __init__(self, threshold=0.05):
        self.threshold = threshold

    def run(self, paragraph: Paragraph, lines: List[Line], index: int, **kwargs):
        """ If the `line` is much shorter than the paragraph, the it shouldn't belong to the paragraph.
        Example:
            aaaaaaaaaaaa
            aaaaaaaaaaaa
            aaaaaa
            aaaaaaaaaaaa <-- this one shouldn't belong to the previous paragraph.
        """
        # Previous line shorter than current line

        length_diff = lines[index].x1 - paragraph.lines[-1].x1
        if length_diff > float(kwargs['page'].width) * self.threshold:
            return False

        if len(paragraph.lines) == 1 and paragraph.lines[-1].x1 < kwargs['page'].width * 2 / 3:
            return False
