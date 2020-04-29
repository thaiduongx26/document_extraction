from typing import List

from numpy.core.multiarray import ndarray


def get_formatted_text(match, format_highlight='', format_default=''):
    """Get representation of the diff with specific format
    :param match: representing the matching part
    :param format_highlight: style for different characters
    :param format_default: default style for matching text in a and b
    :return: a tuple of the two list a and b
    """

    def format(text: str, index: int, size: int) -> List:
        fmt = []
        if text[:index] != '':
            fmt.extend([format_highlight, text[:index]])
        if text[index:index + size] != '':
            fmt.extend([format_default, text[index:index + size]])
        if text[index + size:] != '':
            fmt.extend([format_highlight, text[index + size:]])

        fmt.extend([format_default, ' ', ' '])
        return fmt

    return format(match.a, match.index_a, match.size), format(match.b, match.index_b, match.size)


def get_optimal_col_widths(data: ndarray, header: List[str], max_width=100):
    """Get the appropriate width for all columns in `data` with `header`
    :param data: ndarray in which the size of the column needed to calculate/
    :param header: list of header text.
    :param max_width: The maximum allowed width.
    :return: a list of appropriate widths for all the columns in imputed DataFrame.
    """
    return [
        min(max_width, max([len(str(s)) for s in data[:, index]] + [len(header[index])]))
        for index in range(len(header))]


def setup_worksheet(workbook, header, col_widths):
    """ Setup worksheet with provided header and column widths.
    The worksheet is named 'Sheet1' and has freeze header row
    :param workbook: the workbook where worksheet will be created
    :param header: column headers of the worksheet
    :param col_widths: the widths of each column in the worksheet
    :return: the worksheet which has been set up
    """
    worksheet = workbook.add_worksheet('Sheet1')

    # Fill the header row
    for index, header in enumerate(header):
        header_format = workbook.add_format(dict(align='center', bold=True))
        worksheet.write_string(0, 2 * index, header, header_format)
        worksheet.write_string(0, 2 * index + 1, 'CA', header_format)

    # Freeze the first row
    worksheet.freeze_panes(1, 0)

    # set appropriate column widths
    for i, width in enumerate(col_widths):
        worksheet.set_column(2 * i, 2 * i, width)
        worksheet.set_column(2 * i + 1, 2 * i + 1, width)

    return worksheet


def write_acc(workbook, worksheet, row_index, col_count, acc_meter):
    """ Write accuracy metric to excel report file.
    :param workbook: excel report file.
    :param worksheet: report sheet.
    :param row_index: index of the row of the cell to be written.
    :param col_count: the total number of column in the dataset.
    :param acc_meter: AccuracyMeter, holding the accuracy data of dataset.
    """
    for col_index in range(col_count):
        worksheet.write_string(row_index, col_index * 2,
                               '{0:.2f}% '.format(
                                   acc_meter.get_acc_by_field(col=col_index) * 100),
                               workbook.add_format(dict(bold=1,
                                                        font_color='green',
                                                        bg_color='yellow')))
