from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField
from wtforms import validators

_uid = TextField("User id", [
    validators.Required("User id is empty")
])

_upw = PasswordField("User password", [
    validators.Required("User password is empty")
])


class RegisterForm(FlaskForm):
    uid = _uid
    upw = _upw
    msg = TextField("Message to others")
    email = TextField("User email", [
       validators.Required("User email is empty"),
       validators.Email("User email is not valid")
    ])


class MypageForm(FlaskForm):
    msg = TextField("Message to others")
    new_upw = PasswordField("New password (Optional)") # can be empty
    confirm = PasswordField("Confirm new password (Optional)", [
        validators.EqualTo('new_upw', message='Password does not match')
    ])


class LoginForm(FlaskForm):
    uid = _uid
    upw = _upw
