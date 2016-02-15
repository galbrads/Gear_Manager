from __future__ import division
import unittest
from PySide import QtGui, QtCore
import tests
import Main
import Util
import sys
import os


class MemberValueTests(unittest.TestCase):

    def setUp(self):

        self.app = QtGui.QApplication.instance()
        if self.app is None:
            self.app = QtGui.QApplication(sys.argv)
            self.app.setQuitOnLastWindowClosed(True)
            if os.path.isfile(tests.dBName):
                os.remove(tests.dBName)
        self.ui = Main.MainUI(tests.dBName)

        self.ui.defDueDateWin.okBut.click()

        self.ui.tabWid.setCurrentIndex(1)

        self.tMemb = self.ui.tabWid.widget(1)

        self.membA1 = tests.mkMember('A', 1)

        # Clear the current member and member fields
        self.tMemb.nameSearch.clear()
        self.tMemb.clear_fields()

    def test_AddUpdMember(self):
        tests.enterMemberInfo(self, self.membA1)
        self.assertTrue(self.tMemb.Button_addUpdButClick())

    # AddUpd the same member but with a bad local zip code, should fail
    def test_AddUpdMember_shortZip(self):
        self.membA1['zip'] = '1' * 4
        tests.enterMemberInfo(self, self.membA1)
        self.assertFalse(self.tMemb.Button_addUpdButClick())

    # Zip field is limited to 5 numbers. Trying to enter 6 will strip it to 5
    def test_AddUpdMember_longZip(self):
        zip_code = '1' * 6
        self.membA1['PermZip'] = zip_code
        tests.enterMemberInfo(self, self.membA1)
        self.assertTrue(self.tMemb.Button_addUpdButClick())
        self.assertEqual(self.tMemb.zipEdit.text(), zip_code[:5])

    def test_AddUpdMember_badZipA(self):
        self.membA1['zip'] = 'a' * 5
        tests.enterMemberInfo(self, self.membA1)
        self.assertFalse(self.tMemb.Button_addUpdButClick())

    def test_AddUpdMember_bDayToday(self):
        self.membA1['Birthday'] = Util.convert_date('Qt2DB', QtCore.QDate.currentDate())
        tests.enterMemberInfo(self, self.membA1)
        self.assertFalse(self.tMemb.Button_addUpdButClick())

    def test_AddUpdMember_bDayInFuture(self):
        self.membA1['Birthday'] = Util.convert_date('Qt2DB', QtCore.QDate.currentDate().addDays(1))
        tests.enterMemberInfo(self, self.membA1)
        self.assertFalse(self.tMemb.Button_addUpdButClick())

    def test_AddUpdMember_no_AT_inEmal(self):
        self.membA1['Email'] = 'AAA.AAA.com'
        tests.enterMemberInfo(self, self.membA1)
        self.assertFalse(self.tMemb.Button_addUpdButClick())

    def test_AddUpdMember_shortPhone(self):
        self.membA1['Phone'] = '1' * 9
        tests.enterMemberInfo(self, self.membA1)
        self.assertFalse(self.tMemb.Button_addUpdButClick())

    def test_AddUpdMember_longPhone(self):
        self.membA1['Phone'] = '1' * 11
        tests.enterMemberInfo(self, self.membA1)
        self.assertFalse(self.tMemb.Button_addUpdButClick())

    def test_AddUpdMember_lettersInPhone(self):
        self.membA1['Phone'] = '11111A1111'
        tests.enterMemberInfo(self, self.membA1)
        self.assertFalse(self.tMemb.Button_addUpdButClick())

    def test_AddUpdMember_quotesInName1(self):
        self.membA1['FirstName'] = "AA'A"
        tests.enterMemberInfo(self, self.membA1)
        self.assertTrue(self.tMemb.Button_addUpdButClick())

    def test_AddUpdMember_quotesInName2(self):
        self.membA1['FirstName'] = 'AA"A'
        tests.enterMemberInfo(self, self.membA1)
        self.assertTrue(self.tMemb.Button_addUpdButClick())

    def tearDown(self):

        self.ui.tabWid.setCurrentIndex(1)
        self.tMemb.nameSearch.clear()
        self.tMemb.clear_fields()

        for table in self.ui.db.tableDefs.keys():
            self.ui.db.execQuery('DROP TABLE ' + table, 'tests_trans -> tearDown')
        self.ui.db.close()
        self.app.quit()
        del self.app


class MemberAddUpdateTests(unittest.TestCase):

    def setUp(self):

        self.app = QtGui.QApplication.instance()
        if self.app is None:
            self.app = QtGui.QApplication(sys.argv)
            self.app.setQuitOnLastWindowClosed(True)
            if os.path.isfile(tests.dBName):
                os.remove(tests.dBName)
        self.ui = Main.MainUI(tests.dBName)

        self.ui.defDueDateWin.okBut.click()

        self.ui.tabWid.setCurrentIndex(1)

        self.tMemb = self.ui.tabWid.widget(1)

        self.membA1 = tests.mkMember('A', 1)
        self.membB2 = tests.mkMember('B', 2)

    # Check that the database is open
    def test_databaseConnection(self):
        self.assertTrue(self.ui.db.SQLDB.isOpen(), 'Database is not open')

    # Add a member, should work
    # def test_AddMember_addNewMember(self):
        self.tMemb.nameSearch.clear()
        self.tMemb.clear_fields()
        tests.enterMemberInfo(self, self.membA1)
        self.assertTrue(self.tMemb.areMemberFieldsValid())
        self.assertTrue(self.tMemb.Button_addUpdButClick())

    # Add the same member, should fail
    # def test_AddMember_addIdenticalMember(self):
        self.tMemb.nameSearch.clear()
        self.tMemb.clear_fields()
        tests.enterMemberInfo(self, self.membA1)
        self.assertTrue(self.tMemb.areMemberFieldsValid())
        self.assertFalse(self.tMemb.Button_addUpdButClick())

    # Update existing member, but no valid member in the search field, should fail
    # def test_AddMember_updateMember_noCurrentMember(self):
        self.tMemb.nameSearch.clear()
        self.tMemb.clear_fields()
        tests.enterMemberInfo(self, self.membA1)
        self.assertTrue(self.tMemb.areMemberFieldsValid())
        self.assertFalse(self.tMemb.Button_addUpdButClick())

    # Update existing member, should work
    # def test_AddMember_updateMember_currentMember(self):
        self.tMemb.nameSearch.clear()
        self.tMemb.clear_fields()
        self.tMemb.nameSearch.setText('{} {}'.format(self.membA1['FirstName'], self.membA1['LastName']))
        self.assertTrue(self.tMemb.Button_addUpdButClick())

    # Add non-existing member, should work
    # def test_AddMember_addNonMember(self):
        self.tMemb.nameSearch.clear()
        self.tMemb.clear_fields()
        tests.enterMemberInfo(self, self.membB2)
        self.assertTrue(self.tMemb.areMemberFieldsValid())
        self.assertTrue(self.tMemb.Button_addUpdButClick())

    # AddUpd the same member, should work
    # def test_AddMember_updateMember(self):
        self.tMemb.nameSearch.clear()
        self.tMemb.clear_fields()
        tests.enterMemberInfo(self, self.membA1)
        self.assertFalse(self.tMemb.Button_addUpdButClick())

    # AddUpd the same member but with a new first name, should work
    # def test_AddMember_newFName(self):
        self.tMemb.nameSearch.clear()
        self.tMemb.clear_fields()
        self.membA1['FirstName'] = 'AAAA'
        tests.enterMemberInfo(self, self.membA1)
        self.assertTrue(self.tMemb.Button_addUpdButClick())

    # AddUpd the same member but with a new last name, should work
    # def test_AddMember_newLName(self):
        self.tMemb.nameSearch.clear()
        self.tMemb.clear_fields()
        self.membA1['LastName'] = 'AAAA'
        tests.enterMemberInfo(self, self.membA1)
        self.assertTrue(self.tMemb.Button_addUpdButClick())

    # AddUpd the same member but with a new birthday, should work
    # def test_AddMember_newBDay(self):
        self.tMemb.nameSearch.clear()
        self.tMemb.clear_fields()
        self.membA1['Birthday'] = '1800-01-01'
        tests.enterMemberInfo(self, self.membA1)
        self.assertTrue(self.tMemb.Button_addUpdButClick())

    # AddUpd the current member with a new birthday, should work
    # def test_AddMember_newBDay(self):
        self.tMemb.nameSearch.clear()
        self.tMemb.clear_fields()
        self.membA1['Birthday'] = '1800-01-02'
        tests.enterMemberInfo(self, self.membA1)
        self.assertTrue(self.tMemb.Button_addUpdButClick())

    # AddUpd the current member with a new birthday
    # Two members with the same name, but different birthdays now exist,
    # should fail without selecting the correct birthday
    # def test_AddMember_newBDay(self):
        self.tMemb.nameSearch.clear()
        self.tMemb.clear_fields()
        self.tMemb.nameSearch.setText('{} {}'.format(self.membA1['FirstName'], self.membA1['LastName']))
        tests.enterMemberInfo(self, self.membA1)
        self.assertFalse(self.tMemb.Button_addUpdButClick())

    # AddUpd the current member with a new birthday
    # Two members with the same name, but different birthdays now exist,
    # should work if selecting the first birthday
    # def test_AddMember_newBDay(self):
        self.tMemb.nameSearch.clear()
        self.tMemb.clear_fields()
        self.tMemb.nameSearch.setText('{} {}'.format(self.membA1['FirstName'], self.membA1['LastName']))
        self.tMemb.bDayBox.setCurrentIndex(self.tMemb.bDayBox.findText(Util.convert_date('DB2Disp', '1800-01-01')))
        self.assertTrue(self.tMemb.Button_addUpdButClick())

    # AddUpd the current member with a new birthday
    # Two members with the same name, but different birthdays now exist,
    # should work if selecting the second birthday
    # def test_AddMember_newBDay(self):
        self.tMemb.nameSearch.clear()
        self.tMemb.clear_fields()
        self.tMemb.nameSearch.setText('{} {}'.format(self.membA1['FirstName'], self.membA1['LastName']))
        self.tMemb.bDayBox.setCurrentIndex(self.tMemb.bDayBox.findText(Util.convert_date('DB2Disp', '1800-01-02')))
        self.assertTrue(self.tMemb.Button_addUpdButClick())

    # AddUpd the current member with a new birthday that matches an existing members name/birthday, should not work
    # def test_AddMember_newBDay(self):
        self.tMemb.nameSearch.clear()
        self.tMemb.clear_fields()
        self.tMemb.nameSearch.setText('{} {}'.format(self.membA1['FirstName'], self.membA1['LastName']))
        self.tMemb.bDayBox.setCurrentIndex(self.tMemb.bDayBox.findText(Util.convert_date('DB2Disp', '1900-01-01')))
        self.membA1['Birthday'] = '1800-01-02'
        tests.enterMemberInfo(self, self.membA1)
        self.assertFalse(self.tMemb.Button_addUpdButClick())

    def tearDown(self):

        self.ui.tabWid.setCurrentIndex(1)
        self.tMemb.nameSearch.clear()
        self.tMemb.clear_fields()

        for table in self.ui.db.tableDefs.keys():
            self.ui.db.execQuery('DROP TABLE ' + table, 'tests_memb -> tearDown')
        self.ui.db.close()
        self.app.quit()
        del self.app
