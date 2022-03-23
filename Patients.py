from PyQt5 import *
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import *

from DB_Structure import Patient
from addpatient import AddPatient
from edit_patient import EditPatient


class LoadPatients(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('ui/patient.ui', self)
        self.list_patients_data()

        # add button
        self.addbutton = self.findChild(QPushButton, 'addrecord')
        self.addbutton.clicked.connect(self.load_add_patient_page)

        self.editbtn = self.findChild(QPushButton, "edit")
        self.editbtn.clicked.connect(self.load_edit_patient_page)

        # delete button
        self.deleteButton = self.findChild(QPushButton, "deleteButton")
        self.deleteButton.clicked.connect(self.Delete_patient)

        # refresh button
        self.refresh = self.findChild(QPushButton, 'refresh')
        self.refresh.clicked.connect(self.list_patients_data)

    def list_patients_data(self):
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch)
        patients = Patient.select()
        self.tableWidget.setRowCount(len(patients))
        row_index = 0
        for patient in patients:
            self.tableWidget.setItem(row_index, 0, QtWidgets.QTableWidgetItem(str(patient.id)))
            self.tableWidget.setItem(row_index, 1, QtWidgets.QTableWidgetItem(str(patient.patient_name)))
            self.tableWidget.setItem(row_index, 2, QtWidgets.QTableWidgetItem(str(patient.mobile)))
            self.tableWidget.setItem(row_index, 3, QtWidgets.QTableWidgetItem(str(patient.age)))
            self.tableWidget.setItem(row_index, 4, QtWidgets.QTableWidgetItem(str(patient.gender)))
            self.tableWidget.setItem(row_index, 5, QtWidgets.QTableWidgetItem(str(patient.address)))
            self.tableWidget.setItem(row_index, 6, QtWidgets.QTableWidgetItem(str(patient.status)))
            self.tableWidget.setItem(row_index, 7, QtWidgets.QTableWidgetItem(str(patient.disease)))
            self.tableWidget.setItem(row_index, 8, QtWidgets.QTableWidgetItem(str(patient.comming_from)))
            self.tableWidget.setItem(row_index, 9, QtWidgets.QTableWidgetItem(str(patient.diagnosis)))
            self.tableWidget.setItem(row_index, 10, QtWidgets.QTableWidgetItem(str(patient.weight)))
            self.tableWidget.setItem(row_index, 11, QtWidgets.QTableWidgetItem(str(patient.height)))
            row_index = row_index + 1

    def load_add_patient_page(self):
        # add new patient
        self.window = AddPatient()
        self.window.show()

    def load_edit_patient_page(self):
        # edit patient data
        try:
            selected_id = self.tableWidget.item(self.tableWidget.currentRow(), 0).text()
            self.editwindow = EditPatient(selected_id)
            self.editwindow.show()
        except Exception as e:
            QMessageBox.about(self, "Warning", "Please Select Patient Row To Edit")

    def Delete_patient(self):

        try:
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

            self.list_patients_data()
        except Exception as e:
            QMessageBox.about(self, "Warning", "Please Select Patient Row To Delete")