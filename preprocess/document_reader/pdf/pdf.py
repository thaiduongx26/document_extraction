import pdfplumber

import utils
from utils import Folder
from .utils import page_utils, table_utils, paragraph_utils
from ..utils.debug_helper import DebugHelper


class PDF:
    def __init__(self, filename: str):
        self.filename = filename

    def load(self):
        pdf = pdfplumber.open(self.filename)
        reflowed_document = []

        debug_helper = DebugHelper(Folder.working)
        for index, page in enumerate(pdf.pages):
            tables = table_utils.extract_tables(page)
            paragraphs, forced_stop = paragraph_utils.extract_paragraphs(page, tables)
            reflowed_page = page_utils.reflow(tables, paragraphs)

            reflowed_document.extend(reflowed_page)

            # Draw debug output
            if utils.enable_debug:
                debug_helper.generate_debug_image(page, paragraphs, f'{self.filename}-page-{index}.png')

            # image = debug_helper.generate_debug_image(page, page.extract_words(), f'{filename}-page-words-{index}.png')
            if forced_stop:
                break

        # Remove empty paragraph
        indices = []
        for index in range(len(reflowed_document)):
            if reflowed_document[index].is_empty():
                indices.append(index)
        for index in reversed(indices):
            del reflowed_document[index]

        # Add index to paragraph
        for index, paragraph in enumerate(reflowed_document):
            paragraph.index = index + 1

        return reflowed_document
