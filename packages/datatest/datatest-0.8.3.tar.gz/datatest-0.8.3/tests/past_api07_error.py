# -*- coding: utf-8 -*-
from . import _unittest as unittest

from datatest.__past__.api07_diffs import xMissing
from datatest.__past__.api07_error import DataError


class TestDataError(unittest.TestCase):
    def test_subclass(self):
        self.assertTrue(issubclass(DataError, AssertionError))

    def test_instantiation(self):
        DataError('column names', xMissing('foo'))
        DataError('column names', [xMissing('foo')])
        DataError('column names', {'foo': xMissing('bar')})
        DataError('column names', {('foo', 'bar'): xMissing('baz')})

        with self.assertRaises(ValueError, msg='Empty error should raise exception.'):
            DataError(msg='', differences={})

    def test_repr(self):
        error = DataError('different columns', [xMissing('foo')])
        pattern = "DataError: different columns:\n xMissing('foo')"
        self.assertEqual(repr(error), pattern)

        error = DataError('different columns', xMissing('foo'))
        pattern = "DataError: different columns:\n xMissing('foo')"
        self.assertEqual(repr(error), pattern)

        # Test pprint lists.
        error = DataError('different columns', [xMissing('foo'),
                                                xMissing('bar')])
        pattern = ("DataError: different columns:\n"
                   " xMissing('foo'),\n"
                   " xMissing('bar')")
        self.assertEqual(repr(error), pattern)

        # Test dictionary.
        error = DataError('different columns', {'FOO': xMissing('bar')})
        pattern = ("DataError: different columns:\n"
                   " 'FOO': xMissing('bar')")
        self.assertEqual(repr(error), pattern)

    def test_verbose_repr(self):
        reference = 'reference-data-source'
        subject = 'subject-data-source'
        error = DataError('different columns', [xMissing('foo')], subject, reference)
        error._verbose = True  # <- Set verbose flag, here!

        pattern = ("DataError: different columns:\n"
                   " xMissing('foo')\n"
                   "\n"
                   "SUBJECT:\n"
                   "subject-data-source\n"
                   "REQUIRED:\n"
                   "reference-data-source")
        self.assertEqual(repr(error), pattern)
