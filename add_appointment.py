from PyQt5 import *
import psycopg2
from PyQt5 import uic
from PyQt5.QtWidgets import *

from DB_Structure import Patient


class AddAppointment(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('ui/addappointment.ui', self)

        self.day = self.findChild(QComboBox, "comboBox_2")
        self.date_from = self.findChild(QComboBox, "comboBox")
        self.patient_list = self.findChild(QComboBox, "patient_list")
        self.date = self.findChild(QDateEdit, "dateEdit")
        self.load_patient_combobox()

    def load_patient_combobox(self):
        patients = Patient.select()
        for patient in patients:
            self.patient_list.addItem(patient.patient_name, userData=patient.id)
        customer_id = self.patient_list.currentData()
        # print(customer_id)