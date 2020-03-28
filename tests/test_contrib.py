#! /usr/bin/env python3
"""This module tests the contrib functions' functionality
"""


__all__ = [
    'TestMergeSuite',
    'TestOfSuite',
    'TestMapClassSuite',
    'TestMapSuite',
]
__version__ = '0.1.0.0'
__author__ = 'Midhun C Nair <midhunch@gmail.com>'
__maintainers__ = [
    'Midhun C Nair <midhunch@gmail.com>',
]


import unittest
import threading

from time import (
    sleep,
    time,
)

from pspy import (
    Merge,
    Of,
    Map as psMap,
    map as psmap,
    Subject,
)

from .constants import (
    NEXT_WAIT,
)


class TestMergeSuite(unittest.TestCase):
    """
    """
    def test_merge_wrong_input_1(self):
        """
        """
        with self.assertRaises(ValueError):
            Merge("test")

    def test_merge_wrong_input_2(self):
        """
        """
        sub = Subject("test_merge_wrong_input_2", 'init')
        merge = Merge(sub)
        with self.assertRaises(ValueError):
            merge.args = "test"

    def test_initialize_1(self):
        """
        """
        merge = Merge()
        self.assertTrue(hasattr(merge, 'id'))
        self.assertTrue(hasattr(merge, 'int_id'))
        self.assertTrue(hasattr(merge, 'subject'))

    def test_initialize_2(self):
        """
        """
        sub = Subject("test_initialize_2", 'init')
        merge = Merge(sub)
        self.assertTrue(hasattr(merge, 'id'))
        self.assertTrue(hasattr(merge, 'int_id'))
        self.assertTrue(hasattr(merge, 'subject'))
        self.assertTupleEqual((sub,), merge.args)

    def test_merge_subscribe(self):
        """
        """
        sub1 = Subject("test_merge_subscribe1", None)
        sub2 = Subject("test_merge_subscribe2", None)

        merge = Merge(sub1, sub2)

        test_val = False
        def on_success(value):
            nonlocal test_val
            test_val = value

        self.assertEqual(test_val, False)
        merge.subscribe(onSuccess=on_success)
        sleep(NEXT_WAIT)
        self.assertEqual(test_val, None)

        sub1.next("sub1 - new")
        sleep(NEXT_WAIT)
        self.assertEqual(test_val, "sub1 - new")

        sub2.next("sub2 - new")
        sleep(NEXT_WAIT)
        self.assertEqual(test_val, "sub2 - new")

        sub1.next("sub1 - new1")
        sleep(NEXT_WAIT)
        self.assertEqual(test_val, "sub1 - new1")

        sub2.next("sub2 - new1")
        sleep(NEXT_WAIT)
        self.assertEqual(test_val, "sub2 - new1")


class TestOfSuite(unittest.TestCase):
    """
    """

    def test_of_wrong_input(self):
        """
        """
        of_obj = Of("test")
        with self.assertRaises(ValueError):
            of_obj.args = "test"

    def test_initialize_1(self):
        """
        """
        of_obj = Of()
        self.assertTrue(hasattr(of_obj, 'id'))
        self.assertTrue(hasattr(of_obj, 'int_id'))
        self.assertTrue(hasattr(of_obj, 'subject'))
        self.assertTrue(hasattr(of_obj, 'index'))
        self.assertTrue(hasattr(of_obj, 'timeout'))
        self.assertEqual(of_obj.index, -1)
        self.assertEqual(of_obj.timeout, 5)

    def test_initialize_2(self):
        """
        """
        of_obj = Of(1, timeout=10)
        self.assertTrue(hasattr(of_obj, 'id'))
        self.assertTrue(hasattr(of_obj, 'int_id'))
        self.assertTrue(hasattr(of_obj, 'subject'))
        self.assertTupleEqual((1,), of_obj.args)
        self.assertTrue(hasattr(of_obj, 'index'))
        self.assertTrue(hasattr(of_obj, 'timeout'))
        self.assertEqual(of_obj.index, -1)
        self.assertEqual(of_obj.timeout, 10)

    def test_subscibe(self):
        """
        """
        lock = threading.Lock()
        of_args = [1, [1,2,3], (1,2,3), {1,2,3}, {1:1, 2:2, 3:3}]
        timeout = 2
        of_obj = Of(*of_args, timeout=timeout)

        test_val1 = False
        prev_val1 = False
        def on_success1(value):
            nonlocal test_val1, prev_val1
            lock.acquire()
            prev_val1 = test_val1
            test_val1 = value
            lock.release()

        test_val2 = False
        prev_val2 = False
        def on_success2(value):
            nonlocal test_val2, prev_val2
            prev_val2 = test_val2
            test_val2 = value

        self.assertEqual(test_val1, False)
        of_obj.subscribe(onSuccess=on_success1)
        of_obj.subscribe(onSuccess=on_success2)
        # sleep(NEXT_WAIT)
        prev_prev = prev_val1
        start = time()
        loop_start = time()
        while (
            test_val1 != of_args[-1]
            or test_val2 != of_args[-1]
        ):
            if prev_prev != prev_val1:
                if prev_prev is None:
                    check = False
                else:
                    check = True
                end = time()
                elapsed = end - start
                start = time()
                prev_prev = prev_val1
                # print("time taken = ", elapsed)
                if check:
                    self.assertAlmostEqual(elapsed, 2, 0)

            loop_time = time()
            loop_elapsed = loop_time - loop_start
            # if loop_elapsed > timeout * len(of_args) + NEXT_WAIT:
            self.assertFalse(loop_elapsed > timeout * len(of_args) + NEXT_WAIT)


class TestMapClassSuite(unittest.TestCase):
    """
    """
    def test_initialize(self):
        """
        """
        success = lambda value: print(value)
        error = lambda error: print(error)
        map_obj = psMap(success, error)
        self.assertEqual(id(success), id(map_obj.onSuccess))
        self.assertEqual(id(error), id(map_obj.onError))


class TestMapSuite(unittest.TestCase):
    """
    """
    def test_wrong_input_1(self):
        """
        """
        with self.assertRaises(ValueError):
            psmap("test")

    def test_wrong_input_2(self):
        """
        """
        with self.assertRaises(ValueError):
            psmap(lambda value: None, onError="test")

    def test_output_1(self):
        """
        """
        success = lambda value: print(value)
        error = lambda error: print(error)
        map_obj = psmap(success, error)
        self.assertTrue(isinstance(map_obj, psMap))
        self.assertEqual(id(success), id(map_obj.onSuccess))
        self.assertEqual(id(error), id(map_obj.onError))

    def test_output_2(self):
        """
        """
        success = lambda value: print(value)
        map_obj = psmap(success,)
        self.assertTrue(isinstance(map_obj, psMap))
        self.assertEqual(id(success), id(map_obj.onSuccess))
        self.assertTrue(callable(map_obj.onError))
