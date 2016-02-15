from __future__ import division
from PySide import QtGui, QtCore, QtSql
import barcode
import Util
import math
import os

# Conversions
kg2lb = 2.20462
kg2oz = 35.274
kg2g = 1000


class TabGearMan(QtGui.QTabWidget):
    def __init__(self, parent=None):
        super(TabGearMan, self).__init__(parent)

        # Reference stuff
        self.parent = parent
        self.db = parent.db

        # KeyPressEater fields commands/attributes
        # keyPressEater = KeyPressEater(self)
        # self.installEventFilter(keyPressEater)
        self.scannerIsTyping = False
        self.keyStrokeList = ''

        # No focus on the tab itself
        self.setFocusPolicy(QtCore.Qt.NoFocus)

        self.viewGear = QtGui.QTableView()
        self.view_gear_hist = QtGui.QTableView()

        # Search box
        gNameIDLab, self.gNameIDSearch, gDissAmbLab, self.gDissAmbSearch = Util.make_line_edit_combobox(
            self, 'Gear Name/ID', 'Search for gear by name or ID to view/update', 'Gear ID/Name')
        self.gDissAmbSearch.setEditable(False)
        self.gDissAmbSearch.setInsertPolicy(QtGui.QComboBox.InsertAlphabetically)

        # Name and ID fields
        GNameLab, self.GNameEdit = Util.make_line_edit(self, 'Gear Name', 'Gear Name')
        GIDLab, self.GIDEdit = Util.make_line_edit(self, 'Gear ID', 'GearID')

        # Quantity field
        QuantLab = QtGui.QLabel('Quantity')
        self.QuantSpin = QtGui.QSpinBox()
        self.QuantSpin.setValue(0)
        # self.QuantSpin.setMaximum(99)

        # Combine GearID and Quantity into one field
        IDQuantField = QtGui.QHBoxLayout()
        IDQuantField.setSpacing(Util.layoutGridSpacing)
        IDQuantField.setStretch(0, 1)
        IDQuantField.addWidget(self.GIDEdit)
        IDQuantField.addWidget(QuantLab)
        IDQuantField.addWidget(self.QuantSpin)

        cat_lab = QtGui.QLabel('Category')
        self.catBox = QtGui.QComboBox()
        self.catBox.insertItems(0, self.db.gear_category.getList())

        # Add/Update button
        self.updtBut = QtGui.QPushButton()

        # Add/Update radio buttons
        self.radioAdd = QtGui.QRadioButton("Add")
        self.radioUpd = QtGui.QRadioButton("Update")

        hbox = QtGui.QHBoxLayout()
        hbox.setSpacing(Util.layoutGridSpacing)
        hbox.addWidget(self.radioAdd)
        hbox.addWidget(self.radioUpd)
        addUpdLay = QtGui.QGroupBox()
        addUpdLay.setTitle('Add or Update current item')
        addUpdLay.setLayout(hbox)

        hbox = QtGui.QGridLayout()
        hbox.setSpacing(Util.layoutGridSpacing)
        hbox.setColumnStretch(0, 0)     ; hbox.setColumnStretch(1, 1)             ; hbox.setColumnStretch(2, 0)      ; hbox.setColumnStretch(3, 1)
        hbox.addWidget(gNameIDLab, 0, 0); hbox.addWidget(self.gNameIDSearch, 0, 1); hbox.addWidget(gDissAmbLab, 0, 2); hbox.addWidget(self.gDissAmbSearch, 0, 3)
        search_lay = QtGui.QGroupBox()
        search_lay.setTitle('Chose to Add or Update the current item')
        search_lay.setLayout(hbox)

        # Display who has me field
        self.whoNameEdit = Util.make_line_edit_display_only()
        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(self.whoNameEdit)
        who_box_lay = QtGui.QGroupBox()
        who_box_lay.setTitle('Currently checked out to')
        who_box_lay.setLayout(hbox)

        # Gear info fields
        purch_date_lab = QtGui.QLabel('Purchased')
        self.PurchDateEdit = QtGui.QDateEdit()

        price_lab, self.PriceEdit = Util.make_line_edit(self, 'Price', '$$$')

        self.ExpDateCkbx = QtGui.QCheckBox('Expires')
        self.ExpDateCkbx.toggled.connect(self.ExpDateTogg)
        self.ExpDateEdit = QtGui.QDateEdit()
        self.ExpDateEdit.setDisabled(True)

        # Weight
        self.units = ['g', 'kg', 'lb', 'oz', 'lb, oz']
        weight_lab, self.WeightEdit = Util.make_line_edit(self, 'Weight')
        self.unitBox = QtGui.QComboBox()
        self.unitBox.insertItems(0, self.units)

        weight_unit = QtGui.QHBoxLayout()
        weight_unit.setSpacing(Util.layoutGridSpacing)
        weight_unit.addWidget(self.WeightEdit)
        weight_unit.addWidget(self.unitBox)

        manufac_lab, self.ManufacEdit = Util.make_line_edit(self, 'Manufacturer', 'Manufacturer')

        # Required certifications box
        req_cert_lay = QtGui.QGridLayout()
        req_cert_lay.setSpacing(Util.layoutGridSpacing)
        req_cert_lay.setColumnStretch(99, 1)
        req_cert_lay.setRowStretch(0, 0)
        for cert in Util.certifications:
            self.__dict__[cert + 'CertCkbx'] = Util.certification_layout(self, cert, checkbox_only=True)
            req_cert_lay.addWidget(self.__dict__[cert + 'CertCkbx'], 0, Util.certifications.index(cert))
        req_cert_lay.expandingDirections()

        # Put the search box in a group box
        reqCertBox = QtGui.QGroupBox()
        reqCertBox.setTitle('Required Certifications')
        reqCertBox.setLayout(req_cert_lay)

        # Care/maintenance box
        maintenance_label = QtGui.QLabel('Care/Maintenance')
        maintenance_label.setAlignment(QtCore.Qt.AlignTop)
        self.MaintenanceEdit = QtGui.QPlainTextEdit()

        note_label = QtGui.QLabel('Notes')
        note_label.setAlignment(QtCore.Qt.AlignTop)
        self.NoteEdit = QtGui.QPlainTextEdit()

        self.checkoutable = QtGui.QCheckBox("UnRentable")
        self.checkoutable_lineedit = QtGui.QLineEdit(self)
        self.checkoutable_lineedit.setDisabled(True)
        self.checkoutable_lineedit.setPlaceholderText('Why is this item unrentable???')

        remove_button = QtGui.QPushButton("Delete")
        remove_button.clicked.connect(self.button_delete_gear)
        # s = remove_button.sizeHint()
        # print s
        # s.setHeight(s.height()*3)
        # print s
        # remove_button.setIconSize( s )
        # print remove_button.iconSize()
        print_barcode = QtGui.QPushButton("Print Barcode")

        # Make the table view
        view_gear_button = QtGui.QPushButton("Show Gear\nInventory")

        # Show the transaction history for this item
        viewGearHistBut = QtGui.QPushButton("Show Gear\nTransaction History")

        # Generate and populate the table
        dispEd = QtGui.QGridLayout()
        dispEd.setSpacing(Util.layoutGridSpacing)
        dispEd.setColumnStretch(0, 0); dispEd.setColumnStretch(1, 1); dispEd.setColumnStretch(2, 0); dispEd.setColumnStretch(3, 0)
        dispEd.setRowStretch(6, 1)

        dispEd.addWidget(GNameLab         , 0, 0); dispEd.addWidget(self.GNameEdit      , 0, 1)      ; dispEd.addWidget(GIDLab     , 0, 2); dispEd.addLayout(IDQuantField    , 0, 3)
        dispEd.addWidget(purch_date_lab   , 1, 0); dispEd.addWidget(self.PurchDateEdit  , 1, 1)      ; dispEd.addWidget(price_lab  , 1, 2); dispEd.addWidget(self.PriceEdit  , 1, 3)
        dispEd.addWidget(self.ExpDateCkbx , 2, 0); dispEd.addWidget(self.ExpDateEdit    , 2, 1)      ; dispEd.addWidget(weight_lab , 2, 2); dispEd.addLayout(weight_unit     , 2, 3)
        dispEd.addWidget(self.checkoutable, 3, 0); dispEd.addWidget(self.checkoutable_lineedit, 3, 1); dispEd.addWidget(manufac_lab, 3, 2); dispEd.addWidget(self.ManufacEdit, 3, 3)
        pass                                     ; dispEd.addWidget(reqCertBox          , 4, 1)      ; dispEd.addWidget(cat_lab    , 4, 2); dispEd.addWidget(self.catBox     , 4, 3)
        dispEd.addWidget(maintenance_label, 5, 0); dispEd.addWidget(self.MaintenanceEdit, 5, 1, 8, 1); dispEd.addWidget(note_label , 5, 2); dispEd.addWidget(self.NoteEdit, 5, 3, 8, 1)
        dispEd.addWidget(self.updtBut    ,  8, 0)
        dispEd.addWidget(remove_button   ,  9, 0)
        dispEd.addWidget(print_barcode   , 10, 0)
        dispEd.addWidget(view_gear_button, 11, 0)
        dispEd.addWidget(viewGearHistBut , 12, 0)

        hbox = QtGui.QHBoxLayout()
        hbox.setSpacing(Util.layoutGridSpacing)
        hbox.addLayout(dispEd)
        display_box_layout = QtGui.QGroupBox()
        display_box_layout.setTitle('Gear Information')
        display_box_layout.setLayout(hbox)

        grid = QtGui.QGridLayout()
        grid.setSpacing(Util.layoutGridSpacing)
        pass                           ; dispEd.setColumnStretch(0, 0); dispEd.setColumnStretch(1, 1); dispEd.setColumnStretch(2, 0); dispEd.setColumnStretch(3, 1)
        grid.addWidget(addUpdLay, 0, 0); grid.addWidget(search_lay, 0, 1)
        grid.addWidget(who_box_lay, 1, 0, 1, 2)
        grid.addWidget(display_box_layout, 2, 0, 1, 2)

        self.setLayout(grid)

        # Generate the completers
        self.set_completers()

        # # # # # # # # # #
        # Connect objects #
        # # # # # # # # # #

        self.gNameIDSearch.textChanged.connect(self.fillGear)
        self.gDissAmbSearch.activated.connect(self.fillGear)
        self.gDissAmbSearch.currentIndexChanged.connect(self.updCurrentGearComboBox)

        self.updtBut.clicked.connect(self.button_save_gear)

        self.radioAdd.clicked.connect(self.button_radio_add_clicked)
        self.radioUpd.clicked.connect(self.button_radio_update_clicked)
        self.radioAdd.click()

        # Weight/units
        self.WeightEdit.textChanged.connect(self.set_weight_edited)
        self.unitBox.currentIndexChanged.connect(self.set_weight)
        self.unitBox.currentIndexChanged.connect(self.set_weight_edited)
        self.unitBox.setCurrentIndex(1)

        self.checkoutable.stateChanged.connect(self.setUnrentableStat)

        # Buttons
        print_barcode.clicked.connect(self.button_print_barcode)
        view_gear_button.clicked.connect(self.button_show_gear_table)
        viewGearHistBut.clicked.connect(self.button_show_gear_history_table)

    def set_scanner_field(self, gear_id):

        self.gNameIDSearch.setText(gear_id)

    def ExpDateTogg(self):
        if self.ExpDateCkbx.isChecked():
            self.ExpDateEdit.setEnabled(True)
        else:
            self.ExpDateEdit.setDisabled(True)

    def setUnrentableStat(self):
        if self.checkoutable.isChecked():
            self.checkoutable_lineedit.setEnabled(True)
        else:
            self.checkoutable_lineedit.clear()
            self.checkoutable_lineedit.setDisabled(True)

    def gearFieldsAreValid(self):

        error = False

        if not self.GNameEdit.text():
            self.GNameEdit.setColors(bg='red')
            error = True

        if not self.GIDEdit.text() or self.GIDEdit.text().count('*') > 1:
            self.GIDEdit.setColors(bg='red')
            error = True

        if not self.PriceEdit.text():
            self.PriceEdit.setColors(bg='red')
            error = True
        else:
            price = self.PriceEdit.text().strip()
            if '$' == price[0]:
                price = price.lstrip('$')
            if Util.is_number(price) and float(price) >= 0 and len(price.split('.')[-1]) <= 2:
                # Format the price to have 2 decimals
                self.PriceEdit.setText("%0.2f" % float(price))
            else:
                self.PriceEdit.setColors(bg='red')
                error = True

        if not self.catBox.currentText():
            self.catBox.setColors(bg='red')
            error = True

        if not self.WeightEdit.text():
            self.WeightEdit.setText('0')
        else:
            weight = self.WeightEdit.text()
            unit = self.unitBox.currentText()

            if unit == 'lb, oz':
                lb, oz = weight.replace(' ', '').split(',')
                lb = float(lb)
                oz = float(oz)
                if not Util.is_number(lb) and not Util.is_number(oz):
                    self.WeightEdit.setColors(bg='red')
                    error = True

            elif not Util.is_number(weight) or float(weight) < 0:
                self.WeightEdit.setColors(bg='red')
                error = True

        if self.PurchDateEdit.date() > QtCore.QDate.currentDate():
            self.PurchDateEdit.setColors(bg='red')
            error = True

        if not self.ManufacEdit.text():
            self.ManufacEdit.setColors(bg='red')
            error = True

        if self.ExpDateCkbx.isChecked():
            if self.ExpDateEdit.date() <= QtCore.QDate.currentDate().addDays(-30):
                self.ExpDateEdit.setColors(bg='yellow')
            if self.ExpDateEdit.date() <= QtCore.QDate.currentDate():
                self.ExpDateEdit.setColors(bg='red')
                error = True

        if self.checkoutable.isChecked() and not self.checkoutable_lineedit.text():
            self.checkoutable_lineedit.setColors(bg='red')
            error = True

        # Valid fields = not error
        return not error

    def fillGear(self):

        self.db.fill_gear(self.gNameIDSearch, self.gDissAmbSearch)

        self.setAddUpdt()

    def updCurrentGearComboBox(self):

        self.parent.currentGear = self.db.getGear(self.gNameIDSearch, self.gDissAmbSearch)

        self.parent.currentGearComboBox = self.gDissAmbSearch.currentText()

        self.fillGearFields()

        self.setAddUpdt()

    def setAddUpdt(self):

        if self.parent.currentGear:
            self.radioUpd.setEnabled(True)
        else:
            self.radioUpd.setDisabled(True)

    def fillGearFields(self):

        # If the gear is found, fill out the gear information
        if self.parent.currentGear:

            self.GNameEdit    .setText(self.parent.currentGear.Name)
            self.GIDEdit      .setText(self.parent.currentGear.ID)
            self.QuantSpin    .setValue(self.parent.currentGear.Quantity)
            self.PurchDateEdit.setDate(self.parent.currentGear.PurchaseDate)
            self.PriceEdit.setText('%.2f' % self.parent.currentGear.Price)
            if self.parent.currentGear.ExpirationDate:
                self.ExpDateCkbx.setChecked(True)
                self.ExpDateEdit.setDate(self.parent.currentGear.ExpirationDate)
            else:
                self.ExpDateCkbx.setChecked(False)
                self.ExpDateEdit.setDate(QtCore.QDate.currentDate())
            self.ManufacEdit    .setText(self.parent.currentGear.Manufacturer)
            self.catBox         .setCurrentIndex(self.parent.currentGear.Category)
            self.checkoutable     .setChecked(bool(self.parent.currentGear.Unrentable))
            self.checkoutable_lineedit .setText(self.parent.currentGear.UnrentableReason)
            for cert in Util.certifications:
                self.__dict__[cert + 'CertCkbx'].setChecked(self.parent.currentGear.__dict__[cert + 'Cert'])
            self.MaintenanceEdit.setPlainText(self.parent.currentGear.CareMaintenance)
            self.NoteEdit       .setPlainText(self.parent.currentGear.Misc)
            self.set_weight()

            clear_who_name_edit = False

            if self.parent.currentGear.numCheckedOut() > 0:

                transaction_list = self.db.getTrans(gear=self.parent.currentGear)

                # If transactions exist
                if transaction_list:

                    # Generate a list of members who have this item
                    name_list_count = {}
                    for trans in transaction_list:
                        member = self.db.getMember(trans.MID)

                        if member.full_name() not in name_list_count.keys():
                            name_list_count[member.full_name()] = 1
                        elif member.full_name() in name_list_count.keys():
                            name_list_count[member.full_name()] += 1

                    # Sort the list
                    name_list = name_list_count.keys()
                    name_list.sort()

                    # Create the list of names and number of items each person has
                    people_count = ''
                    for name in name_list:
                        if people_count:
                            people_count += ', '
                        people_count += '{0} x{1}'.format(name, name_list_count[name])

                    self.whoNameEdit.setText(people_count)

                else:
                    clear_who_name_edit = True
            else:
                clear_who_name_edit = True

            if clear_who_name_edit:
                self.whoNameEdit.clear()

        # If the gear is not found, clear the gear information
        else:

            self.clear_fields()

    def clear_fields(self):

        self.parent.currentGear = None

        self.GNameEdit.clear()
        self.GIDEdit.clear()
        self.QuantSpin.setValue(1)
        self.PurchDateEdit.setDate(QtCore.QDate.currentDate())
        self.PriceEdit.clear()
        self.ExpDateCkbx.setChecked(False)
        self.ExpDateEdit.setDate(QtCore.QDate.currentDate())
        self.ManufacEdit.clear()
        self.catBox.setCurrentIndex(0)
        self.checkoutable.setChecked(False)
        self.checkoutable_lineedit.clear()
        for cert in Util.certifications:
            self.__dict__[cert + 'CertCkbx'].setChecked(False)
        self.MaintenanceEdit.clear()
        self.NoteEdit.clear()
        self.WeightEdit.clear()

    def setCurrentMemberGear(self):

        current_gear_line_edit = self.parent.currentGearLineEdit
        current_gear_combo_box = self.parent.currentGearComboBox
        self.gNameIDSearch.clear()
        self.gNameIDSearch.setText(current_gear_line_edit)
        if current_gear_combo_box:
            self.gDissAmbSearch.setCurrentIndex(self.gDissAmbSearch.findText(current_gear_combo_box))

    def set_completers(self):

        # Set the already existing completers
        self.gNameIDSearch.setCompleter2(self.parent.gearNameIDComp)
        self.ManufacEdit.setCompleter2(self.parent.manufacturer_completer)

    def update_completers(self):

        # Generate the completers
        self.parent.gearNameIDComp = self.parent.get_gear_name_id_comp()
        self.parent.manufacturer_completer = self.parent.get_manufacturer_comp()

        # Set the completers
        self.set_completers()

    def update_tab(self):

        self.radioAdd.click()
        self.keyStrokeList = ''
        self.setCurrentMemberGear()
        self.fillGearFields()
        self.set_completers()
        self.setAddUpdt()

    def get_gear_id_from_gear_inventory_table(self):

        # Clear the message window
        self.parent.set_stat_message()

        row = self.viewGear.currentIndex().row()
        gid = self.db.getAttrFromTable('Gear', 'ID', row)
        self.parent.currentGear = self.db.getGear(gid)

        self.gNameIDSearch.setText(self.parent.currentGear.ID)

    def get_gear_id_from_gear_history_table(self):

        # Clear the message window
        self.parent.set_stat_message()

        row = self.view_gear_hist.currentIndex().row()
        mid_out = self.db.getAttrFromTable('ArchiveTrans', 'MID_OUT', row, 'ORDER BY CheckInDateTime DESC')
        gid = self.db.getAttrFromTable('ArchiveTrans', 'GID', row, 'ORDER BY CheckInDateTime DESC')

        member = self.db.getMember(mid_out)
        self.parent.currentGear = self.db.getGear(gid)

        self.parent.currentMemberNameID = member.full_name()
        self.parent.currentBDayBox = Util.convert_date('Qt2Disp', member.Birthday)

        self.gNameIDSearch.setText(self.parent.currentGear.ID)

    def get_weight(self):

        weight = self.WeightEdit.text()
        current_unit = self.unitBox.currentText()

        if weight != '' and (Util.is_number(weight) or ',' in weight):

            if Util.is_number(weight):

                # Convert from string to float
                weight = float(weight)

                # Convert current weight to kg
                if current_unit == 'g':
                    weight /= kg2g
                elif current_unit == 'lb':
                    weight /= kg2lb
                elif current_unit == 'oz':
                    weight /= kg2oz

            elif ',' in weight:

                # Convert current weight to kg
                if current_unit == 'lb, oz':
                    lb, oz = weight.replace(' ', '').split(',')
                    lb = float(lb)
                    oz = float(oz)
                    weight = lb / kg2lb + oz / kg2oz

            return weight  # In kg

    def set_weight(self):

        if self.parent.currentGear:

            weight = self.parent.currentGear.Weight
            new_unit = self.unitBox.currentText()

            # if weight != '' and (Util.isNumber(weight) or ',' in weight):

            # Convert to the new unit
            if new_unit == 'g':
                weight = '{:0.0f}'.format(weight * kg2g)
            elif new_unit == 'kg':
                weight = '{:0.1f}'.format(weight)  # Weight already in kg
            elif new_unit == 'lb':
                weight = '{:0.1f}'.format(weight * kg2lb)
            elif new_unit == 'oz':
                weight = '{:0.1f}'.format(weight * kg2oz)
            elif new_unit == 'lb, oz':
                lb = int('{:0.0f}'.format(math.floor(weight * kg2lb)))
                oz = float('{:0.1f}'.format(weight * kg2lb % 1 * 16))
                if oz >= 16.0:
                    lb += 1
                    oz -= 16
                weight = '{}, {}'.format(lb, oz)

            self.WeightEdit.setText(weight)

    def set_weight_edited(self):

        new_unit = self.unitBox.currentText()
        text = 'Enter weight in '
        if new_unit == 'g':
            self.WeightEdit.setPlaceholderText(text + 'grams')
        elif new_unit == 'kg':
            self.WeightEdit.setPlaceholderText(text + 'kilograms')
        elif new_unit == 'lb':
            self.WeightEdit.setPlaceholderText(text + 'pounds')
        elif new_unit == 'oz':
            self.WeightEdit.setPlaceholderText(text + 'ounces')
        elif new_unit == 'lb, oz':
            self.WeightEdit.setPlaceholderText(text + 'pounds, ounces')

    def button_save_gear(self):

        # Clear the message window
        self.parent.set_stat_message()

        if self.gearFieldsAreValid():

            gear_attributes = {
                'Name': self.GNameEdit.text().strip(),
                'ID': self.GIDEdit.text().strip(),
                'Quantity':  self.QuantSpin.value(),
                'Price': "%0.2f" % float(self.PriceEdit.text()),
                'PurchaseDate': self.PurchDateEdit.date_db(),
                'Weight': self.get_weight(),
                'Category': self.catBox.currentText(),
                'Manufacturer': self.ManufacEdit.text().strip(),
                'Unrentable': self.checkoutable.isChecked(),
                'CareMaintenance': self.MaintenanceEdit.document().toPlainText().strip(),
                'Misc': self.NoteEdit.document().toPlainText().strip()}

            if self.ExpDateCkbx.isChecked():
                gear_attributes['ExpirationDate'] = self.ExpDateEdit.date_db()
            else:
                gear_attributes['ExpirationDate'] = ''

            if gear_attributes['Unrentable']:
                gear_attributes['UnrentableReason'] = self.checkoutable_lineedit.text().strip()
            else:
                gear_attributes['UnrentableReason'] = ''
            for cert in Util.certifications:
                gear_attributes[cert + 'Cert'] = self.__dict__[cert + 'CertCkbx'].isChecked()

            if self.addGear:

                # If there are * characters in the gearID, generate a new id
                if '*' in gear_attributes['ID']:
                    gear_attributes['ID'] = self.db.getUniqueID('Gear', gear_attributes['ID'])

                    # Place the new ID in the gearID window
                    self.GIDEdit.setText(gear_attributes['ID'])

                self.parent.currentGear = self.db.getGear(gear_attributes['ID'])

                if not self.parent.currentGear:
                    self.db.addItem('Gear', gear_attributes)
                    self.parent.set_stat_message('{0}, {1} was added'.format(gear_attributes['Name'], gear_attributes['ID']))
                    self.update_completers()

                    self.gNameIDSearch.clear()
                    self.gNameIDSearch.setText(gear_attributes['Name'])
                    this_bday_index = self.gDissAmbSearch.findText(gear_attributes['ID'])
                    self.gDissAmbSearch.setCurrentIndex(this_bday_index)

                    return True
                else:
                    self.GIDEdit.setColors(bg='red')
                    self.parent.set_stat_message('Gear already exists and cannot be added', c='red')
                    return False
            else:

                self.parent.currentGear = self.db.getGear(self.gNameIDSearch, self.gDissAmbSearch)

                # Check to make sure that the new gearID is either the same as the old one or unique
                if self.parent.currentGear:

                    if not (self.parent.currentGear.ID == gear_attributes['ID'] or self.db.isGearIDUnique(gear_attributes['ID'])):
                        self.parent.set_stat_message('Gear ID is not unique!', c='red')
                        self.GIDEdit.setColors(bg='red')
                        return False
                    else:

                        self.db.updateItem('Gear', gear_attributes, self.parent.currentGear)
                        self.parent.set_stat_message('Gear was updated')

                        self.update_completers()

                        self.gNameIDSearch.clear()
                        self.gNameIDSearch.setText(gear_attributes['Name'])
                        this_bday_index = self.gDissAmbSearch.findText(gear_attributes['ID'])
                        self.gDissAmbSearch.setCurrentIndex(this_bday_index)
                        return True
                else:
                    if self.gDissAmbSearch.count() >= 2 and self.gDissAmbSearch.currentIndex() == 0:
                        self.gDissAmbSearch.showPopup()
                    else:
                        self.parent.set_stat_message('Gear does not exists and cannot be updated', c='red')
                    return False

        else:
            self.parent.set_stat_message('Red fields are required and/or have invalid values!!!', c='red')

    def button_radio_add_clicked(self):

        # Clear the message window
        self.parent.set_stat_message()

        self.gNameIDSearch .setEnabled(True)
        self.gDissAmbSearch.setEnabled(True)
        self.addGear = True
        self.updtBut.setText('Add\nGear')

    def button_radio_update_clicked(self):

        # Clear the message window
        self.parent.set_stat_message()

        if self.parent.currentGear:

            self.gNameIDSearch .setDisabled(True)
            self.gDissAmbSearch.setDisabled(True)

            self.addGear = False
            self.updtBut.setText('Update\nGear')

        else:

            self.radioAdd.click()
            self.parent.set_stat_message('Select an item to update.', c='red')

    def button_delete_gear(self):

        # Clear the message window
        self.parent.set_stat_message()

        if self.parent.currentGear:
            if self.parent.currentGear.numCheckedOut() > 0:
                self.parent.set_stat_message('Cannot delete gear because it is currently checked out!!!', c='red')
            else:
                reply = QtGui.QMessageBox.question(self, 'Confirm Delete',
                        'Are you sure you want to remove:\n\n{}, {}'.format(self.parent.currentGear.Name, self.parent.currentGear.ID),
                        QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)

                if reply == QtGui.QMessageBox.Yes:
                    self.db.delItem('Gear', self.parent.currentGear)
                    self.parent.set_stat_message('Gear: {}, ID: {} deleted'.format(self.parent.currentGear.Name, self.parent.currentGear.ID))
                    self.parent.currentGear = None

                    # Clear/reset all the fields
                    self.clear_fields()
                    self.update_completers()

        else:
            self.parent.set_stat_message(Util.noActiveGear, c='red')
            if self.gDissAmbSearch.count() > 1 and self.gDissAmbSearch.currentIndex() == 1:
                self.gDissAmbSearch.showPopup()
                
    def button_show_gear_table(self):

        # Clear the message window
        self.parent.set_stat_message()

        model = QtSql.QSqlTableModel(self)
        model.setTable('Gear')
        model.select()

        self.viewGear.setWindowTitle('Gear Inventory')
        self.viewGear.setWindowIcon(self.parent.icon)
        self.viewGear.resize(600, 500)
        self.viewGear.setModel(model)
        self.viewGear.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.viewGear.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.viewGear.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.viewGear.clicked.connect(self.get_gear_id_from_gear_inventory_table)
        self.viewGear.resizeColumnsToContents()
        self.viewGear.show()
        
    def button_show_gear_history_table(self):

        # Clear the message window
        self.parent.set_stat_message()

        if self.parent.currentGear:

            cmd = ('SELECT (M1.FirstName||' '||M1.LastName), (M2.FirstName||' '||M2.LastName), G.Name, '
                   'strftime("%m/%d/%Y %H:%M:%S", AT.CheckOutDateTime), strftime("%m/%d/%Y", AT.DueDate), '
                   'strftime("%m/%d/%Y %H:%M:%S", AT.CheckInDateTime) '
                   'FROM ArchiveTrans AT, Member M1, Member M2, Gear G WHERE AT.GID="{GID}" '
                   'AND AT.MID_OUT=M1.ID AND AT.GID=G.ID AND AT.MID_IN=M2.ID '
                   'ORDER BY AT.CheckInDateTime ASC').format(GID=self.parent.currentGear.ID)

            query = self.db.execQuery(cmd, 'TabGearMan.py -> showGearHist')

            model = QtSql.QSqlQueryModel()
            model.setQuery(query)
            model.setHeaderData(0, QtCore.Qt.Horizontal, 'Rented By')
            model.setHeaderData(1, QtCore.Qt.Horizontal, 'Returned By')
            model.setHeaderData(2, QtCore.Qt.Horizontal, 'Gear Name')
            model.setHeaderData(3, QtCore.Qt.Horizontal, 'Checkout Date/Time')
            model.setHeaderData(4, QtCore.Qt.Horizontal, 'DueDate')
            model.setHeaderData(5, QtCore.Qt.Horizontal, 'Checkin Date/Time')

            self.view_gear_hist.setWindowTitle('Gear Transaction History')
            self.view_gear_hist.setWindowIcon(self.parent.icon)
            self.view_gear_hist.resize(600, 500)
            self.view_gear_hist.setModel(model)
            self.view_gear_hist.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
            self.view_gear_hist.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
            self.view_gear_hist.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
            self.view_gear_hist.clicked.connect(self.get_gear_id_from_gear_history_table)
            self.view_gear_hist.resizeColumnsToContents()
            self.view_gear_hist.show()

        else:
            self.parent.set_stat_message(Util.noActiveGear, c='red')
            if self.gDissAmbSearch.count() > 1 and self.gDissAmbSearch.currentIndex() == 1:

                self.gDissAmbSearch.showPopup()

    def button_print_barcode(self):

        # Clear the message window
        self.parent.set_stat_message()

        if self.parent.currentGear:
            self.parent.set_stat_message('Writing barcode: {}, {} to directory: {}'.format(self.parent.currentGear.Name,
                                                                                           self.parent.currentGear.ID,
                                                                                           self.parent.barCodeDir))

            # # TODO: Figure out how many characters/line that can be written on under the bar code, then split the gear
            # # name over however many lines are needed to write the whole name
            #
            # # Generate the gear_name string
            # maxCharPerLine = 21
            # gearNameSplit = self.parent.currentGear.Name.split()
            # gear_name = ''
            # row = ''
            # for word in gearNameSplit:
            #     if len(row + ' ' + word) > maxCharPerLine:
            #         gear_name += '\n'
            #         row = ''
            #     else:
            #         if gear_name:
            #             gear_name += ' '
            #         row += ' ' + word
            #     gear_name += word
            #
            # # FIXME: Get the old PIL, pillow libraries
            # # Save the image of the barcode
            # # ean = barcode.get('Code39', [self.parent.currentGear.ID, gear_name], writer=barcode.writer.ImageWriter())
            # ean = barcode.get('Code39', self.parent.currentGear.ID, writer=barcode.writer.ImageWriter())
            #
            # # Replace characters that will make a nasty file name
            # file_name = gear_name.replace('\n', '_').replace('/', '_').replace(' ', '_').replace('"', '').replace("'", '')
            #
            # file_name = '{}_{}'.format(file_name, self.parent.currentGear.ID)
            #
            # # Save the barcode
            # ean.save(os.path.join(self.parent.barCodeDir, file_name))
            # # ean.save('{1}.png'.format(self.parent.pathDesktop, gear_name, self.parent.currentGear.ID))

            from reportlab.graphics.barcode import code39
            from reportlab.lib.pagesizes import letter
            from reportlab.lib.units import mm
            from reportlab.pdfgen import canvas

            barcode_value = self.parent.currentGear.ID
            barcode_name = self.parent.currentGear.Name

            file_name = os.path.join(self.parent.barCodeDir, '{}_{}.pdf'.format(barcode_value, barcode_name))

            c = canvas.Canvas(file_name, pagesize=letter)
            c.setFont('Helvetica-Bold', 6)

            barcode39 = code39.Extended39(barcode_value)

            x = 1 * mm
            y = 270 * mm

            barcode39.drawOn(c, x, y)
            w = barcode39.width / 2
            c.drawCentredString(x + w, y - 2 * mm, barcode_value)
            c.drawCentredString(x + w, y - 4 * mm, barcode_name[:20])

            c.save()

        else:
            self.parent.set_stat_message(Util.noActiveGear, c='red')
            self.gDissAmbSearch.showPopup()
            if self.gDissAmbSearch.count() > 1 and self.gDissAmbSearch.currentIndex() == 1:

                self.gDissAmbSearch.showPopup()
