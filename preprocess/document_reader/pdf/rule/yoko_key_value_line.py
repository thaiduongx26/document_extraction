from typing import List

from . import NegativeBaseRule
from ..line import Line
from ..paragraph import Paragraph


class YokoKeyValueLine(NegativeBaseRule):
    def run(self, paragraph: Paragraph, lines: List[Line], index: int, **kwargs):
        line = lines[index]
        pline = paragraph.lines[-1]

        text = line.text + pline.text
        text = text.replace('：', ':')

        half_page_width = kwargs['page'].width * 4 / 5

        if text.find(':') > 0 \
                and (line.length < half_page_width or pline.length < half_page_width):
            return False
