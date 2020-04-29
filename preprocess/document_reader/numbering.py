import logging
import re

from preprocess.document_reader import Bullet

logger = logging.getLogger(__name__)


class Numbering:
    def __init__(self, text: str = '', indentation: int = 0):
        self.text = ''
        self.indentation = indentation

        # paragraph may have both bullet and numbering, so remove bullet fist.
        if len(text) > 0:
            if text[0] in Bullet.patterns:
                text = text[1:]
        text = text.replace('．', '. ')
        text = text.replace('（', '(')
        text = text.replace('）', ')')
        matches = re.findall("\A[\d\.()-]+[\.\s]+", text + ' ')
        if matches:
            match = matches[0]
            if re.findall("\d", match):
                try:
                    # exclude the case that initial is a number such as year...
                    if int(match) < 20:
                        self.text = match.strip()
                except BaseException:
                    self.text = match.strip()

    def __str__(self):
        return self.text

    def __repr__(self):
        import json
        return json.dumps({
            'text': self.text,
            'indentation': self.indentation
        }, ensure_ascii=False, indent=2)

    def is_subsequence_of(self, other):
        """ As 1.2(self) to 1.1(other)
        """
        try:
            if len(self.text) == len(other.text):
                diff = 0
                for index in range(len(self.text)):
                    diff += abs(ord(self.text[index]) - ord(other.text[index]))

                return diff == 1
            elif len(self.text) - len(other.text) == 1:
                digits = re.findall("\d", self.text)
                if digits:
                    return digits[-1] == '0'

        except Exception as e:
            logger.warning('Caught exception: ' + str(e.args) + ', numbering: ' + other.text)

        return False

    def is_subitem_of(self, other):
        """ As of 1.1.1(self) to 1.1(other)
        """
        other_text: str = other.text
        if other_text.endswith('.0.'):
            other_text = other_text[:-2]

        if 0 < len(self.text) - len(other_text) <= 2:
            return self.text.startswith(other_text)

        return False

    def is_initial(self):
        matches = re.findall("\d", self.text)
        return len(matches) == 1 and matches[0] == '1'

    def is_empty(self):
        return self.text == ''
