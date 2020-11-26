from flask_wtf import Form 
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired

class LoginForm(Form):
    usuario = StringField("username", validators=[DataRequired()])
    senha = PasswordField("password", validators=[DataRequired()])