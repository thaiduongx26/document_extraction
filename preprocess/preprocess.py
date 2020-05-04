import logging
import os
from os import path
from pathlib import Path
from typing import List

import utils
from .document_reader import Document, Bullet
from .document_reader.pdf.line import Line
from .document_reader.pdf.paragraph import Paragraph
from .document_reader.pdf.style import ALIGNMENT
from .document_reader.pdf.utils import custom_handler
from .document_structuring import ParsingManager
from .document_structuring.parsers.bullet_parser import BulletParser
from .document_structuring.parsers.document_title_parser import DocumentTitleParser
from .document_structuring.parsers.fontsize_parser import FontSizeParser
from .document_structuring.parsers.indent_parser import IndentParser
from .document_structuring.parsers.normal_text_parser import NormalTextParser
from .document_structuring.parsers.numbering_parser import NumberingParser
from .document_structuring.parsers.right_alignment import RightAlignmentParser
from .document_structuring.parsers.root_parser import RootParser
from .document_structuring.parsers.table_parser import TableParser
from .exporter import *
from .utils.utils import convert_docx_to_html

logger = logging.getLogger(__name__)


def line_preprocess(words: List, page):
    lines = []
    for index in range(min(len(words), 5)):
        if words[index]['text'] == '販売ニュース':
            line = Line(page)
            line.add(words[index])
            lines.append(line)

            del words[index]
            break

    return lines


def paragraph_preprocess(lines: List[Line], **kwargs):
    paragraphs = []
    try:
        if kwargs['page'].page_number > 1:
            return

        if lines[0].text == '販売ニュース':
            paragraph = Paragraph()
            paragraph.add(lines[0])
            paragraphs.append(paragraph)

            del lines[0]

        title = Paragraph()
        title.add(lines[0])
        for i in (1, 2):
            line = lines[i]
            if line.get_first_char_font() == title.get_fist_char_font() and abs(line.x0 - title.indentation) < 100:
                title.add(line)
            else:
                break

        paragraphs.append(title)
        del lines[:len(title.lines)]
    finally:
        return paragraphs, lines


custom_handler.line_preprocess = line_preprocess
custom_handler.paragraph_preprocess = paragraph_preprocess


def line_postprocess(lines: List[Line]):
    def is_page_number_line(l: Line):
        if l.text.startswith('P.') and len(l.text) < 8:
            return True

    indexes = []
    forced_stop = False

    if lines and is_page_number_line(lines[0]):
        lines.pop(0)

    if lines and is_page_number_line(lines[-1]):
        lines.pop(-1)

    for i, line in enumerate(lines):
        if line.text in ('Internal Use Only',
                         '改訂1版'
                         ):
            indexes.append(i)

        if line.is_blank():
            indexes.append(i)

        if line.text.startswith('#######################') \
                or (line.text == '以上' and line.alignment == ALIGNMENT.RIGHT):
            lines = lines[:i]
            forced_stop = True
            break

    for index in reversed(indexes):
        lines.pop(index)

    return lines, forced_stop


custom_handler.line_postprocess = line_postprocess


def process_file(filename: str):
    if Path(filename).suffix.lower() in ('.doc', '.docx'):
        filename = convert_docx_to_html(filename)

    document = Document(filename)
    root = _build_document_tree(document)

    # DEBUG: caching files --> move to tests
    outfile = path.join(path.dirname(filename), '.cache2', os.path.basename(filename))
    print("outfile: ", outfile)
    if not path.exists(path.dirname(outfile)):
        os.mkdir(path.dirname(outfile))

    # if enable_debug:
    exporter = Exporter(root)
    excel_output = exporter.to_xlsx(outfile + '.xlsx')

    if utils.enable_debug:
        exporter.to_json(outfile + '.tree.json')
        exporter.to_json_flattened(outfile + '.flattened.json')

    return _convert_tree_to_list(root), excel_output


def process_folder(dirname: str, filter=('.pdf', '.docx', '.doc')):
    import glob

    for file in glob.glob(str(dirname) + '/**/*.*', recursive=True):
        for ext in filter:
            if file.lower().endswith(ext):
                process_file(file)
                logger.info('DONE\n')


def _build_document_tree(document):
    parsing_manager = ParsingManager()

    # TODO: add parsers here
    parsers = (
        RootParser,
        DocumentTitleParser(),
        TableParser,
        RightAlignmentParser,
        NumberingParser,
        BulletParser,
        # FontSizeParser,
        IndentParser,
        NormalTextParser
    )

    parsing_manager.register_parsers(parsers)

    return parsing_manager.run(document)


def _convert_tree_to_list(root):
    return Exporter(root).flatten_tree()
