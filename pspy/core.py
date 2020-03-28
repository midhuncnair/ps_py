#! /usr/bin/env python3
"""This module defines the core functionalities for the pub-sub-python
"""


__version__ = '0.1.0.0'
__author__ = 'Midhun C Nair <midhunch@gmail.com>'
__maintainers__ = [
    'Midhun C Nair <midhunch@gmail.com>',
]


# import threading

# from uuid import uuid4

from .subject import Subject


class Publisher:
    """Defines a Publisher who publishes the subjects
    A SingleTon instance.
    """
    _subjects = {}
    _instance = None

    def __new__(cls, *args, **kwargs):
        """
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance

    def __init__(self, subject=None, value=None):
        """
        """
        if subject is not None:
            self.add(subject, value)

    @property
    def subjects(self):
        """
        """
        return self._subjects

    def get_subject(self, subject):
        """
        """
        return self.add(subject, None)

    def add(self, subject, value):
        """
        """
        if subject not in self.subjects:
            Subject(subject, value)  # automatically adds to self.subjects
        else:
            if value is not None:
                self.subjects[subject].next(value)

        return self.subjects[subject]

    def subscribe(self, subject, onSuccess, onError=None):
        """
        """
        return self.subjects[subject].subscribe(onSuccess, onError)

    def next(self, subject, value):
        """
        """
        return self.subjects[subject].next(value)
