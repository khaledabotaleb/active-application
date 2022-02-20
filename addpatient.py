from operator import add
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5 import *
import psycopg2
from DB_Structure import Patient


class AddPatient(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('ui/addpatient.ui', self)

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

        self.addbutton = self.findChild(QPushButton, 'addrecord')
        self.addbutton.clicked.connect(self.addRecord_clicked)

    def addRecord_clicked(self):
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

        Patient.create(patient_name=patient_name, age=age, address=address, gender=gender, mobile=mobile, status=status, comming_from=comming_from, disease=disease, diagnosis=diagnosis, weight=weight, height=height)
        # self.conn = psycopg2.connect(host='localhost', user='postgres', password='postgres')
        # self.cur = self.conn.cursor()
        
        # query = f"INSERT INTO patient(patient_name, age, address, gender, mobile, status, comming_from, disease, diagnosis, weight, height) VALUES ({patient_name}, {age}, {address}, {gender}, {mobile},{status}, {comming_from}, {disease}, {diagnosis}, {weight}, {height})"
        # self.cur.execute(query)

        # self.db.commit()
        QMessageBox.about(self, "Patient", "New patient Added")
        # self.statusbar.showMessage('New patient Added')
        self.name.setText('')
        self.age.setText('')
        self.address.setText('')
        self.gender.setCurrentIndex(0)
        self.mobile.setText('')
        self.comming_from.setText('')
        self.disease.setText('')
        self.diagnosis.setPlainText('')
        self.weight.setText('')
        self.patient_height.setText('')

