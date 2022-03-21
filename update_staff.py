from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5 import *
import psycopg2
from DB_Structure import Patient, Staff





class UpdateStaff(QWidget):
    def __init__(self, ids, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ids = ids
        uic.loadUi('ui/updatestaff.ui', self)

        self.name = self.findChild(QLineEdit, 'name_lineEdit')
        self.age = self.findChild(QSpinBox, 'age_spinBox')
        self.role = self.findChild(QComboBox, 'role_comboBox')
        self.address = self.findChild(QLineEdit, 'address_lineEdit')
        self.gender = self.findChild(QComboBox, 'gender_comboBox')
        self.mobile = self.findChild(QLineEdit, 'mobile_lineEdit')
        self.load_staff_data(ids)

        self.addbutton = self.findChild(QPushButton, 'update_staff')
        self.addbutton.clicked.connect(self.update_staff_button_clicked)

    def load_staff_data(self, id):
        staff = Staff.get(id=id)
        self.name.setText(staff.staff_name)
        self.age.setValue(staff.age)
        self.address.setText(staff.address)
        self.gender.setCurrentText(staff.gender)
        self.mobile.setText(str(staff.mobile))

    def update_staff_button_clicked(self):
        from add_staff import AddStaff
        name = self.name.text()
        age = self.age.text()
        address = self.address.text()
        gender = self.gender.currentText()
        mobile = self.mobile.text()
        role = self.role.currentText()
        q = (Staff.update(
            {Staff.staff_name: name, Staff.age: age, Staff.address: address, Staff.gender: gender,
             Staff.role: role, Staff.mobile: mobile})
             .where(Staff.id == self.ids))
        q.execute()
        QMessageBox.about(self, "Staff", "Update staff")
        self.window().close()
