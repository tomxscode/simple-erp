from flask import Blueprint, request, jsonify
from flask_login import current_user, login_required
from models import db
from models.Empresa import Empresa

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