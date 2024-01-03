from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Email, Length
from wtforms import StringField, PasswordField, SubmitField, DateField, SelectField, IntegerField

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
  
# Ventas
class VentaForm(FlaskForm):
  fecha = DateField('Fecha', validators=[DataRequired()])
  empresa_mandante = StringField('Empresa Mandante', validators=[DataRequired()])
  empresa_venta = StringField('Empresa Venta', validators=[DataRequired()])
  # info de la factura
  factura = StringField('Factura')
  glosa = StringField('Glosa')
  monto_neto = StringField('Monto Neto', validators=[DataRequired()])
  estado = SelectField('Estado', choices=[(0, 'Por pagar'), (1, 'Pagada')], validators=[DataRequired()])
  submit = SubmitField('Guardar')
  
# Facturas
class DetalleFacturaForm(FlaskForm):
  descripcion = StringField('Descripcion', validators=[DataRequired()])
  cantidad = IntegerField('Cantidad', validators=[DataRequired()])
  precio_unitario = IntegerField('Precio Unitario', validators=[DataRequired()])
  submit = SubmitField('Guardar')

# Empleados
class EmpleadoForm(FlaskForm):
  rut = StringField('Run', validators=[DataRequired()])
  nombre = StringField('Nombre', validators=[DataRequired()])
  apellido = StringField('Apellido', validators=[DataRequired()])
  email = StringField('Email', validators=[DataRequired()])
  telefono = StringField('Telefono', validators=[DataRequired()])
  direccion = StringField('Direccion', validators=[DataRequired()])
  fecha_nacimiento = DateField('Fecha Nacimiento', validators=[DataRequired()])
  fecha_ingreso = DateField('Fecha Ingreso', validators=[DataRequired()])
  submit = SubmitField('Guardar')