import logging
from typing import List

from .paragraph import Paragraph

logger = logging.getLogger(__name__)


class HTML:
    def __init__(self, file_name: str):
        self.file_name: str = file_name
        self.paragraphs: List[Paragraph] = []

    def __iter__(self):
        for text_block in self.paragraphs:
            yield text_block

    def load(self):
        logger.info(f'Loading {self.file_name}')

        from . import LibreOfficeHTMLParser
        parser = LibreOfficeHTMLParser()
        with open(self.file_name, 'r', encoding='utf8') as f:
            for line in f:
                parser.feed(line)
            else:
                self.paragraphs = parser.paragraphs

        for index, paragraph in enumerate(self.paragraphs, 1):
            paragraph.index_ = index

        return self
