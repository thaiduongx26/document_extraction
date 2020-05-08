import logging
from typing import List

from pdfplumber.page import Page

import utils
from . import custom_handler
from .line_utils import construct_lines
from .table_utils import remove_words_within_table
from .word_utils import extract_words
from .. import rule
from ..line import Line
from ..paragraph import Paragraph
from ..rule import BaseRule, NegativeBaseRule, PositiveBaseRule, FirstLine
from ..table import Table

logger = logging.getLogger(__name__)


class ParagraphParser:
    def __init__(self, rules: List[BaseRule]):
        self.rules: List[BaseRule] = rules

    def run(self, lines: List[Line], **kwargs):
        paragraphs: List[Paragraph] = []

        if custom_handler.paragraph_preprocess is not None:
            paragraphs, lines = custom_handler.paragraph_preprocess(lines, **kwargs)

        paragraph = Paragraph()

        for index in range(len(lines)):
            for rule in self.rules:
                try:
                    is_included = rule.run(paragraph, lines, index, **kwargs)
                    if is_included is not None:
                        if is_included:
                            paragraph.add(lines[index])
                        else:
                            paragraphs.append(paragraph)
                            paragraph = Paragraph()
                            paragraph.add(lines[index])

                        logger.debug(f'"{lines[index]}" - "{rule.name}"')
                        # if the line is handled, then move forward to the next line
                        break
                except BaseException as e:
                    log = logger.exception if utils.enable_debug else logger.warning
                    log(f'Exception occurred while applying rule "{rule.name}" for line "{lines[index]}"')
            else:
                logger.warning(f'[Line skipped] There isn\'t any capable rule to process: "{lines[index]}"')

        if not paragraph.is_empty():
            paragraphs.append(paragraph)

        return paragraphs

    def test_rule(self, lines, parser, **kwargs):
        # Save the list of parser
        parsers = self.rules

        base_rule = NegativeBaseRule() if isinstance(parser, PositiveBaseRule) else PositiveBaseRule()
        self.rules = [FirstLine(), parser, base_rule]
        paragraphs = self.run(lines, **kwargs)

        # Restore the list of parsers
        self.rules = parsers
        return paragraphs


def get_last_char(paragraph: Paragraph):
    return paragraph.lines[-1].words[-1]['text'].strip()[-1]


def construct_paragraphs(lines: List[Line], **kwargs):
    # Note: Add rules here
    parser = ParagraphParser([
        rule.FirstLine(),
        rule.YokoTitle(),
        # rule.TitleStyle(13),
        rule.YokoRightAlignment(),
        rule.BulletLine(),
        rule.YokoKeyValueLine(),
        rule.IndentationDifference(),
        rule.AlignmentDifference(),
        # Title(with big font > 17, same font face) should form a single paragraph.
        # Font size should stay consistence within a paragraph
        # Text with the same special style(font face, font size, alignment, indentation) should be on the same paragraph
        rule.LineLength(),
        rule.DotEnding(),
        rule.LineDistance(4.5),
        # SameIndentationRule(0.008),
        rule.NumberingLine(),
        rule.PositiveBaseRule()
    ])
    TEST_RULE = False
    # TEST_RULE = True

    if TEST_RULE:
        # Note: Test rule here
        paragraphs = parser.test_rule(lines, rule.YokoKeyValueLine(), **kwargs)
    else:
        paragraphs = parser.run(lines, **kwargs)

    return paragraphs


def extract_paragraphs(page: Page, tables: List[Table]):
    words = extract_words(page, y_tolerance=4)
    words = remove_words_within_table(words, tables)

    lines, forced_stop = construct_lines(words, page)
    paragraphs = construct_paragraphs(lines, page=page)

    return paragraphs, forced_stop
