from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models import db
from models.Usuario import Usuario
from forms import RegistroForm

usuario = Blueprint('usuario', __name__)

@usuario.route('/usuario/registro')
def registro():
  return render_template('usuario/Registro.html')