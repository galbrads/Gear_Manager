from __future__ import division
from PySide import QtGui, QtCore
from PySide.QtTest import QTest
import unittest
import tests
import GearManager
import Util
import sys
import os


#
# --- Member Tab tests -------------------------------------------------------------------------------------------------
#
class MemberValueTests(unittest.TestCase):

    def setUp(self):

        self.app = QtGui.QApplication.instance()
        if self.app is None:
            self.app = QtGui.QApplication(sys.argv)
            self.app.setQuitOnLastWindowClosed(True)
            if os.path.isfile(tests.dBName):
                os.remove(tests.dBName)
        self.ui = GearManager.MainUI(tests.dBName)

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
        self.ui = GearManager.MainUI(tests.dBName)

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


#
# --- Gear Tab tests ---------------------------------------------------------------------------------------------------
#
class GearValueTests(unittest.TestCase):

    def setUp(self):

        self.app = QtGui.QApplication.instance()
        if self.app is None:
            self.app = QtGui.QApplication(sys.argv)
            self.app.setQuitOnLastWindowClosed(True)
            if os.path.isfile(tests.dBName):
                os.remove(tests.dBName)
        self.ui = GearManager.MainUI(tests.dBName)

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

#
# --- Transaction Tab tests --------------------------------------------------------------------------------------------
#
membList = [tests.mkMember('A', 1), tests.mkMember('B', 2)]
gearList = [tests.mkGear('A', 1), tests.mkGear('B', 2)]


class TransactionTests(unittest.TestCase):

    def setUp(self):

        self.app = QtGui.QApplication.instance()
        if self.app is None:
            self.app = QtGui.QApplication(sys.argv)
            self.app.setQuitOnLastWindowClosed(True)
            if os.path.isfile(tests.dBName):
                os.remove(tests.dBName)
        self.ui = GearManager.MainUI(tests.dBName)

        self.ui.defDueDateWin.okBut.click()

        self.tTran = self.ui.tabWid.widget(0)
        self.tMemb = self.ui.tabWid.widget(1)
        self.tGear = self.ui.tabWid.widget(2)
        self.tAdmn = self.ui.tabWid.widget(3)

        self.ui.tabWid.setCurrentIndex(3)
        self.tAdmn.semFalStr.setDate(QtCore.QDate.currentDate().addDays(1))
        self.tAdmn.semFalStr.setDate(QtCore.QDate.currentDate().addDays(-1))
        self.tAdmn.semSprStr.setDate(QtCore.QDate.currentDate().addDays(7))
        self.tAdmn.amountBox.setValue(20)

        self.ui.tabWid.setCurrentIndex(1)
        for memb in membList:
            self.tMemb.nameSearch.clear()
            tests.enterMemberInfo(self, memb)
            self.tMemb.Button_addUpdButClick()

        self.ui.tabWid.setCurrentIndex(0)
        for memb in membList:
            setTransMemb(self, memb)
            QTest.mouseClick(self.tTran.payBut, QtCore.Qt.LeftButton)
            QTest.mouseClick(self.tTran.payWind.payBut, QtCore.Qt.LeftButton)
            self.tTran.payWind.close()

        for gear in gearList:
            self.tGear.gNameIDSearch.clear()
            tests.enterGearInfo(self, gear)
            QTest.mouseClick(self.tGear.updtBut, QtCore.Qt.LeftButton)

        self.ui.tabWid.setCurrentIndex(1)
        self.tMemb.nameSearch.clear()
        self.tMemb.clear_fields()

        self.ui.tabWid.setCurrentIndex(2)
        self.tGear.gNameIDSearch.clear()
        self.tGear.clear_fields()

        self.ui.tabWid.setCurrentIndex(0)
        self.tTran.nameSearch.clear()
        self.tTran.gNameIDSearch.clear()

        setTransMemb(self, membList[0])
        setTransGear(self, gearList[0], 'Name')

    def test_trans(self):
        self.tTran.radioIn.click()
        self.assertFalse(self.tTran.trans())
        self.tTran.radioOut.click()
        self.assertTrue(self.tTran.trans())
        self.tTran.radioOut.click()
        self.assertFalse(self.tTran.trans())
        self.tTran.radioIn.click()
        self.assertTrue(self.tTran.trans())

    def test_returnForSomeoneElse(self):
        self.assertFalse(self.tTran.nameRetSearch.isEnabled())
        self.tTran.radioOut.click()
        self.assertTrue(self.tTran.trans())

        self.assertFalse(self.tTran.nameRetSearch.isEnabled())

        setTransMemb(self, membList[1])
        self.assertFalse(self.tTran.nameRetSearch.isEnabled())
        self.tTran.radioIn.click()
        self.assertTrue(self.tTran.nameRetSearch.isEnabled())
        self.assertTrue(self.tTran.nameRetSearch.count(), 2)
        self.tTran.nameRetSearch.setCurrentIndex(self.tTran.nameRetSearch.findText(
            membList[0]['FirstName'] + ' ' + membList[0]['LastName']))
        self.assertTrue(self.tTran.trans())

    def test_returnForSomeoneElseFields(self):
        self.assertFalse(self.tTran.nameRetSearch.isEnabled())
        self.tTran.radioOut.click()
        self.assertTrue(self.tTran.trans())
        self.assertFalse(self.tTran.nameRetSearch.isEnabled())
        setTransMemb(self, membList[1])
        self.assertFalse(self.tTran.nameRetSearch.isEnabled())
        self.tTran.radioIn.click()
        self.assertTrue(self.tTran.nameRetSearch.isEnabled())
        setTransMemb(self, membList[0])
        self.assertFalse(self.tTran.nameRetSearch.isEnabled())

    def test_notPaid(self):

        self.ui.tabWid.setCurrentIndex(2)
        gear = tests.mkGear('E', 5)
        tests.enterGearInfo(self, gear)
        QTest.mouseClick(self.tGear.updtBut, QtCore.Qt.LeftButton)

        self.ui.tabWid.setCurrentIndex(1)
        self.tMemb.nameSearch.clear()
        memb = tests.mkMember('V', 6, forms=True, campusLink=True,
                              formsDate=Util.convert_date('Qt2DB', QtCore.QDate.currentDate().addDays(1)),
                              campusDate=Util.convert_date('Qt2DB', QtCore.QDate.currentDate().addDays(-2)))
        QTest.keyClicks(self.tMemb.nameSearch, memb['FirstName'] + ' ' + memb['LastName'])
        tests.enterMemberInfo(self, memb)
        self.assertTrue(self.tMemb.Button_addUpdButClick())

        self.ui.tabWid.setCurrentIndex(0)
        setTransGear(self, gear, 'Name')
        setTransMemb(self, memb)

        self.tTran.radioOut.click()
        self.assertFalse(self.tTran.trans())

    def test_noForm(self):

        self.ui.tabWid.setCurrentIndex(2)
        gear = tests.mkGear('F', 6)
        tests.enterGearInfo(self, gear)
        QTest.mouseClick(self.tGear.updtBut, QtCore.Qt.LeftButton)

        self.ui.tabWid.setCurrentIndex(1)
        self.tMemb.nameSearch.clear()
        memb = tests.mkMember('A', 1, forms=False, campusLink=True,
                              formsDate=Util.convert_date('Qt2DB', QtCore.QDate.currentDate()),
                              campusDate=Util.convert_date('Qt2DB', QtCore.QDate.currentDate().addDays(-2)))
        QTest.keyClicks(self.tMemb.nameSearch, memb['FirstName'] + ' ' + memb['LastName'])
        tests.enterMemberInfo(self, memb)
        self.assertTrue(self.tMemb.Button_addUpdButClick())

        self.ui.tabWid.setCurrentIndex(0)
        setTransGear(self, gear, 'Name')
        setTransMemb(self, memb)

        QTest.mouseClick(self.tTran.payBut, QtCore.Qt.LeftButton)
        QTest.mouseClick(self.tTran.payWind.payBut, QtCore.Qt.LeftButton)
        self.tTran.payWind.close()

        self.tTran.radioOut.click()
        self.assertFalse(self.tTran.trans())

    def test_oldForm(self):

        self.ui.tabWid.setCurrentIndex(2)
        gear = tests.mkGear('G', 7)
        tests.enterGearInfo(self, gear)
        QTest.mouseClick(self.tGear.updtBut, QtCore.Qt.LeftButton)

        self.ui.tabWid.setCurrentIndex(1)
        self.tMemb.nameSearch.clear()
        memb = tests.mkMember('A', 1, forms=True, campusLink=True,
                              formsDate=Util.convert_date('Qt2DB', QtCore.QDate.currentDate().addDays(-10)),
                              campusDate=Util.convert_date('Qt2DB', QtCore.QDate.currentDate().addDays(2)))
        QTest.keyClicks(self.tMemb.nameSearch, memb['FirstName'] + ' ' + memb['LastName'])
        tests.enterMemberInfo(self, memb)
        self.assertTrue(self.tMemb.Button_addUpdButClick())

        self.ui.tabWid.setCurrentIndex(0)
        setTransGear(self, gear, 'Name')
        setTransMemb(self, memb)

        QTest.mouseClick(self.tTran.payBut, QtCore.Qt.LeftButton)
        QTest.mouseClick(self.tTran.payWind.payBut, QtCore.Qt.LeftButton)
        self.tTran.payWind.close()

        self.tTran.radioOut.click()
        self.assertFalse(self.tTran.trans())

    def test_paid_currentForm_currentCampus(self):

        self.ui.tabWid.setCurrentIndex(2)
        gear = tests.mkGear('H', 8)
        tests.enterGearInfo(self, gear)
        QTest.mouseClick(self.tGear.updtBut, QtCore.Qt.LeftButton)

        self.ui.tabWid.setCurrentIndex(1)
        self.tMemb.nameSearch.clear()
        memb = tests.mkMember('A', 1, forms=True, campusLink=True,
                              formsDate=Util.convert_date('Qt2DB', QtCore.QDate.currentDate().addDays(1)),
                              campusDate=Util.convert_date('Qt2DB', QtCore.QDate.currentDate().addDays(-1)))
        QTest.keyClicks(self.tMemb.nameSearch, memb['FirstName'] + ' ' + memb['LastName'])
        tests.enterMemberInfo(self, memb)
        self.assertTrue(self.tMemb.Button_addUpdButClick())

        self.ui.tabWid.setCurrentIndex(0)
        setTransGear(self, gear, 'Name')
        setTransMemb(self, memb)

        QTest.mouseClick(self.tTran.payBut, QtCore.Qt.LeftButton)
        QTest.mouseClick(self.tTran.payWind.payBut, QtCore.Qt.LeftButton)
        self.tTran.payWind.close()

        self.tTran.radioOut.click()
        self.assertTrue(self.tTran.trans())

    def test_noCampusLink(self):

        self.ui.tabWid.setCurrentIndex(2)
        gear = tests.mkGear('I', 9)
        tests.enterGearInfo(self, gear)
        QTest.mouseClick(self.tGear.updtBut, QtCore.Qt.LeftButton)

        self.ui.tabWid.setCurrentIndex(1)
        self.tMemb.nameSearch.clear()
        memb = tests.mkMember('A', 1, forms=True, campusLink=False,
                              formsDate=Util.convert_date('Qt2DB', QtCore.QDate.currentDate().addDays(-2)),
                              campusDate=Util.convert_date('Qt2DB', QtCore.QDate.currentDate()))
        QTest.keyClicks(self.tMemb.nameSearch, memb['FirstName'] + ' ' + memb['LastName'])
        tests.enterMemberInfo(self, memb)
        self.assertTrue(self.tMemb.Button_addUpdButClick())

        self.ui.tabWid.setCurrentIndex(0)
        setTransGear(self, gear, 'Name')
        setTransMemb(self, memb)

        QTest.mouseClick(self.tTran.payBut, QtCore.Qt.LeftButton)
        QTest.mouseClick(self.tTran.payWind.payBut, QtCore.Qt.LeftButton)
        self.tTran.payWind.close()

        self.tTran.radioOut.click()
        self.assertFalse(self.tTran.trans())

    def test_campusLinkLastYears(self):

        self.ui.tabWid.setCurrentIndex(2)
        gear = tests.mkGear('J', 10)
        tests.enterGearInfo(self, gear)
        QTest.mouseClick(self.tGear.updtBut, QtCore.Qt.LeftButton)

        self.ui.tabWid.setCurrentIndex(1)
        self.tMemb.nameSearch.clear()
        memb = tests.mkMember('A', 1, forms=True, campusLink=True,
                              formsDate=Util.convert_date('Qt2DB', QtCore.QDate.currentDate().addDays(1)),
                              campusDate=Util.convert_date('Qt2DB', QtCore.QDate.currentDate().addDays(-10)))
        QTest.keyClicks(self.tMemb.nameSearch, memb['FirstName'] + ' ' + memb['LastName'])
        tests.enterMemberInfo(self, memb)
        self.assertTrue(self.tMemb.Button_addUpdButClick())

        self.ui.tabWid.setCurrentIndex(0)
        setTransGear(self, gear, 'Name')
        setTransMemb(self, memb)

        QTest.mouseClick(self.tTran.payBut, QtCore.Qt.LeftButton)
        QTest.mouseClick(self.tTran.payWind.payBut, QtCore.Qt.LeftButton)
        self.tTran.payWind.close()

        self.tTran.radioOut.click()
        self.assertTrue(self.tTran.trans())

    def test_defaultDueDateWhenMemberChanges(self):

        nDays = 50

        self.tTran.dueDateCal.setSelectedDate(self.ui.db.getDefaultDueDate())

        self.ui.tabWid.setCurrentIndex(0)
        setTransMemb(self, membList[0])
        self.tTran.dueDateCal.setSelectedDate(QtCore.QDate.currentDate().addDays(nDays))
        self.assertEquals(self.tTran.dueDateCal.selectedDate(), QtCore.QDate.currentDate().addDays(nDays))

        setTransMemb(self, membList[1])
        self.assertEquals(self.tTran.dueDateCal.selectedDate(), self.ui.db.getDefaultDueDate())

    def tearDown(self):

        self.ui.tabWid.setCurrentIndex(1)
        self.tMemb.nameSearch.clear()
        self.tMemb.clear_fields()

        self.ui.tabWid.setCurrentIndex(2)
        self.tGear.gNameIDSearch.clear()
        self.tGear.clear_fields()

        self.ui.tabWid.setCurrentIndex(0)
        self.tTran.nameSearch.clear()
        self.tTran.gNameIDSearch.clear()

        for table in self.ui.db.tableDefs.keys():
            self.ui.db.execQuery('DROP TABLE ' + table, 'tests_trans -> tearDown')
        self.ui.db.close()
        self.app.quit()
        del self.app


def setTransMemb(this, membAttr):

    this.tTran.nameSearch.clear()
    QTest.keyClicks(this.tTran.nameSearch, membAttr['FirstName'] + ' ' + membAttr['LastName'])
    if this.tTran.bDayBox.count() > 1:
        this.tTran.bDayBox.setCurrentIndex(this.tTran.bDayBox.findText(membAttr['Birthday']))


def setTransGear(this, gearAttr, nameID):

    if nameID == 'Name':
        IDName = 'ID'
    else:
        IDName = 'Name'

    this.tTran.gNameIDSearch.clear()
    QTest.keyClicks(this.tTran.gNameIDSearch, gearAttr[nameID])
    if this.tTran.gDissAmbSearch.count() > 1:
        this.tTran.gDissAmbSearch.setCurrentIndex(this.tTran.gDissAmbSearch.findText(gearAttr[IDName]))


def setReturnMemb(this, membAttr):

    if this.tTran.nameRetSearch.isEnabled():
        this.tTran.nameRetSearch.setCurrentIndex(this.tTran.nameRetSearch.findText(membAttr['FirstName'] + ' ' + membAttr['LastName']))

    if this.tTran.bDayRetBox.isEnabled() and this.tTran.bDayRetBox.count() > 1:
        this.tTran.bDayRetBox.setCurrentIndex(this.tTran.bDayRetBox.findText(membAttr['Birthday']))
