from typing import List

from . import NegativeBaseRule
from ..line import Line
from ..paragraph import Paragraph


class LineDistance(NegativeBaseRule):
    def __init__(self, distance_threshold=5):
        self.distance_threshold = distance_threshold

    def run(self, paragraph: Paragraph, lines: List[Line], index: int, **kwargs):
        """ `lines[index]` should not belong to `paragraph` if the distance between the two lines are too big.
        """
        line_distance = lines[index].top - paragraph.bottom
        if line_distance > self.distance_threshold:
            return False
