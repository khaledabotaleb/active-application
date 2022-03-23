import datetime
from calendar import calendar

from PyQt5 import *
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import *

from DB_Structure import Patient
from DB_Structure import Staff, Visits


class Visit(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('ui/addvisit.ui', self)
        self.load_visits()

        self.patient_list = self.findChild(QComboBox, "patient_comboBox")
        self.doctor_list = self.findChild(QComboBox, "doctor_comboBox")
        self.recovery = self.findChild(QLineEdit, "percentage_lineEdit")
        self.load_patient_combobox()
        self.load_doctor_combobox()

        self.addButton = self.findChild(QPushButton, "addvisit")
        self.addButton.clicked.connect(self.add_button_clicked)

    def load_patient_combobox(self):
        patients = Patient.select()
        for patient in patients:
            self.patient_list.addItem(patient.patient_name, userData=patient.id)

    def load_doctor_combobox(self):
        doctors = Staff.select().where(Staff.role == "Doctor")
        for staff in doctors:
            self.doctor_list.addItem(staff.staff_name, userData=staff.id)

    def add_button_clicked(self):
        doctor = self.doctor_list.currentData()
        patient = self.patient_list.currentData()
        recovery = self.recovery.text()

        Visits.create(doctor_id=doctor, patient_id=patient, recovery_percentage_after_visit=recovery, date=datetime.datetime.now().date())
        QMessageBox.about(self, "Visit", "Visit Added Successfully")
        self.recovery.setText('')
        self.load_visits()
        # self.doctor_list.setIndex(0)
        # self.patient_list.setIndex(0)

    def load_visits(self):
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch)
        visits = Visits.select()
        self.tableWidget.setRowCount(len(visits))
        row_index = 0
        for visit in visits:
            self.tableWidget.setItem(row_index, 0, QtWidgets.QTableWidgetItem(str(visit.patient_id.patient_name)))
            self.tableWidget.setItem(row_index, 1, QtWidgets.QTableWidgetItem(str(visit.doctor_id.staff_name)))
            self.tableWidget.setItem(row_index, 2, QtWidgets.QTableWidgetItem(str(visit.date.strftime('%A'))))
            self.tableWidget.setItem(row_index, 3, QtWidgets.QTableWidgetItem(str(visit.date)))
            self.tableWidget.setItem(row_index, 4, QtWidgets.QTableWidgetItem(str(visit.recovery_percentage_after_visit)))
            row_index = row_index + 1