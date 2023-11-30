import datetime
from flask import Blueprint, request, jsonify, render_template
from models import db
from models.Factura import Factura, DetalleFactura
from models.Empresa import Empresa
from models.Usuario import Usuario
from utils.general import convertir_fecha, dinero_formato

factura = Blueprint('factura', __name__)

@factura.route('/api/factura', methods=['GET', 'POST', 'PUT', 'DELETE'])
def factura_api():
  # patch
  if request.method == 'GET':
    facturas = Factura.query.all()
    return jsonify(facturas)
  elif request.method == 'POST':
    if not request.json:
      return jsonify({'success': True, 'message': 'No hay datos'}), 400
    infoFactura = request.json
    # Comprobar que la empresa existe
    empresa_recibida = Empresa.query.get(infoFactura['empresa_id'])
    if not empresa_recibida:
      return jsonify({'success': False, 'message': 'Empresa no encontrada'}), 404
    usuario_recibido = Usuario.query.get(infoFactura['responsable'])
    if not usuario_recibido:
      return jsonify({'success': False, 'message': 'Usuario no encontrado'}), 404
    # Convertir la fecha (input DD/MM/AAAA a fecha)
    fecha_factura_conv = datetime.datetime.strptime(infoFactura['fecha_factura'], '%d/%m/%Y')
    factura = Factura(
      numero_factura = infoFactura['numero_factura'],
      glosa = infoFactura['glosa'],
      fecha_factura = fecha_factura_conv,
      empresa_id = infoFactura['empresa_id'],
      responsable = infoFactura['responsable'],
      monto_total = infoFactura['monto_total']
    )
    db.session.add(factura)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Factura creada correctamente', 'factura': factura.id}), 200
  

@factura.route('/factura/<int:id>')
def ver_factura(id):
  factura = Factura.query.get(id)
  detalles = DetalleFactura.query.filter_by(factura_id=id).all()
  
  def obtener_nombre_empresa(empresa_id):
    empresa = Empresa.query.get(empresa_id)
    if empresa:
      return empresa.nombre
    return None
  
  return render_template('factura/factura.html', factura=factura, detalles=detalles, obtener_nombre_empresa=obtener_nombre_empresa, convertir_fecha=convertir_fecha, dinero_formato=dinero_formato)