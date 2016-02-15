from PySide import QtGui, QtCore
import database as datab
import TabTransMan
import TabMembMan
import TabGearMan
import TabAdmin
import ctypes
import Util
import os

# TODO: Show gear name in checked out gear table
# TODO: Right now the disambiguity of an item is only done when an item name is entered that is in the database. Make it
#  so that the all item numbers that match the currently entered text populates the item number box.
# TODO: Make the database windows sortable by columns
# TODO: Make sure that the scanner auto focuses on the gearID line


class QCompleterCustom(QtGui.QCompleter):

    def __init__(self, comp_list, parent=None):
        class KeyPressEater(QtCore.QObject):

            def eventFilter(self, obj, event):

                if event.type() == QtCore.QEvent.KeyPress:

                    print event.key(), event.text()

                    # if event.key() == QtCore.Qt.Key_Escape:
                    #     print '3 real esc pressed'

                    if event.key() == 16777269:
                        # print 'yesssss...'
                        event.ignore()
                        # print event.type(), event.key()
                        del event
                        event = QtGui.QKeyEvent(QtCore.QEvent.KeyPress, QtCore.Qt.Key_Escape, QtCore.Qt.NoModifier)
                        # print event.type(), event.key()

                    # if event.key() == QtCore.Qt.Key_Escape:
                    #    print '4 real esc pressed'

                return QtCore.QObject.eventFilter(self, obj, event)

        super(QCompleterCustom, self).__init__(comp_list, parent)

        self.installEventFilter(KeyPressEater(self))

# QtGui.QCompleter = QCompleter_Custom


class DefScannerField(object):

    def set_scanner_field(self, gear_id):

        self.parent.set_scanner_field(gear_id)


class ColorOptions(object):

    def setColors(self, bg='white', text='black'):

        p = QtGui.QPalette()
        p.setColor(QtGui.QPalette.Active, QtGui.QPalette.Text, Util.color[text])
        p.setColor(QtGui.QPalette.Active, QtGui.QPalette.Base, Util.color[ bg ])
        p.setColor(QtGui.QPalette.Inactive, QtGui.QPalette.Base, Util.color[ bg ])
        self.setPalette(p)

    def defCols(self):
        self.setColors()


class QLineEditCustom(QtGui.QLineEdit, ColorOptions, DefScannerField):
    def __init__(self, parent):
        super(QLineEditCustom, self).__init__(parent)

        self.parent = parent
        self.scannerIsTyping = False
        self.keyStrokeList = ''
        self.installEventFilter(Util.KeyPressEater(self))

        self.textChanged.connect(self.defCols)

        self.clear = self.decorated_clear(self.clear)

    def decorated_clear(self, fn):
        def new_clear(*args, **kwargs):
            fn(*args, **kwargs)
            self.setColors()
        return new_clear

    def popupMan(self):

        if self.completer().completionCount() == 1 and self.text().upper() == self.completer().currentCompletion().upper():
            empty = QtGui.QCompleter([])
            self.setCompleter(empty)
        elif self.completer().model().rowCount() == 0:
            self.setCompleter(self.origComp)

    def setCompleter2(self, comp):
        self.setCompleter(comp)
        self.origComp = comp
        self.textChanged.connect(self.popupMan)


class QPlainTextEditCustom(QtGui.QPlainTextEdit, ColorOptions, DefScannerField):
    def __init__(self, parent=None):
        super(QPlainTextEditCustom, self).__init__(parent)

        self.parent = parent
        self.scannerIsTyping = False
        self.keyStrokeList = ''
        self.installEventFilter(Util.KeyPressEater(self))

# TODO: Make place holder text "Cannot be empty, must be None or other text"
#     def paintEvent(self, pe):
#
#         if not self.document().toPlainText() and not self.hasFocus():
#             p = QtGui.QPainter(self.viewport())
#             p.drawText(self.frameRect(), QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter, "PlaceHolder")
#         else:
#             super(QPlainTextEdit_Custom, self).paintEvent(pe)


class QDateEditCustom(QtGui.QDateEdit, ColorOptions, DefScannerField):
    def __init__(self, parent=None, date=None):
        super(QDateEditCustom, self).__init__(date, parent)

        if not date:
            date = QtCore.QDate.currentDate()
        self.setDate(date)

        self.setDisplayFormat(Util.dateDispFormat)

        self.dateChanged.connect(self.defCols)

        self.parent = parent
        self.isDirty = False
        self.scannerIsTyping = False
        self.keyStrokeList = ''
        self.installEventFilter(Util.KeyPressEater(self))

    def date_db(self):

        return self.date().toString(Util.DB_Date)

    def date_disp(self):

        return self.date().toString(Util.dateDispFormat)


class QComboBoxCustom(QtGui.QComboBox, DefScannerField):
    def __init__(self, parent=None):
        super(QComboBoxCustom, self).__init__(parent)

        self.parent = parent
        self.scannerIsTyping = False
        self.keyStrokeList = ''
        self.installEventFilter(Util.KeyPressEater(self))

        self.defPal = QtGui.QPalette()

        self.currentIndexChanged.connect(self.defCols)

    def setColors(self, bg=None):

        if bg:
            #  p = QtGui.QPalette()
            #  for m in [QtGui.QPalette.Active, QtGui.QPalette.Inactive]:
            #    p.setColor(m, QtGui.QPalette.ButtonText, Util.color[bg])
            # self.setPalette(p)
            self.setStyleSheet("QComboBox {{ background-color: rgba({}, {}, {}); }}".format(Util.color[bg].red(), Util.color[bg].green(), Util.color[bg].blue()))
        else:
            # self.setPalette(self.defPal)
            self.setStyleSheet("")

    def defCols(self):
        self.setColors()

    def setCurrentIndex(self, ind):

        self.defCols()
        super(QComboBoxCustom, self).setCurrentIndex(ind)

    def setMenu(self, item_list, block_signals=False):

        if block_signals:
            self.blockSignals(True)

        self.clear()
        if isinstance(item_list, list):
            for n in xrange(len(item_list)):
                if isinstance(item_list[n], QtCore.QDate):
                    item_list[n] = Util.convert_date('Qt2Disp', item_list[n])
                self.insertItem(n, item_list[n])

        elif isinstance(item_list, (basestring, unicode)):
            self.insertItem(0, item_list)

        elif isinstance(item_list, QtCore.QDate):
            item_list = Util.convert_date('Qt2Disp', item_list)
            self.insertItem(0, item_list)

        if block_signals:
            self.blockSignals(False)

    def get_menu(self):

        menu = []

        for n in xrange(self.count()):
            if self.itemText(n) != Util.selectOne and self.itemText(n) != Util.returnFor:
                menu.append(self.itemText(n))

        return menu

QtGui.QLineEdit = QLineEditCustom
QtGui.QPlainTextEdit = QPlainTextEditCustom
QtGui.QDateEdit = QDateEditCustom
QtGui.QComboBox = QComboBoxCustom
QtGui.QPlainTextEdit = QPlainTextEditCustom


class ShowRetDateWin(QtGui.QWidget):

    def __init__(self, parent):
        super(ShowRetDateWin, self).__init__(None, QtCore.Qt.WindowStaysOnTopHint)

        self.parent = parent
        self.parent.setEnabled(False)
        self.setWindowIcon(self.parent.icon)
        self.setWindowTitle('Set Return Date')

        # Due date calendar
        self.dueDateCal = QtGui.QCalendarWidget()
        self.dueDateCal.setVerticalHeaderFormat(QtGui.QCalendarWidget.NoVerticalHeader)
        self.dueDateCal.setSelectedDate(self.parent.sessionDueDate)
        self.dueDateCal.setMinimumDate(QtCore.QDate.currentDate())

        # Buttons
        self.okBut = QtGui.QPushButton("Ok")

        # Create the layout
        lay = QtGui.QGridLayout()
        lay.setSpacing(Util.layoutGridSpacing)
        lay.addWidget(self.dueDateCal, 0, 0)
        lay.addWidget(self.okBut, 1, 0)

        self.setLayout(lay)

        # Connect objects
        self.dueDateCal.selectionChanged.connect(self.date_changed)
        self.okBut.clicked.connect(self.ok_clicked)

        self.show()
        self.activateWindow()

    def date_changed(self):

        self.parent.tabWid.widget(0).dueDateCal.setSelectedDate(self.dueDateCal.selectedDate())

    def ok_clicked(self):

        self.close()

    def closeEvent(self, event):

        self.parent.sessionDueDate = self.dueDateCal.selectedDate()

        self.parent.setEnabled(True)

        # Accept the close window event
        event.accept()


class MainUI(QtGui.QWidget):
    def __init__(self, db_name):
        super(MainUI, self).__init__()

        # Need this to set the application icon
        app_id = u'mycompany.myproduct.subproduct.version'  # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)

        self.scannerIsTyping = False
        self.keyStrokeList = ''
        self.installEventFilter(Util.KeyPressEater(self))

        self.icon = QtGui.QIcon('UCMC.ico')
        self.setWindowIcon(QtGui.QIcon(self.icon))
        self.setWindowTitle('Gear Manager')
        self.resize(900, 556)
        # self.move(450, 0)
        self.setWindowState(QtCore.Qt.WindowMaximized)

        # Set default directories
        self.pathDesktop = os.path.join(os.path.expanduser('~'), 'Desktop')
        self.barCodeDir = os.path.join(os.path.expanduser('~'), 'Desktop')

        # Read relevant db info
        self.db = datab.Database(self, db_name)

        # Define current fields
        self.currentMember = None
        self.currentGear = None
        self.currentMemberNameID = ''
        self.currentBDayBox = ''
        self.currentGearLineEdit = ''
        self.currentGearComboBox = ''
        self.sessionDueDate = self.db.getDefaultDueDate()

        # Generate auto completers
        self.memberNameComp = self.get_member_name_comp()
        self.gearNameIDComp = self.get_gear_name_id_comp()
        self.manufacturer_completer = self.get_manufacturer_comp()

        # Make the status window
        self.statBar = QtGui.QStatusBar()
        self.set_stat_message("I'm a message window.  Pay attention to me!!!")

        # Make tabs
        self.tabWid = QtGui.QTabWidget()
        self.tabWid.addTab(TabTransMan.TabTransMan(self), 'Transaction Manager')
        self.tabWid.addTab(TabMembMan.TabMembMan(self), 'Member Manager')
        self.tabWid.addTab(TabGearMan.TabGearMan(self), 'Gear Manager')
        self.tabWid.addTab(TabAdmin.TabAdmin(self), 'Administrative')
        self.tabWid.currentChanged.connect(self.when_tab_changes)

        # Generate the grid layout
        grid = QtGui.QVBoxLayout()
        grid.setSpacing(Util.layoutGridSpacing)

        # Set the row spacings
        grid.setStretch(0, 1)
        grid.setStretch(1, 0)

        # Place the objects on the page
        grid.addWidget(self.tabWid)
        grid.addWidget(self.statBar)

        # Show the grid
        self.setLayout(grid)

        self.show()

        self.defDueDateWin = ShowRetDateWin(self)

    def set_stat_message(self, text=None, c=None, delay=Util.messageDelay):
        
        if text:
            if c:
                p = self.statBar.palette()
                p.setColor(QtGui.QPalette.WindowText, Util.color[c])
                self.statBar.setPalette(p)
            self.statBar.showMessage(text, delay)
        else:
            self.statBar.clearMessage()

    def when_tab_changes(self):

        self.set_stat_message()

        if self.tabWid.currentIndex() != 3:
            self.tabWid.currentWidget().update_tab()

    def set_scanner_field(self, gear_id):

        if self.tabWid.currentIndex() != 3:
            self.tabWid.currentWidget().set_scanner_field(gear_id)

    def get_member_name_comp(self):

        return self.db.autoCompleter('FirstName, LastName', 'Member')

    def get_gear_name_id_comp(self):

        return self.db.autoCompleter('Name, ID', 'Gear')

    def get_manufacturer_comp(self):

        return self.db.autoCompleter('Manufacturer', 'Gear', sort='ORDER BY Manufacturer COLLATE NOCASE')

    def get_who_has_this_gear_comp(self, gear):

        return self.db.autoCompleter('MID', 'TRANS',
                                     searchAtt='GID',
                                     search=gear.ID,
                                     sort='ORDER BY Manufacturer COLLATE NOCASE')

    def closeEvent(self, event):

        # Close the database
        self.db.close()

        # Accept the close window event
        event.accept()

if __name__ == "__main__":
    import sys

    app = QtGui.QApplication(sys.argv)

    ui = MainUI('UCMC_DB.sqlite')

    sys.exit(app.exec_())
