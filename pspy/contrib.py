#! /usr/bin/env python3
"""This module implements the operators that can be used as helpers
"""


# __all__ = []
__version__ = '0.1.0.0'
__author__ = 'Midhun C Nair <midhunch@gmail.com>'
__maintainers__ = [
    'Midhun C Nair <midhunch@gmail.com>',
]


from threading import Thread
from uuid import uuid4
from time import sleep

from .subject import Subject
from .subscriber import Subscriber
from .utils import (
    get_unique_id,
)


class Merge:
    """This will allow us to merge multiple subscriptions to one.
    Expects Subcriber iterables.
    """
    def __init__(self, *args):
        """
        """
        self.id = str(uuid4())
        self.int_id = get_unique_id(self.id)[0]
        self.subject = Subject(self.int_id, initial_value=None)

        self.args = args
        for sub in self.args:
            self.add(sub)

    @property
    def args(self):
        """
        """
        return self._args

    @args.setter
    def args(self, value):
        """
        """
        if (
            isinstance(value, str)
            or not hasattr(value, '__iter__')
        ):
            raise ValueError("Expected an iterable value but got type '%s'" % type(value))
        self._args = value

    def add(self, sub):
        """
        """
        if isinstance(sub, Subscriber):
            subject = sub.subject
        elif isinstance(sub, Subject):
            subject = sub
        else:
            raise ValueError(
                "Expected an value of type Subscriber|Subject but got %s" % type(sub)
            )

        sub.subscribe(onSuccess=self.onSuccess, onError=self.onSuccess)

    def subscribe(self, onSuccess, onError=None):
        """
        """
        sub = self.subject.subscribe(onSuccess=onSuccess, onError=onError)
        self.subscribers[sub.name] = sub
        return sub

    def onSuccess(self, value):
        """
        """
        self.subject.next(value)

    def onError(self, error):
        """
        """
        self.subject.next(error, error=True)

    @property
    def subscribers(self):
        """
        """
        try:
            if not isinstance(self._subscribers, dict):
                self._subscribers = {}
        except AttributeError:
            self._subscribers = {}

        return self._subscribers


class Of:
    """
    """
    def __init__(self, *args, timeout=5):
        """
        """
        self.id = str(uuid4())
        self.int_id = get_unique_id(self.id)[0]
        self.subject = Subject(self.int_id, initial_value=None)

        self.args = args
        self.index = -1
        self.timeout = timeout

    @property
    def args(self):
        """
        """
        return self._args

    @args.setter
    def args(self, value):
        """
        """
        if (
            isinstance(value, str)
            or not hasattr(value, '__iter__')
        ):
            raise ValueError("Expected an iterable value but got type '%s'" % type(value))
        self._args = value

    def subscribe(self, onSuccess, onError=None):
        """
        """
        sub = self.subject.subscribe(onSuccess=onSuccess, onError=onError)
        self.subscribers[sub.name] = sub
        if self.index == -1:
            self.run()
        return sub

    def run(self):
        """
        """
        self.index = 0
        def _run():
            """
            """
            for item in self.args:
                self.subject.next(item)
                sleep(self.timeout)

        thread = Thread(target=_run)
        thread.daemon = True
        thread.start()
        # thread.join()

    @property
    def subscribers(self):
        """
        """
        try:
            if not isinstance(self._subscribers, dict):
                self._subscribers = {}
        except AttributeError:
            self._subscribers = {}

        return self._subscribers


class Map:
    def __init__(self, success, error):
        """
        """
        self.onSuccess = success
        self.onError = error


def map(onSuccess, onError=None):
    """
    """
    if not callable(onSuccess):
        raise ValueError(
            "Expecting a callable but got type %s" % (type(onSuccess))
        )

    if onError is not None and not callable(onError):
        raise ValueError(
            "Expecting a callable but got type %s" % (type(onError))
        )
    elif callable(onError):
        pass
    else:
        onError = lambda error: None

    return Map(onSuccess, onError)
