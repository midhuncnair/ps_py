#! /usr/bin/env python3
"""This module defines the subject functionalities for the pub-sub-python
"""


__version__ = '0.1.0.0'
__author__ = 'Midhun C Nair <midhunch@gmail.com>'
__maintainers__ = [
    'Midhun C Nair <midhunch@gmail.com>',
]


import threading

from threading import Thread
from time import sleep
from concurrent.futures import (
    ThreadPoolExecutor,
    as_completed,
)

# from uuid import uuid4

from .subscriber import Subscriber


class Subject:
    """Defines a subject to which anyone can subscribe to.
    """
    _publisher = None
    _lock = threading.Lock()

    def __new__(cls, subject, *args, initial_value=None, **kwargs):
        """
        """
        from .core import Publisher
        pub = Publisher()
        if subject not in pub.subjects:
            pub.subjects[subject] = super().__new__(cls)
        else:
            if initial_value is not None:
                pub.subjects[subject].next(initial_value)

        return pub.subjects[subject]

    def __init__(self, subject, initial_value=None):
        """
        """
        self.subject = subject
        self.initial_value = initial_value
        self.value = initial_value

    @property
    def publisher(self):
        """
        """
        from .core import Publisher
        if not isinstance(self._publisher, Publisher):
            self._publisher = Publisher()
        return self._publisher

    def subscribe(self, onSuccess, onError=None):
        """
        """
        sub = Subscriber(subject=self, onSuccess=onSuccess, onError=onError)
        # subscriber gets added to the instance on creation automatically.
        return sub

    def add_subscriber(self, subscriber):
        """
        """
        from .subscriber import Subscriber
        if not isinstance(subscriber, Subscriber):
            raise ValueError(
                "Expected value of type Subscriber but got %s." % type(subscriber)
            )
        self._lock.acquire()
        self.subscribers[subscriber.name] = subscriber
        subscriber.subject = self
        self._lock.release()
        self.call_target(subscriber.success, self.value)

    def pipe(self, *args):
        """
        """
        for arg in args:
            self.add_pipe(arg)

    def add_pipe(self, item):
        """
        """
        from .contrib import (
            Map,
        )
        if not (
            isinstance(item, Map)
        ):
            raise ValueError(
                "Expected value of type Map but got type %s" % type(item)
            )

        self.pipes.append(item)

    def call_target(self, target, *args, executer=None, **kwargs):
        """
        """
        if executer is None:
            thread = Thread(
                target=target,
                args=args,
                kwargs=kwargs,
            )
            thread.daemon = True
            thread.start()
            return thread
        else:
            return executer.submit(target, *args, **kwargs)

    def call_on_success(self, value, executer=None):
        """
        """
        calls = []
        self._lock.acquire()
        for pipe in self.pipes:
            calls.append(
                self.call_target(
                    pipe.onSuccess,
                    value,
                    executer=executer
                )
            )

        for sub in self.subscribers.values():
            calls.append(
                self.call_target(
                    sub.success,
                    value,
                    executer=executer
                )
            )
        self._lock.release()
        return calls

    def call_on_error(self, error, executer=None):
        """
        """
        calls = []
        self._lock.acquire()
        for pipe in self.pipes:
            calls.append(
                self.call_target(
                    pipe.onError,
                    error,
                    executer=executer
                )
            )

        for sub in self.subscribers.values():
            calls.append(
                self.call_target(
                    sub.error,
                    error,
                    executer=executer
                )
            )
        self._lock.release()

        return calls

    def next(self, value, error=False):
        """This will take the new value to and send
        that to all the subscribers
        """
        def run(threads):
            with ThreadPoolExecutor(5) as executer:
                try:
                    self._lock.acquire()
                    self.value = value
                    self._lock.release()
                    if not error:
                        threads.extend(self.call_on_success(value, executer=executer))
                    else:
                        threads.extend(self.call_on_error(value, executer=executer))
                except Exception as err:
                        threads.extend(self.call_on_error(err, executer=executer))
        calls = []
        thread = Thread(
            target=run,
            args=(calls,),
            kwargs={},
        )
        thread.daemon = True
        thread.start()

        return calls

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

    @property
    def pipes(self):
        """
        """
        try:
            if not isinstance(self._pipes, list):
                self._pipes = []
        except AttributeError:
            self._pipes = []

        return self._pipes

    @property
    def value(self):
        """
        """
        return self._value

    @value.setter
    def value(self, value):
        """
        """
        self._value = value

    def unsubscribe(self, subscriber):
        """
        """
        del self.subscribers[subscriber.name]
        del subscriber


class SubjectFromCallable(Subject):
    """
    """
    def __init__(self, subject, *args, initial_value=None, **kwargs):
        """
        """
        self.subject = subject
        self.initial_value = initial_value
        self.value = None
        self._args = args
        self._kwargs = kwargs
        self.index = -1

    @property
    def subject(self):
        """
        """
        return self._subject

    @subject.setter
    def subject(self, value):
        """
        """
        if not callable(value):
            raise ValueError(
                "Expected a value of type callable but got %s" % type(value)
            )

        self._subject = value

    def subscribe(self, *args, **kwargs):
        """
        """
        sub = super().subscribe(*args, **kwargs)
        # subscriber gets added to the instance on creation automatically.
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
            result = None

            with ThreadPoolExecutor(2) as executer:
                future = executer.submit(self.subject, *self._args, **self._kwargs)
                while not future.done():
                    sleep(1)
                result = future.result()

            self.next(result)

        thread = Thread(target=_run)
        thread.daemon = True
        thread.start()
