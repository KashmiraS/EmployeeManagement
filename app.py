from project import app
from flask import Blueprint
from flask_restful import Api
from project.login_api import Login,Register

api_bp=Blueprint('api',__name__,url_prefix='/api')
api=Api(api_bp)

api.add_resource(Login,'/login')
api.add_resource(Register,'/register')
app.register_blueprint(api_bp)

if __name__ == '__main__':
    app.run(debug=True)
