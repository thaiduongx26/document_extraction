from typing import List

from . import NegativeBaseRule
from ..line import Line
from ..paragraph import Paragraph
from ..style import ALIGNMENT


class AlignmentDifference(NegativeBaseRule):
    def run(self, paragraph: Paragraph, lines: List[Line], index: int, **kwargs):
        """ Lines with different alignment should be on different paragraph
        """
        line = lines[index]
        if paragraph.alignment != line.alignment \
                and paragraph.alignment != ALIGNMENT.UNKNOWN \
                and line.alignment != ALIGNMENT.UNKNOWN:
            return False
