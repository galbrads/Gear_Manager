from PySide import QtGui, QtCore, QtSql
import Util


class TabAdmin(QtGui.QTabWidget):
    def __init__(self, parent):
        super(TabAdmin, self).__init__(parent)

        # Inherit stuff
        self.parent = parent
        self.statBar = parent.statBar
        self.db = parent.db

        self.viewShitList = QtGui.QTableView(None)
        self.adminList = QtGui.QTableView()

        # # # # # # # # # # # #
        # Hard coded holidays #
        # # # # # # # # # # # #
#         # Current year
#         self.thisYear  = QtCore.QDate.currentDate().year()
#         self.holidays = []
#
#         # New year's day, Jan 1st
#         self.holidays.append( QtCore.QDate(self.thisYear, 1, 1) )
#
#         # MLK Day, 3rd mon in Jan
#         self.holidays.append( self.nthDayOfMonth(1, 1, 3) )
#
#         # President's day, 3rd mon in Feb
#         self.holidays.append( self.nthDayOfMonth(1, 2, 3) )
#
#         # Memorial day, last mon in May
#         self.holidays.append( self.lastDayOfMonth(1, 5) )
#
#         # Independence day, 4th Jul
#         self.holidays.append( QtCore.QDate(self.thisYear, 7, 4) )
#
#         # Labor day, 1st Monday in Sep
#         self.holidays.append( self.nthDayOfMonth(1, 9, 1) )
#
#         # Columbus day, 2nd mon in Oct
#         #self.holidays.append( self.nthDayOfMonth(1, 10, 2) )
#
#         # Veteran's day, 11th Nov
#         self.holidays.append( QtCore.QDate(self.thisYear, 11, 11) )
#
#         # Thanks giving, 4th thu of Nov
#         self.holidays.append( self.nthDayOfMonth(4, 11, 4) )
#
#         # Day after thanks giving
#         self.holidays.append( self.holidays[-1].addDays(1) )
#
#         # Christmas, 24-25th of Dec
#         self.holidays.append( QtCore.QDate(self.thisYear, 12, 24) )
#         self.holidays.append( QtCore.QDate(self.thisYear, 12, 25) )
#
#         # Adjust for weekends
#         self.adjustHolidaysForWeekends()
#
        # # # # # # # # # # # #

        # No focus on the tab itself
        self.setFocusPolicy(QtCore.Qt.NoFocus)

        # Shit list button
        shit_list_label = QtGui.QLabel("Show Shit List")
        shit_list_button = QtGui.QPushButton('Show\nShit List')
        shit_list_button.clicked.connect(self.show_shit_list)

        # Weekday of meetings
        meeting_day_label = QtGui.QLabel('Day of Weekly Meetings')
        self.meetingDayBox = QtGui.QComboBox(self)
        self.meetingDayBox.insertItem(0, 'Mondays')
        self.meetingDayBox.insertItem(1, 'Tuesdays')
        self.meetingDayBox.insertItem(2, 'Wednesdays')
        self.meetingDayBox.insertItem(3, 'Thursdays')
        self.meetingDayBox.insertItem(4, 'Fridays')
        self.meetingDayBox.insertItem(5, 'Saturdays')
        self.meetingDayBox.insertItem(6, 'Sundays')
        self.get_day_of_meetings()
        self.meetingDayBox.activated.connect(self.set_day_of_meetings)

        # Frequency of meetings
        meeting_frequency_label = QtGui.QLabel('Meeting frequency')
        self.meetingFreqBox = QtGui.QComboBox(self)
        self.meetingFreqBox.insertItem(1, 'Every Week')
        self.meetingFreqBox.insertItem(2, 'Every Other Week')
        self.meetingFreqBox.insertItem(3, 'Every Third week')
        self.meetingFreqBox.insertItem(4, 'Once a Month')
        self.meetingFreqBox.setCurrentIndex(self.get_meeting_frequency())

        # Gear rental fee amount
        amount_label = QtGui.QLabel('Rental Fee')
        self.amountBox = QtGui.QDoubleSpinBox()
        self.amountBox.setPrefix("$")
        self.amountBox.setSingleStep(5)
        self.amountBox.setMaximum(10000)
        self.amountBox.setValue(self.db.getRentalPrice())

        # Export database button
        self.setBarcodeDirBut = QtGui.QPushButton('Set Barcode\nSave Directory')
        self.exportDatabaseBut = QtGui.QPushButton('Export Database')
        self.importDatabaseBut = QtGui.QPushButton('Import Database')
        self.exportShitBut = QtGui.QPushButton("Export Shit List")

        # Semester start and end dates
        # Payments are good for the duration of the semester and the following brakes
        # The default gear due date is on the next meeting.  Meetings are not held on breakes by default

        self.semFalStr = QtGui.QDateEdit()
        self.semFalEnd = QtGui.QDateEdit()
        self.semSprStr = QtGui.QDateEdit()
        self.semSprEnd = QtGui.QDateEdit()
        self.semSumStr = QtGui.QDateEdit()
        self.semSumEnd = QtGui.QDateEdit()

        self.semFalStr.setCalendarPopup(True)
        self.semFalEnd.setCalendarPopup(True)
        self.semSprStr.setCalendarPopup(True)
        self.semSprEnd.setCalendarPopup(True)
        self.semSumStr.setCalendarPopup(True)
        self.semSumEnd.setCalendarPopup(True)
        self.set_semester_dates()

        semester_box = QtGui.QGridLayout()
        semester_box.setSpacing(Util.layoutGridSpacing)
        pass                            ; semester_box.setColumnStretch(0, 0); semester_box.setColumnStretch(1, 0); semester_box.setColumnStretch(2, 0); semester_box.setColumnStretch(3, 1)
        semester_box.setRowStretch(0, 0)

        pass                                                ; semester_box.addWidget(QtGui.QLabel('Start'), 0, 1); semester_box.addWidget(QtGui.QLabel('End'), 0, 2)
        semester_box.addWidget(QtGui.QLabel('Fall')  , 1, 0); semester_box.addWidget(self.semFalStr       , 1, 1); semester_box.addWidget(self.semFalEnd     , 1, 2)
        semester_box.addWidget(QtGui.QLabel('Spring'), 2, 0); semester_box.addWidget(self.semSprStr       , 2, 1); semester_box.addWidget(self.semSprEnd     , 2, 2)
        semester_box.addWidget(QtGui.QLabel('Summer'), 3, 0); semester_box.addWidget(self.semSumStr       , 3, 1); semester_box.addWidget(self.semSumEnd     , 3, 2)

        semester_dates = QtGui.QGroupBox()
        semester_dates.setTitle('Semester/break start end end dates. Dates between semesters are breaks.')
        semester_dates.setLayout(semester_box)

        # Show Admin Table
        admin_label = QtGui.QLabel('Show Admin Table')
        admin_button = QtGui.QPushButton('Show Admin Table')
        admin_button.clicked.connect(self.show_admin_table)

        # Generate and populate the table
        grid = QtGui.QGridLayout()
        grid.setSpacing(Util.layoutGridSpacing)
        pass                    ; grid.setColumnStretch(0, 0); grid.setColumnStretch(1, 0); grid.setColumnStretch(3, 1)
        grid.setRowStretch(0, 0)
        grid.setRowStretch(1, 0)
        grid.setRowStretch(2, 0)
        grid.setRowStretch(9, 1)

        grid.addWidget(shit_list_label        , 0, 0); grid.addWidget(shit_list_button   , 0, 1)
        grid.addWidget(meeting_day_label      , 1, 0); grid.addWidget(self.meetingDayBox , 1, 1)
        grid.addWidget(meeting_frequency_label, 2, 0); grid.addWidget(self.meetingFreqBox, 2, 1)
        grid.addWidget(amount_label           , 3, 0); grid.addWidget(self.amountBox     , 3, 1)
        grid.addWidget(admin_label            , 4, 0); grid.addWidget(admin_button       , 4, 1)
        # grid.addWidget(self.setBarcodeDirBut , 5, 1)
        grid.addWidget(self.importDatabaseBut, 6, 1)
        grid.addWidget(self.exportDatabaseBut, 7, 1)
        grid.addWidget(self.exportShitBut, 8, 1)

        buttons_box = QtGui.QGroupBox()
        buttons_box.setTitle('')
        buttons_box.setLayout(grid)

        table_grid = QtGui.QGridLayout()
        table_grid.setSpacing(Util.layoutGridSpacing)
        pass                                         ; table_grid.setColumnStretch(3, 1)
        table_grid.setRowStretch(9, 1)
        table_grid.addWidget(buttons_box, 0, 0, 2, 1); table_grid.addWidget(semester_dates, 0, 1)

        self.setLayout(table_grid)

        # # # # # # # # # #
        # Connect objects #
        # # # # # # # # # #

        self.semFalStr.dateChanged.connect(self.semFalStrEdited)
        self.semFalEnd.dateChanged.connect(self.semFalEndEdited)
        self.semSprStr.dateChanged.connect(self.semSprStrEdited)
        self.semSprEnd.dateChanged.connect(self.semSprEndEdited)
        self.semSumStr.dateChanged.connect(self.semSumStrEdited)
        self.semSumEnd.dateChanged.connect(self.semSumEndEdited)

        self.meetingFreqBox.currentIndexChanged.connect(self.set_meeting_frequency)

        self.amountBox.valueChanged.connect(self.set_rental_price)

        self.setBarcodeDirBut.clicked.connect(self.set_barcode_save_directory)
        self.exportDatabaseBut.clicked.connect(self.export_database)
        self.importDatabaseBut.clicked.connect(self.import_database)
        self.exportShitBut.clicked.connect(self.export_shit_list)

        # Change the tab order for the meetingDayBox field
        self.setTabOrder(self.meetingDayBox, admin_button)

    def set_semester_dates(self):

        dates = self.db.getSemesterDates()

        self.semFalStr.setDate(dates['SemFallStart'])
        self.semFalEnd.setDate(dates['SemFallEnd'])
        self.semSprStr.setDate(dates['SemSprStart'])
        self.semSprEnd.setDate(dates['SemSprEnd'])
        self.semSumStr.setDate(dates['SemSumStart'])
        self.semSumEnd.setDate(dates['SemSumEnd'])

    def semFalStrEdited(self):
        if self.semFalStr.date() > self.semFalEnd.date(): self.semFalEnd.setDate(self.semFalStr.date())
        self.db.setFieldTo('Admin', 'SemFallStart', self.semFalStr.date_db())

    def semFalEndEdited(self):
        if self.semFalEnd.date() < self.semFalStr.date(): self.semFalStr.setDate(self.semFalEnd.date())
        self.db.setFieldTo('Admin', 'SemFallEnd', self.semFalEnd.date_db())

    def semSprStrEdited(self):
        if self.semSprStr.date() > self.semSprEnd.date(): self.semSprEnd.setDate(self.semSprStr.date())
        self.db.setFieldTo('Admin', 'SemSprStart', self.semSprStr.date_db())

    def semSprEndEdited(self):
        if self.semSprEnd.date() < self.semSprStr.date(): self.semSprStr.setDate(self.semSprEnd.date())
        self.db.setFieldTo('Admin', 'SemSprEnd', self.semSprEnd.date_db())

    def semSumStrEdited(self):
        if self.semSumStr.date() > self.semSumEnd.date(): self.semSumEnd.setDate(self.semSumStr.date())
        self.db.setFieldTo('Admin', 'SemSumStart', self.semSumStr.date_db())

    def semSumEndEdited(self):
        if self.semSumEnd.date() < self.semSumStr.date(): self.semSumStr.setDate(self.semSumEnd.date())
        self.db.setFieldTo('Admin', 'SemSumEnd', self.semSumEnd.date_db())

    def nth_day_of_month(self, day_of_week, month, nth_day):

        # Find the first occurrence of day in this month
        date = QtCore.QDate(self.thisYear, month, 1)

        while date.dayOfWeek() != day_of_week:
            date = date.addDays(1)

        date = date.addDays((nth_day - 1) * 7)

        if date.isValid() and date.month() == month:
            return date

    def last_day_of_month(self, day_of_week, month):

        # Find the first occurrence of day in this month
        date = QtCore.QDate(self.thisYear, month, 1)

        while date.dayOfWeek() != day_of_week:
            date = date.addDays(1)

        while date.month() == date.addDays(7).month():
            date = date.addDays(7)

        if date.isValid() and date.month() == month:
            return date

    def adjust_holidays_for_weekends(self):

        for n in xrange(len(self.hollidays)):

            if self.hollidays[n].dayOfWeek() == 6:
                self.hollidays[n].addDays(-1)
            if self.hollidays[n].dayOfWeek() == 7:
                self.hollidays[n].addDays(1)

    # def set_all_members_no_forms(self):
    #
    #     reply = QtGui.QMessageBox.question(self, 'Make EVERYONE as no forms on file?',
    #                                        'Are you sure you want to change the forms\n'
    #                                        'to no forms on file for ALL members?',
    #                                        QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
    #
    #     if reply == QtGui.QMessageBox.Yes:
    #         self.db.setFieldTo('Member', 'FormsCurrent', 0)

    def set_rental_price(self):

        self.db.set_rental_price(self.amountBox.value())

    def show_shit_list(self):

        query = self.db.getShitListQuery()

        model = QtSql.QSqlQueryModel()
        model.setQuery(query)
        model.setHeaderData(0, QtCore.Qt.Horizontal, 'Member First Name')
        model.setHeaderData(1, QtCore.Qt.Horizontal, 'Member Last Name')
        model.setHeaderData(2, QtCore.Qt.Horizontal, 'Gear Name')
        model.setHeaderData(3, QtCore.Qt.Horizontal, 'Gear ID')
        model.setHeaderData(4, QtCore.Qt.Horizontal, 'Check Out Date/Time')
        model.setHeaderData(5, QtCore.Qt.Horizontal, 'Due Date')

        self.viewShitList.setWindowTitle('Shit List')
        self.viewShitList.setWindowIcon(self.parent.icon)
        self.viewShitList.resize(600, 500)
        self.viewShitList.setModel(model)
        self.viewShitList.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.viewShitList.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.viewShitList.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.viewShitList.resizeColumnsToContents()
        self.viewShitList.show()

    def get_day_of_meetings(self):

        day_of_meeting = self.db.get_day_of_meetings()

        self.meetingDayBox.setCurrentIndex(day_of_meeting - 1)

    def set_day_of_meetings(self):

        self.db.set_day_of_meetings(self.meetingDayBox.currentIndex() + 1)

    def get_meeting_frequency(self):

        return self.db.get_meeting_frequency() - 1

    def set_meeting_frequency(self):

        meeting_frequency = self.meetingFreqBox.currentIndex()

        self.db.set_meeting_frequency(meeting_frequency + 1)

    def show_admin_table(self):

        model = QtSql.QSqlTableModel(self)
        model.setTable('Admin')
        model.select()
        # model.setHeaderData(0, QtCore.Qt.Horizontal, 'Day Of Meetings')

        self.adminList.setWindowTitle('Admin List')
        self.adminList.setWindowIcon(self.parent.icon)
        self.adminList.resize(600, 500)
        self.adminList.setModel(model)
        self.adminList.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.adminList.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.adminList.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.adminList.resizeColumnsToContents()
        self.adminList.show()

    def set_barcode_save_directory(self):

        dialog = QtGui.QFileDialog()
        dialog.setAcceptMode(QtGui.QFileDialog.AcceptOpen)
        dialog.setFileMode(QtGui.QFileDialog.Directory)
        self.parent.barCodeDir = dialog.getExistingDirectory(self, "Set Save Dir for Barcodes",
                                                             dir=self.parent.barCodeDir,
                                                             options=QtGui.QFileDialog.ShowDirsOnly)

        self.parent.barCodeDir += '\\'

    def import_database(self):

        self.file_dialog_xlsx(self.db.import_database, "Import Database", "database")

    def export_database(self):

        self.file_dialog_xlsx(self.db.export_database, "Export Database", "database")

    def export_shit_list(self):

        self.file_dialog_xlsx(self.db.export_shit_list, "Export Shit List", "shit list")
    
    def file_dialog_xlsx(self, export_function, window_title, file_identifier):

        dialog = QtGui.QFileDialog()
        dialog.setAcceptMode(QtGui.QFileDialog.AcceptSave)
        dialog.setFileMode(QtGui.QFileDialog.AnyFile)
        dialog.setDefaultSuffix('xlsx')
        file_name = dialog.getSaveFileName(self, window_title, self.parent.pathDesktop, "Excel Files (*.xlsx)")

        if file_name[0]:

            self.parent.set_stat_message('Exporting {}, be patient...'.format(file_identifier), delay=0)
            export_function(file_name[0])
            self.parent.set_stat_message('Exported {}: {}'.format(file_identifier, file_name[0]))
