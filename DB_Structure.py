from peewee import *

db = PostgresqlDatabase('active_database', host='localhost', port=5432, user='postgres', password='postgres')


class Patient(Model):
    patient_name = CharField(null=False)
    age = IntegerField()
    address = TextField(null=True)
    gender = CharField()
    mobile = IntegerField()
    status = CharField()
    comming_from = TextField()
    disease = CharField()
    diagnosis = TextField(null=True)
    weight = FloatField(null=True)
    height = FloatField(null=True)

    class Meta:
        database = db


class AvailableDays(Model):
    day = CharField()
    time_from = TimeField(null=True)
    closed = BooleanField(null=True)

    class Meta:
        database = db


class Appointments(Model):
    date = DateField(null=True)
    attendance = BooleanField(null=True)
    patient_id = ForeignKeyField(Patient, backref='patients', null=True)
    available_day_id = ForeignKeyField(AvailableDays, backref='days', null=True)

    class Meta:
        database = db


class Staff(Model):
    staff_name = CharField(null=True) 
    age = IntegerField(null=True)
    role = CharField(null=True)
    address = TextField(null=True)
    gender = CharField(null=True)
    mobile = IntegerField(null=True)

    class Meta:
        database = db


class Visits(Model):
    doctor_id = ForeignKeyField(Staff, backref='doctors', null=True)
    patient_id = ForeignKeyField(Patient, backref='patient_visits', null=True)
    recovery_percentage_after_visit = TextField(null=True)
    date = DateField(null=True)

    class Meta:
        database = db


class Invoice(Model):
    visit_id = ForeignKeyField(Visits, backref='visits', null=True),
    price = DecimalField(null=True)
    paid = DecimalField(null=True)
    rest = DecimalField(null=True)
    date = DateField(null=True)

    class Meta:
        database = db


db.connect()
db.create_tables([Patient, Visits, AvailableDays, Appointments, Staff, Invoice])