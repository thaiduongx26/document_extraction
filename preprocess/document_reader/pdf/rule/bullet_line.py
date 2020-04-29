from typing import List

from . import NegativeBaseRule
from ..line import Line
from ..paragraph import Paragraph


class BulletLine(NegativeBaseRule):
    def run(self, paragraph: Paragraph, lines: List[Line], index: int, **kwargs):
        """ if `lines[index]` holds a bullet then it should be on a new paragraph.
        """
        if lines[index].has_numbering():
            return False
