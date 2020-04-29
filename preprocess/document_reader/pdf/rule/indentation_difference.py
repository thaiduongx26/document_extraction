from typing import List

from . import NegativeBaseRule
from ..line import Line
from ..paragraph import Paragraph


class IndentationDifference(NegativeBaseRule):
    def __init__(self, threshold=0.2):
        self.threshold = threshold

    def run(self, paragraph: Paragraph, lines: List[Line], index: int, **kwargs):
        """ A loose rule -> should be placed at the very bottom of the rule list.
        Lines with the same indentation should be in the same paragraph.
        """
        indentation_diff = abs(lines[index].x0 - paragraph.lines[-1].x0)
        diff_threshold = float(kwargs['page'].width) * self.threshold

        if indentation_diff > diff_threshold:
            return False
