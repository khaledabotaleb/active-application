from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUiType
from PyQt5 import uic, QtWidgets
import psycopg2

import sys
from addpatient import AddPatient
from DB_Structure import Patient
from edit_patient import EditPatient

DashboardUI, _ = loadUiType("ui/dashboard.ui")


class Dashboard(QMainWindow, DashboardUI):
    def __init__(self):
        super(Dashboard).__init__()
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.Db_connect()
        self.Show_all_patients()

        self.addbutton = self.findChild(QPushButton, 'addrecord')
        self.addbutton.clicked.connect(self.load_add_patient_page)

        self.editbtn = self.findChild(QPushButton, "edit")
        self.editbtn.clicked.connect(self.load_edit_patient_page)

        self.refresh = self.findChild(QPushButton, 'refresh')
        self.refresh.clicked.connect(self.Show_all_patients)

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
        patients = Patient.select()
        self.tableWidget.setRowCount(len(patients))
        rowindex = 0
        for patient in patients:
            self.tableWidget.setItem(rowindex, 0, QtWidgets.QTableWidgetItem(str(patient.id)))
            self.tableWidget.setItem(rowindex, 1, QtWidgets.QTableWidgetItem(patient.patient_name))
            self.tableWidget.setItem(rowindex, 2, QtWidgets.QTableWidgetItem(str(patient.age)))
            self.tableWidget.setItem(rowindex, 3, QtWidgets.QTableWidgetItem(patient.gender))
            self.tableWidget.setItem(rowindex, 4, QtWidgets.QTableWidgetItem(str(patient.mobile)))
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
        # delete patient from db
        pass

    def refresh_table(self):
        conn = self.Db_connect()
        sql = "SELECT * FROM entry"
        cur = conn.cursor()
        result = cur.execute(sql)
        no_row = len(result.fetchall())

        self.tableWidget.setRowCount(no_row)
        rowindex = 0
        for row in cur.execute(sql):
            self.tableWidget.setItem(rowindex, 0, QtWidgets.QTableWidgetItem(row[1]))
            self.tableWidget.setItem(rowindex, 1, QtWidgets.QTableWidgetItem(row[2]))
            self.tableWidget.setItem(rowindex, 2, QtWidgets.QTableWidgetItem(row[3]))
            self.tableWidget.setItem(rowindex, 3, QtWidgets.QTableWidgetItem(row[4]))
            self.tableWidget.setItem(rowindex, 4, QtWidgets.QTableWidgetItem(row[5]))
            self.tableWidget.setItem(rowindex, 5, QtWidgets.QTableWidgetItem(row[6]))
            self.tableWidget.setItem(rowindex, 6, QtWidgets.QTableWidgetItem(row[7]))
            self.tableWidget.setItem(rowindex, 7, QtWidgets.QTableWidgetItem(row[8]))
            self.tableWidget.setItem(rowindex, 8, QtWidgets.QTableWidgetItem(row[9]))
            self.tableWidget.setItem(rowindex, 9, QtWidgets.QTableWidgetItem(row[10]))
            self.tableWidget.setItem(rowindex, 10, QtWidgets.QTableWidgetItem(row[13]))
            self.tableWidget.setItem(rowindex, 11, QtWidgets.QTableWidgetItem(row[11]))
            self.tableWidget.setItem(rowindex, 12, QtWidgets.QTableWidgetItem(row[12]))
            self.tableWidget.setItem(rowindex, 13, QtWidgets.QTableWidgetItem(row[14]))
            self.tableWidget.setItem(rowindex, 14, QtWidgets.QTableWidgetItem(row[15]))
            self.tableWidget.setItem(rowindex, 15, QtWidgets.QTableWidgetItem(row[16]))
            rowindex = rowindex + 1

        conn.commit()
        conn.close()


def main():
    app = QApplication(sys.argv)
    window = Dashboard()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
