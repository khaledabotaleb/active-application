from PyQt5 import *
import psycopg2
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import *

from DB_Structure import Patient, AvailableDays, Appointments
from update_appointment import UpdateAppointment


class AddAppointment(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('ui/addappointment.ui', self)
        self.show_patient_appointments()

        self.day = self.findChild(QComboBox, "comboBox_2")
        self.date_from = self.findChild(QComboBox, "comboBox")
        self.patient_list = self.findChild(QComboBox, "patient_list")
        self.date = self.findChild(QDateEdit, "dateEdit")
        self.load_patient_combobox()
        self.selectionchange()
        self.day.currentIndexChanged.connect(self.selectionchange)

        self.addbutton = self.findChild(QPushButton, 'addrecord')
        self.addbutton.clicked.connect(self.add_appointment_record)

    def load_patient_combobox(self):
        patients = Patient.select()
        for patient in patients:
            self.patient_list.addItem(patient.patient_name, userData=patient.id)
        # customer_id = self.patient_list.currentData()

        # print(customer_id)

    def selectionchange(self):
        print("Items in the list are :")
        # self.cur.execute('''
        #             SELECT time_from FROM public.availabledays where day='saturday' and closed is null
        #             ''')
        # data = self.cur.fetchall()

        data = AvailableDays.select(AvailableDays.time_from, AvailableDays.id).where(AvailableDays.day == self.day.currentText(), AvailableDays.closed==False)
        self.date_from.clear()
        for item in data:
            self.date_from.addItem(str(item.time_from), userData=item.id)
            # self.date_from.itemText(count)

        print("selection changed ", self.day.currentText())

    def add_appointment_record(self):

        time = self.date_from.currentData()
        patient = self.patient_list.currentData()
        date = self.date.text()

        appointment = Appointments.create(date=date, attendance=True, patient_id=patient, available_day_id=time)
        appointments_num = Appointments.select().where(Appointments.available_day_id == time).count()
        print(appointments_num)
        if appointments_num == 6:
            available_day = (AvailableDays.update({AvailableDays.closed: True}).where(AvailableDays.id==time))
            available_day.execute()
        self.selectionchange()
        QMessageBox.about(self, "Appointment", "Appointment Added Successfully")

    def show_patient_appointments(self):
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch)
        patient_appointments = (Appointments.select()
         .join(Patient).where(Patient.id==Appointments.patient_id)
         .switch(Appointments)
         .join(AvailableDays).where(AvailableDays.id==Appointments.available_day_id)
         .order_by(Appointments.date.asc(), AvailableDays.time_from.asc()))
        self.tableWidget.setRowCount(len(patient_appointments))
        rowindex = 0
        for item in patient_appointments:
            self.tableWidget.setItem(rowindex, 0, QtWidgets.QTableWidgetItem(str(item.patient_id.patient_name)))
            self.tableWidget.setItem(rowindex, 1, QtWidgets.QTableWidgetItem(str(item.available_day_id.day)))
            self.tableWidget.setItem(rowindex, 2, QtWidgets.QTableWidgetItem(str(item.available_day_id.time_from)))
            self.tableWidget.setItem(rowindex, 3, QtWidgets.QTableWidgetItem(str(item.date)))
            self.tableWidget.setItem(rowindex, 4, QtWidgets.QTableWidgetItem(str(item.attendance)))

            self.btn_update = QPushButton('Edit')
            self.btn_update.button_row = item.id
            self.btn_update.clicked.connect(self.handleUpdateButtonClicked)
            self.tableWidget.setCellWidget(rowindex, 5, self.btn_update)
            self.btn_delete = QPushButton('Delete')
            self.btn_delete.button_row = item.id
            # self.btn_delete.clicked.connect(self.handleButtonClicked)
            self.tableWidget.setCellWidget(rowindex, 6, self.btn_delete)
            rowindex = rowindex + 1

    def handleUpdateButtonClicked(self):
        button = self.sender()
        self.editwindow = UpdateAppointment(button.button_row)
        self.editwindow.show()
