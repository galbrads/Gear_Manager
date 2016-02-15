from PySide import QtGui, QtCore, QtSql

__updated__ = "2015-07-14 10:12:08"

# Display formats
dateDispFormat = 'M/d/yyyy'
disp_DateTime = 'M/d/yyyy h:map'
timeDispFormat = 'h:mmap'

# Internal formats
DB_Date = 'yyyy-MM-dd'
DB_Time = 'hh:mm:ss'
DB_DateTime = DB_Date + ' ' + DB_Time

# Scanner prefixes
scanPrefix = '%!#'
scanSuffix = scanPrefix[::-1]

# Message window text delay
messageDelay = 10000

# Standard messages
selectOne = '-- Select One --'
returnFor = 'OR return this gear for...'
noActiveMember = 'No member currently selected!!!'
noActiveGear = 'No gear currently selected!!!'

# Global widget grid spacing
layoutGridSpacing = 10

# Colors
color = {'white': QtCore.Qt.white,
         'red': QtGui.QColor(225, 60, 60),
         'yellow': QtCore.Qt.yellow,
         'green': QtGui.QColor(66, 225, 61),
         'gray': QtCore.Qt.gray,
         'black': QtCore.Qt.black}

# Certifications in database 
certifications = ['LeadSport', 'LeadTrad', 'LeadIce', 'KayakRoll']


class KeyPressEater(QtCore.QObject):

    def eventFilter(self, obj, event):

        if event.type() == QtCore.QEvent.KeyPress:

            if event.key() == 16777269:
                event.ignore()
                event = QtGui.QKeyEvent(QtCore.QEvent.KeyPress, QtCore.Qt.Key_Escape, QtCore.Qt.NoModifier)
                return QtCore.QObject.eventFilter(self, obj, event)

            if event.key() == QtCore.Qt.Key_Backspace or event.key() == QtCore.Qt.Key_Delete:
                self.parent().keyStrokeList = ''

            # If the KeyPress event was a character key on the key board
            elif event.text().strip():

                scanner_just_finished = False

                # Check to see if the prefix (or parts of it) are in text
                prefix_len = len(scanPrefix)
                for n in xrange(prefix_len):
                    if scanPrefix[:prefix_len - n] in self.parent().keyStrokeList + event.text():

                        self.parent().keyStrokeList += event.text().strip()

                        self.parent().scannerIsTyping = True

                        if scanSuffix in self.parent().keyStrokeList:
                            self.parent().scannerIsTyping = False
                            scanner_just_finished = True
                            gear_id = self.parent().keyStrokeList.strip(scanSuffix).strip()
                            self.parent().keyStrokeList = ''
                            self.parent().set_scanner_field(gear_id)
                        break

                if self.parent().scannerIsTyping or scanner_just_finished:
                    event.accept()
                    return True

        # standard event processing
        return QtCore.QObject.eventFilter(self, obj, event)

outDateCol = 3
dueDateCol = 4


class DateEditDelegate(QtGui.QStyledItemDelegate):

    def createEditor(self, parent, option, index):
        
        if index.column() == outDateCol or index.column() == dueDateCol:
            editor = QtGui.QDateEdit(parent)
            return editor
        else:
            return super(DateEditDelegate, self).createEditor(parent, option, index)

    def setEditorData(self, date_edit, index):

        if index.column() == outDateCol or index.column() == dueDateCol:
            d = index.model().data(index, QtCore.Qt.EditRole)
            date_edit.setCalendarPopup(True)
            date_edit.setDate(d)
        else:
            return super(DateEditDelegate, self).setEditorData(date_edit, index)

    def setModelData(self, date_edit, model, index):

        if index.column() == dueDateCol:
            d = convert_date('Qt2DB', date_edit.date())
            model.setData(index, d, QtCore.Qt.EditRole)
        else:
            return super(DateEditDelegate, self).setModelData(date_edit, model,  index)
        
    def updateEditorGeometry(self, editor, option, index):
        
        if index.column() == outDateCol or index.column() == dueDateCol:
            editor.setGeometry(option.rect)
        else:
            return super(DateEditDelegate, self).updateEditorGeometry(editor, option, index)

#     def displayText(self, value, locale):
#         
#         if locale.column() == outDateCol:
#             pass
#         else:
#             return super(DateEditDelegate, self).displayText(value, locale)


class TransactionSqlModel(QtSql.QSqlRelationalTableModel):

    def flags(self, index):
        
        flags = super(TransactionSqlModel, self).flags(index)

        if 0 <= index.column() < dueDateCol:
            
            if flags & QtCore.Qt.ItemIsEditable:
                flags ^= QtCore.Qt.ItemIsEditable
        
        return flags
        
    def data(self, index, role):

        due_date = super(TransactionSqlModel, self).data(self.index(index.row(), dueDateCol), QtCore.Qt.DisplayRole)
        due_date = QtCore.QDate.fromString(due_date, DB_Date)

        if role == QtCore.Qt.BackgroundRole:

            if QtCore.QDate.currentDate().daysTo(due_date) == 0:  # Gear is due today
                return QtGui.QBrush(QtGui.QColor(color['yellow']))
            elif QtCore.QDate.currentDate().daysTo(due_date) < 0:  # Gear is late
                return QtGui.QBrush(QtGui.QColor(color['red']))
            else:  # Gear is not due yet
                return QtGui.QBrush(QtGui.QColor(color['green']))

        if role == QtCore.Qt.DisplayRole:
            
            if index.column() == outDateCol:
                d = super(TransactionSqlModel, self).data(index, role)
                if d:
                    d = QtCore.QDateTime.fromString(d, DB_DateTime)
                    return d.toString(disp_DateTime)

        # Set column 'dueDateCol' to a date edit field
        if index.column() == dueDateCol:
            d = super(TransactionSqlModel, self).data(index, role)
            if d:
                return convert_date('DB2Qt', d)
                    
        return super(TransactionSqlModel, self).data(index, role)


class QTableViewCustom(QtGui.QTableView):
    def __init__(self, parent):
        super(QTableViewCustom, self).__init__(parent)

        self.parent = parent
        # self.editCol = editCol
        self.scannerIsTyping = False
        self.keyStrokeList = ''
        self.installEventFilter(KeyPressEater(self))

    def set_scanner_field(self, gear_id):

        self.parent.set_scanner_field(gear_id)


def make_line_edit(this, label_name, place_holder=None):

    lab = QtGui.QLabel(label_name)
    edit = QtGui.QLineEdit(this)
    if place_holder:
        edit.setPlaceholderText(place_holder)

    return lab, edit


def make_line_edit_display_only():

    line_edit = QtGui.QLineEdit(None)

    line_edit.setFrame(False)
    line_edit.setReadOnly(True)
    line_edit.setFocusPolicy(QtCore.Qt.NoFocus)
    line_edit.setAutoFillBackground(True)

    return line_edit


def make_line_edit_combobox(this, line_label, line_placeholder, box_label):

    # Search box
    name_label, line_edit = make_line_edit(this, line_label, line_placeholder)

    # Birthday display box
    box_label = QtGui.QLabel(box_label)
    box = QtGui.QComboBox()
    box.setEditable(False)
    box.setInsertPolicy(QtGui.QComboBox.InsertAlphabetically)

    return name_label, line_edit, box_label, box


def address_layout(this, pre, address_label):

    this.__dict__[pre + 'addrLab'] = QtGui.QLabel(address_label)
    this.__dict__[pre + 'addrLab'].setAlignment(QtCore.Qt.AlignTop)
    this.__dict__[pre + 'streetEdit'] = make_line_edit(this, 'Street', 'Street')[1]
    this.__dict__[pre + 'cityEdit'] = make_line_edit(this, 'City', 'City')[1]
    this.__dict__[pre + 'stateBox'] = QtGui.QComboBox()
    this.__dict__[pre + 'zipEdit'] = make_line_edit(this, 'Zipcode', 'Zip')[1]
    this.__dict__[pre + 'zipEdit'].setMaxLength(5)
    states = ['AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
              'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD',
              'ME', 'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH',
              'NJ', 'NM', 'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
              'SD', 'TN', 'TX', 'UT', 'VA', 'VT', 'WA', 'WI', 'WV', 'WY']
    this.__dict__[pre + 'stateBox'].insertItem(0, '')
    this.__dict__[pre + 'stateBox'].insertItems(1, states)

    grid = QtGui.QGridLayout()
    grid.setSpacing(10)
    grid.setColumnStretch(0, 1)

    # Place the objects on the page
    grid.addWidget(this.__dict__[pre + 'streetEdit'], 0, 0, 1, 3)
    grid.addWidget(this.__dict__[pre + 'cityEdit'], 1, 0); grid.addWidget(this.__dict__[pre + 'stateBox'], 1, 1); grid.addWidget(this.__dict__[pre + 'zipEdit'], 1, 2)

    return grid


def emergency_contact_layout(this, suff):

    this.__dict__['emNameLab' + suff], this.__dict__['emNameEdit' + suff] = make_line_edit(this, 'Name', '')
    this.__dict__['emRelatLab' + suff], this.__dict__['emRelaltEdit' + suff] = make_line_edit(this, 'Relation', '')
    this.__dict__['emHPhoneLab' + suff], this.__dict__['emHPhoneEdit' + suff] = make_line_edit(this, 'H Phone', 'XXX-XXX-XXXX')
    this.__dict__['emWPhoneLab' + suff], this.__dict__['emWPhoneEdit' + suff] = make_line_edit(this, 'W Phone', 'XXX-XXX-XXXX')
    this.__dict__['emCPhoneLab' + suff], this.__dict__['emCPhoneEdit' + suff] = make_line_edit(this, 'C Phone', 'XXX-XXX-XXXX')

    grid = QtGui.QGridLayout()
    grid.setSpacing(10)

    # Place the objects on the page

    # addrLay = addressLayout(this, 'em' + suff, 'Address')

    grid.addWidget(this.__dict__['emNameLab' + suff], 0, 0); grid.addWidget(this.__dict__['emNameEdit' + suff], 0, 1, 1, 3);                                                                                                                      grid.addWidget(this.__dict__['emRelatLab' + suff], 0, 4); grid.addWidget(this.__dict__['emRelaltEdit' + suff], 0, 5)
    grid.addWidget(this.__dict__['emHPhoneLab' + suff], 1, 0); grid.addWidget(this.__dict__['emHPhoneEdit' + suff], 1, 1); grid.addWidget(this.__dict__['emWPhoneLab' + suff], 1, 2); grid.addWidget(this.__dict__['emWPhoneEdit' + suff], 1, 3); grid.addWidget(this.__dict__['emCPhoneLab' + suff], 1, 4); grid.addWidget(this.__dict__['emCPhoneEdit' + suff], 1, 5)
    # grid.addWidget(this.__dict__['em' + suff + 'addrLab'], 2, 0); grid.addLayout(addrLay             , 2, 1, 2, 5)

    return grid


def certification_layout(this, lab, checkbox_only=False):

    set_label = ''
    for c in lab:
        if c.isupper():
            set_label += ' '
        set_label += c

    set_label = set_label.strip()

    Ckbx = QtGui.QCheckBox(set_label)

    if checkbox_only:
        return Ckbx

    date_edit = QtGui.QDateEdit(date=QtCore.QDate.currentDate())
    date_edit.setDisabled(True)
    vouched = QtGui.QLineEdit(this)
    vouched.setCompleter(this.parent.memberNameComp)
    vouched.setDisabled(True)

    if checkbox_only:
        return Ckbx
    else:
        return Ckbx, date_edit, vouched


def convert_date(conversion, input_date):

    def DB2Qt(in_date):
        return QtCore.QDate.fromString(in_date, DB_Date)

    def DB2Disp(in_date):
        return Qt2Disp(DB2Qt(in_date))

    def Disp2DB(in_date):
        return QtCore.QDate.fromString(in_date, dateDispFormat).toString(DB_Date)

    def Disp2Qt(in_date):
        return DB2Qt(Disp2DB(in_date))

    def Qt2Disp(in_date):
        return in_date.toString(dateDispFormat)

    def Qt2DB(in_date):
        return Disp2DB(Qt2Disp(in_date))

    conversions = {'DB2Qt': DB2Qt,
                   'DB2Disp': DB2Disp,
                   'Disp2DB': Disp2DB,
                   'Disp2Qt': Disp2Qt,
                   'Qt2Disp': Qt2Disp,
                   'Qt2DB': Qt2DB}

    if isinstance(input_date, list):
        for n in xrange(len(input_date)):
            input_date[n] = conversions[conversion](input_date[n])
    else:
        input_date = conversions[conversion](input_date)

    return input_date


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def remove_duplicates(dup_list):

    if not isinstance(dup_list, (list, set)):
        raise ValueError

    seen = set()
    seen_add = seen.add
    return [x for x in dup_list if x not in seen and not seen_add(x)]


def sort_list(list_to_sort):

    # Remove duplicates
    list_to_sort = list(set(list_to_sort))

    # Sort the list case insensitively
    list_to_sort = sorted(list_to_sort, key=lambda s: s.lower())

    return list_to_sort
