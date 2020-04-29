import itertools
from typing import List

from pdfplumber.page import Page

from ..table import Table


def extract_tables(page: Page):
    tables = []
    plumber_tables = page.find_tables()
    for table in plumber_tables:
        if len(table.rows) > 1 and len(table.cells) > 1.5 * len(table.rows):
            tables.append(Table(table))

    return tables


def is_within_any_table(word, tables: List[Table]) -> bool:
    """ Check if a `word` is within any of the `tables`
    """
    x0, top = word['x0'], word['top']
    for tbl in tables:
        if tbl.x0 <= x0 <= tbl.x1 and tbl.top <= top <= tbl.bottom:
            return True

    return False


def remove_words_within_table(words, tables):
    return [word for word in words if not is_within_any_table(word, tables)]
