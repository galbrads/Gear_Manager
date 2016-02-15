from __future__ import division
from PySide import QtCore
from PySide.QtTest import QTest
import Util
import sys
import os

dBName = '__TEST__.sqlite'


def mkMember(c='A', n=1, **kwargs):

    date = '2{0:03}-{0:02}-{0:02}'.format(n)
    bday = '2000-{0:02}-{0:02}'.format(n)
    today = Util.convert_date('Qt2DB', QtCore.QDate.currentDate())
    AAA111 = '{} {}'.format(111 * n, c * 3)
    email = '{0}@{0}.com'.format(c * 3)
    phone = str(n)[0] * 10
    AAA = c * 3
    num3 = str(n) * 3
    num5 = str(n) * 5

    cert = ['1', '1', '1', '1']
    membStat = 'Regular'
    studStat = 'Undergrad'
    forms = True
    campusLink = True
    formsDate = today
    campuDate = today

    for arg in kwargs:
        if arg == 'cert':
            cert = kwargs[arg]
        elif arg == 'membStat':
            membStat = kwargs[arg]
        elif arg == 'studStat':
            studStat = kwargs[arg]
        elif arg == 'forms':
            forms = kwargs[arg]
        elif arg == 'formsDate':
            formsDate = kwargs[arg]
        elif arg == 'campusLink':
            campusLink = kwargs[arg]
        elif arg == 'campusDate':
            campuDate = kwargs[arg]
        else:
            print "ERROR: Incorrect karg in 'mkMember'"
            sys.exit()

    attrs = {'FirstName'   :AAA      , 'LastName'     :AAA       , 'Phone'         :phone , \
             'Email'       :email    , 'StudentID'    :''        , 'FormsCurrent'  :forms , \
             'FormsDate'   :formsDate, 'CampusLink'   :campusLink, 'CampusLinkDate':campuDate, \
             'Birthday'    :bday     , 'MembStat'     :membStat  , 'StudStat'      :studStat , \
             'street'      :AAA111   , 'city'         :AAA       , 'state'         :'KS'  , 'zip':num5, \
             'EmName'      :AAA      , 'EmRel'        :AAA       , \
             'EmPhoneH'    :phone    , 'EmPhoneW'     :phone     , 'EmPhoneC'      :phone , \
             'EmStreet'    :AAA111   , 'EmCity'       :AAA       , 'EmState'       :'KS'  , 'EmZip' :num5, \
             'RoommateName':AAA      , 'RoommatePhone':phone     , \
             'InsurName'   :AAA      , 'InsurPol'     :num3      , 'InsurGrp'      :num3  , \
             'Med'         :AAA      , 'Note'         :AAA}

    for cert in Util.certifications:

        attrs[cert + 'Cert'] = 0
        attrs[cert + 'CertDate'] = date
        attrs[cert + 'CertVouch'] = AAA

    return attrs


def mkGear(c='A', n=1, cert=['1', '1', '1', '1'], quant=1, unRnt=False, unReas=''):

    date = '2{0:03}-{0:02}-{0:02}'.format(n)
    expir = '21{0:02}-{0:02}-{0:02}'.format(n)
    AAA111 = '{} {}'.format(111 * n, c * 3)
    AAA = c * 3
    num = 11.11 * n

    attrs = {'Name'           :AAA , 'ID'        :AAA111 , 'Quantity'        :quant  , 'Price':num, \
             'PurchaseDate'   :date, 'Weight'    :num    , 'ExpirationDate'  :expir  , \
             'Manufacturer'   :AAA , 'Unrentable':unRnt  , 'UnrentableReason':unReas , \
             'CareMaintenance':AAA , 'Misc' :AAA}

    for cert in Util.certifications:

        attrs[cert + 'Cert'] = 0

    return attrs


def enterMemberInfo(this, memberAttr):

    this.tMemb.clear_fields()

    # this.tMemb.nameSearch.clear()

    QTest.keyClicks(this.tMemb.MFNameEdit, memberAttr['FirstName' ])
    QTest.keyClicks(this.tMemb.MLNameEdit, memberAttr['LastName'  ])
    QTest.keyClicks(this.tMemb.PhoneEdit , memberAttr['Phone'     ])
    QTest.keyClicks(this.tMemb.EmailEdit , memberAttr['Email'     ])
    QTest.keyClicks(this.tMemb.MNumEdit  , memberAttr['StudentID' ])
    this.tMemb.FormsCkbx       .setChecked(memberAttr['FormsCurrent'])
    this.tMemb.campLinkCkbx    .setChecked(memberAttr['CampusLink'  ])
    this.tMemb.FormsDateEdit   .setDate(Util.convert_date('DB2Qt', memberAttr['FormsDate'     ]))
    this.tMemb.campLinkDateEdit.setDate(Util.convert_date('DB2Qt', memberAttr['CampusLinkDate']))
    this.tMemb.BirthdayEdit    .setDate(Util.convert_date('DB2Qt', memberAttr['Birthday'      ]))
    this.tMemb.statusBox       .setCurrentIndex(this.tMemb.statusBox.findText(memberAttr['MembStat']))
    this.tMemb.studStatBox     .setCurrentIndex(this.tMemb.studStatBox.findText(memberAttr['StudStat']))
    QTest.keyClicks(this.tMemb .streetEdit, memberAttr['street'])
    QTest.keyClicks(this.tMemb .cityEdit  , memberAttr['city'  ])
    this.tMemb.stateBox        .setCurrentIndex(this.tMemb.stateBox.findText(memberAttr['state']))
    QTest.keyClicks(this.tMemb .zipEdit   , memberAttr['zip'   ])

    # Emergency Contact 1 Info
    QTest.keyClicks(this.tMemb.emNameEdit  , memberAttr['EmName'  ])
    QTest.keyClicks(this.tMemb.emRelaltEdit, memberAttr['EmRel'   ])
    QTest.keyClicks(this.tMemb.emHPhoneEdit, memberAttr['EmPhoneH'])
    QTest.keyClicks(this.tMemb.emWPhoneEdit, memberAttr['EmPhoneW'])
    QTest.keyClicks(this.tMemb.emCPhoneEdit, memberAttr['EmPhoneC'])
#     QTest.keyClicks(this.tMemb.emStreetEdit, memberAttr['EmStreet'])
#     QTest.keyClicks(this.tMemb.emCityEdit  , memberAttr['EmCity'  ])
#     this.tMemb.emStateBox.setCurrentIndex(this.tMemb.emStateBox.findText(memberAttr['EmState' ]))
#     QTest.keyClicks(this.tMemb.emZipEdit   , memberAttr['EmZip'   ])

    # Room mate name and phone
    QTest.keyClicks(this.tMemb.rommateEdit     , memberAttr['RoommateName' ])
    QTest.keyClicks(this.tMemb.rommatePhoneEdit, memberAttr['RoommatePhone'])

    # Insurance fields
    QTest.keyClicks(this.tMemb.insEdit   , memberAttr['InsurName'])
    QTest.keyClicks(this.tMemb.insPolEdit, memberAttr['InsurPol' ])
    QTest.keyClicks(this.tMemb.insGrpEdit, memberAttr['InsurGrp' ])

    # Certifications
    for cert in Util.certifications:
        this.tMemb.__dict__[cert + 'CertCkbx'].setChecked(memberAttr[cert + 'Cert'])
        if this.tMemb.__dict__[cert + 'CertCkbx'].isChecked():
            this.tMemb.__dict__[cert + 'DateEdit'].setDate(memberAttr[cert + 'CertDate'])
        this.tMemb.__dict__[cert + 'Vouched'].setText(memberAttr[cert + 'CertVouch'])

    # Medical Condition
    this.tMemb.medEdit.setPlainText(memberAttr['Med'])

    # Member Notes
    this.tMemb.noteEdit.setPlainText(memberAttr['Note'])


def enterGearInfo(this, gearAttr):

    this.tGear.clear_fields()

    this.tGear.gNameIDSearch.clear()

    QTest.keyClicks(this.tGear.GNameEdit    , gearAttr['Name'])
    QTest.keyClicks(this.tGear.GIDEdit      , gearAttr['ID'])
    this.tGear.QuantSpin    .setValue(gearAttr['Quantity'])
    QTest.keyClicks(this.tGear.PriceEdit    , '{:0.2f}'.format(gearAttr['Price']))
    this.tGear.PurchDateEdit.setDate(Util.convert_date('DB2Qt', gearAttr['PurchaseDate']))
    this.tGear.unitBox      .setCurrentIndex(this.tGear.unitBox.findText('kg'))
    QTest.keyClicks(this.tGear.WeightEdit   , str(gearAttr['Weight']))
    if gearAttr['ExpirationDate']:
        this.tGear.ExpDateCkbx.setChecked(True)
        this.tGear.ExpDateEdit.setDate(Util.convert_date('DB2Qt', gearAttr['ExpirationDate']))
    else:
        this.tGear.ExpDateCkbx.setChecked(False)
    QTest.keyClicks(this.tGear.ManufacEdit, gearAttr['Manufacturer'])
    this.tGear.checkoutable.setChecked(gearAttr['Unrentable'])
    QTest.keyClicks(this.tGear.checkoutable_lineedit, gearAttr['UnrentableReason'])

    # Certifications
    for cert in Util.certifications:
        this.tGear.__dict__[cert + 'CertCkbx'].setChecked(gearAttr[cert + 'Cert'])

    this.tGear.MaintenanceEdit.setPlainText(gearAttr['CareMaintenance'])
    this.tGear.NoteEdit       .setPlainText(gearAttr['Misc'])

if __name__ == '__main__':

    os.system('python -m unittest discover')
