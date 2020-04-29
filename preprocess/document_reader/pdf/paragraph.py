from typing import List, Any

from .line import Line
from .style import Font, ALIGNMENT
from .. import Numbering
from ..paragraph import Paragraph as BaseParagraph


class Paragraph(BaseParagraph):
    @property
    def title(self) -> str:
        return ''

    @property
    def numbering(self) -> Numbering:
        return Numbering(self.text)

    def __init__(self):
        self.lines: List[Line] = []

    def __str__(self):
        return self.all_text

    def __repr__(self):
        import json
        return json.dumps({
            'paragraph_indentation': self.indentation,
            'paragraph_text': self.text,
            'is_title': self.is_title,
            'layout': self.layout
        }, ensure_ascii=False, indent=2)

    @property
    def all_text(self) -> str:
        return self.text

    @property
    def indentation(self) -> int:
        return self.x0

    @property
    def layout(self) -> Any:
        return dict(
            alignment=self.alignment,
            font_size=self.get_fist_char_font().size
        )

    @property
    def page_number(self) -> int:
        return self.lines[0].page.page_number

    @property
    def text(self):
        return ' '.join([line.text for line in self.lines])

    @property
    def bbox(self) -> tuple:
        return self.x0, self.top, self.x1, self.bottom

    @property
    def x1(self):
        return max((line.bbox[2] for line in self.lines))

    @property
    def x0(self):
        return min([line.bbox[0] for line in self.lines])

    @property
    def top(self):
        return min([line.bbox[1] for line in self.lines])

    @property
    def bottom(self):
        return max([line.bbox[3] for line in self.lines])

    @property
    def bullet(self):
        return self.lines[0].bullet

    def has_bullet(self):
        return not self.bullet.is_empty()

    @property
    def alignment(self):
        if self.is_empty():
            return ALIGNMENT.UNKNOWN

        shortest_line = self.lines[0]
        for line in self.lines:
            if shortest_line.length < line.length:
                shortest_line = line

        return shortest_line.alignment

    def get_fist_char_font(self) -> Font:
        return self.lines[0].get_first_char_font()

    def get_last_char_font(self) -> Font:
        return self.lines[-1].get_last_char_font()

    def is_title(self) -> bool:
        first_char_font = self.get_fist_char_font()
        last_char_font = self.get_last_char_font()

        if first_char_font.is_bold() and last_char_font.is_bold():
            return True

        if first_char_font.is_italic() and last_char_font.is_italic():
            return True

        font_size_title = 11.5
        if first_char_font.size > font_size_title and last_char_font.size > font_size_title:
            return True

        if len(self.text) > 2:
            if self.text.startswith('【') and self.text.endswith('】'):
                return True

        return False

    def is_empty(self):
        return len(self.lines) == 0

    def add(self, line_segment):
        self.lines.append(line_segment)
