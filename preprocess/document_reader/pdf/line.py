from operator import itemgetter
from typing import List

from .. import Numbering
from ..bullet import Bullet
from .style import ALIGNMENT, Font


class Line:

    def __init__(self, page):
        self.page = page
        self.words: List = []

    def __repr__(self):
        return self.text

    @property
    def text(self):
        t = ' '.join([word['text'] for word in self.words])
        if t.startswith('(cid:190)'):
            t = t.replace('(cid:190)', '􀂾', 1)
        return t

    @property
    def bbox(self) -> tuple:
        return self.x0, self.top, self.x1, self.bottom

    @property
    def x0(self):
        return min(map(itemgetter('x0'), self.words))

    @property
    def x1(self):
        return max(map(itemgetter('x1'), self.words))

    @property
    def top(self):
        return min(map(itemgetter('top'), self.words))

    @property
    def bottom(self):
        return max(map(itemgetter('bottom'), self.words))

    @property
    def bullet(self):
        return Bullet(self.words[0]['text'])

    def has_bullet(self):
        return not self.bullet.is_empty()

    @property
    def numbering(self):
        return Numbering(self.text)

    def has_numbering(self):
        return not self.numbering.is_empty()

    @property
    def length(self):
        return self.x1 - self.x0

    def is_blank(self):
        return len(self.words) == 0

    @property
    def alignment(self):
        from .utils import page_utils
        x0, _, x1, _ = page_utils.get_text_area(self.page)
        canvas_width = x1 - x0

        left_margin = self.x0 - x0
        right_margin = x1 - self.x1

        if abs(left_margin - right_margin) < ALIGNMENT.THRESHOLD:
            return ALIGNMENT.CENTER

        if left_margin > canvas_width / 2:
            return ALIGNMENT.RIGHT

        if right_margin > canvas_width / 2:
            return ALIGNMENT.LEFT

        return ALIGNMENT.UNKNOWN

    def add(self, word):
        self.words.append(word)

    def get_first_char_font(self) -> Font:
        first_char = self.words[0]['chars'][0]
        font_face = first_char['fontname']
        font_size = first_char['size']

        return Font(font_face, font_size)

    def get_last_char_font(self):
        last_char = self.words[-1]['chars'][0]
        font_face = last_char['fontname']
        font_size = last_char['size']
        return Font(font_face, font_size)
