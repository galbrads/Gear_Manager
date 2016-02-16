from PySide import QtGui, QtCore, QtSql
import Util
import re


class TabMembMan(QtGui.QTabWidget):
    def __init__(self, parent):
        super(TabMembMan, self).__init__(parent)

        # Inherit stuff
        self.parent = parent
        self.db = parent.db

        # KeyPressEater fields commands/attributes
        # keyPressEater = KeyPressEater(self)
        # self.installEventFilter(keyPressEater)
        self.scannerIsTyping = False
        self.keyStrokeList = ''
        self.viewMembers = None
        self.viewGearHist = None

        # No focus on the tab itself
        self.setFocusPolicy(QtCore.Qt.NoFocus)

        # # # # # # # # # # # # # # # # # #
        # Member Name/Bday search fields  #
        # # # # # # # # # # # # # # # # # #
        nameLab, self.nameSearch, bDayLab, self.bDayBox = Util.make_line_edit_combobox(self, 'Name', 'Search for member to view/update', 'Birthday')

        # Assemble the search fields into a search box
        hbox = QtGui.QGridLayout()
        hbox.setSpacing(Util.layoutGridSpacing)
        pass                         ; hbox.setColumnStretch(0, 0); hbox.setColumnStretch(1, 2), hbox.setColumnStretch(2, 0); hbox.setColumnStretch(3, 1)
        hbox.setRowStretch(0, 0)
        hbox.addWidget(nameLab, 0, 0); hbox.addWidget(self.nameSearch, 0, 1); hbox.addWidget(bDayLab, 0, 2); hbox.addWidget(self.bDayBox, 0, 3)

        # Put the search box in a group box
        searchBox = QtGui.QGroupBox()
        searchBox.setTitle('Search')
        searchBox.setLayout(hbox)

        # # # # # # # # # # # # # # #
        # Member information fields #
        # # # # # # # # # # # # # # #

        MFNameLab, self.MFNameEdit = Util.make_line_edit(self, 'First Name', 'First Name')
        MLNameLab, self.MLNameEdit = Util.make_line_edit(self, 'Last Name' , 'Last Name')
        EmailLab , self.EmailEdit = Util.make_line_edit(self, 'Email'     , 'Email')
        PhoneLab , self.PhoneEdit = Util.make_line_edit(self, 'Phone'     , 'XXX-XXX-XXXX')
        MNumLab  , self.MNumEdit = Util.make_line_edit(self, 'M Number'  , 'M Number')

        # Form fields
        self.FormsCkbx = QtGui.QCheckBox('Waviers\nCurrent')
        self.FormsDateEdit = QtGui.QDateEdit()
        self.FormsDateEdit.setDisabled(True)

        # CampusLink fields
        self.campLinkCkbx = QtGui.QCheckBox('Campus Link\nCurrent')
        self.campLinkDateEdit = QtGui.QDateEdit()
        self.campLinkDateEdit.setDisabled(True)

        # Membership status box
        statusLab = QtGui.QLabel('Membership\nStatus')
        self.statusBox = QtGui.QComboBox()
        self.statusBox.insertItems(0, self.db.memberStatus.getList())

        # Student status box
        studStatLab = QtGui.QLabel('Student\nStatus')
        self.studStatBox = QtGui.QComboBox()
        self.studStatBox.insertItems(0, self.db.studentStatus.getList())

        # Birthday
        BirthdayLab = QtGui.QLabel('Birthday')
        self.BirthdayEdit = QtGui.QDateEdit()

        # Addresses
        addrLay = Util.address_layout(self, '', 'Address')

        # Set the row and column spacings
        memberLay = QtGui.QGridLayout()
        memberLay.setSpacing(Util.layoutGridSpacing)
        pass                          ; memberLay.setColumnStretch(0, 0); memberLay.setColumnStretch(1, 1), memberLay.setColumnStretch(2, 0); memberLay.setColumnStretch(3, 1)
        memberLay.setRowStretch(0, 0)
        memberLay.setRowStretch(1, 0)
        memberLay.setRowStretch(2, 0)
        memberLay.setRowStretch(3, 0)
        memberLay.setRowStretch(4, 0)
        memberLay.setRowStretch(5, 0)
        memberLay.setRowStretch(6, 0)
        memberLay.setRowStretch(7, 0)
        memberLay.setRowStretch(8, 0)
        memberLay.setRowStretch(9, 0)
        memberLay.setRowStretch(10, 0)

        # Place the objects on the page
        memberLay.addWidget(MFNameLab     , 0, 0); memberLay.addWidget(self.MFNameEdit   , 0, 1); memberLay.addWidget(MLNameLab        , 0, 2); memberLay.addWidget(self.MLNameEdit      , 0, 3)
        memberLay.addWidget(BirthdayLab   , 1, 0); memberLay.addWidget(self.BirthdayEdit , 1, 1); memberLay.addWidget(EmailLab         , 1, 2); memberLay.addWidget(self.EmailEdit       , 1, 3)
        memberLay.addWidget(PhoneLab      , 2, 0); memberLay.addWidget(self.PhoneEdit    , 2, 1); memberLay.addWidget(studStatLab      , 2, 2); memberLay.addWidget(self.studStatBox     , 2, 3)
        memberLay.addWidget(statusLab     , 3, 0); memberLay.addWidget(self.statusBox    , 3, 1); memberLay.addWidget(MNumLab          , 3, 2); memberLay.addWidget(self.MNumEdit        , 3, 3)
        memberLay.addWidget(self.FormsCkbx, 4, 0); memberLay.addWidget(self.FormsDateEdit, 4, 1); memberLay.addWidget(self.campLinkCkbx, 4, 2); memberLay.addWidget(self.campLinkDateEdit, 4, 3)
        memberLay.addWidget(self.addrLab  , 5, 0); memberLay.addLayout(addrLay           , 5, 1, 2, 3)

        memberBox = QtGui.QGroupBox()
        memberBox.setTitle('Member Information')
        memberBox.setLayout(memberLay)

        # # # # # # # # # # # # #
        # Member Certifications #
        # # # # # # # # # # # # #

        # Header
        certDate = 'Date Certified'
        vouchedBy = 'Vouched for by'
        certDateLab1 = QtGui.QLabel(certDate)
        certDateLab2 = QtGui.QLabel(certDate)
        vouchedByLab1 = QtGui.QLabel(vouchedBy)
        vouchedByLab2 = QtGui.QLabel(vouchedBy)

        for cert in Util.certifications:
            self.__dict__[cert + 'CertCkbx'], self.__dict__[cert + 'DateEdit'], self.__dict__[cert + 'Vouched'] = Util.certification_layout(self, cert)

        box = QtGui.QGridLayout()
        box.setSpacing(Util.layoutGridSpacing)
        pass                    ; box.setColumnStretch(0, 0); box.setColumnStretch(1, 0); box.setColumnStretch(2, 1); box.setColumnStretch(3, 0); box.setColumnStretch(4, 0); box.setColumnStretch(5, 1)
        box.setRowStretch(0, 0)
        box.setRowStretch(1, 0)
        box.setRowStretch(2, 0)
        row = 0
        col = 0
        pass                   ; box.addWidget(certDateLab1, 0, 1); box.addWidget(vouchedByLab1, 0, 2); box.addWidget(certDateLab2, 0, 4); box.addWidget(vouchedByLab2, 0, 5)
        for cert in Util.certifications:
            ind = Util.certifications.index(cert)
            if ind % 2 == 0:
                row += 1
                col = 0
            else:
                col += 3
            box.addWidget(self.__dict__[cert + 'CertCkbx'], row, col); box.addWidget(self.__dict__[cert + 'DateEdit'], row, col + 1); box.addWidget(self.__dict__[cert + 'Vouched'], row, col + 2)
        certBox = QtGui.QGroupBox()
        certBox.setTitle('Certifications')
        certBox.setLayout(box)

        # # # # # # # # # # # # # #
        # Emergency Contact Info  #
        # # # # # # # # # # # # # #

        emContactLay = Util.emergency_contact_layout(self, '')

        rommateLab     , self.rommateEdit = Util.make_line_edit(self, 'Roommate\nName' , 'Roommate Name')
        rommatePhoneLab, self.rommatePhoneEdit = Util.make_line_edit(self, 'Roommate\nPhone', 'XXX-XXX-XXXX')
        insLab         , self.insEdit = Util.make_line_edit(self, 'Insurance\nCompany', 'Insurance Company')
        insPolLab      , self.insPolEdit = Util.make_line_edit(self, 'Policy#', 'Policy#')
        insGrpLab      , self.insGrpEdit = Util.make_line_edit(self, 'Group#' , 'Group#')

        grid = QtGui.QGridLayout()
        grid.setSpacing(Util.layoutGridSpacing)

        grid.addLayout(emContactLay, 0, 0, 4, 6)
        grid.addWidget(rommateLab  , 8, 0); grid.addWidget(self.rommateEdit, 8, 1, 1 , 2); grid.addWidget(rommatePhoneLab, 8, 3); grid.addWidget(self.rommatePhoneEdit, 8, 4, 1, 2)
        grid.addWidget(insLab      , 9, 0); grid.addWidget(self.insEdit    , 9, 1, 1, 5)
        grid.addWidget(insPolLab   , 10, 0); grid.addWidget(self.insPolEdit, 10, 1)      ; grid.addWidget(insGrpLab      , 10, 3); grid.addWidget(self.insGrpEdit      , 10, 4)

        emContactBox = QtGui.QGroupBox()
        emContactBox.setTitle('Emergency Contact/Insurance Information')
        emContactBox.setLayout(grid)

        # Medical condition
        self.medEdit = QtGui.QPlainTextEdit()

        box = QtGui.QGridLayout()
        box.setSpacing(Util.layoutGridSpacing)
        box.addWidget(self.medEdit, 0, 0)

        medBox = QtGui.QGroupBox()
        medBox.setTitle('Medical Condition')
        medBox.setLayout(box)

        # Notes
        self.noteEdit = QtGui.QPlainTextEdit()

        box = QtGui.QGridLayout()
        box.setSpacing(Util.layoutGridSpacing)
        box.addWidget(self.noteEdit, 0, 0)

        noteBox = QtGui.QGroupBox()
        noteBox.setTitle('Note')
        noteBox.setLayout(box)

        # # # # # #
        # Buttons #
        # # # # # #

        # Save/Update button
        self.addUpdBut = QtGui.QPushButton()
        self.addUpdBut.setText('\nAdd Member\n')
        self.addUpdBut.setAutoDefault(True)
        self.addUpdBut.setDefault(True)

        # Delete button
        RemBtn = QtGui.QPushButton("\nRemove\n")

        # Member transaction history button
        MembHistBtn = QtGui.QPushButton("\nMember Transaction History\n")

        # Make the table view
        viewMembsBut = QtGui.QPushButton("\nView All Members\n")

        # Create the layout for the buttons
        buttonLay = QtGui.QGridLayout()
        buttonLay.setSpacing(Util.layoutGridSpacing)
        pass                         ; buttonLay.setColumnStretch(0, 0)
        buttonLay.setRowStretch(0, 0)

        buttonLay.addWidget(self.addUpdBut, 0, 0); buttonLay.addWidget(RemBtn      , 0, 1)
        buttonLay.addWidget(MembHistBtn   , 1, 0); buttonLay.addWidget(viewMembsBut, 1, 1)

        # # # # # # # # # # # # # #
        # Assemble the tab layout #
        # # # # # # # # # # # # # #

        lCol = QtGui.QGridLayout()
        lCol.setSpacing(Util.layoutGridSpacing)
        lCol.addWidget(memberBox, 0, 0)
        lCol.addWidget(certBox, 1, 0)
        lCol.setRowStretch(2, 1)
        lCol.addLayout(buttonLay, 3, 0)

        rCol = QtGui.QGridLayout()
        rCol.setSpacing(Util.layoutGridSpacing)
        rCol.setRowStretch(2, 1)
        rCol.addWidget(emContactBox, 1, 0)
        rCol.addWidget(medBox, 2, 0)
        rCol.addWidget(noteBox, 3, 0)

        grid = QtGui.QGridLayout()
        grid.setSpacing(Util.layoutGridSpacing)
        pass                    ; grid.setColumnStretch(0, 1); grid.setColumnStretch(1, 1)
        grid.setRowStretch(0, 0)
        grid.setRowStretch(1, 0)

        grid.addWidget(searchBox, 0, 0, 1, 2)
        grid.addLayout(lCol, 1, 0); grid.addLayout(rCol, 1, 1)

        self.setLayout(grid)

        # Generate the completers
        self.setCompleters()

        # # # # # # # # # #
        # Connect objects #
        # # # # # # # # # #

        # Search fields
        self.nameSearch.textChanged.connect(self.fillMemberSearch)
        self.bDayBox.activated.connect(self.fillMemberSearch)
        self.bDayBox.currentIndexChanged.connect(self.fillBDaySearch)

        # Member info fields
        self.FormsCkbx   .toggled.connect(self.FormsTogg)
        self.campLinkCkbx.toggled.connect(self.campusLinkTogg)
        self.studStatBox .currentIndexChanged.connect(self.studStatFeat)

        # Certifications
        for cert in Util.certifications:
            self.addCertTogg(self, cert)
            self.__dict__[cert + 'CertCkbx'].toggled.connect(self.__dict__[cert + 'Togg'])

        # Emergency Contact Phones
        self.emHPhoneEdit.textChanged.connect(self.EmPhoneHEdited)
        self.emWPhoneEdit.textChanged.connect(self.EmPhoneWEdited)
        self.emCPhoneEdit.textChanged.connect(self.EmPhoneCEdited)

        # Buttons
        self.addUpdBut.clicked.connect(self.Button_addUpdButClick)
        RemBtn.clicked.connect(self.Button_remMem)
        MembHistBtn.clicked.connect(self.Button_showMembHist)
        viewMembsBut.clicked.connect(self.Button_showMembs)

    def set_scanner_field(self, gear_id):

        self.parent.currentGearLineEdit = gear_id
        self.parent.currentGearComboBox = None

    def fillMemberFields(self):

        # If the member is found, fill out the member information
        if self.parent.currentMember:

            self.addUpdBut.setText('\nUpdate Member\n')

            self.MFNameEdit  .setText(self.parent.currentMember.FirstName)
            self.MLNameEdit  .setText(self.parent.currentMember.LastName)
            self.FormsCkbx   .setChecked(self.parent.currentMember.formsCurrent())
            if not self.parent.currentMember.campus_link_waived():
                self.campLinkCkbx.setChecked(self.parent.currentMember.campusLink())
            if self.parent.currentMember.formsCurrent():
                self.FormsDateEdit.setDate(self.parent.currentMember.FormsDate)
            if self.campLinkCkbx.isChecked():
                self.campLinkDateEdit.setDate(self.parent.currentMember.CampusLinkDate)
            if self.parent.currentMember.StudentID.upper() != 'NULL':
                self.MNumEdit.setText(self.parent.currentMember.StudentID)
            self.EmailEdit   .setText(self.parent.currentMember.Email)
            self.PhoneEdit   .setText(self.parent.currentMember.Phone)
            self.BirthdayEdit.setDate(self.parent.currentMember.Birthday)
            self.statusBox   .setCurrentIndex(self.statusBox.findText(self.parent.currentMember.MembStat))
            self.studStatBox .setCurrentIndex(self.studStatBox.findText(self.parent.currentMember.StudStat))

            # Address
            self.streetEdit.setText(self.parent.currentMember.Street)
            self.cityEdit  .setText(self.parent.currentMember.City)
            self.stateBox  .setCurrentIndex(self.stateBox.findText(self.parent.currentMember.State))
            self.zipEdit   .setText(self.parent.currentMember.Zip)

            # Emergency Contact Info
            self.emNameEdit .setText(self.parent.currentMember.EmName)
            self.emRelaltEdit.setText(self.parent.currentMember.EmRel)
            self.emHPhoneEdit.setText(self.parent.currentMember.EmPhoneH)
            self.emWPhoneEdit.setText(self.parent.currentMember.EmPhoneW)
            self.emCPhoneEdit.setText(self.parent.currentMember.EmPhoneC)
#             self.emStreetEdit.setText(self.parent.currentMember.EmStreet1)
#             self.emCityEdit  .setText(self.parent.currentMember.EmCity1)
#             self.emStateBox  .setCurrentIndex(self.em1StateBox.findText(self.parent.currentMember.EmState1))
#             self.emZipEdit   .setText(self.parent.currentMember.EmZip1)

            # Certifications
            for cert in Util.certifications:
                self.__dict__[cert + 'CertCkbx'].setChecked(self.parent.currentMember.__dict__[cert + 'Cert'])
                self.__dict__[cert + 'DateEdit'].setDate(self.parent.currentMember.__dict__[cert + 'CertDate'])
                self.__dict__[cert + 'Vouched'] .setText(self.parent.currentMember.__dict__[cert + 'CertVouch'])

            # Room mate name and phone
            self.rommateEdit     .setText(self.parent.currentMember.RoommateName)
            self.rommatePhoneEdit.setText(self.parent.currentMember.RoommatePhone)

            # Insurance fields
            self.insEdit   .setText(self.parent.currentMember.InsurName)
            self.insPolEdit.setText(self.parent.currentMember.InsurPol)
            self.insGrpEdit.setText(self.parent.currentMember.InsurGrp)

            # Medical Condition
            self.medEdit.setPlainText(self.parent.currentMember.Med)

            # Member notes
            self.noteEdit.setPlainText(self.parent.currentMember.Note)

        else:

            self.addUpdBut.setText('\nAdd Member\n')
            self.clear_fields()

    def fillMemberSearch(self):

        self.db.fillMember(self.nameSearch.text(), self.bDayBox)

    def fillBDaySearch(self):

        self.parent.currentMember = self.db.getMember(self.nameSearch, self.bDayBox)

        self.parent.currentBDayBox = self.bDayBox.currentText()

        self.fillMemberFields()

    def studStatFeat(self):

        if self.studStatBox.currentText() == self.db.studentStatus[2] or \
           self.studStatBox.currentText() == self.db.studentStatus[3]:
            self.MNumEdit.clear()
            self.MNumEdit.setEnabled(False)
            self.campLinkCkbx.setChecked(False)
            self.campLinkCkbx.setEnabled(False)
        else:
            self.MNumEdit.setEnabled(True)
            self.campLinkCkbx.setEnabled(True)

        self.campusLinkTogg()

    def FormsTogg(self):

        if self.FormsCkbx.isChecked():
            self.FormsDateEdit.setEnabled(True)
        else:
            self.FormsDateEdit.setDisabled(True)

    def campusLinkTogg(self):

        if self.campLinkCkbx.isEnabled():

            if self.campLinkCkbx.isChecked():
                self.campLinkDateEdit.setEnabled(True)
            else:
                self.campLinkDateEdit.setDisabled(True)

        else:
            self.campLinkCkbx.setChecked(False)
            self.campLinkDateEdit.setDisabled(True)

    def addCertTogg(self, cls, cert):
        def togg():
            if cls.__dict__[cert + 'CertCkbx'].isChecked():
                cls.__dict__[cert + 'DateEdit'].setEnabled(True)
                cls.__dict__[cert + 'Vouched'].setEnabled(True)
            else:
                cls.__dict__[cert + 'DateEdit'].setDisabled(True)
                cls.__dict__[cert + 'Vouched'].setDisabled(True)
                cls.__dict__[cert + 'Vouched'].clear()

        setattr(cls, cert + 'Togg', togg)

    def EmPhoneHEdited(self):

        self.emWPhoneEdit.setColors()
        self.emCPhoneEdit.setColors()

    def EmPhoneWEdited(self):

        self.emHPhoneEdit.setColors()
        self.emCPhoneEdit.setColors()

    def EmPhoneCEdited(self):

        self.emWPhoneEdit.setColors()
        self.emHPhoneEdit.setColors()

    def areMemberFieldsValid(self):

        def isPhoneValid(phoneEdit, required=False):

            # Clean up the phone number
            phone = phoneEdit.text()
            phone = re.sub('[^0-9]', '', phone)

            if not phone and not required:
                return True

            if len(phone) == 10:
                phone = '{}-{}-{}'.format(phone[:3], phone[3:6], phone[6:])
                phoneEdit.setText(phone)
                return True

            phoneEdit.setColors(bg='red')
            return False

        def isAddressValid(streetEdit, cityEdit, stateBox, zipEdit, required=False):

            Valid = True

            street = streetEdit.text().strip()
            city = cityEdit.text().strip()
            state = stateBox.currentText()
            zipCode = zipEdit.text().strip()

            # If any field is not empty and any field is empty, error
            if street or city or state or zipCode or required:

                if not street:
                    streetEdit.setColors(bg='red')
                    Valid = False
                if not city:
                    cityEdit.setColors(bg='red')
                    Valid = False
                if not state:
                    stateBox.setColors(bg='red')
                    Valid = False
                if not zipCode or len(zipCode) != 5 or not Util.is_number(zipCode):
                    zipEdit.setColors(bg='red')
                    Valid = False

            return Valid

        def isCertificationValid(Ckbx, DateEdit, Vouched):

            valid = True

            if Ckbx.isChecked():
                if DateEdit.date() > QtCore.QDate.currentDate():
                    DateEdit.setColors(bg='red')
                    valid = False
#                 if not Vouched.text():
#                     Vouched.setColors(bg='red')
#                     valid = False

            return valid

        def isEmergencyContactValid(nameEdit, relatEdit, hPhoneEdit, wPhoneEdit, cPhoneEdit, streetEdit, cityEdit, stateBox, zipEdit, required=False):

            valid = True

            name = nameEdit.text()
            relat = relatEdit.text()
            hPhone = hPhoneEdit.text()
            wPhone = wPhoneEdit.text()
            cPhone = cPhoneEdit.text()

            nameEdit.setColors()
            relatEdit.setColors()
            hPhoneEdit.setColors()
            wPhoneEdit.setColors()
            cPhoneEdit.setColors()
            streetEdit.setColors()
            cityEdit.setColors()
            zipEdit.setColors()

            if name or relat or hPhone or wPhone or cPhone or streetEdit.text() or cityEdit.text() or stateBox.currentText() or zipEdit.text() or required:
                if not name:
                    nameEdit.setColors(bg='red')
                    valid = False
                if not relat:
                    relatEdit.setColors(bg='red')
                    valid = False
                if not hPhone and not wPhone and not cPhone:
                    hPhoneEdit.setColors(bg='yellow')
                    wPhoneEdit.setColors(bg='yellow')
                    cPhoneEdit.setColors(bg='yellow')
                    valid = False
                else:
                    if hPhoneEdit.text() and not isPhoneValid(hPhoneEdit):
                        valid = False
                    if wPhoneEdit.text() and not isPhoneValid(wPhoneEdit):
                        valid = False
                    if cPhoneEdit.text() and not isPhoneValid(cPhoneEdit):
                        valid = False

                if not isAddressValid(streetEdit, cityEdit, stateBox, zipEdit):
                    valid = False

            return valid

        error = False

        if not self.MFNameEdit.text():
            self.MFNameEdit.setColors(bg='red')
            error = True

        if not self.MLNameEdit.text():
            self.MLNameEdit.setColors(bg='red')
            error = True

        if not self.EmailEdit.text() or '@' not in self.EmailEdit.text():
            self.EmailEdit.setColors(bg='red')
            error = True

        if self.BirthdayEdit.date() >= QtCore.QDate.currentDate() or self.BirthdayEdit.date() == QtCore.QDate(1900, 1, 1):
            self.BirthdayEdit.setColors(bg='red')
            error = True

        if not isPhoneValid(self.PhoneEdit, required=True):
            error = True

        # Make sure the student ID is unique before proceeding
        # if not self.db.isStudentIDAvailable( self.MFNameEdit.text(), self.MLNameEdit.text(), self.BirthdayEdit.dateDB(), self.MNumEdit.text() ):
        if self.nameSearch.text() and not self.db.isStudentIDAvailable(self.nameSearch.text(), Util.convert_date('Disp2Qt', self.bDayBox.currentText()), self.MNumEdit.text()):
            self.MNumEdit.setColors(bg='red')
            self.parent.set_stat_message('Student ID is not unique!!!', c='red')
            error = True

        if not self.statusBox.currentText():
            self.statusBox.setColors(bg='red')
            error = True

        if not self.studStatBox.currentText():
            self.studStatBox.setColors(bg='red')
            error = True

        # Address
        if not isAddressValid(self.streetEdit, self.cityEdit, self.stateBox, self.zipEdit, required=True):
            error = True

        # Certifications
        for cert in Util.certifications:
            if not isCertificationValid(self.__dict__[cert + 'CertCkbx'], self.__dict__[cert + 'DateEdit'], self.__dict__[cert + 'Vouched']):
                error = True

#         # Emergency contact 1
#         if not isEmergencyContactValid(self.emNameEdit, self.emRelaltEdit, self.emHPhoneEdit, self.emWPhoneEdit, self.emCPhoneEdit, self.emStreetEdit, self.emCityEdit, self.emStateBox, self.emZipEdit, required=True):
#             error = True

        # Room mate fields
        if not isPhoneValid(self.rommatePhoneEdit):
            error = True

#         # Insurance fields
#         if not self.insEdit.text():
#             self.insEdit.setColors(bg='red')
#             error = True
#
#         if not self.insPolEdit.text():
#             self.insPolEdit.setColors(bg='red')
#             error = True
#
#         if not self.insGrpEdit.text():
#             self.insGrpEdit.setColors(bg='red')
#             error = True

        # Medical information
        if not self.medEdit.document().toPlainText().strip():
            self.medEdit.setColors(bg='red')
            error = True

        # If no errors were found, return True
        return not error

    def addUpdMember(self, memberAttr):

        # If the member is not found, but a name is found,
        # and it has more than one bDay associated with it, show all other bDays
        if not self.parent.currentMember and self.bDayBox.count() >= 2:
            self.bDayBox.showPopup()
            self.parent.set_stat_message('Multiple members with the same name exist!!!', c='red')
            return False

        feildMember = self.db.getMember(memberAttr['FirstName'], memberAttr['LastName'], memberAttr['Birthday'])

        # If no member was found, this is a new member, and they should be added
        if not self.parent.currentMember and not feildMember:

            self.db.addItem('Member', memberAttr)
            self.updateCompleters()
            # self.fillBDaySearch()

            self.nameSearch.clear()
            self.nameSearch.setText('{0} {1}'.format(memberAttr['FirstName'], memberAttr['LastName']))
            thisBDayIndex = self.bDayBox.findText(Util.convert_date('DB2Disp', memberAttr['Birthday']))
            self.bDayBox.setCurrentIndex(thisBDayIndex)

            self.parent.set_stat_message('{0} {1}, {2} added'.format(memberAttr['FirstName'], memberAttr['LastName'], Util.convert_date('DB2Disp', memberAttr['Birthday'])))
            return True

        elif self.parent.currentMember and feildMember:

            if self.parent.currentMember.ID == feildMember.ID:

                # If a member was not found using the field info, but the entered ID is the same as
                #   that of the ID that of the member that was searched for, then update the information
                #   of the member that was searched for

                self.db.updateItem('Member', memberAttr, feildMember)

                # Get the new member information
                self.parent.currentMember = self.db.getMember(self.parent.currentMember.ID)

    #             # Update the completers if the member name changed
    #             if feildMember.fullName() != self.parent.currentMember.fullName():
    #                 self.updateCompleters()
    #                 self.nameSearch.setText(self.parent.currentMember.fullName())
    #
    #             # Update the birthday field if the birthday changed
    #             if feildMember.Birthday != self.parent.currentMember.Birthday or self.bDayBox.count() > 1:
    #                 thisBDayIndex = self.bDayBox.findText(self.parent.currentMember.BirthdayForm('Disp'))
    #                 self.bDayBox.setCurrentIndex(thisBDayIndex)
                self.fillBDaySearch()
                self.parent.set_stat_message('{0} updated'.format(self.parent.currentMember.nameBDay()))
                return True

            else:

                # If a member was generated using the field info, then the search member cannot be updated
                #   because the search member info conflicts with a existing member.
                self.MFNameEdit.setColors(bg='red')
                self.MLNameEdit.setColors(bg='red')
                self.BirthdayEdit.setColors(bg='red')
                self.parent.set_stat_message('Cannot add member! Another member with the same Name/Birthday already exists', c='red')
                return False

        return False

    def clear_fields(self):

        self.MFNameEdit.clear()
        self.MLNameEdit.clear()
        self.FormsCkbx.setChecked(False)
        self.campLinkCkbx.setChecked(False)
        self.EmailEdit.clear()
        self.MNumEdit.clear()
        self.PhoneEdit.clear()
        self.BirthdayEdit.setDate(QtCore.QDate.currentDate())
        self.FormsDateEdit.setDate(QtCore.QDate.currentDate())
        self.campLinkDateEdit.setDate(QtCore.QDate.currentDate())
        self.statusBox.setCurrentIndex(0)
        self.studStatBox.setCurrentIndex(0)

        # Address
        self.streetEdit.clear()
        self.cityEdit.clear()
        self.stateBox.setCurrentIndex(0)
        self.zipEdit.clear()

        # Emergency Contact 1 Info
        self.emNameEdit  .clear()
        self.emRelaltEdit.clear()
        self.emHPhoneEdit.clear()
        self.emWPhoneEdit.clear()
        self.emCPhoneEdit.clear()
#         self.emStreetEdit.clear()
#         self.emCityEdit  .clear()
#         self.emStateBox.setCurrentIndex(0)
#         self.emZipEdit   .clear()

        # Room mate name and phone
        self.rommateEdit     .clear()
        self.rommatePhoneEdit.clear()

        # Insurance fields
        self.insEdit   .clear()
        self.insPolEdit.clear()
        self.insGrpEdit.clear()

        # Certifications
        for cert in Util.certifications:
            self.__dict__[cert + 'CertCkbx'].setChecked(False)
            self.__dict__[cert + 'DateEdit'].setDate(QtCore.QDate.currentDate())
            self.__dict__[cert + 'Vouched'] .clear()

        # Medical edit
        self.medEdit.clear()

        # Member Notes
        self.noteEdit.clear()

    def setCurrentMemberGear(self):

        currentMemberNameID = self.parent.currentMemberNameID
        currentBDayBox = self.parent.currentBDayBox
        self.nameSearch.clear()
        self.nameSearch.setText(currentMemberNameID)
        self.bDayBox.setCurrentIndex(self.bDayBox.findText(currentBDayBox))

    def setCompleters(self):

        # Set the already existing completers
        self.nameSearch.setCompleter2(self.parent.memberNameComp)

#         for cert in Util.certifications:
#             self.__dict__[cert + 'Vouched'].setCompleter2(self.parent.memberNameComp)

    def updateCompleters(self):

        # Generate the completers
        self.parent.memberNameComp = self.parent.get_member_name_comp()

        # Set the completers
        self.setCompleters()

    def update_tab(self):

        self.keyStrokeList = ''
        self.setCurrentMemberGear()
        self.fillMemberFields()
        self.setCompleters()

    def getMIDMemberTable(self):

        # Clear the message window
        self.parent.set_stat_message()

        row = self.viewMembers.currentIndex().row()
        mid = self.db.getAttrFromTable('Member', 'ID', row)
        self.parent.currentMember = self.db.getMember(mid)

        self.nameSearch.setText(self.parent.currentMember.full_name())
        bDayInd = self.bDayBox.findText(Util.convert_date('Qt2Disp', self.parent.currentMember.Birthday))
        self.bDayBox.setCurrentIndex(bDayInd)

    def getGIDMembHistTable(self):

        # Clear the message window
        self.parent.set_stat_message()

        if not self.parent.currentMember:
            self.parent.set_stat_message(Util.noActiveMember, c='red')

        row = self.viewGearHist.currentIndex().row()
        gid = self.db.getAttrFromTable('ArchiveTrans', 'gid', row, 'ORDER BY CheckInDateTime DESC')

        self.parent.currentGearLineEdit = gid
        self.parent.currentGearComboBox = None

        # gid  = self.db.getAttrFromTable('ArchiveTrans', 'gid', row, 'ORDER BY CheckInDateTime DESC')

        # self.parent.currentMember = self.db.getMember(MID)

        # self.nameSearch.setText(self.parent.currentMember.fullName())
        # self.bDayBox.clear()
        # self.bDayBox.insertItem(0, self.parent.currentMember.BirthdayForm('Disp') )

    def Button_remMem(self):

        # Clear the message window
        self.parent.set_stat_message()

        if self.parent.currentMember:

            if self.parent.currentMember.has_active_transactions():
                self.parent.set_stat_message(self.parent.currentMember.nameBDay() + ' has gear checked out and cannot be deleted!!!', c='red')
            else:
                reply = QtGui.QMessageBox.question(self, 'Confirm Delete',
                                                   'Are you sure you want to remove:\n\n' +
                                                   self.parent.currentMember.nameBDay(),
                                                   QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)

                if reply == QtGui.QMessageBox.Yes:
                    self.db.delItem('Member', self.parent.currentMember)

                    # Clear/reset all the fields
                    self.parent.set_stat_message(self.parent.currentMember.nameBDay() + ' removed')
                    self.clear_fields()
                    self.nameSearch.clear()
                    self.bDayBox.clear()
                    self.updateCompleters()

                    self.parent.currentMember = None

        else:
            
            self.parent.set_stat_message(Util.noActiveMember, c='red')
            
            if self.bDayBox.count() > 1 and self.bDayBox.currentIndex() == 1:

                self.bDayBox.showPopup()

    def Button_addUpdButClick(self):

        # Clear the message window
        self.parent.set_stat_message()

        # Proceed if the fields are valid
        if self.areMemberFieldsValid():

            member_attributes = {
                'FirstName': self.MFNameEdit.text().strip(),
                'LastName': self.MLNameEdit.text().strip(),
                'Phone': self.PhoneEdit.text().strip(),
                'Email': self.EmailEdit.text().strip(),
                'StudentID': self.MNumEdit.text().strip(),
                'Birthday': self.BirthdayEdit.date_db(),
                'MembStat': self.statusBox.currentText(),
                'StudStat': self.studStatBox.currentText(),
                'Street': self.streetEdit.text().strip(),
                'City': self.cityEdit.text().strip(),
                'State': self.stateBox.currentText(),
                'Zip': self.zipEdit.text().strip(),
                'EmName': self.emNameEdit .text().strip(),
                'EmRel': self.emRelaltEdit.text().strip(),
                'EmPhoneH': self.emHPhoneEdit.text().strip(),
                'EmPhoneW': self.emWPhoneEdit.text().strip(),
                'EmPhoneC': self.emCPhoneEdit.text().strip(),

                # Room mate name and phone
                'RoommateName': self.rommateEdit.text().strip(),
                'RoommatePhone': self.rommatePhoneEdit.text().strip(),

                # Insurance fields
                'InsurName': self.insEdit.text().strip(),
                'InsurPol': self.insPolEdit.text().strip(),
                'InsurGrp': self.insGrpEdit.text().strip(),

                # Medical Condition
                'Med': self.medEdit.document().toPlainText().strip(),
                'Note': self.noteEdit.document().toPlainText().strip(),
                'LastUpdated': Util.convert_date('Qt2DB', QtCore.QDate.currentDate())}

            # Certifications
            for cert in Util.certifications:
                member_attributes[cert + 'Cert'] = self.__dict__[cert + 'CertCkbx'].isChecked()
                if member_attributes[cert + 'Cert']:
                    member_attributes[cert + 'CertDate'] = self.__dict__[cert + 'DateEdit'].date_db()
                else:
                    member_attributes[cert + 'CertDate'] = ''
                member_attributes[cert + 'CertVouch'] = self.__dict__[cert + 'Vouched'].text().strip()

            if self.FormsCkbx.isChecked():
                member_attributes['FormsDate'] = self.FormsDateEdit.date_db()
            else:
                member_attributes['FormsDate'] = ''

            if self.campLinkCkbx.isChecked():
                member_attributes['CampusLinkDate'] = self.campLinkDateEdit.date_db()
            else:
                member_attributes['CampusLinkDate'] = ''

            return self.addUpdMember(member_attributes)

        else:

            self.parent.set_stat_message('Red fields are required and/or have invalid values!!!', c='red')
            return False
    
    def Button_showMembs(self):

        # Clear the message window
        self.parent.set_stat_message()

        model = QtSql.QSqlTableModel(self)
        model.setTable('Member')
        model.select()

        self.viewMembers = QtGui.QTableView(None)
        self.viewMembers.setWindowTitle('Member List')
        self.viewMembers.setWindowIcon(self.parent.icon)
        self.viewMembers.resize(600, 500)
        self.viewMembers.setModel(model)
        self.viewMembers.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.viewMembers.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.viewMembers.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.viewMembers.clicked.connect(self.getMIDMemberTable)
        self.viewMembers.resizeColumnsToContents()
        self.viewMembers.show()

    def Button_showMembHist(self):
        
        # Clear the message window
        self.parent.set_stat_message()

        if self.parent.currentMember:

            cmd = ('SELECT (M2.LastName||' '||M2.FirstName), G.Name, strftime("%m/%d/%Y, %H:%M", AT.CheckOutDateTime), '
                   'strftime("%m/%d/%Y", AT.DueDate), strftime("%m/%d/%Y, %H:%M", AT.CheckInDateTime) '
                   'FROM ArchiveTrans AT, Member M1, Member M2, Gear G '
                   'WHERE AT.MID_OUT={MID} AND AT.MID_OUT=M1.ID AND AT.GID=G.ID AND AT.MID_IN=M2.ID '
                   'ORDER BY AT.CheckInDateTime ASC').format(MID=self.parent.currentMember.ID)

            query = self.db.execQuery(cmd, 'TabMemberMan.py -> showMembHist')

            model = QtSql.QSqlQueryModel()
            model.setQuery(query)
            model.setHeaderData(0, QtCore.Qt.Horizontal, 'Return Name')
            model.setHeaderData(1, QtCore.Qt.Horizontal, 'Gear Name')
            model.setHeaderData(2, QtCore.Qt.Horizontal, 'Checkout Date/Time')
            model.setHeaderData(3, QtCore.Qt.Horizontal, 'DueDate')
            model.setHeaderData(4, QtCore.Qt.Horizontal, 'Checkin Date/Time')

            self.viewGearHist = QtGui.QTableView()
            self.viewGearHist.setWindowTitle('Gear Transaction History')
            self.viewGearHist.setWindowIcon(self.parent.icon)
            self.viewGearHist.resize(600, 500)
            self.viewGearHist.setModel(model)
            self.viewGearHist.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
            self.viewGearHist.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
            self.viewGearHist.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
            self.viewGearHist.clicked.connect(self.getGIDMembHistTable)
            self.viewGearHist.resizeColumnsToContents()
            self.viewGearHist.show()

        else:
            
            self.parent.set_stat_message(Util.noActiveMember, c='red')

            if self.bDayBox.count() > 1 and self.bDayBox.currentIndex() == 1:

                self.bDayBox.showPopup()
