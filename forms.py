#forms.py

from flask_wtf import Form
from wtforms import TextField, IntegerField, DecimalField, DateField
from wtforms.validators import DataRequired

class AddTaskForm(Form):
	_id = IntegerField("Priority")
	entryDate = DateField("entryDate", validators=[DataRequired()], format="%Y-%m-%d")
	batch = TextField("batch", validators =[DataRequired()])
	batch = TextField("action", validators =[DataRequired()])
	action = IntegerField("actionNo")
	value = DecimalField("value")
	note = TextField("notes")

