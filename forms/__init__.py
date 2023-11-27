from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Email, Length
from wtforms import StringField

class RegistroForm(FlaskForm):
  run = StringField('Run', validators=[DataRequired()])
  email = StringField('Email', validators=[DataRequired(), Email()])
  nombre = StringField('Nombre', validators=[DataRequired()])
  apellido = StringField('Apellido', validators=[DataRequired()])
  telefono = StringField('Telefono')
  pin = StringField('Pin', validators=[DataRequired(), Length(max=4)])