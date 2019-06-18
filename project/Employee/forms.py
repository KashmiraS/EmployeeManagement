from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


class LoginForm(FlaskForm):
    username = StringField("Username", render_kw={"placeholder": "Username"})
    password = StringField("Password", render_kw={"placeholder": "Password"})
    submit = SubmitField("Submit")

