from PyQt5 import *
import psycopg2
from PyQt5 import uic
from PyQt5.QtWidgets import *

from DB_Structure import Patient, AvailableDays


class AddAppointment(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('ui/addappointment.ui', self)

        self.day = self.findChild(QComboBox, "comboBox_2")
        self.date_from = self.findChild(QComboBox, "comboBox")
        self.patient_list = self.findChild(QComboBox, "patient_list")
        self.date = self.findChild(QDateEdit, "dateEdit")
        self.load_patient_combobox()
        self.selectionchange()
        self.day.currentIndexChanged.connect(self.selectionchange)

    def load_patient_combobox(self):
        patients = Patient.select()
        for patient in patients:
            self.patient_list.addItem(patient.patient_name, userData=patient.id)
        customer_id = self.patient_list.currentData()
        # print(customer_id)

    def selectionchange(self):
        self.conn = psycopg2.connect(host='localhost', user='postgres', password='postgres')
        self.cur = self.conn.cursor()

        print("Items in the list are :")
        # self.cur.execute('''
        #             SELECT time_from FROM public.availabledays where day='saturday' and closed is null
        #             ''')
        # data = self.cur.fetchall()

        data = AvailableDays.select(AvailableDays.time_from, AvailableDays.id).where(AvailableDays.day == self.day.currentText())
        self.date_from.clear()
        for item in data:
            self.date_from.addItem(str(item.time_from), userData=item.id)
            # self.date_from.itemText(count)

        print("selection changed ", self.day.currentText())