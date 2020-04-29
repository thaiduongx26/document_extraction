from abc import ABC, abstractmethod
from typing import Any

from .bullet import Bullet
from .numbering import Numbering


class Paragraph(ABC):
    def __init__(self):
        """ Base class for Paragraph classes such as HTMLParagraph or PDFParagraph.
        """
        self.index = 0

    def __str__(self):
        return self.all_text

    def __repr__(self):
        import json
        return json.dumps({
            'bullet_indentation': self.bullet.indentation,
            'bullet_text': self.bullet.text,
            'numbering_indentation': self.numbering.indentation,
            'numbering_text': self.numbering.text,
            'paragraph_indentation': self.indentation,
            'paragraph_text': self.text,
            'title': self.title,
            'is_title': self.is_title,
            'layout': self.layout
        }, ensure_ascii=False, indent=2)

    def __iter__(self):
        for text in [self.bullet.text, self.numbering.text, self.text]:
            yield text

    @property
    @abstractmethod
    def all_text(self) -> str:
        """ All text in the paragraph.
        :return: string represent all the text in the paragraph.
        """
        return ' '.join([self.bullet.text, self.numbering.text, self.text])

    @property
    @abstractmethod
    def bullet(self) -> Bullet:
        pass

    @property
    @abstractmethod
    def numbering(self) -> Numbering:
        pass

    @property
    @abstractmethod
    def text(self) -> str:
        """Abstract getter for paragraph text.
        :return: string represents the text in the paragraph(without bullet and numbering part).
        """
        pass

    @property
    @abstractmethod
    def indentation(self) -> int:
        """Abstract getter for paragraph indentation.
        :return: indentation of the paragraph.
        """
        pass

    @property
    @abstractmethod
    def title(self) -> str:
        """Abstract getter for title of the paragraph.
        Title is the initial text of the paragraph with emphasis style(bold or italic).
        :return: string represents title of the paragraph, if any.
        """
        return ''

    @abstractmethod
    def is_title(self) -> bool:
        """Abstract getter for indicator of the paragraph is a title.
        A paragraph is a title if the format or layout suggest it is a title.
        For example: an all capitalized text with center alignment.
        :return: boolean value to indicate whether the paragraph is a title or not.
        """
        return False

    @property
    @abstractmethod
    def layout(self) -> Any:
        """Abstract getter for layout attribute.
        Layout includes position, alignment of the paragraph
        :return: a dictionary with layout information.
        """
        return dict()

    @property
    @abstractmethod
    def page_number(self) -> int:
        """ Getter for page number of the current paragraph.
        :return: page number of the paragraph.
        """
        return 0

    def has_numbering(self) -> bool:
        return not self.numbering.is_empty()

    def has_bullet(self) -> bool:
        return not self.bullet.is_empty()

    def is_table(self) -> bool:
        return False
