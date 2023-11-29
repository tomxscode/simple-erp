from flask import Blueprint, request, jsonify, render_template, flash, redirect, url_for
from models.Factura import Factura, DetalleFactura
from models.Venta import Venta
from models.Empresa import Empresa
from forms import VentaForm
from flask_login import current_user
from models import db

ventas = Blueprint('ventas', __name__)

@ventas.route('/api/ventas', methods=['GET', 'POST', 'PUT', 'DELETE'])
def ventas_api():
  if request.method == 'GET':
    ventas = Venta.query.all()
    return jsonify([venta.to_dict() for venta in ventas]), 200
  
@ventas.route('/ventas/crear', methods=['GET', 'POST'])
def crear_venta():
  form = VentaForm()
  
  if form.validate_on_submit():
    venta_info = form.data
    
    empresa_mandante = Empresa.query.filter_by(rut=venta_info['empresa_mandante']).first()
    empresa_venta = Empresa.query.filter_by(rut=venta_info['empresa_venta']).first()
    
    if not empresa_mandante:
      flash('La empresa mandante no existe', 'error')
      return redirect(url_for('ventas.crear_venta'))
    if not empresa_venta:
      flash('La empresa venta no existe', 'error')
      return redirect(url_for('ventas.crear_venta'))
    
    if not venta_info['factura']:
      ultima_factura = Factura.query.order_by(Factura.id.desc()).first()
      nuevo_numero_factura = ultima_factura.id + 1 if ultima_factura else 1
      monto_neto = float(venta_info['monto_neto'])
      nueva_factura = Factura(
        numero_factura=f'F-{nuevo_numero_factura}',
        glosa = venta_info['glosa'],
        fecha_factura = venta_info['fecha'],
        empresa_id = empresa_venta.id,
        responsable = current_user.run,
        monto_neto = monto_neto,
        monto_iva = monto_neto * 0.19
      )
      
      db.session.add(nueva_factura)
      db.session.commit()
      # Agregar detalle de la factura
      detalle_factura = DetalleFactura(
        factura_id = nueva_factura.id,
        descripcion = venta_info['glosa'] + " TEMPORAL",
        cantidad = 1,
        precio_unitario = monto_neto + (monto_neto * 0.19),
        monto_neto = monto_neto,
        monto_iva = monto_neto * 0.19
      )
      db.session.add(detalle_factura)
      db.session.commit()
      
      flash("Factura " + nueva_factura.numero_factura + " creada", 'success')
    else:
      pass
    
    nueva_venta = Venta(
      fecha = venta_info['fecha'],
      empresa_mandante = empresa_mandante.id,
      empresa_venta = empresa_venta.id,
      factura=venta_info['factura'] if venta_info['factura'] else nueva_factura.id,
      monto_neto = venta_info['monto_neto'],
      monto_iva = monto_neto * 0.19,
      monto_total = monto_neto + (monto_neto * 0.19),
      estado = venta_info['estado']
    )
    db.session.add(nueva_venta)
    db.session.commit()
    flash("Venta #" + str(nueva_venta.id) + " creada", 'success')
    return redirect(url_for('ventas.crear_venta'))
  return render_template('ventas/crear.html', form=form)