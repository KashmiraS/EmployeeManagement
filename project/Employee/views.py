from project import host_address
from flask import render_template, Blueprint, redirect, url_for, request, flash, session
from project.Employee.forms import LoginForm
from project.models import Salary
import requests, json
from datetime import datetime
from project import db

employee_blueprint = Blueprint("employee", __name__, template_folder="templates/Employee")


@employee_blueprint.route('/', methods={'GET', 'POST'})
def login():
    form = LoginForm()
    if request.method == 'POST':
        email = request.form['inputEmail']
        password = request.form['inputPassword']

        data = {'email': email,
                'password': password}

        r = json.loads(requests.post(f'{host_address}/login', json.dumps(data)).text)
        print(r)
        exists = json.loads(r)
        print(exists)
        session['id'] = int(exists["empId"][0])
        if exists["status"]:
            return redirect(url_for('employee.dashboard'))
        else:
            flash('Invalid username or password')

    return render_template('employee_login.html', form=form)


@employee_blueprint.route('/registration', methods={'GET', 'POST'})
def register():
    data = dict()
    if request.method == 'POST':
        data['firstName'] = request.form['inputFName']
        data['lastName'] = request.form['inputLName']
        data['gender'] = request.form['inlineRadioOptions']
        data['email'] = request.form['inputEmail']
        data['mobileNo'] = request.form['inputMobNo']
        data['address'] = request.form['inputAddress']
        date_dt = datetime.strptime(str(request.form['joiningDate']), '%Y-%m-%d')
        data['joiningDate'] = str(date_dt)
        data['password'] = request.form['inputPassword']
        data['salary'] = '0'

        r = requests.post(f'{host_address}/register', json.dumps(data)).text
        print(r)
        is_registered = json.loads(r)
        print(is_registered)
        if is_registered["status"]:
            flash('You are registered successfully')
            return redirect(url_for('employee.login'))
        else:
            flash('Error while registration')

    return render_template('registration.html')


@employee_blueprint.route('/dashboard', methods={'GET', 'POST'})
def dashboard():
    return render_template('dashboard.html')


@employee_blueprint.route('/profile', methods={'GET', 'POST'})
def profile():
    empId = session["id"]
    print(f'login id in profile {empId}')
    print(f'{host_address}/get_employee/{empId}')
    employee = json.loads((requests.get(f'{host_address}/get_employee/{empId}')).text)
    return render_template('profile.html', employee=employee)


@employee_blueprint.route('/salary', methods={'GET', 'POST'})
def view_salary():
    empId = session["id"]
    print(f'login id in salary {empId}')
    salary_details = Salary.query.filter(Salary.empId == empId).first()
    return render_template('salary.html', salary_details=salary_details)


@employee_blueprint.route('/records', methods={'GET', 'POST'})
def view_records():
    all_employee_list = json.loads((requests.get(f'{host_address}/getAllEmployees')).text)
    print(all_employee_list)

    return render_template('manage_employees.html', len=len(all_employee_list), all_employee_list=all_employee_list)


@employee_blueprint.route('/view/<int:empId>', methods={'GET'})
def view(empId):
    employee = json.loads((requests.get(f'{host_address}/get_employee/{empId}')).text)
    return render_template('profile.html', employee=employee)


@employee_blueprint.route('/edit/<int:empId>', methods={'GET', 'POST'})
def edit(empId):
    employee = json.loads((requests.get(f'{host_address}/get_employee/{empId}')).text)
    return render_template('edit_profile.html', employee=employee)


@employee_blueprint.route('/delete/<int:empId>', methods={'GET', 'POST'})
def delete(empId):
    flash('Record deleted successfully!')
    json.loads((requests.delete(f'{host_address}/get_employee/{empId}')).text)
    all_employee_list = json.loads((requests.get(f'{host_address}/getAllEmployees')).text)
    return render_template('manage_employees.html', len=len(all_employee_list), all_employee_list=all_employee_list)


@employee_blueprint.route('/add_salary/<int:empId>', methods={'GET', 'POST'})
def add_salary(empId):
    if request.method == 'POST':
            data = dict()
            data['employeeId'] = empId
            data['workingDays'] = request.form['inputWorkingDays']
            data['paymentMode'] = request.form['inputPaymentMode']
            data['basicSalary'] = request.form['inputBasicSalary']
            data['pf'] = request.form['inputPf']
            data['totalEarnings'] = request.form['inputTotEarning']
            data['professionalTax'] = request.form['inputProfTax']
            data['netSalary'] = request.form['inputNetSalary']

            salary = Salary(data)
            print(str(salary))
            db.session.add(salary)
            db.session.commit()
    return render_template('add_salary.html')

@employee_blueprint.route('/add_employee', methods={'GET', 'POST'})
def add_employee():
    data = dict()
    if request.method == 'POST':
        data['firstName'] = request.form['inputFName']
        data['lastName'] = request.form['inputLName']
        data['gender'] = request.form['inlineRadioOptions']
        data['email'] = request.form['inputEmail']
        data['mobileNo'] = request.form['inputMobNo']
        data['address'] = request.form['inputAddress']
        date_dt = datetime.strptime(str(request.form['joiningDate']), '%Y-%m-%d')
        data['joiningDate'] = str(date_dt)
        data['password'] = request.form['inputPassword']
        data['salary'] = '0'

        r = requests.post(f'{host_address}/register', json.dumps(data)).text
        print(r)
        is_registered = json.loads(r)
        print(is_registered)
        if is_registered["status"]:
            flash('You are registered successfully')
            all_employee_list = json.loads((requests.get(f'{host_address}/getAllEmployees')).text)
            return render_template('manage_employees.html', len=len(all_employee_list),
                                   all_employee_list=all_employee_list)
        else:
            flash('Error while add employee')

    return render_template('add_employee.html')
