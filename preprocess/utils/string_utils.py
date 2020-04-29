import string


def is_white(string: str):
    return len(string.strip()) == 0


def is_empty(string: str):
    return len(string) == 0


def has_digit(string: str):
    for c in string:
        if c.isdigit():
            return True
    else:
        return False


def is_roman_number(string: str):
    s = ''.join([c for c in string if c.isalpha()])
    if len(s) == 0:
        return False
    else:
        return all([c in 'ivx' for c in s.lower()])


def roman_to_int(roman: str):
    s = roman.upper()
    rom_val = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    int_val = 0
    for i in range(len(s)):
        if i > 0 and rom_val[s[i]] > rom_val[s[i - 1]]:
            int_val += rom_val[s[i]] - 2 * rom_val[s[i - 1]]
        else:
            int_val += rom_val[s[i]]
    return int_val


def nonalphanum_strip(numbering: str):
    """ strip out all leading/trailing non-alphanum
    """
    # left strip
    for i in range(len(numbering)):
        if numbering[i].isalnum():
            numbering = numbering[i:]
            break

    # right strip
    for i, c in enumerate(reversed(numbering)):
        if c.isalnum():
            numbering = numbering[:-i]
            break

    return numbering


def compare_ignore_white(a: str, b: str):
    import difflib

    return difflib.SequenceMatcher(lambda x: x in string.whitespace, a, b).ratio() == 1


def remove_whites(s: str):
    return s.translate({ord(c): None for c in string.whitespace})
