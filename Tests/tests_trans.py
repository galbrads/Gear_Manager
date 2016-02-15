from __future__ import division
import unittest
from PySide import QtGui, QtCore
from PySide.QtTest import QTest
import tests
import Util
import Main
import sys
import os

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
        self.ui = Main.MainUI(tests.dBName)

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

os.remove(tests.dBName)
