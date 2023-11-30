import datetime
from flask import Blueprint, redirect, request, jsonify, render_template
from models import db
from models.Factura import Factura, DetalleFactura
from models.Empresa import Empresa
from models.Usuario import Usuario
from models.Venta import Venta
from utils.general import convertir_fecha, dinero_formato, actualizar_venta_montos
from forms import DetalleFacturaForm
from flask import flash
from flask import url_for

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

@factura.route('/factura/detalle/<int:id>', methods=['GET', 'POST'])
def detalle_factura(id):
  form = DetalleFacturaForm()
  factura = Factura.query.get(id)
  if form.validate_on_submit():
    detalle = DetalleFactura(
      descripcion = form.descripcion.data,
      cantidad = form.cantidad.data,
      precio_unitario = form.precio_unitario.data,
      monto_neto = form.precio_unitario.data * form.cantidad.data,
      monto_iva = float(form.precio_unitario.data * form.cantidad.data) * 0.19,
      factura_id = id
    )
    db.session.add(detalle)
    db.session.commit()
    flash('Detalle agregado correctamente', 'success')
    if actualizar_factura(id):
      flash('Factura actualizada correctamente', 'success')
      venta = Venta.query.filter_by(factura=id).first()
      if venta:
        actualizar_venta_montos(venta.id)
        flash('Venta actualizada correctamente', 'success')
    else:
      flash('Error al actualizar la factura', 'error')
    return redirect(url_for('factura.ver_factura', id=id))
  return render_template('factura/detalle_factura.html', form=form, factura=factura, convertir_fecha=convertir_fecha, dinero_formato=dinero_formato)

@factura.route('/factura/actualizar/<int:id>')
def actualizar_montos(id):
  if actualizar_factura(id):
    flash('Factura actualizada correctamente', 'success')
    # Obtener la Venta según la factura asociada
    venta = Venta.query.filter_by(factura=id).first()
    if venta:
      actualizar_venta_montos(venta.id)
      flash('Venta actualizada correctamente', 'success')
  else:
    flash('Error al actualizar la factura', 'error')
  return redirect(url_for('factura.ver_factura', id=id))
  

def actualizar_factura(id):
  factura = Factura.query.get(id)
  if factura:
    factura.monto_neto = 0
    factura.monto_iva = 0
    for detalle in DetalleFactura.query.filter_by(factura_id=id).all():
      factura.monto_neto += detalle.monto_neto
      factura.monto_iva += detalle.monto_iva
    db.session.commit()
    return True
  return False