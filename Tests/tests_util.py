import unittest
from PySide import QtCore
import Util


class IsNumTests(unittest.TestCase):

    def test_IsFloat(self):
        self.assertTrue(Util.is_number(5.2), 'Is Float')

    def test_IsInt(self):
        self.assertTrue(Util.is_number(5), 'Is Int')

    def test_IsChar(self):
        self.assertFalse(Util.is_number('C'), 'Is Char')


class RemoveDupTests(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(RemoveDupTests, self).__init__(*args, **kwargs)

        self.dups = ['1', '3' '2', '3', '4', '5', '3', '5']
        self.nodups = ['1', '2', '3', '4', '5']

    def test_IsList(self):
        self.assertRaises(ValueError, Util.remove_duplicates, 'not a list')

    def test_LengthTest(self):
        self.assertEqual(len(Util.remove_duplicates(self.dups)), len(set(self.dups)))

    def test_Unique(self):
        self.assertTrue(all([Util.remove_duplicates(self.dups).count(n) == 1 for n in Util.remove_duplicates(self.dups)]))


class DateTests(unittest.TestCase):

    def testDates(self):

        y = 2001; m = 1; d = 1

        self.assertEqual(Util.convert_date('DB2Qt', '2001-01-01'), QtCore.QDate(y, m, d))
        self.assertEqual(Util.convert_date('DB2Disp', '2001-01-01'), '1/1/2001')
        self.assertEqual(Util.convert_date('Disp2DB', '1/1/2001'), '2001-01-01')
        self.assertEqual(Util.convert_date('Disp2Qt', '1/1/2001'), QtCore.QDate(y, m, d))
        self.assertEqual(Util.convert_date('Qt2Disp', QtCore.QDate(y, m, d)), '1/1/2001')
        self.assertEqual(Util.convert_date('Qt2DB', QtCore.QDate(y, m, d)), '2001-01-01')
