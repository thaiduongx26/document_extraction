import logging
from html.parser import HTMLParser
from typing import List

from .paragraph import Paragraph
from .text_block import TextBlock

logger = logging.getLogger(__name__)


class LibreOfficeHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.paragraphs: List[Paragraph] = []
        self.current_paragraph = Paragraph()
        self.tags = []

        self.inBody = False
        self.ol_index = 0
        self.table_count = 0

    def _handle_attrs(self, tag, attrs):
        if tag == 'ol':
            self.tags.append(f'ol_index:{self.ol_index}')
            self.ol_index += 1
        elif tag == 'font':
            for key, value in attrs:
                if key in ('size', 'color'):
                    self.tags.append(f'{key}:{value}')
        elif tag == 'p':
            for key, value in attrs:
                if key == 'align':
                    self.tags.append(f'{key}:{value}')

    def handle_starttag(self, tag, attrs):
        if tag == "body":
            self.inBody = True
            return

        # Ignore data that is outside of the body tag
        if not self.inBody:
            return

        # TODO: ignore table for now
        if tag == 'table':
            self.table_count += 1
        if self.table_count > 0:
            return

        self.tags.append(tag)

        self._handle_attrs(tag, attrs)

    def handle_endtag(self, tag):
        if tag == 'body':
            self.inBody = False
            return

        if not self.inBody:
            return

        # TODO: ignore table for now
        if tag == 'table':
            self.table_count -= 1
            return
        if self.table_count > 0:
            return

        while self.tags:
            if self.tags.pop() == tag:
                break

        if tag == 'p':
            if self.current_paragraph.all_text.strip():
                self.paragraphs.append(self.current_paragraph)

            self.current_paragraph = Paragraph()

    def handle_data(self, data: str):
        data = data.strip()
        if all((self.inBody, self.table_count == 0, data)):
            self.current_paragraph.append(TextBlock(data, self.tags.copy()))

    def error(self, message):
        logger.warning(message)
