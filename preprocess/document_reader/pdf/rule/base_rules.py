from typing import List

from ..line import Line
from ... import Paragraph


class BaseRule:
    def run(self, paragraph: Paragraph, lines: List[Line], index: int, **kwargs):
        """ Decide whether the line specified by `lines` and `index` belong to `paragraph`.
        """
        pass

    @property
    def name(self):
        return self.__class__.__name__

class NegativeBaseRule(BaseRule):
    def run(self, paragraph: Paragraph, lines: List[Line], index: int, **kwargs):
        """ Negative Rule states that the `lines[index]` shouldn't belong to `paragraph`.
        Return False or None.
        """
        return False


class PositiveBaseRule(BaseRule):
    def run(self, paragraph: Paragraph, lines: List[Line], index: int, **kwargs):
        """ Positive Rule states that `lines[index]` should belong to `paragraph`
        Return True or None
        """
        return True
