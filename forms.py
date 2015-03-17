#forms.py

from flask_wtf import Form
#from flask.ext.wtf import Form
from wtforms import TextField, IntegerField, DecimalField, DateField, SelectField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo

class AddTaskForm(Form):

	_id = IntegerField("Priority")
	entryDate = DateField("entryDate", validators=[DataRequired()], format="%Y-%m-%d")
	batch = TextField("batch", validators =[DataRequired()])
	action = TextField("action", validators =[DataRequired()])
	actionNo = DecimalField("actionNo")
	value = DecimalField("value")
	notes = TextField("notes")


class RegisterForm(Form):
	name = TextField('Username', validators=[DataRequired(), Length(min=6, max=25)])
	email = TextField('Email', validators=[DataRequired(), Length(min=6, max=40)])
	password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=40)])
	confirm = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])

class LoginForm(Form):
	name = TextField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])