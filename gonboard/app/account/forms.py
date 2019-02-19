from flask_wtf import Form
from wtforms import TextField, PasswordField
from wtforms import validators

_uid = TextField("User id", [
    validators.Required("User id is empty")
])

_upw = PasswordField("User password", [
    validators.Required("User password is empty")
])


class RegisterForm(Form):
    uid = _uid
    upw = _upw
    msg = TextField("Message to others")
    email = TextField("User email", [
       validators.Required("User email is empty"),
       validators.Email("User email is not valid")
    ])


class LoginForm(Form):
    uid = _uid
    upw = _upw
