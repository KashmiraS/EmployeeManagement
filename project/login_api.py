from flask_restful import Resource
from flask import request,session
import json
from project.models import db, Employee
from datetime import datetime




class Login(Resource):
    def post(self):
        json_data = request.data

        if not json_data:
            return {'message': 'No input data provided'}

        data = json.loads(json_data)
        exists = bool(db.session.query(Employee.employeeId).filter(
            db.and_(Employee.email == data['email'], Employee.password == data['password'])).first())
        if exists:
            session['id'] = db.session.query(Employee.employeeId).filter(
            db.and_(Employee.email == data['email'], Employee.password == data['password'])).first()
            print(f'login id {session["id"]}')

        responseData = dict()
        responseData['status'] = exists
        responseData['empId']= session['id']

        return json.dumps(responseData)

    def get(self):  # forgot password
        json_data = request.data

        if not json_data:
            return {'message': 'No input data provided'}

        data = json.loads(json_data)
        email_exists = bool(db.session.query(Employee.employeeId).filter(Employee.email == data['email']).first())

        response = dict()
        response['valid'] = email_exists

        return json.dumps(response)


class Verification:
    def get(self):
        json_data = request.data

        if not json_data:
            return {'message': 'No input data provided'}

        data = json.loads(json_data)
        email_exists = bool(db.session.query(Employee.employeeId).filter(Employee.email == data['email']).first())

        response = dict()
        response['valid'] = email_exists

        return json.dumps(response)


class Register(Resource):
    def post(self):

        json_data = request.data
        data = json.loads(json_data)
        print("JSON FOR REGISTER : {}".format(data))
        is_exist = bool(db.session.query(Employee.employeeId).filter(Employee.email == data['email']).first())
        print("DATA is exist {}".format(is_exist))
        if not is_exist:
            employee = Employee(data)
            print(str(employee))
            db.session.add(employee)
            db.session.commit()
            return {'status': 'True'}
        else:
            return {'status': 'False'}

    def patch(self):

        json_data = request.data
        data = json.loads(json_data)
        print("JSON FOR UPDATE : {}".format(data))
        try:
            empObj = Employee.query.get(data['employeeId'])
            if empObj:
                empObj.firstName = data['firstName']
                empObj.lastName = data['lastName']
                empObj.address = data['address']
                empObj.email = data['email']
                empObj.mobileNo = data['mobileNo']
                empObj.salary = data['salary']

                try:
                    print('date form user {}'.format(str(data['joiningDate'])))
                    date_dt = datetime.strptime(str(data['joiningDate']), '%d/%m/%Y')
                    empObj.joiningDate = date_dt
                except Exception as e:
                    print("ERROR {}".format(e))
                empObj.gender = data['gender']
                empObj.password = data['password']
                db.session.commit()
                return {'message': 'Record updated successfully!'}
            else:
                return {'message': 'Error while updating details'}
        except (Exception):
            pass


class SpecificRecord(Resource):

    def get(self,empId):
        employeeRecord = Employee.query.get(empId)
        obj=employeeRecord.__dict__
        obj.pop('_sa_instance_state')
        obj.pop('password')
        obj['joiningDate'] =str(obj['joiningDate'])
        print(str(obj))
        return obj

    def delete(self,empId):
        Employee.query.filter(Employee.employeeId == empId).delete()
        db.session.commit()


class AllRecords(Resource):
    def get(self):
        allEmployee=Employee.query.all()
        obj=list()
        for emp in allEmployee:
            temp=emp.__dict__
            temp.pop('_sa_instance_state')
            temp.pop('password')
            temp['joiningDate'] = str(temp['joiningDate'])
            obj.append(temp)
        return obj
