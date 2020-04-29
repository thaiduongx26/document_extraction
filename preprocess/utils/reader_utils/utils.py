import logging
from typing import List

logger = logging.getLogger(__name__)


def launch(filename: str):
    """ Launch (open) the file with its associated application.
    :param filename: name of the file to be launched.
    """
    import os
    if os.path.exists(filename):
        cmd = 'start' if os.name == 'nt' else 'xdg-open'
        os.system(f'{cmd} {os.path.abspath(filename)}')
    else:
        logger.error(f'ERROR: file does not exist (while launching {filename})')


def find_longest_common_string(a: str, b: str, ignore_white_char=True):
    """ Find the longest common string of `a` and `b`
    :param a: string
    :param b: string
    :param ignore_white_char: will ignore all white character if True, default: True
    :return: a namedtuple('Match', 'a, b, a_index, b_index, size, score')
    """
    from difflib import SequenceMatcher
    from collections import namedtuple

    Match = namedtuple('Match', 'a, b, index_a, index_b, size, score')

    if ignore_white_char:
        a = normalize_white_char(a)
        b = normalize_white_char(b)

    match = SequenceMatcher(None, a, b).find_longest_match(0, len(a), 0, len(b))
    score = 1 if len(a) == len(b) == 0 else match.size / max(len(a), len(b))
    if a[match.a:match.a + match.size].strip() == '':
        score = 0

    return Match(a, b, match.a, match.b, match.size, score)


def normalize_white_char(s: str):
    """ Replace all unicode white characters with ASCII space
    :param s: string to be normalized
    :return: a normalized string
    """
    import re
    return re.sub(r'\s+', ' ', s, flags=re.UNICODE)


def convert_docx_to_html(filename: str) -> str:
    """ Convert document to .html format using soffice utility provided by libreoffice
    The output file will be placed in `.cache` folder, which is in the same folder with the
    original file. Name of the output file is the same with the input file, different in extension.
    :param filename: path/name of the file to be converted from
    :return: the path of the converted .html file
    """
    from pathlib import Path
    outdir: Path = Path(filename).parent.joinpath('.cache')

    logger.info(f'Converting {filename} to HTML')

    from os import system
    if system(f'soffice --headless --convert-to html --outdir {outdir} {filename}'):
        raise Exception('Cannot convert {filename} to html with soffice')
    else:
        return str(outdir.joinpath(filename).with_suffix('.html'))


def setup_worksheet(workbook, headers: List[str], col_widths: List[int], name: str = 'Sheet1'):
    """ Setup worksheet with provided header and column widths.
    The worksheet is named 'Sheet1' and has frozen header row.
    :param workbook: the workbook where worksheet will be created.
    :param headers: column headers of the worksheet.
    :param col_widths: the widths of each column in the worksheet.
    :param name: name of the sheet to be created, default: `Sheet1`.
    :return: the worksheet, which has been set up.
    """
    worksheet = workbook.add_worksheet('Sheet1')
    header_format = workbook.add_format(dict(align='center', bold=True))

    for index, headers in enumerate(headers):
        worksheet.write_string(0, index, headers, header_format)

    worksheet.freeze_panes(1, 0)

    for i, width in enumerate(col_widths):
        worksheet.set_column(i, i, width)

    return worksheet


def write_excel_row(worksheet, row_index: int, cells: List):
    for index, cell in enumerate(cells):
        import numbers
        writer = worksheet.write_number if \
            isinstance(cell, numbers.Number) else worksheet.write_string

        writer(row_index, cell, cell)
