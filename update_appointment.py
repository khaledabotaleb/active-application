from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import *

from DB_Structure import Appointments, AvailableDays


class UpdateAppointment(QWidget):
    def __init__(self, id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('ui/updateappointment.ui', self)

        self.id = self.findChild(QLineEdit, "lineEdit_4")
        self.id.setText(str(id))
        self.patient = self.findChild(QLineEdit, "lineEdit")
        self.date = self.findChild(QDateEdit, "dateEdit")
        self.appointment_day = self.findChild(QLineEdit, "lineEdit_2")
        self.appointment_time = self.findChild(QLineEdit, "lineEdit_3")
        self.day = self.findChild(QComboBox, "comboBox_2")
        self.date_from = self.findChild(QComboBox, "comboBox")
        self.selectionchange()
        self.day.currentIndexChanged.connect(self.selectionchange)
        self.load_patient_appointment(id)
        self.updatebutton = self.findChild(QPushButton, 'updateappointment')
        self.updatebutton.clicked.connect(self.update_patient_appointment)

    def selectionchange(self):
        data = AvailableDays.select(AvailableDays.time_from, AvailableDays.id).where(AvailableDays.day == self.day.currentText(), AvailableDays.closed==False)
        self.date_from.clear()
        for item in data:
            self.date_from.addItem(str(item.time_from), userData=item.id)

    def load_patient_appointment(self, id):
        appointment = Appointments.get(id=id)
        self.patient.setText(appointment.patient_id.patient_name)
        self.date.setDate(appointment.date)
        self.appointment_day.setText(appointment.available_day_id.day)
        self.appointment_time.setText(str(appointment.available_day_id.time_from))
        self.selectionchange()
        self.day.currentIndexChanged.connect(self.selectionchange)

    def update_patient_appointment(self):
        time = self.date_from.currentData()
        date = self.date.text()
        id = int(self.id.text())
        old_time = Appointments.select(Appointments.available_day_id).where(Appointments.id==id)
        q = (Appointments
             .update(
            {Appointments.available_day_id: time, Appointments.date: date})
             .where(Appointments.id == id))
        q.execute()
        new_time = Appointments.select(Appointments.available_day_id).where(Appointments.id==id)
        appointments_num_for_old = Appointments.select().where(Appointments.available_day_id == old_time).count()
        appointments_num_for_new = Appointments.select().where(Appointments.available_day_id == new_time).count()
        if appointments_num_for_old < 6:
            available_day = (AvailableDays.update({AvailableDays.closed: False}).where(AvailableDays.id==old_time))
            available_day.execute()
        if appointments_num_for_new == 6:
            available_day = (AvailableDays.update({AvailableDays.closed: True}).where(AvailableDays.id == new_time))
            available_day.execute()
        self.selectionchange()
        QMessageBox.about(self, "Appointment", "Update patient appointment")