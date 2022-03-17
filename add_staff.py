from PyQt5 import *
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import *

from DB_Structure import Staff


class AddStaff(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('ui/addstaff.ui', self)

        self.name = self.findChild(QLineEdit, 'name_lineEdit')
        self.age = self.findChild(QSpinBox, 'AgespinBox')
        self.role = self.findChild(QComboBox, 'role_comboBox')
        self.address = self.findChild(QLineEdit, 'address_lineEdit')
        self.gender = self.findChild(QComboBox, 'gender_comboBox')
        self.mobile = self.findChild(QLineEdit, 'mobile_lineEdit')

        self.addbutton = self.findChild(QPushButton, 'addstaff')
        self.addbutton.clicked.connect(self.add_staff_clicked)

    def add_staff_clicked(self):
        name = self.name.text()
        age = self.age.text()
        address = self.address.text()
        gender = self.gender.currentText()
        mobile = self.mobile.text()
        role = self.role.currentText()

        Staff.create(staff_name=name, age=age, address=address, gender=gender, mobile=mobile, role=role)

        QMessageBox.about(self, "Staff", "New Staff Added")
        self.name.setText('')
        self.age.setValue(0)
        self.address.setText('')
        self.gender.setCurrentIndex(0)
        self.role.setCurrentIndex(0)
        self.mobile.setText('')