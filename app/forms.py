from flask_wtf import Form
from wtforms import TextField, DateField, IntegerField, SelectField
from wtforms.validators import DataRequired

class ProposeNew(Form):
	hangout_id = IntegerField('')
	title = TextField('Hangout Name', validators=[DataRequired()])
	hangout_date = DateField('hangout_date (mm/dd/yyyy)',validators = [DataRequired()], format='%m/%d/%Y')
	level = SelectField('level', validators = [DataRequired()], choices = [('Beginner', '1'), ('Intermediate', '2'), ('Advanced', '3')])
	language_tag = TextField('language', validators = [DataRequired()], choices = [('Python', 1), ('Javascript', '2'), ('')])
	description = TextField('description', validators = [DataRequired(),])
	status = IntegerField('Status')