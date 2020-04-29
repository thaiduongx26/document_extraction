from typing import List

from . import NegativeBaseRule
from ..line import Line
from ..paragraph import Paragraph
from ..style import ALIGNMENT


class YokoRightAlignment(NegativeBaseRule):
    def run(self, paragraph: Paragraph, lines: List[Line], index: int, **kwargs):
        line = lines[index]
        if line.alignment == ALIGNMENT.RIGHT or paragraph.alignment == ALIGNMENT.RIGHT:
            return False
