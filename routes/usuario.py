from flask import Blueprint, render_template, flash
from flask_login import login_required, current_user, login_user
from models import db
from models.Usuario import Usuario
from forms import RegistroForm
from utils.validar_run import validar_rut
from utils.check_email import validar_email

usuario = Blueprint('usuario', __name__)

@usuario.route('/usuario/registro', methods=['GET', 'POST'])
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