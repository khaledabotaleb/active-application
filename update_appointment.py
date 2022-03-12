from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import *


class UpdateAppointment(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('ui/updateappointment.ui', self)
