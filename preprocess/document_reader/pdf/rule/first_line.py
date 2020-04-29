from typing import List

from . import PositiveBaseRule
from ..line import Line
from ..paragraph import Paragraph


class FirstLine(PositiveBaseRule):
    def run(self, paragraph: Paragraph, lines: List[Line], index: int, **kwargs):
        if paragraph.is_empty():
            return True
