import logging
import re

logger = logging.getLogger(__name__)


def is_contain_digit(s: str) -> bool:
    """ Check if string `s` contains any digit.
    :param s: string to be checked.
    :return: True if there is at least one digit in the string, False otherwise.
    """
    return re.search(r'\d', s) is not None


def is_roman_number(s: str) -> bool:
    """ Check if string `s` is a valid roman number.
    :param s: string to be checked.
    :return: True if `s` is a roman number, False otherwise.
    """
    return s and all([c in 'ivx' for c in s.lower()])


def roman_to_int(roman: str) -> int:
    """ Convert roman number to int.
    :param roman: string represents a roman number
    :return: integer value of the roman number.
    """
    if not is_roman_number(roman):
        raise Exception(f'Invalid roman number {roman}')

    s = roman.upper()
    rom_val = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    int_val = 0
    for i in range(len(s)):
        if i > 0 and rom_val[s[i]] > rom_val[s[i - 1]]:
            int_val += rom_val[s[i]] - 2 * rom_val[s[i - 1]]
        else:
            int_val += rom_val[s[i]]

    return int_val


def nonalphanum_strip(s: str) -> str:
    """ Strip out all leading and trailing non-alphanum.
    :param s: string to be stripped.
    :return: stripped string.
    """
    # left strip
    for i in range(len(s)):
        if s[i].isalnum():
            s = s[i:]
            break

    # right strip
    for i, c in enumerate(reversed(s)):
        if c.isalnum():
            s = s[:-i]
            return s

    return ''
