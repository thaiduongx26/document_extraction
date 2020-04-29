from typing import List

from . import NegativeBaseRule
from ..line import Line
from ..paragraph import Paragraph


class DotEnding(NegativeBaseRule):
    def run(self, paragraph: Paragraph, lines: List[Line], index: int, **kwargs):
        from ..utils.paragraph_utils import get_last_char
        if get_last_char(paragraph) in '。.!?':
            return False
