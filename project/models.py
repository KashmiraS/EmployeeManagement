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
    joiningDate = db.Column(db.DateTime)
    gender = db.Column(db.Text)
    password = db.Column(db.Text)
    payment = db.relationship('Salary',backref='Salary',uselist=False,passive_deletes=True)

    def __init__(self,data):
        self.firstName = data['firstName']
        self.lastName = data['lastName']
        self.address = data['address']
        self.email = data['email']
        self.mobileNo = data['mobileNo']

        try:
            print('date form user {}'.format(str(data['joiningDate'])))
            date_dt = datetime.strptime(str(data['joiningDate']), '%d/%m/%Y')
            self.joiningDate = date_dt
        except Exception as e:
            print("ERROR {}".format(e))
        self.gender = data['gender']
        self.password = data['password']



class Salary(db.Model):
    __table_name__ = "salary"

    salaryId = db.Column(db.Integer, primary_key=True)
    empId = db.Column(db.Integer,db.ForeignKey('employee.employeeId',ondelete='CASCADE'),nullable=False)
    # employeeObj = db.relationship("employee", backref="salary")
    #employeeRef = db.relationship('Employee', backref=backref("salary", cascade="all,delete"))
    workingDays = db.Column(db.Integer)
    paymentMode = db.Column(db.Text)
    basicSalary = db.Column(db.Float)
    pf = db.Column(db.Float)
    totalEarnings = db.Column(db.Float)
    professionalTax = db.Column(db.Float)
    netSalary = db.Column(db.Float)

    def __init__(self,data):
        self.empId = data['employeeId']
        self.workingDays = data['workingDays']
        self.paymentMode = data['paymentMode']
        self.basicSalary = data['basicSalary']
        self.pf = data['pf']
        self.totalEarnings = data['totalEarnings']
        self.professionalTax = data['professionalTax']
        self.netSalary = data['netSalary']


