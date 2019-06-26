from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from project import db
from datetime import datetime


class Employee(db.Model):

    __table_name__ = "employees"

    employeeId = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.Text)
    lastName=db.Column(db.Text)
    address = db.Column(db.Text)
    email = db.Column(db.Text)
    mobileNo = db.Column(db.Text)
    salary = db.Column(db.Integer)
    joiningDate = db.Column(db.DateTime)
    gender=db.Column(db.Text)
    password=db.Column(db.Text)

    def __init__(self,data):
        self.firstName = data['firstName']
        self.lastName = data['lastName']
        self.address = data['address']
        self.email = data['email']
        self.mobileNo = data['mobileNo']
        self.salary = data['salary']
        self.password = data['']
        try:
            print('date form user {}'.format(str(data['joiningDate'])))
            date_dt = datetime.strptime(str(data['joiningDate']), '%d/%m/%Y')
            self.joiningDate = date_dt
        except Exception as e:
            print("ERROR {}".format(e))
        self.gender = data['gender']
        self.password = data['password']


