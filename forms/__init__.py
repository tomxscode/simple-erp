from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Email, Length
from wtforms import StringField, PasswordField, SubmitField

class RegistroForm(FlaskForm):
  run = StringField('Run', validators=[DataRequired()])
  email = StringField('Email', validators=[DataRequired()])
  nombre = StringField('Nombre', validators=[DataRequired()])
  apellido = StringField('Apellido', validators=[DataRequired()])
  telefono = StringField('Telefono')
  pin = PasswordField('Pin', validators=[DataRequired(), Length(max=4)])
  submit = SubmitField('Registrar')
  
class LoginForm(FlaskForm):
  run = StringField('Run', validators=[DataRequired()])
  pin = PasswordField('Pin', validators=[DataRequired(), Length(max=4)])
  submit = SubmitField('Iniciar Sesión')
  
# Empresas
class EmpresaForm(FlaskForm):
  rut = StringField('Rut', validators=[DataRequired()])
  nombre = StringField('Nombre', validators=[DataRequired()])
  telefono = StringField('Telefono', validators=[DataRequired()])
  direccion = StringField('Direccion', validators=[DataRequired()])
  email = StringField('Email', validators=[DataRequired()])
  giro = StringField('Giro', validators=[DataRequired()])
  submit = SubmitField('Guardar')