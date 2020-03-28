#! /usr/bin/env python3
"""This module tests the publisher's functionality
"""


# __all__ = []
__version__ = '0.1.0.0'
__author__ = 'Midhun C Nair <midhunch@gmail.com>'
__maintainers__ = [
    'Midhun C Nair <midhunch@gmail.com>',
]


import unittest

from time import sleep

from pspy import Publisher


class TestPublisherSuite(unittest.TestCase):
    """
    """
    def test_singleton(self):
        """
        """
        pub1 = Publisher()
        pub2 = Publisher()
        pub3 = Publisher()

        self.assertEqual(id(pub1), id(pub2))
        self.assertEqual(id(pub3), id(pub2))
        self.assertEqual(id(pub1), id(pub3))

    def test_initialize(self):
        """
        """
        pub1 = Publisher()
        pub2 = Publisher(subject='test_initialize', value='test_value')
        self.assertTrue('test_initialize' in pub1.subjects)
        self.assertTrue('test_initialize' in pub2.subjects)

    def test_different_subject_addition(self):
        """
        """
        pub = Publisher()
        subject = pub.get_subject('test_different_subject_addition')
        self.assertTrue('test_different_subject_addition' in pub.subjects)
        subject2 = pub.add('test_different_subject_addition', None)
        self.assertEqual(id(subject), id(subject2))

    def test_subscribe(self):
        """
        """
        pub = Publisher()
        test_var = False
        def on_success(value):
            nonlocal test_var
            test_var = value

        self.assertEqual(test_var, False)
        pub.get_subject('test_subscribe')
        pub.subscribe('test_subscribe', onSuccess=on_success)
        sleep(.1)
        self.assertNotEqual(test_var, False)
        pub.next('test_subscribe', True)
        sleep(.1)
        self.assertEqual(test_var, True)

    def test_next(self):
        """
        """
        pub = Publisher()
        test_var1 = False
        def on_success1(value):
            nonlocal test_var1
            test_var1 = value

        test_var2 = False
        def on_success2(value):
            nonlocal test_var2
            test_var2 = value

        # base for subject = test_next1
        self.assertEqual(test_var1, False)
        pub.get_subject('test_next1')
        pub.subscribe('test_next1', onSuccess=on_success1)
        sleep(.1)
        self.assertNotEqual(test_var1, False)
        pub.next('test_next1', True)
        sleep(.1)
        self.assertEqual(test_var1, True)

        # base for subject = test_next2
        self.assertEqual(test_var2, False)
        pub.get_subject('test_next2')
        pub.subscribe('test_next2', onSuccess=on_success2)
        sleep(.1)
        self.assertNotEqual(test_var2, False)
        pub.next('test_next2', True)
        sleep(.1)
        self.assertEqual(test_var2, True)

        # cross test by changing subject test_next1
        pub.next('test_next1', 'new_val')
        sleep(.1)
        self.assertEqual(test_var1, 'new_val')  # value should change
        self.assertEqual(test_var2, True)  # should be last value.

        # cross test by changing subject test_next2
        pub.next('test_next2', 'new_val2')
        sleep(.1)
        self.assertEqual(test_var1, 'new_val')  # shold be last value.
        self.assertEqual(test_var2, 'new_val2')  # value should change

    def test_subject_property(self):
        """
        """
        pub = Publisher()
        self.assertTrue(isinstance(pub.subjects, dict))
        pub.get_subject('test_subject_property')
        self.assertTrue(isinstance(pub.subjects, dict))
        self.assertTrue('test_subject_property' in pub.subjects)
        pub.get_subject('test_subject_property1')
        self.assertTrue(isinstance(pub.subjects, dict))
        self.assertTrue('test_subject_property' in pub.subjects)
        self.assertTrue('test_subject_property1' in pub.subjects)
