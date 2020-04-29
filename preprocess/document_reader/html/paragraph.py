import logging
from typing import List, Dict

from .text_block import TextBlock
from ..bullet import Bullet
from ..numbering import Numbering
from ..paragraph import Paragraph as BaseParagraph

logger = logging.getLogger(__name__)


def _remove_first_word(text_blocks: List[TextBlock]):
    first_block = text_blocks[0]
    first_word_text = first_block.text.strip().split()[0]
    remaining_text = first_block.text.strip().lstrip(first_word_text).strip()

    if remaining_text:
        first_block.text = remaining_text
    else:
        del text_blocks[0]


class Paragraph(BaseParagraph):

    def __init__(self, text_blocks: List[TextBlock] = None):
        """ Represents a paragraph, which is the text within tag p, typically.
        One paragraph may consist of one or more text block.
        :param text_blocks: list of text block within this paragraph.
        """
        self.text_blocks = [] if text_blocks is None else text_blocks
        self.index_ = 0

        self.is_parsed_ = False
        self.bullet_ = Bullet()
        self.numbering_ = Numbering()

    def _parse_bullet(self):
        try:
            first_block = self.text_blocks[0]
            bullet_text = first_block.text.strip().split()[0]

            if Bullet.is_valid(bullet_text):
                self.bullet_ = Bullet(bullet_text)
                _remove_first_word(self.text_blocks)
        except BaseException as e:
            logger.debug(f'Unable to parse bullet for paragraph: "{self}", due to "{e}"')

    def _parse_numbering(self):
        try:
            first_block = self.text_blocks[0]
            first_block_text = first_block.text.strip()
            first_word = first_block_text.split()[0]

            if Numbering.is_valid(first_word):
                self.numbering_ = Numbering(first_word)
                _remove_first_word(self.text_blocks)
        except BaseException as e:
            logger.exception(f'Unable to parse numbering for paragraph: "{self}", due to {e}')

    def _parse(self):
        if self.is_parsed_:
            return

        self.is_parsed_ = True

        self._parse_bullet()
        self._parse_numbering()

    def append(self, text_block: TextBlock):
        """ Append `text_block` to the paragraph.
        :param text_block: text block to be added to this paragraph.
        """
        self.text_blocks.append(text_block)

    @property
    def all_text(self) -> str:
        return ' '.join([tb.text for tb in self.text_blocks]).strip()

    @property
    def bullet(self) -> Bullet:
        self._parse()
        return self.bullet_

    @property
    def numbering(self) -> Numbering:
        self._parse()
        return self.numbering_

    @property
    def text(self) -> str:
        self._parse()
        return ' '.join([tb.text for tb in self.text_blocks])

    @property
    def indentation(self) -> int:
        self._parse()
        # TODO: to implement getter for `paragraph_indentation` property
        return 0

    @property
    def title(self) -> str:
        self._parse()
        title_blocks = []
        for tb in self.text_blocks:
            if 'b' in tb.tags or 'i' in tb.tags:
                title_blocks.append(tb)
            else:
                break

        return ' '.join([tb.text for tb in title_blocks])

    @property
    def is_title(self) -> bool:
        self._parse()
        return self.layout.get('size', 0) > 3 or \
               ((self.text == self.title or self.text.isupper()) and
                0 < len(self.title) < 80
                )

    @property
    def layout(self) -> Dict:
        self._parse()
        return dict(
            tags=self.text_blocks[0].tags
        ) if self.text_blocks else {}

    @property
    def index(self) -> int:
        return self.index_

    @property
    def page_number(self) -> int:
        return 0
