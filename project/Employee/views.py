from project import host_address
from flask import render_template, Blueprint,redirect,url_for,request,flash
from project.Employee.forms import LoginForm
from project.models import Employee,db
import requests, json


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
        if exists["status"]:
            return redirect(url_for('employee.dashboard'))
        else:
            flash('Invalid username or password')

    return render_template('employee_login.html', form=form)


@employee_blueprint.route('/registration', methods={'GET', 'POST'})
def register():
    return render_template('registration.html')


@employee_blueprint.route('/dashboard', methods={'GET', 'POST'})
def dashboard():
    return render_template('dashboard.html')


@employee_blueprint.route('/profile', methods={'GET', 'POST'})
def profile():
    return render_template('profile.html')


@employee_blueprint.route('/records', methods={'GET', 'POST'})
def view_records():
    return render_template('records.html')


@employee_blueprint.route('/edit_profile', methods={'GET', 'POST'})
def edit():
    return render_template('registration.html')
