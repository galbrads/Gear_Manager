from __future__ import division
import unittest
from PySide import QtGui
import tests
import Main
import sys
import os


class GearValueTests(unittest.TestCase):

    def setUp(self):

        self.app = QtGui.QApplication.instance()
        if self.app is None:
            self.app = QtGui.QApplication(sys.argv)
            self.app.setQuitOnLastWindowClosed(True)
            if os.path.isfile(tests.dBName):
                os.remove(tests.dBName)
        self.ui = Main.MainUI(tests.dBName)

        self.ui.defDueDateWin.okBut.click()

        self.ui.tabWid.setCurrentIndex(2)

        self.tGear = self.ui.tabWid.widget(2)

        self.gearA1 = tests.mkGear('A', 1)

        # Clear the current member and member fields
        self.tGear.gNameIDSearch.clear()
        self.tGear.clear_fields()

    def test_addGear(self):
        tests.enterGearInfo(self, self.gearA1)
        self.assertTrue(self.tGear.button_save_gear())

    # The quantity window has limits on the inouts that cover this case
    def test_negativeQuant(self):
        self.gearA1['Quantity'] = -self.gearA1['Quantity']
        tests.enterGearInfo(self, self.gearA1)
        self.assertTrue(self.tGear.button_save_gear())

    def test_iD(self):
        self.gearA1['ID'] = 'ID1'
        tests.enterGearInfo(self, self.gearA1)
        self.assertTrue(self.tGear.button_save_gear())

    def test_iDWithStar1(self):

        for n in [1, 2, 5, 22, 10, 3, 42]:

            self.gearA1['ID'] = 'ID{:02}'.format(n)
            tests.enterGearInfo(self, self.gearA1)
            self.assertTrue(self.tGear.button_save_gear())

        self.gearA1['ID'] = 'ID*'
        tests.enterGearInfo(self, self.gearA1)
        self.assertTrue(self.tGear.button_save_gear())
        self.assertEqual(self.tGear.GIDEdit.text(), 'ID04')

    def test_iDWithStar2(self):

        end = 23

        for n in xrange(1, end):

            self.gearA1['ID'] = 'ID{:02}'.format(n)
            tests.enterGearInfo(self, self.gearA1)
            self.assertTrue(self.tGear.button_save_gear())

        self.gearA1['ID'] = 'ID{:02}'.format(end + 1)
        tests.enterGearInfo(self, self.gearA1)
        self.assertTrue(self.tGear.button_save_gear())

        self.gearA1['ID'] = 'ID*'
        tests.enterGearInfo(self, self.gearA1)
        self.assertTrue(self.tGear.button_save_gear())
        self.assertEqual(self.tGear.GIDEdit.text(), 'ID{}'.format(end))

    def test_iDWithStarX2(self):
        self.gearA1['ID'] = 'ID**'
        tests.enterGearInfo(self, self.gearA1)
        self.assertFalse(self.tGear.button_save_gear())

    def test_negativeWeight(self):
        self.gearA1['Weight'] = -self.gearA1['Weight']
        tests.enterGearInfo(self, self.gearA1)
        self.assertFalse(self.tGear.button_save_gear())

    def test_characterInWeight(self):
        self.gearA1['Weight'] = 'AAA'
        tests.enterGearInfo(self, self.gearA1)
        self.assertFalse(self.tGear.button_save_gear())

    def test_negativePrice(self):
        self.gearA1['Price'] = -self.gearA1['Price']
        tests.enterGearInfo(self, self.gearA1)
        self.assertFalse(self.tGear.button_save_gear())

    def tearDown(self):

        self.ui.tabWid.setCurrentIndex(2)
        self.tGear.gNameIDSearch.clear()
        self.tGear.clear_fields()

        for table in self.ui.db.tableDefs.keys():
            self.ui.db.execQuery('DROP TABLE ' + table, 'tests_trans -> tearDown')
        self.ui.db.close()
        self.app.quit()
        del self.app

os.remove(tests.dBName)
