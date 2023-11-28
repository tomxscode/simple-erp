from flask import Blueprint, request, jsonify
from flask_login import current_user, login_required
from models import db
from models.Empresa import Empresa
from flask import render_template

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
        'rut': empresa.rut
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
      rut=request.json['rut']
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
    'rut': empresa.rut
  }), 200
  
@empresa.route('/empresa/listar', methods=['GET'])
def listar():
  pagina = request.args.get('pagina', 1, type=int)
  por_pagina = request.args.get('por_pagina', 10, type=int)
  # Obtener todas las empresas y paginarlas
  empresas = Empresa.query.paginate(page=pagina, per_page=por_pagina, error_out=False)
  return render_template('empresa/listar.html', empresas=empresas)