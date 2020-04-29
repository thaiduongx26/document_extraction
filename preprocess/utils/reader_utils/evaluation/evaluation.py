import logging
from collections import namedtuple
from typing import List

import xlsxwriter
from numpy.core.multiarray import ndarray
from pandas import read_excel
from xlsxwriter.format import Format
from xlsxwriter.worksheet import Worksheet

from utils import utils
from utils.evaluation import excel_utils as excel
from utils.evaluation.accuracy_meter import AccuracyMeter

logger = logging.getLogger(__name__)

Match = namedtuple('Match', 'a, b, score, index_a, index_b, length_a, length_b')


def evaluate(filename: str, ca: str, headers: list, main: str) -> AccuracyMeter:
    """ Evaluate the output of the module based on the ca.
    :param filename: output to be evaluated.
    :param ca: correct answer corresponding to the output.
    :param headers: header of the columns to be evaluated.
    :param main: header of the main column to be compared.
    :return: metric representing how good the output is.
    """
    try:
        a = read_excel(filename, dtype=str).loc[:, headers].fillna('').values
        b = read_excel(ca, dtype=str).loc[:, headers].fillna('').values

        return _make_report(filename + '.diff.xlsx', _match_all(a, b, headers.index(main)), a, b,
                            headers)
    except BaseException as e:
        logger.exception(e)
        return AccuracyMeter()


def _make_report(filename: str, matches: List[Match], a: ndarray, b: ndarray,
                 headers: List[str]) -> AccuracyMeter:
    """ Write evaluation result to excel file.
    :param filename: str, name of excel file where the result will be written.
    :param matches:  List[Match], represents the matching rows between the 2 dataset `a` and `b`.
    :param a: the first dataset to be compared.
    :param b: the second dataset to be compared.
    :param headers: the of the headers in the dataset.
    :return:
    """
    acc_meter = AccuracyMeter()
    with xlsxwriter.Workbook(filename) as workbook:
        worksheet = excel.setup_worksheet(workbook, headers,
                                          excel.get_optimal_col_widths(a, headers))

        row_index = 0
        for match in matches:
            for offset in range(max(match.length_a, match.length_b)):
                row_index += 1
                _write_row(worksheet, a, b, match, acc_meter, headers, row_index, offset,
                           workbook.add_format(),
                           workbook.add_format(dict(font_color='red')),
                           workbook.add_format(dict(font_color='purple')))
        else:
            excel.write_acc(workbook, worksheet, row_index + 2, len(headers), acc_meter)

        logger.info(f'ACCURACY: {acc_meter} -->{filename}')
        return acc_meter


def _write_row(worksheet: Worksheet, a: ndarray, b: ndarray, match: Match, acc_meter: AccuracyMeter,
               headers: List[str], row_index: int, offset: int, fmt_default: Format,
               fmt_highlight: Format, fmt_highlight2: Format):
    """ Write a row to `worksheet`
    :param worksheet: the worksheet where the new row(s) will be written.
    :param a: ndarray, represents the first dataset.
    :param b: ndarray,  represents the second dataset.
    :param match: Match, represents the current matching rows of the 2 dataset.
    :param acc_meter: AccuracyMeter, for calculating accuracy.
    :param headers: List of text of the headers of the dataset.
    :param row_index: index of the current writing row.
    :param offset: offset of the `row_index`, based on the number of the matching rows.
    :param fmt_default: format used for default cell.
    :param fmt_highlight: format used text in cell that different in position.
    :param fmt_highlight2: format used for text in cell that different in value.
    """
    write_rich = worksheet.write_rich_string
    write_normal = worksheet.write_string
    highlight = fmt_highlight if match.score < 0.99 else fmt_highlight2
    for col_index in range(len(headers)):
        text_a = a[match.index_a + offset, col_index] if match.index_a + offset < len(a) else ''
        text_b = b[match.index_b + offset, col_index] if match.index_b + offset < len(b) else ''
        if offset < match.length_a and offset < match.length_b:
            lcs = utils.find_longest_common_string(text_a, text_b)

            formatted_a, formatted_b = excel.get_formatted_text(lcs, highlight, fmt_default)

            write_rich(row_index, 2 * col_index, *formatted_a)
            write_rich(row_index, 2 * col_index + 1, *formatted_b)
            acc_meter.add(row_index, col_index, lcs.score, max(len(text_a), len(text_b)))
        elif offset < match.length_a:
            write_normal(row_index, 2 * col_index, text_a, highlight)

            acc_meter.add(row_index, col_index, 0, len(text_a))
        elif offset < match.length_b:
            write_normal(row_index, 2 * col_index + 1, text_b, highlight)
            acc_meter.add(row_index, col_index, 0, len(text_b))


def _match_one(a: List[str], index_a: int, b: List[str], index_b: int,
               matching_threshold: float = 0.3) -> Match:
    """ Find a match between dataset `a` at `index_a` and dataset `b` at `index_b`.
    :param a: the first dataset.
    :param index_a: the current index of the first dataset to find the matching.
    :param b: the second dataset.
    :param index_b: the current index of the second dataset to find the matching.
    :param matching_threshold: threshold to accept a match, default: 0.3 (30 percent).
    :return: Match, represents matching rows between the two data sets.
    """
    if index_a >= len(a):
        return Match('', ' '.join(b[index_b:]), 0,
                     index_a, index_b, 0, len(b) - index_b)

    if index_b >= len(b):
        return Match(' '.join(a[index_a:]), '', 0,
                     index_a, index_b, len(a) - index_a, 0)

    text_a = a[index_a]
    text_b = b[index_b]

    length_a, length_b = (1, _match_length(text_a, b, index_b)) if len(text_a) > len(
        text_b) else (_match_length(text_b, a, index_a), 1)

    m = utils.find_longest_common_string(
        ' '.join(a[index_a:index_a + length_a]),
        ' '.join(b[index_b:index_b + length_b]))

    if m.score < matching_threshold and m.index_a > 0 and m.index_b > 0:
        length_b = 0

    return Match(text_a, text_b, m.score, index_a, index_b, length_a, length_b)


def _match_all(a: ndarray, b: ndarray, col_index) -> List[Match]:
    """ Matching all row of column specified by `col_index` between 2 data sets `a` and `b`.
    :param a: the first dataset to be compared.
    :param b: the second dataset to be compared.
    :param col_index: index of the column in the data sets to be compared.
    :return: List[Match], represents the matching rows
    """
    index_a = index_b = 0
    result = []
    while index_a < len(a) or index_b < len(b):
        m = _match_one(a[:, col_index], index_a, b[:, col_index], index_b)
        index_a += m.length_a
        index_b += m.length_b
        result.append(m)

    return result


def _match_length(big_string: str, text_list: List[str], index: int) -> int:
    """ Find the number of adjacent element in `text_list` from `index` so that the joined string
     would be closest to `big_string` in length.
    :param big_string: the big_string.
    :param text_list: the list of text.
    :param index: the index of `text_list`.
    :return: the offset from index so that the joined text from `text_list`
     could be closed to `big_string` in length.
    """
    offset = 1
    while True:
        text = ' '.join(text_list[index:index + offset + 1])
        if len(text) > len(big_string) or index + offset >= len(text_list):
            return offset
        else:
            offset += 1
