import os
from flask import Flask,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


host_address='http://127.0.0.1:5000/api'
app = Flask(__name__)
app.config['SECRET_KEY'] = "EmployeeSecreteKey"

basedir = os.path.abspath(os.path.dirname('__file__'))
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///"+os.path.join(basedir, "data.sqlite")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
Migrate(app, db)

from flasgger import Swagger
from flasgger import LazyString, LazyJSONEncoder
import request

app.config["SWAGGER"] = {"title": "Swagger-UI", "uiversion": 2}

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": "swag",
            "route": '/../static/swag.yml',
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/swagger/",
}

template = dict(
    swaggerUiPrefix=LazyString(lambda: request.environ.get("HTTP_X_SCRIPT_NAME", ""))
)

app.json_encoder = LazyJSONEncoder
swagger = Swagger(app, config=swagger_config, template=template)

from project.Employee.views import employee_blueprint
#from project.Salary.views import salary_blueprint

app.register_blueprint(employee_blueprint,url_prefix='/employee')
#app.register_blueprint(salary_blueprint,url_prefix='/salary')


@app.route('/')
def redirect_login():
    return redirect(url_for('employee.login'))
