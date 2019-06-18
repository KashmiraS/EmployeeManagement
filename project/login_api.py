from flask_restful import Resource
from flask import request
import json
from project.models import db,Employee


class Login(Resource):
    def post(self):
        json_data = request.data

        if not json_data:
            return {'message':'No input data provided'}

        data = json.loads(json_data)
        exists = bool(db.session.query(Employee.employeeId).filter(
            db.and_(Employee.email == data['email'], Employee.password == data['password'])).first())

        responseData=dict()
        responseData['status'] = exists

        return json.dumps(responseData)

    def get(self):#forgot password
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

        is_exist = bool(db.session.query(Employee.employeeId).filter(Employee.email == data['email']).first())
        if not is_exist:
            employee = Employee(data)
            db.session.add(employee)
            db.session.commit()
        else:
            return {'message': 'This email id is already exist'}


    def patch(self):
        pass


