from typing import List

from . import NegativeBaseRule
from ..line import Line
from ..paragraph import Paragraph


class YokoTitle(NegativeBaseRule):
    TITLE = '販売ニュース'

    def run(self, paragraph: Paragraph, lines: List[Line], index: int, **kwargs):
        def match_title(line):
            return line.text == self.TITLE \
                   and line.get_first_char_font().size > 15

        if match_title(lines[index]) or match_title(paragraph.lines[-1]):
            return False
