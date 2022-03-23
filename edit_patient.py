from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5 import *
import psycopg2
from DB_Structure import Patient


class EditPatient(QWidget):
    def __init__(self, ids, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('ui/editpatient.ui', self)

        self.id = self.findChild(QLineEdit, "id")
        self.id.setText(str(ids))
        self.name = self.findChild(QLineEdit, 'name')
        self.age = self.findChild(QLineEdit, 'age')
        self.address = self.findChild(QLineEdit, 'address')
        self.gender = self.findChild(QComboBox, 'gender')
        self.mobile = self.findChild(QLineEdit, 'mobile')
        self.new = self.findChild(QRadioButton, 'radio_new')
        self.existed = self.findChild(QRadioButton, 'radio_exiting')
        self.comming_from = self.findChild(QLineEdit, 'comming_from')
        self.patient_height = self.findChild(QLineEdit, 'height')
        self.weight = self.findChild(QLineEdit, 'weight')
        self.disease = self.findChild(QLineEdit, 'disease')
        self.diagnosis = self.findChild(QTextEdit, 'diagnosis')

        self.load_patient_data(ids)
        self.update_button = self.findChild(QPushButton, 'editpatient')
        self.update_button.clicked.connect(self.Update_button_clicked)

    def load_patient_data(self, id):
        patient = Patient.get(id=id)
        self.name.setText(patient.patient_name)
        self.age.setText(str(patient.age))
        self.address.setText(patient.address)
        self.gender.setCurrentText(patient.gender)
        self.mobile.setText(str(patient.mobile))
        self.comming_from.setText(patient.comming_from)
        self.patient_height.setText(str(patient.height))
        self.weight.setText(str(patient.weight))
        self.disease.setText(patient.disease)
        self.diagnosis.insertPlainText(patient.diagnosis)

        if patient.status == "new":
            self.new.setChecked(True)
        elif patient.status == "existing":
            self.existed.setChecked(True)

    def Update_button_clicked(self):

        status_radio = None
        if self.new.isChecked() == True:
            status_radio = "new"
        elif self.existed.isChecked() == True:
            status_radio = "existing"

        patient_name = self.name.text()
        age = self.age.text()
        address = self.address.text()
        gender = self.gender.currentText()
        mobile = self.mobile.text()
        status = status_radio
        comming_from = self.comming_from.text()
        disease = self.disease.text()
        diagnosis = self.diagnosis.toPlainText()
        weight = self.weight.text()
        height = self.patient_height.text()
        id = int(self.id.text())
        q = (Patient
             .update({Patient.patient_name: patient_name, Patient.age: age, Patient.address: address, Patient.gender: gender,
                     Patient.mobile: mobile, Patient.status: status, Patient.comming_from: comming_from, Patient.disease: disease,
                     Patient.diagnosis: diagnosis, Patient.weight: weight, Patient.height: height})
             .where(Patient.id == id))
        q.execute()
        QMessageBox.about(self, "Patient", "Update patient")
        self.window().close()