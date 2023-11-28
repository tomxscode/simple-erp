from datetime import datetime
from flask import Blueprint, request, jsonify, flash, url_for, redirect, render_template
from flask_login import current_user, login_required
from models import db
from models.Empresa import Empresa
from forms import EmpresaForm
import openpyxl
import tempfile
from flask import send_file

empresa = Blueprint('empresa', __name__)

# API
# Campo opcional, ejemplo /api/empresa/id puede estar o no
@empresa.route('/api/empresa/', methods=['GET', 'POST', 'PUT', 'DELETE'])
def api_empresa():
  # Comprobando el método HTTP
  if request.method == 'GET':
    # Obtener todas las empresas
    empresas = Empresa.query.all()
    empresas_json = []
    for empresa in empresas:
      empresas_json.append({
        'id': empresa.id,
        'nombre': empresa.nombre,
        'direccion': empresa.direccion,
        'telefono': empresa.telefono,
        'email': empresa.email,
        'rut': empresa.rut,
        'giro': empresa.giro
      })
    return jsonify(empresas_json), 200
  elif request.method == 'POST':
    # Comprobar que no viene vacio
    if not request.json:
      return jsonify({'success': False, 'message': 'No se recibieron datos'}), 400
    # Comprobar que no existe una empresa con el mismo rut
    if Empresa.query.filter_by(rut=request.json['rut']).first():
      return jsonify({'success': False, 'message': 'Ya existe una empresa con ese rut'}), 400
    # Crear empresa
    empresa = Empresa(
      nombre=request.json['nombre'],
      direccion=request.json['direccion'],
      telefono=request.json['telefono'],
      email=request.json['email'],
      rut=request.json['rut'],
      giro=request.json['giro']
    )
    db.session.add(empresa)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Empresa creada correctamente', 'empresa': empresa.id}), 200
  
  elif request.method == 'PUT':
    # Actualizar empresa
    empresa = Empresa.query.get(request.json['id'])
    empresa.nombre = request.json['nombre']
    empresa.direccion = request.json['direccion']
    empresa.telefono = request.json['telefono']
    empresa.email = request.json['email']
    empresa.rut = request.json['rut']
    empresa.giro = request.json['giro']
    db.session.commit()
    return jsonify({'success': True, 'message': 'Empresa actualizada correctamente'}), 200
  
  elif request.method == 'DELETE':
    # Eliminar empresa
    empresa = Empresa.query.get(request.json['id'])
    if not empresa:
      return jsonify({'success': False, 'message': 'Empresa no encontrada'}), 404
    db.session.delete(empresa)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Empresa eliminada correctamente'}), 200
  
# API PARA OBTENER UNA EN PARTICULAR

@empresa.route('/api/empresa/<int:id>', methods=['GET'])
def api_empresa_id(id):
  empresa = Empresa.query.get(id)
  if not empresa:
    return jsonify({'success': False, 'message': 'Empresa no encontrada'}), 404
  return jsonify({
    'id': empresa.id,
    'nombre': empresa.nombre,
    'direccion': empresa.direccion,
    'telefono': empresa.telefono,
    'email': empresa.email,
    'rut': empresa.rut,
    'giro': empresa.giro
  }), 200
  
@empresa.route('/empresa/listar', methods=['GET'])
@login_required
def listar():
  pagina = request.args.get('pagina', 1, type=int)
  por_pagina = request.args.get('por_pagina', 10, type=int)
  # Obtener todas las empresas y paginarlas
  empresas = Empresa.query.paginate(page=pagina, per_page=por_pagina, error_out=False)
  return render_template('empresa/listar.html', empresas=empresas)

@empresa.route('/empresa/crear', methods=['GET', 'POST'])
@login_required
def crear():
  form = EmpresaForm()
  if form.validate_on_submit():
    # Comprobar que el rut no esté repetido
    if Empresa.query.filter_by(rut=form.rut.data).first():
      flash('Ya existe una empresa con ese rut', 'error')
      return redirect(url_for('empresa.crear'))
    # Crear empresa
    empresa = Empresa(
      nombre=form.nombre.data,
      direccion=form.direccion.data,
      telefono=form.telefono.data,
      email=form.email.data,
      rut=form.rut.data,
      giro=form.giro.data
    )
    db.session.add(empresa)
    db.session.commit()
    flash('Empresa creada correctamente', 'success')
    return redirect(url_for('empresa.listar'))
  return render_template('empresa/crear.html', form=form)

# Descarga de Excel
@empresa.route('/empresa/descargar/empresas', methods=['GET'])
@login_required
def descargar_empresas():
  empresas = Empresa.query.all()
  
  # Crear un nuevo libro
  libro_trabajo = openpyxl.Workbook()
  hoja_calculo = libro_trabajo.active
  
  # Encabezados
  hoja_calculo['A1'] = 'ID'
  hoja_calculo['B1'] = 'RUT'
  hoja_calculo['C1'] = 'NOMBRE'
  hoja_calculo['D1'] = 'EMAIL'
  hoja_calculo['E1'] = 'TELEFONO'
  hoja_calculo['F1'] = 'DIRECCION'
  hoja_calculo['G1'] = 'GIRO'
  
  # Datos
  for fila, empresa in enumerate(empresas, start=2):
    hoja_calculo['A' + str(fila)] = empresa.id
    hoja_calculo['B' + str(fila)] = empresa.rut
    hoja_calculo['C' + str(fila)] = empresa.nombre
    hoja_calculo['D' + str(fila)] = empresa.email
    hoja_calculo['E' + str(fila)] = empresa.telefono
    hoja_calculo['F' + str(fila)] = empresa.direccion
    hoja_calculo['G' + str(fila)] = empresa.giro
    
  # Guardar el libro en un archivo temporal
  archivo_temporal = tempfile.NamedTemporaryFile(delete=False)
  libro_trabajo.save(archivo_temporal.name)
  
  # Generar el nombre del archivo de descarga: empresa_FECHA Y HORA DE HOY.xlsx
  fecha_hora = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
  nombre_archivo = 'empresa_' + fecha_hora + '.xlsx'
  
  # Descargar el archivo temporal
  return send_file(archivo_temporal.name, as_attachment=True, download_name=nombre_archivo)