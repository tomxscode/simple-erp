from flask import Blueprint, render_template, flash
from flask_login import login_required, current_user, login_user
from models import db
from models.Usuario import Usuario
from forms import RegistroForm, LoginForm
#from utils.validar_run import validar_rut deprecado
from rut_chile import rut_chile
from utils.check_email import validar_email
from flask import url_for, redirect
from flask_login import logout_user
from flask_bcrypt import Bcrypt
from flask import request

usuario = Blueprint('usuario', __name__)

@usuario.route('/usuario/login', methods=['GET', 'POST'])
def login():
  form = LoginForm()
  if form.validate_on_submit():
    if not rut_chile.is_valid_rut(form.run.data):
      flash('El run ingresado no es válido', 'error')
      return redirect(url_for('usuario.login'))
    usuario = Usuario.query.filter_by(run=form.run.data).first()
    if not usuario:
      flash('El usuario no existe', 'error')
      return redirect(url_for('usuario.login'))
    # Desencriptar el pin
    bcrypt = Bcrypt()
    pin = bcrypt.check_password_hash(usuario.pin, form.pin.data)
    # Comprobar si el pin es correcto y si el usuario está activo
    if not pin:
      flash('El pin es incorrecto', 'error')
      return redirect(url_for('usuario.login'))
    else:
      login_user(usuario)
      flash('Sesión iniciada correctamente', 'success')
      next_page = request.args.get('next')
      return redirect(next_page or url_for('usuario.registro'))
  return render_template('usuario/Login.html', form=form)

@usuario.route('/usuario/registro', methods=['GET', 'POST'])
def registro():
  form = RegistroForm()
  if form.validate_on_submit():
    # Comprobar si el run es un run chileno válido
    if not rut_chile.is_valid_rut(form.run.data):
      flash('El run ingresado no es válido', 'error')
      return redirect(url_for('usuario.registro'))
    # Revisar el email es válido
    if not validar_email(form.email.data):
      flash('El email ingresado no es válido', 'error')
      return redirect(url_for('usuario.registro'))

    # Encriptar el PIN con bcrypt
    bcrypt = Bcrypt()
    hashed_pin = bcrypt.generate_password_hash(form.pin.data).decode('utf-8')
    form.pin.data = hashed_pin

    # Crear el usuario
    usuario = Usuario(
      run=form.run.data,
      pin=form.pin.data,
      nombre=form.nombre.data,
      apellido=form.apellido.data,
      email=form.email.data,
      telefono=form.telefono.data,
      rol=1,
      estado=1
    )
    db.session.add(usuario)
    db.session.commit()
    flash('Usuario registrado correctamente', 'success')
    # Iniciar sesión con la cuenta
    login_user(usuario)
  return render_template('usuario/Registro.html', form=form)

@usuario.route('/usuario/logout')
@login_required
def logout():
  logout_user()
  flash('Sesión cerrada correctamente', 'success')  
  return redirect(url_for('usuario.login'))