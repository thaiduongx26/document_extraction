from typing import List

from . import custom_handler
from ..line import Line


def construct_lines(words: List, page):
    lines = []
    line = Line(page)
    previous_word = None

    if custom_handler.line_preprocess is not None:
        lines = custom_handler.line_preprocess(words, page)

    for word in words:
        if previous_word is None:
            previous_word = word
            line.add(word)
        else:
            # New line
            if abs(previous_word['bottom'] - word['bottom']) > 0.4 * int(word['bottom'] - word['top']):
                lines.append(line)
                line = Line(page)
                line.add(word)
                previous_word = word
            else:  # The word is on the same line
                line.add(word)
    else:
        lines.append(line)

    forced_stop = False
    if custom_handler.line_postprocess is not None:
        lines, forced_stop = custom_handler.line_postprocess(lines)

    return lines, forced_stop
