#! /usr/bin/env python3
"""This module defines the utility functionalities for the pub-sub-python
"""


# __all__ = []
__version__ = '0.1.0.0'
__author__ = 'Midhun C Nair <midhunch@gmail.com>'
__maintainers__ = [
    'Midhun C Nair <midhunch@gmail.com>',
]


from hashlib import (
    md5,
)


DIGITS = 8
BASE_16 = 16


def get_unique_id(key):
    """computes the crc of agiven key with md5 algo
    and computes a unique base 16 evaluation of last
    DIGITS (specified by const DIGITS).
    Returns both the base 16 and crc.
    """
    crc = md5(
        key.encode('utf-8')
    ).hexdigest()

    return (
        int(
            crc[-DIGITS:],
            BASE_16
        ),
        crc
    )
