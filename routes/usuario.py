from flask import Blueprint, render_template, flash
from flask_login import login_required, current_user, login_user
from models import db
from models.Usuario import Usuario
from forms import RegistroForm, LoginForm
from utils.validar_run import validar_rut
from utils.check_email import validar_email
from flask import url_for, redirect
from flask_login import logout_user

usuario = Blueprint('usuario', __name__)

@usuario.route('/usuario/login', methods=['GET', 'POST'])
def login():
  form = LoginForm()
  if form.validate_on_submit():
    if not validar_rut(form.run.data):
      flash('El run ingresado no es válido', 'error')
    # Comprobar que la contraseña es válida (pin)
    usuario = Usuario.query.filter_by(run=form.run.data).first()
    if usuario is None or not usuario.pin == form.pin.data:
      flash('El run o el pin son incorrectos', 'error')
    else:
      login_user(usuario)
      flash('Sesión iniciada correctamente', 'success')
      return "Exito"
  return render_template('usuario/Login.html', form=form)

@usuario.route('/usuario/registro', methods=['GET', 'POST'])
@login_required
def registro():
  form = RegistroForm()
  if form.validate_on_submit():
    # Comprobar si el run es un run chileno válido
    if not validar_rut(form.run.data):
      flash('El run ingresado no es válido', 'error')
    # Revisar el email es válido
    if not validar_email(form.email.data):
      flash('El email ingresado no es válido', 'error')
    
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