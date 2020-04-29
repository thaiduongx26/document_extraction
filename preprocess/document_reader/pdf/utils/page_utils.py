from typing import List

from pdfplumber.page import Page

# TODO: cache this function output
from ..paragraph import Paragraph
from ..table import Table
from ...utils.algorithm import find_first_index_of


def get_text_area(page: Page):
    words = page.extract_words()
    x0 = min([word['x0'] for word in words])
    top = min([word['top'] for word in words])
    x1 = max([word['x1'] for word in words])
    bottom = max([word['bottom'] for word in words])

    return x0, top, x1, bottom


def reflow(tables: List[Table], paragraphs: List[Paragraph]):
    flow = paragraphs.copy()
    tables.sort(key=lambda tbl: tbl.top)

    mappings = []
    for table in tables:
        index = find_first_index_of(paragraphs, lambda p: p.top > table.top)
        mappings.append(dict(index=index if index is not None else len(paragraphs), table=table))

    for mapping in reversed(mappings):
        for row in reversed(mapping['table'].get_rows()):
            flow.insert(mapping['index'], row)

    return flow
