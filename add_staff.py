from PyQt5 import *
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import *

from DB_Structure import Staff
from update_staff import UpdateStaff


class AddStaff(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('ui/addstaff.ui', self)
        self.show_staff_records()

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
        self.show_staff_records()

    def show_staff_records(self):
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch)
        staffs = Staff.select()
        self.tableWidget.setRowCount(len(staffs))
        rowindex = 0
        for staff in staffs:
            self.tableWidget.setItem(rowindex, 0, QtWidgets.QTableWidgetItem(str(staff.staff_name)))
            self.tableWidget.setItem(rowindex, 1, QtWidgets.QTableWidgetItem(str(staff.age)))
            self.tableWidget.setItem(rowindex, 2, QtWidgets.QTableWidgetItem(str(staff.role)))
            self.tableWidget.setItem(rowindex, 3, QtWidgets.QTableWidgetItem(str(staff.address)))
            self.tableWidget.setItem(rowindex, 4, QtWidgets.QTableWidgetItem(str(staff.mobile)))
            self.btn_update = QPushButton('Edit')
            self.btn_update.button_row = staff.id
            self.btn_update.clicked.connect(self.handleUpdateButtonClicked)
            self.tableWidget.setCellWidget(rowindex, 5, self.btn_update)
            self.btn_delete = QPushButton('Delete')
            self.btn_delete.button_row = staff.id
            self.btn_delete.clicked.connect(self.handleDeleteButtonClicked)
            self.tableWidget.setCellWidget(rowindex, 6, self.btn_delete)
            rowindex = rowindex + 1

    def handleUpdateButtonClicked(self):
        button = self.sender()
        self.editwindow = UpdateStaff(button.button_row)
        self.editwindow.show()


    def handleDeleteButtonClicked(self):
        button = self.sender()
        staff_id = button.button_row
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("Want to delete appointment of ID = " + str(staff_id))
        msgBox.setWindowTitle("Confirmation")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            Staff.delete_by_id(int(staff_id))

        self.show_staff_records()