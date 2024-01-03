from flask import Blueprint
from models import db
from models.Empleado import Empleado
from flask import request
from flask import url_for
from flask import render_template
from forms import EmpleadoForm
from flask import flash

empleado = Blueprint('empleado', __name__)

@empleado.route('/empleado/crear/', methods=['POST', 'GET'])
def crear_empleado():
    if request.method == 'POST':
        pass
    elif request.method == 'GET':
        form = EmpleadoForm()
        return render_template('empleado/crear.html', form=form)