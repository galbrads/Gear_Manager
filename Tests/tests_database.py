import unittest
import database as db


class FunctionTests(unittest.TestCase):

    def setUp(self):

        self.testList = ['Zero', 'One', 'Two', 'Three']
        self.testDL = db.DictList(self.testList)

    def test_DictList1(self):
        self.assertIsInstance(self.testDL, list)

    def test_DictList2(self):
        self.assertEquals(self.testDL['One'], 1)

    def test_DictList3(self):
        self.assertEquals(self.testDL[1], 'One')

    def test_DictList4(self):
        self.assertIsInstance(self.testDL.getList(), list)

    def test_DictList5(self):
        self.assertIsInstance(self.testDL.getDict(), dict)

    def test_DictList6(self):
        self.assertEquals(self.testDL.nCerts(), len(self.testList))
