from PySide import QtGui, QtCore, QtSql
import Util


class TabTransMan(QtGui.QTabWidget):
    def __init__(self, parent):
        super(TabTransMan, self).__init__(parent)

        class KeyPressEater(QtCore.QObject):
            def eventFilter(self, obj, event):
                if event.type() == QtCore.QEvent.KeyPress:
                    if event.key() == QtCore.Qt.Key_Enter or event.key() == QtCore.Qt.Key_Return:
                        event.accept()
                        self.parent().checkInOutBut.click()
                        return True
                return QtCore.QObject.eventFilter(self, obj, event)

        # Reference Stuff
        self.parent = parent
        self.db = parent.db
        self.GIDFromScanner = False
        self.viewTransactions = None
        self.transModel = None

        # KeyPressEater fields commands/attributes
        self.scannerIsTyping = False
        self.keyStrokeList = ''

        # No focus on the tab itself
        self.setFocusPolicy(QtCore.Qt.NoFocus)

        # Member Search box
        name_label, self.nameSearch, bDayLay, self.bDayBox = \
            Util.make_line_edit_combobox(self, 'Member Name', 'Search for member name...', 'Birthday')

        # Make the gear ID search field
        gNameIDSearchLab, self.gNameIDSearch, gDissAmbLab, self.gDissAmbSearch = \
            Util.make_line_edit_combobox(self, 'Gear Name/ID', 'Search for gear name or ID', 'Gear ID/Name')
        self.gNameIDSearch.setPlaceholderText('Search for gear name or ID...')

        # Member return search box
        name_return_label = QtGui.QLabel('Return for')
        self.nameRetSearch = QtGui.QComboBox()
        self.nameRetSearch.setEditable(False)
        self.nameRetSearch.setInsertPolicy(QtGui.QComboBox.InsertAlphabetically)
        self.nameRetSearch.setEnabled(False)

        bDayRetLay = QtGui.QLabel('Birthday')
        self.bDayRetBox = QtGui.QComboBox()
        self.bDayRetBox.setEditable(False)
        self.bDayRetBox.setInsertPolicy(QtGui.QComboBox.InsertAlphabetically)
        self.bDayRetBox.setEnabled(False)

        # Make the # to check out / available / total items field
        self.numToCheckOutLab = QtGui.QLabel()
        self.numToCheckOutSpin = QtGui.QSpinBox()
        numToCheckOutSpinLE = self.numToCheckOutSpin.lineEdit()
        numToCheckOutSpinLE.setReadOnly(True)
        numToCheckOutSpinLE.setFocusPolicy(QtCore.Qt.NoFocus)
        numSlash1Lab = QtGui.QLabel('/')
        self.numRemEdit = Util.make_line_edit_display_only()
        numSlash2Lab = QtGui.QLabel('/')
        self.numTotEdit = Util.make_line_edit_display_only()

        self.numRemEdit.setAlignment(QtCore.Qt.AlignHCenter)
        self.numTotEdit.setAlignment(QtCore.Qt.AlignHCenter)

        self.numRemEdit.setText('0')
        self.numTotEdit.setText('0')

        self.numToCheckOutSpin.setRange(1, 1)
        self.numRemEdit.setMaximumWidth(20)
        self.numTotEdit.setMaximumWidth(20)

        numToCheckOutLay = QtGui.QHBoxLayout()
        numToCheckOutLay.setSpacing(Util.layoutGridSpacing)
        numToCheckOutLay.setStretch(7, 1)
        numToCheckOutLay.addWidget(self.numToCheckOutSpin)
        numToCheckOutLay.addWidget(numSlash1Lab)
        numToCheckOutLay.addWidget(self.numRemEdit)
        numToCheckOutLay.addWidget(numSlash2Lab)
        numToCheckOutLay.addWidget(self.numTotEdit)
        numToCheckOutLay.addStretch()

        # Make the member check out eligibility field
        self.PaidEdit = Util.make_line_edit_display_only()
        self.PaidEdit.setAlignment(QtCore.Qt.AlignHCenter)

        # Search box
        box = QtGui.QGridLayout()
        box.setSpacing(Util.layoutGridSpacing)
        pass                                      ; box.setColumnStretch(0, 0); box.setColumnStretch(1, 1); box.setColumnStretch(2, 0); box.setColumnStretch(3, 1)
        box.setRowStretch(0, 0)
        box.setRowStretch(1, 0)
        box.setRowStretch(2, 0)
        box.addWidget(name_label           , 0, 0); box.addWidget(self.nameSearch   , 0, 1); box.addWidget(bDayLay    , 0, 2); box.addWidget(self.bDayBox       , 0, 3)
        box.addWidget(gNameIDSearchLab     , 1, 0); box.addWidget(self.gNameIDSearch, 1, 1); box.addWidget(gDissAmbLab, 1, 2); box.addWidget(self.gDissAmbSearch, 1, 3)
        box.addWidget(name_return_label    , 2, 0); box.addWidget(self.nameRetSearch, 2, 1); box.addWidget(bDayRetLay , 2, 2); box.addWidget(self.bDayRetBox    , 2, 3)
        box.addWidget(self.numToCheckOutLab, 3, 0); box.addLayout(numToCheckOutLay  , 3, 1)
        box.addWidget(self.PaidEdit        , 4, 0, 1, 4)

        search_box_lay = QtGui.QGroupBox()
        search_box_lay.setTitle('Search')
        search_box_lay.setLayout(box)

        # Due date calendar
        self.dueDateCal = QtGui.QCalendarWidget()
        self.dueDateCal.setVerticalHeaderFormat(QtGui.QCalendarWidget.NoVerticalHeader)
        self.dueDateCal.setSelectedDate(self.parent.sessionDueDate)
        self.dueDateCal.setMinimumDate(QtCore.QDate.currentDate())

        # Make the active date appear as the same even when the calendar is inactive
        p = QtGui.QPalette()
        col = p.color(QtGui.QPalette.Active, QtGui.QPalette.Highlight)
        p.setColor(QtGui.QPalette.Inactive, QtGui.QPalette.Highlight, col)
        p.setColor(QtGui.QPalette.Inactive, QtGui.QPalette.HighlightedText, Util.color['white'])
        self.dueDateCal.setPalette(p)

        due_date_lay = QtGui.QGridLayout(parent)
        due_date_lay.setSpacing(Util.layoutGridSpacing)
        due_date_lay.addWidget(self.dueDateCal, 0, 0)

        due_date_box = QtGui.QGroupBox()
        due_date_box.setTitle('Due Date')
        due_date_box.setLayout(due_date_lay)

        # Make the check in/out button
        self.checkInOutBut = QtGui.QPushButton()
        self.checkInOutBut.wasJustClicked = False

        # Make check in/out radio buttons
        transaction_group_box = QtGui.QGroupBox()
        transaction_group_box.setTitle('Transaction Filter')
        self.radioIn = QtGui.QRadioButton("In")
        self.radioOut = QtGui.QRadioButton("Out")

        vbox = QtGui.QVBoxLayout()
        vbox.setSpacing(Util.layoutGridSpacing)
        vbox.addWidget(self.radioIn)
        vbox.addWidget(self.radioOut)
        transaction_group_box.setLayout(vbox)

        # Make the payment button view
        self.payBut = QtGui.QPushButton("Make payment")
        self.payBut.clicked.connect(self.Button_showPaymentWindow)

        # Make the table view
        viewTransBut = QtGui.QPushButton("Show Active\nTransaction")
        viewTransBut.clicked.connect(self.Button_showTrans)

        # Make the checked out gear window
        self.transView = Util.QTableViewCustom(self)
        self.transView.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.transView.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.transView.setCornerButtonEnabled(False)
        self.update_table()

        # Generate the grid
        table_lay = QtGui.QGridLayout()
        table_lay.setSpacing(Util.layoutGridSpacing)
        pass                         ; table_lay.setColumnStretch(0, 0); table_lay.setColumnStretch(1, 1)
        table_lay.setRowStretch(0, 0)
        table_lay.setRowStretch(4, 1)

        # Populate the table_lay
        table_lay.addWidget(transaction_group_box, 0, 0); table_lay.addWidget(self.transView, 0, 1, 5, 3)
        table_lay.addWidget(self.checkInOutBut, 1, 0)
        table_lay.addWidget(self.payBut, 2, 0)
        table_lay.addWidget(viewTransBut, 3, 0)

        hbox = QtGui.QHBoxLayout()
        hbox.setSpacing(Util.layoutGridSpacing)
        hbox.addLayout(table_lay)
        disp_box_lay = QtGui.QGroupBox()
        disp_box_lay.setTitle('Transaction Info')
        disp_box_lay.setLayout(hbox)

        grid = QtGui.QGridLayout(parent)
        grid.setSpacing(Util.layoutGridSpacing)
        pass                                ; grid.setColumnStretch(0, 1); grid.setColumnStretch(1, 0)
        grid.setRowStretch(0, 0)
        grid.setRowStretch(1, 1)
        grid.addWidget(search_box_lay, 0, 0); grid.addWidget(due_date_box, 0, 1)
        grid.addWidget(disp_box_lay, 1, 0, 2, 2)

        self.setLayout(grid)

        # Generate the completers
        self.set_completers()

        # # # # # # # # # #
        # Connect objects #
        # # # # # # # # # #

        # Search fields
        self.nameSearch.textChanged.connect(self.fillMemberSearch)
        self.bDayBox.activated.connect(self.fillMemberSearch)
        self.bDayBox.currentIndexChanged.connect(self.updCurrentBDayComboBox)

        self.gNameIDSearch.textChanged.connect(self.fillGearSearch)
        self.gDissAmbSearch.activated.connect(self.fillGearSearch)
        self.gDissAmbSearch.currentIndexChanged.connect(self.updCurrentGearComboBox)

        self.nameRetSearch.currentIndexChanged.connect(self.fillMemberReturn)

        self.checkInOutBut.clicked.connect(self.Button_checkInOutButClicked)
        self.installEventFilter(KeyPressEater(self))

        self.radioIn.clicked.connect(self.Button_radInClicked)
        self.radioOut.clicked.connect(self.Button_radOutClicked)
        self.radioIn.click()

        self.transView.clicked.connect(self.Button_getGIDTransTable)

    def setScannerField(self, gear_id):

        self.gNameIDSearch.setText(gear_id)
        self.GIDFromScanner = True
        self.trans()

    def update_table(self):

        if self.parent.currentMember:
            # cmd = ('SELECT G.Name, G.ID, strftime("%m/%d/%Y %H:%M", T.CheckOutDateTime), '
            #        'strftime("%m/%d/%Y", T.DueDate) '
            #        'FROM Member M, Gear G, Transactions T '
            #        'WHERE M.ID={mid} AND M.ID=T.MID AND T.GID=G.ID '
            #        'ORDER BY T.DueDate ASC').format(mid=self.parent.currentMember.ID)

            filt = 'MID={}'.format(self.parent.currentMember.ID)
        else:
            # cmd = ''
            filt = 'MID=-1'

        # query = self.db.execQuery(cmd, 'TabTransMan.py -> updateTable')

        trans_model = Util.TransactionSqlModel()
        trans_model.setEditStrategy(Util.TransactionSqlModel.OnFieldChange)
        # trans_model.setQuery(query)
        trans_model.setTable('Transactions')
        trans_model.setFilter(filt)
        trans_model.select()
        trans_model.setHeaderData(0, QtCore.Qt.Horizontal, 'Transaction ID')
        trans_model.setHeaderData(1, QtCore.Qt.Horizontal, 'Member ID')
        trans_model.setHeaderData(2, QtCore.Qt.Horizontal, 'Gear ID')
        trans_model.setHeaderData(3, QtCore.Qt.Horizontal, 'Check Out Date/Time')
        trans_model.setHeaderData(4, QtCore.Qt.Horizontal, 'Due Date')

        self.transView.setModel(trans_model)
        self.transView.hideColumn(0)
        self.transView.hideColumn(1)
        self.transView.setItemDelegate(Util.DateEditDelegate())
        self.transView.resizeColumnsToContents()
        self.transView.setSortingEnabled(True)
        self.transView.sortByColumn(4, QtCore.Qt.AscendingOrder)

    def trans(self):

        # Clear the message window
        self.parent.set_stat_message()

        # Attempt to return an item
        if self.radioIn.isChecked():

            ok = self.check_gear_in()

            # Update the inventory counts
            self.update_inventory_display()

            return ok

        # Attempt to check out an item
        elif self.radioOut.isChecked():

            if self.is_able_to_check_gear_out():

                # Pass all these checks before attempting to check out or return an item
                error = False
                if not self.parent.currentMember:
                    if self.bDayBox.count() > 1:
                        self.bDayBox.showPopup()
                    else:
                        self.nameSearch.setColors(bg='red')
                        self.parent.set_stat_message('Invalid Name/Birthday Entered!!!', c='red')
                    error = True

                if not self.parent.currentGear:
                    if self.gDissAmbSearch.count() > 1:
                        self.gDissAmbSearch.showPopup()
                    else:
                        self.gNameIDSearch.setColors(bg='red')
                        self.parent.set_stat_message('Invalid Gear ID / Name Entered!!!', c='red')
                    error = True

                if not error:
                    ok = self.check_gear_out()

                    # Update the inventory counts
                    self.update_inventory_display()

                    return ok

        return False

    def check_gear_in(self):

        if self.parent.currentGear:
            
            if self.parent.currentMember:

                trans = self.db.getTrans(gear=self.parent.currentGear)
    
                if trans:
    
                    other_member = self.db.getMember(self.nameRetSearch, self.bDayRetBox)
    
                    if other_member and trans.hasMID(other_member.ID):
    
                        # If currentTID is defined, return the item associated with that transaction
                        if self.checkInOutBut.wasJustClicked:
    
                            self.checkInOutBut.wasJustClicked = False
    
#                             reply = QtGui.QMessageBox.question(self, 'Confirm Check In',
#                                 'Are you sure you want to check in item:\n\n{}, {}'.format(
#                                       self.parent.currentGear.Name, self.parent.currentGear.ID),
#                                 QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
#
#                             # If the user does not want to return the item, exit this function
#                             if reply == QtGui.QMessageBox.No:
#                                 return
    
                        reply = QtGui.QMessageBox.question(self, 'Confirm Check In',
                                                           'Do you want to return this item for {}?'.format(
                                                           other_member.full_name()),
                                                           QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,
                                                           QtGui.QMessageBox.No)
    
                        # If the user does not want to return the item, exit this function
                        if reply == QtGui.QMessageBox.No:
                            return False
    
                        trans = self.db.getTrans(gear=self.parent.currentGear, member=other_member)
    
                        # Check in all the items requested
                        self.db.returnItem(trans, self.numToCheckOutSpin.value(), self.parent.currentMember)
                        return_message = '"{}" returned for {}'.format(self.parent.currentGear.Name, other_member.full_name())
    
                        self.update_table()
                        self.fillMemberReturn()
                        self.parent.set_stat_message(return_message)
                        return True
    
                    elif trans.hasMID(self.parent.currentMember.ID):
    
                        # If currentTID is defined, return the item associated with that transaction
                        if self.checkInOutBut.wasJustClicked:
    
                            self.checkInOutBut.wasJustClicked = False
    
    #                         reply = QtGui.QMessageBox.question(self, 'Confirm Check In',
    #                             'Are you sure you want to check in item:\n\n{}, {}'.format(self.parent.currentGear.Name, self.parent.currentGear.ID),
    #                             QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
    #
    #                         # If the user does not want to return the item, exit this function
    #                         if reply == QtGui.QMessageBox.No:
    #                             return False
    
                        trans = self.db.getTrans(gear=self.parent.currentGear, member=self.parent.currentMember)
    
                        # Check in all the items requested
                        self.db.returnItem(trans, self.numToCheckOutSpin.value())
                        return_message = '"{}" returned'.format(self.parent.currentGear.Name)
    
                        self.update_table()
                        self.fillMemberReturn()
                        self.parent.set_stat_message(return_message)
                        return True
    
            else:
                self.parent.set_stat_message(Util.noActiveGear, c='red')
                if self.gDissAmbSearch.count() > 1 and self.gDissAmbSearch.currentIndex() == 1:
                    self.gDissAmbSearch.showPopup()
    
        else:
            self.parent.set_stat_message(Util.noActiveMember, c='red')
            if self.bDayBox.count() > 1 and self.bDayBox.currentIndex() == 1:
                self.bDayBox.showPopup()

        return False

    def check_gear_out(self):

        if self.parent.currentMember:
            
            if self.parent.currentGear:

                # Check out the specified number of items
                for _ in xrange(self.numToCheckOutSpin.value()):
    
                    if self.parent.currentMember.eligibleToCheckOut() and self.parent.currentGear.is_checkoutable():
    
                        due_date = self.dueDateCal.selectedDate()
                        self.db.wTransaction(self.parent.currentMember, self.parent.currentGear, due_date)
                        self.transView.clearSelection()
                        self.update_table()
                        self.parent.set_stat_message("'{}' checked out to: {}".format(self.parent.currentGear.Name, self.parent.currentMember.nameBDay()))
                        return True
                    else:
    
                        # Figure out why the transaction cannot be done
    
                        reasons = []
    
                        if self.parent.currentGear.Unrentable:
                            reasons.append('Gear marked as Unrentable: {}'.format(self.parent.currentGear.UnrentableReason))
    
                        if self.parent.currentGear.numAvailable() == 0:
                            reasons.append('Out of stock of this item')
                            self.numRemEdit.setColors(bg='red', text='white')
                        elif self.parent.currentGear.numAvailable < 0:
                            reasons.append('Inventory error!  Less than 0 items left!?!?')
    
                        if not self.parent.currentMember.is_currently_paid():
                            reasons.append('Dues not Paid')
    
                        if not self.parent.currentMember.formsCurrent():
                            reasons.append('Waivers not up to date')
    
                        if not self.parent.currentMember.campusLink():
                            reasons.append('Not in CampusLink')
    
                        self.parent.set_stat_message(', '.join(reasons), c='red')
                        break
    
            else:
                self.parent.set_stat_message(Util.noActiveGear, c='red')
                if self.gDissAmbSearch.count() > 1 and self.gDissAmbSearch.currentIndex() == 1:
                    self.gDissAmbSearch.showPopup()
    
        else:
            self.parent.set_stat_message(Util.noActiveMember, c='red')
            if self.bDayBox.count() > 1 and self.bDayBox.currentIndex() == 1:
                self.bDayBox.showPopup()

        return False

    def update_inventory_display(self):

        disable = False

        # Is there a current member and current gear to use to look for a potential transaction?
        if self.parent.currentGear:

            # How many items are available to check out?
            num_available = self.parent.currentGear.numAvailable()
            num_total = self.parent.currentGear.numInInventory()

            self.numRemEdit.setText('{}'.format(num_available))
            self.numTotEdit.setText('{}'.format(num_total))

            if self.parent.currentMember:

                if self.radioIn.isChecked():

                    # Is there a transaction with the current member and current gear?
                    trans = self.db.getTrans(gear=self.parent.currentGear, member=self.parent.currentMember)

                    if trans:
                        self.numToCheckOutSpin.setRange(1, len(trans))
                        self.numToCheckOutSpin.setValue(1)
                    else:
                        disable = True

                elif self.radioOut.isChecked():

                    if num_available >= 1:
                        self.numToCheckOutSpin.setRange(1, num_available)
                        self.numToCheckOutSpin.setValue(1)
                    elif num_available == 0:
                        self.numToCheckOutSpin.setRange(1, 1)
                        self.numToCheckOutSpin.setValue(0)
                    else:
                        disable = True

        else:
            disable = True

        if not self.parent.currentGear:
            self.numRemEdit.setText('0')
            self.numTotEdit.setText('0')

        if disable:
            self.numToCheckOutSpin.setRange(1, 1)

    def fillMemberSearch(self):

        self.db.fillMember(self.nameSearch.text(), self.bDayBox)

        self.update_inventory_display()
        self.update_table()
        self.parent.tabWid.widget(1).fillMemberFields()

        self.is_able_to_check_gear_out()

        self.fillMemberReturn()

        if not self.parent.currentMember:
            self.dueDateCal.setSelectedDate(self.parent.sessionDueDate)

    def updCurrentBDayComboBox(self):

        self.parent.currentMember = self.db.getMember(self.nameSearch, self.bDayBox)

        self.parent.currentBDayBox = self.bDayBox.currentText()

    def fillGearSearch(self):

        self.db.fill_gear(self.gNameIDSearch, self.gDissAmbSearch)

        self.update_inventory_display()

        self.fillMemberReturn()

    def updCurrentGearComboBox(self):

        self.parent.currentGear = self.db.getGear(self.gNameIDSearch, self.gDissAmbSearch)

        self.parent.currentGearComboBox = self.gDissAmbSearch.currentText()

    def fillMemberReturn(self):

        self.db.fillMember(self.nameRetSearch.currentText(), self.bDayRetBox, updCurFields=False)

        if self.parent.currentMember and self.parent.currentGear and self.radioIn.isChecked() and \
                        self.parent.currentGear.numCheckedOut() > 0:

            mid_list = self.parent.currentGear.whoHasMe()

            mid_list = [MID for MID in mid_list if MID != self.parent.currentMember.ID]

            if mid_list:

                name_list = []
                for MID in mid_list:
                    member = self.db.getMember(MID)

                    name_list.append(member.full_name())

                name_list = Util.sort_list(name_list)

                self.nameRetSearch.setEnabled(True)
                self.bDayRetBox.setEnabled(True)

                old_item_list = self.nameRetSearch.get_menu()

                if name_list != old_item_list:

                    self.nameRetSearch.setMenu([Util.returnFor] + name_list, block_signals=True)

                return

        self.nameRetSearch.clear()
        self.nameRetSearch.setEnabled(False)
        self.bDayRetBox.setEnabled(False)

    def is_able_to_check_gear_out(self):

        # Does the member exist?
        if self.parent.currentMember:

            status_string = []

            # Has the member paid (if not exempt)
            if self.parent.currentMember.is_currently_paid() or self.parent.currentMember.MembStat != self.db.memberStatus[0]:
                able_to_check_out = True
            else:
                status_string.append('No Current Payment')
                able_to_check_out = False

            # Does the member have up to date papers on file?
            if not self.parent.currentMember.formsCurrent():
                status_string.append('No current waivers')
                able_to_check_out = False

            # Is the member in campus link (only if the member is a undergraduate or graduate)?
            if not self.parent.currentMember.campusLink():
                status_string.append('No current campusLink registration')
                able_to_check_out = False

            # Does the member have the required certifications to check out this piece of gear?
            if self.parent.currentGear and not self.parent.currentMember.hasReqCerts(self.parent.currentGear):
                status_string.append('Lacking proper certifications')  # TODO: specify which certifications are missing
                able_to_check_out = False

            # TODO: This only checks the member window, not currentMember object.  So if the user fixes the member
            # info, but does not update the current member, the transaction will be able to complete.
            # Is this a feature or a bug?
            # Detect whether the info in the window matches the info in the member object
            # TODO: Do this for the gear too.
            if not self.parent.tabWid.widget(1).areMemberFieldsValid():
                status_string.append('Member profile not complete')
                able_to_check_out = False

            if self.parent.currentMember.LastUpdated <= self.db.getSemesterDates()['SemFallStart']:
                status_string.append('Member profile has not been updated this school year')
                able_to_check_out = False

            # Format and fill the checkout eligibility window
            status_string = ' !!! '.join(status_string)
            if status_string:
                status_string = '!!! {} !!!'.format(status_string)

            if able_to_check_out:
                self.PaidEdit.setText('Member can rent gear')
                self.PaidEdit.setColors(bg='green', text='black')
            else:
                self.PaidEdit.setText(status_string)
                self.PaidEdit.setColors(bg='red', text='white')

            return able_to_check_out

        else:
            self.PaidEdit.clear()
            return False

    def set_current_member_gear(self):

        # Member name
        currentMemberNameID = self.parent.currentMemberNameID
        currentBDayBox = self.parent.currentBDayBox
        self.nameSearch.clear()
        self.nameSearch.setText(currentMemberNameID)
        self.bDayBox.setCurrentIndex(self.bDayBox.findText(currentBDayBox))

        # Gear name and ID
        currentGearLineEdit = self.parent.currentGearLineEdit
        currentGearComboBox = self.parent.currentGearComboBox
        self.gNameIDSearch.setText(currentGearLineEdit)
        if currentGearComboBox:
            self.gDissAmbSearch.setCurrentIndex(self.gDissAmbSearch.findText(currentGearComboBox))

    def set_completers(self):

        # Set the already existing completers
        self.nameSearch.setCompleter2(self.parent.memberNameComp)
        self.gNameIDSearch.setCompleter2(self.parent.gearNameIDComp)

    def update_completers(self):

        # Generate the completers
        self.parent.memberNameComp = self.parent.get_member_name_comp()
        self.parent.gearNameIDComp = self.parent.get_gear_name_id_comp()

        # Set the completers
        self.set_completers()

    def update_tab(self):

        self.keyStrokeList = ''
        self.set_current_member_gear()

        self.parent.tabWid.widget(1).update_tab()

        self.update_table()
        self.update_inventory_display()
        self.is_able_to_check_gear_out()
        self.set_completers()

    def get_member_id_and_gear_id_from_transaction_table(self):

        # Clear the message window
        self.parent.set_stat_message()

        row = self.viewTransactions.currentIndex().row()
        mid, gid, row = self.db.getMID_GID_row_TransTable(row)
        self.parent.currentMember = self.db.getMember(mid)
        self.parent.currentGear = self.db.getGear(gid)

        self.nameSearch.setText(self.parent.currentMember.full_name())
        self.bDayBox.setCurrentIndex(self.bDayBox.findText(
            Util.convert_date('Qt2Disp', self.parent.currentMember.Birthday)))

        gid = self.parent.currentGear.ID
        self.gNameIDSearch.setText(self.parent.currentGear.Name)

        ind = self.gDissAmbSearch.findText(gid)
        self.gDissAmbSearch.setCurrentIndex(ind)

        self.update_table()

        self.transView.selectRow(row)
        
    def get_default_due_date(self):

        return self.db.get_default_due_date()

    def Button_radInClicked(self):

        # Clear the message window
        self.parent.set_stat_message()

        self.checkInOutBut.setText('Check Gear\nIn')
        self.numToCheckOutLab.setText('# Check In')
        self.update_inventory_display()
        self.fillMemberReturn()

    def Button_radOutClicked(self):

        # Clear the message window
        self.parent.set_stat_message()
        
        self.checkInOutBut.setText('Check Gear\nOut')
        self.numToCheckOutLab.setText('# Check Out')
        self.update_inventory_display()
        self.fillMemberReturn()

    def Button_getGIDTransTable(self):

        # Clear the message window
        self.parent.set_stat_message()

        row = self.transView.currentIndex().row()

        self.parent.currentMember = self.db.getMember(self.nameSearch, self.bDayBox)
        gear_id = self.db.getGearIDTransTable(row, self.parent.currentMember)
        self.parent.currentGear = self.db.getGear(gear_id)

        if self.parent.currentGear:
            name = self.parent.currentGear.Name
            gid = self.parent.currentGear.ID
            self.gNameIDSearch.setText(name)
            ind = self.gDissAmbSearch.findText(gid)
            self.gDissAmbSearch.setCurrentIndex(ind)

    def Button_showTrans(self):

        # Clear the message window
        self.parent.set_stat_message()

        cmd = 'SELECT M.FirstName, M.LastName, strftime("%m/%d/%Y", M.Birthday), G.Name, T.GID, ' \
              'strftime("%m/%d/%Y %H:%M:%S", T.CheckOutDateTime), strftime("%m/%d/%Y", T.DueDate) ' \
              'FROM Transactions T ' \
              'JOIN Member M ON T.MID=M.ID ' \
              'JOIN Gear G ON T.GID=G.ID'# ORDER BY T.DueDate ASC')
        query = self.db.execQuery(cmd, 'database.py -> showTrans')

        model = QtSql.QSqlQueryModel()
        model.setQuery(query)
        model.setHeaderData(0, QtCore.Qt.Horizontal, 'First Name')
        model.setHeaderData(1, QtCore.Qt.Horizontal, 'Last Name')
        model.setHeaderData(2, QtCore.Qt.Horizontal, 'Birthday')
        model.setHeaderData(3, QtCore.Qt.Horizontal, 'Gear Name')
        model.setHeaderData(4, QtCore.Qt.Horizontal, 'Gear ID')
        model.setHeaderData(5, QtCore.Qt.Horizontal, 'Check Out Date/Time')
        model.setHeaderData(6, QtCore.Qt.Horizontal, 'Due Date')

        self.viewTransactions = QtGui.QTableView()
        self.viewTransactions.setWindowTitle('Active Transactions List')
        self.viewTransactions.setWindowIcon(self.parent.icon)
        self.viewTransactions.resize(600, 500)
        self.viewTransactions.setModel(model)
        self.viewTransactions.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.viewTransactions.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.viewTransactions.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.viewTransactions.clicked.connect(self.get_member_id_and_gear_id_from_transaction_table)
        self.viewTransactions.resizeColumnsToContents()
        self.viewTransactions.setSortingEnabled(True)
        # self.viewTransactions.sortByColumn(7, QtCore.Qt.AscendingOrder)
        self.viewTransactions.show()

    def Button_checkInOutButClicked(self):

        # Clear the message window
        self.parent.set_stat_message()

        self.checkInOutBut.wasJustClicked = True
        self.trans()

    def Button_showPaymentWindow(self):

        # Clear the message window
        self.parent.set_stat_message()

        def setStatMessage(statBar, text=None, c=None, delay=Util.messageDelay):

            if not text:
                statBar.clearMessage()
                return
            
            if c:
                p = statBar.palette()
                p.setColor(QtGui.QPalette.WindowText, Util.color[c])
                statBar.setPalette(p)

            statBar.showMessage(text, delay)

        def showMembsPayments():

            cmd = 'SELECT M.FirstName, M.LastName, Amount, Date, Type, Comment FROM FinancialTrans F, Member M WHERE M.ID={0} AND F.MID=M.ID ORDER BY DATE ASC'.format(self.parent.currentMember.ID)

            query = self.db.execQuery(cmd, 'TabTransMan.py -> showMembsPayments -> showPaymentWindow')

            model = QtSql.QSqlQueryModel()
            model.setQuery(query)
            model.setHeaderData(0, QtCore.Qt.Horizontal, 'First Name')
            model.setHeaderData(1, QtCore.Qt.Horizontal, 'Last Name')
            model.setHeaderData(2, QtCore.Qt.Horizontal, 'Ammount')
            model.setHeaderData(3, QtCore.Qt.Horizontal, 'Date')
            model.setHeaderData(4, QtCore.Qt.Horizontal, 'Type')
            model.setHeaderData(5, QtCore.Qt.Horizontal, 'Comment')

            self.viewMembers = QtGui.QTableView(None)
            self.viewMembers.setWindowTitle('Member Transactions')
            self.viewMembers.setWindowIcon(self.parent.icon)
            self.viewMembers.resize(600, 500)
            self.viewMembers.setModel(model)
            self.viewMembers.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
            self.viewMembers.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
            self.viewMembers.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
            self.viewMembers.resizeColumnsToContents()
            self.viewMembers.show()

        def submit_payment():

            if self.parent.currentMember.is_currently_paid() and 'Rental' == payTypeBox.currentText():
                mess = 'Usage fee not accepted, already paid this semester!!!'
                setStatMessage(statBar, mess, c='red')
                self.parent.set_stat_message(mess, c='red')
                return

            self.db.submitPayment(payTypeBox, amountBox, payDateEdit, noteEdit)
            mess = 'Submitted payment: {0}, ${1:0.2f}'.format(payTypeBox.currentText(), amountBox.value())
            setStatMessage(statBar, mess)
            self.parent.set_stat_message(mess)
            self.is_able_to_check_gear_out()

        def payTypeBoxChanged():

            if payTypeBox.currentText() == 'Rental':
                amountBox.setValue(self.db.getRentalPrice())
                amountBox.setEnabled(False)
            else:
                amountBox.setEnabled(True)

        if self.parent.currentMember:

            self.payWind = QtGui.QWidget()
            self.payWind.setWindowTitle('Payment')
            self.payWind.setWindowIcon(self.parent.icon)

            # Create the window items
            payTypeLab = QtGui.QLabel('Type')
            payTypeBox = QtGui.QComboBox()
            payTypeBox.insertItems(0, self.db.paymentType.getList())

            # Payment amount
            amountLab = QtGui.QLabel('Amount')
            amountBox = QtGui.QDoubleSpinBox()
            amountBox.setPrefix("$")
            amountBox.setSingleStep(5)
            amountBox.setMaximum(10000.00)
            amountBox.setMinimum(0.00)
            amountBox.setValue(self.db.getRentalPrice())

            # Payment date
            payDateLab = QtGui.QLabel('Date')
            payDateEdit = QtGui.QDateEdit()

            # Buttons
            self.payWind.payBut = QtGui.QPushButton("Make payment")
            viewPaysBut = QtGui.QPushButton("View Payments")

            # Note field
            noteLab = QtGui.QLabel('Note')
            noteEdit = QtGui.QPlainTextEdit()

            statBar = QtGui.QStatusBar()
            setStatMessage(statBar, "I'm a message window.  Pay attention to me!!!")

            # Create the layout
            lay = QtGui.QGridLayout()
            lay.setSpacing(Util.layoutGridSpacing)
            pass                           ; lay.setColumnStretch(2, 1)
            lay.setRowStretch(0, 0)
            lay.addWidget(payTypeLab, 0, 0); lay.addWidget(payTypeBox , 0, 1); pass; lay.addWidget(self.payWind.payBut, 0, 3, 2, 1)
            lay.addWidget(amountLab , 1, 0); lay.addWidget(amountBox  , 1, 1)
            lay.addWidget(payDateLab, 2, 0); lay.addWidget(payDateEdit, 2, 1); pass; lay.addWidget(viewPaysBut        , 2, 3)
            lay.addWidget(noteLab   , 3, 0)
            lay.addWidget(noteEdit  , 4, 0, 1, 4)
            lay.addWidget(statBar   , 5, 0, 1, 4)

            self.payWind.setLayout(lay)
            self.payWind.show()

            # Connect objects
            self.payWind.payBut.pressed.connect(submit_payment)
            payTypeBox.currentIndexChanged.connect(payTypeBoxChanged)
            viewPaysBut.pressed.connect(showMembsPayments)

            # Initiate objects
            payTypeBoxChanged()

        else:
            self.parent.set_stat_message(Util.noActiveMember, c='red')
            if self.bDayBox.count() > 1 and self.bDayBox.currentIndex() == 1:
                self.bDayBox.showPopup()
