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
        self.comming_from = self.findChild(QLineEdit,'comming_from')
        self.patient_height = self.findChild(QLineEdit, 'height')
        self.weight = self.findChild(QLineEdit, 'weight')
        self.disease = self.findChild(QLineEdit, 'disease')
        self.diagnosis = self.findChild(QTextEdit, 'diagnosis')

        self.load_patient_data(ids)
        # self.addbutton = self.findChild(QPushButton, 'addrecord')
        # self.addbutton.clicked.connect(self.addRecord_clicked)

    def load_patient_data(self, id):
        patient = Patient.get(id=id)
        self.name.setText(patient.patient_name)
        self.age.setText(str(patient.age))
        self.address.setText(patient.address)
        self.gender.setCurrentText(patient.gender)
        self.mobile.setText(str(patient.mobile))
        # self.new = self.findChild(QRadioButton, 'radio_new')
        # self.existed = self.findChild(QRadioButton, 'radio_exiting')
        self.comming_from.setText(patient.comming_from)
        self.patient_height.setText(str(patient.height))
        self.weight.setText(str(patient.weight))
        self.disease.setText(patient.disease)
        self.diagnosis.insertPlainText(patient.diagnosis)

        if patient.status == "new":
            self.new.setChecked(True)
        elif patient.status == "existing":
            self.existed.setChecked(True)