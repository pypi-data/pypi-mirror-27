# -*- coding: utf-8 -*-

from num2words import num2words
from decimal import Decimal, ROUND_HALF_UP


def _split_float(number, precision):
    """Split float number into whole and decimal parts.

    Args:
        number (float): float number.
        precision (int): number of digits after decimal point.

    Returns:
        whole_part (int), decimal_part (int): float parts as integers.

    """
    whole_part = int(number // 1)
    # we round float number half up by given precision
    rounded_number = Decimal(str(number)).quantize(
        Decimal('.%s' % ('0' * precision)),
        rounding=ROUND_HALF_UP
    )
    decimal_part = int((
        '%.{}f'.format(precision) % rounded_number
    ).split('.')[-1])
    return whole_part, decimal_part


def float2words(number, lang, sfx1='', sfx2='', connector=', ', precision=2):
    """Convert float to words by given optional parameters.

    Args:
        number (float): float number.
        lang (str): language code (e.g. 'en_US', 'ru_RU', etc.).
        sfx1 (str): suffix for whole part of float number
            (e.g. 'USD', '$', 'kg', etc.).
        sfx2 (str): suffix for decimal part of float number.
            (e.g. 'ct.', 'g', etc.)
        connector (str): connector will be used between whole and
            decimal parts expressed in words.
        precision (int): number of digits after decimal point.

    Returns:
        number_in_words (str): float number in words.

    """
    whole_part, decimal_part = _split_float(number, precision)
    number_in_words = ''.join([
        # we add whitespace before suffix if it is passed for better
        # readability .
        ' '.join(filter(None, [num2words(whole_part, lang=lang), sfx1])),
        connector,
        ' '.join(filter(None, [num2words(decimal_part, lang=lang), sfx2]))
    ])
    return number_in_words
