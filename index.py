import datetime

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUiType
from PyQt5 import uic, QtWidgets
import psycopg2

import sys

from Patients import LoadPatients
from add_appointment import AddAppointment
from add_staff import AddStaff
from addpatient import AddPatient
from DB_Structure import Patient, Appointments, AvailableDays
from edit_patient import EditPatient
from visits import Visit

DashboardUI, _ = loadUiType("ui/dashboard.ui")


class Dashboard(QMainWindow, DashboardUI):
    def __init__(self):
        super(Dashboard).__init__()
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.Db_connect()
        self.Show_all_patients()

        # add button
        self.addbutton = self.findChild(QPushButton, 'addrecord')
        self.addbutton.clicked.connect(self.load_add_patient_page)

        # edit button
        self.editbtn = self.findChild(QPushButton, "edit")
        self.editbtn.clicked.connect(self.load_edit_patient_page)

        # refresh button
        self.refresh = self.findChild(QPushButton, 'refresh')
        self.refresh.clicked.connect(self.Show_all_patients)

        # delete button
        self.deleteButton = self.findChild(QPushButton, "deleteButton")
        self.deleteButton.clicked.connect(self.Delete_patient)

        # Load Visit Page
        # visit_pushButton
        self.VisitButton = self.findChild(QPushButton, "visit_pushButton")
        self.VisitButton.clicked.connect(self.load_visit_page)
        # patient menu action
        # actionPatient
        self.patientAction = self.findChild(QAction, "actionPatient")
        self.patientAction.triggered.connect(self.load_patient_menu)

        # appointment action
        self.appointmentAction = self.findChild(QAction, "actionRefresh")
        self.appointmentAction.triggered.connect(self.load_add_appointment_menu)

        # staff action
        self.staffAction = self.findChild(QAction, "actionStaff")
        self.staffAction.triggered.connect(self.load_staff_menu)

    def Db_connect(self):
        # connection between app and db
        self.conn = psycopg2.connect(host='localhost', user='postgres', password='postgres')
        self.cur = self.conn.cursor()
        # query = """ SELECT * from patient"""
        # result = self.cur.execute(query)
        # print(result)

    def Handel_button(self):
        pass

    def Show_all_patients(self):
        # show all patients

        # self.tableWidget.setRowCount(1)
        # self.tableWidget.setItem(1, 1, QTableWidgetItem("test"))
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch)
        patients = (Appointments.select().where(Appointments.date == datetime.date.today())
                    .join(Patient).where(Patient.id == Appointments.patient_id)
                    .switch(Appointments)
                    .join(AvailableDays).where(AvailableDays.id == Appointments.available_day_id)
                    .order_by(AvailableDays.time_from.desc(), Appointments.date.asc()))
        self.tableWidget.setRowCount(len(patients))
        rowindex = 0
        for patient in patients:
            self.tableWidget.setItem(rowindex, 0, QtWidgets.QTableWidgetItem(str(patient.patient_id.patient_name)))
            self.tableWidget.setItem(rowindex, 1, QtWidgets.QTableWidgetItem(str(patient.patient_id.mobile)))
            self.tableWidget.setItem(rowindex, 2, QtWidgets.QTableWidgetItem(str(patient.available_day_id.time_from)))
            self.tableWidget.setItem(rowindex, 3, QtWidgets.QTableWidgetItem(str(patient.date)))
            self.tableWidget.setItem(rowindex, 4, QtWidgets.QTableWidgetItem(str(patient.available_day_id.day)))
            rowindex = rowindex + 1

    def load_add_patient_page(self):
        # add new patient
        self.window = AddPatient()
        self.window.show()

    def load_edit_patient_page(self):
        # edit patient data
        selected_id = self.tableWidget.item(self.tableWidget.currentRow(), 0).text()
        self.editwindow = EditPatient(selected_id)
        self.editwindow.show()

    def Delete_patient(self):
        selected_id = self.tableWidget.item(self.tableWidget.currentRow(), 0).text()
        patient = Patient.get(id=int(selected_id))
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("Want to delete all data of ID = " + str(selected_id))
        msgBox.setWindowTitle("Confirmation")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            patient.delete_by_id(int(selected_id))

        self.Show_all_patients()

    def load_visit_page(self):
        self.window = Visit()
        self.window.show()

    def load_patient_menu(self):
        self.window = LoadPatients()
        self.window.show()

    def load_add_appointment_menu(self):
        self.window = AddAppointment()
        self.window.show()

    def load_staff_menu(self):
        self.window = AddStaff()
        self.window.show()


def main():
    app = QApplication(sys.argv)
    window = Dashboard()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
