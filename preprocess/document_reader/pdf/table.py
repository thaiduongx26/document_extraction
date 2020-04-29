from typing import Any

from pdfplumber.table import Table as PlumberTable

from .. import Numbering, Bullet
from ..paragraph import Paragraph as BaseParagraph


class TableRow(BaseParagraph):
    CELL_SEPARATOR = '|'

    def __init__(self, table, cells):
        super().__init__()
        self.table = table
        self.row_text = self.CELL_SEPARATOR.join([cell if cell is not None else '' for cell in cells])

    @property
    def all_text(self) -> str:
        return self.row_text

    @property
    def bullet(self) -> Bullet:
        return Bullet()

    @property
    def numbering(self) -> Numbering:
        return Numbering()

    @property
    def text(self) -> str:
        return self.row_text

    @property
    def indentation(self) -> int:
        return 0

    @property
    def title(self) -> str:
        return ''

    def is_title(self) -> bool:
        return False

    @property
    def layout(self) -> Any:
        return dict()

    @property
    def page_number(self) -> int:
        return self.table.page_number

    def is_table(self) -> bool:
        return True

    def is_empty(self) -> bool:
        return self.text == ''


class Table:
    def __init__(self, plumber_table: PlumberTable):
        self.plumber_table = plumber_table

    @property
    def bbox(self):
        return self.plumber_table.bbox

    @property
    def x0(self):
        return self.bbox[0]

    @property
    def top(self):
        return self.bbox[1]

    @property
    def x1(self):
        return self.bbox[2]

    @property
    def bottom(self):
        return self.bbox[3]

    @property
    def page_number(self):
        return self.plumber_table.page.page_number

    def to_list(self):
        return self.plumber_table.extract()

    def get_rows(self):
        extracted_table = self.plumber_table.extract()
        return [TableRow(self, cells) for cells in extracted_table]
