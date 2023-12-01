import datetime
import locale
from flask import Blueprint, request, jsonify, render_template, flash, redirect, url_for
from sqlalchemy import asc, desc
from models.Factura import Factura, DetalleFactura
from models.Venta import Venta
from models.Empresa import Empresa
from forms import VentaForm
from flask_login import current_user, login_required
from models import db
import openpyxl
from utils.general import convertir_mes, convertir_fecha, dinero_formato, obtener_rango_mes
import tempfile
from flask import send_file

ventas = Blueprint('ventas', __name__)

@ventas.route('/api/ventas', methods=['GET', 'POST', 'PUT', 'DELETE'])
def ventas_api():
  if request.method == 'GET':
    ventas = Venta.query.all()
    return jsonify([venta.to_dict() for venta in ventas]), 200
  
@ventas.route('/ventas/crear', methods=['GET', 'POST'])
@login_required
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
        precio_unitario = monto_neto,
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
    return redirect(url_for('ventas.listar'))
  return render_template('ventas/crear.html', form=form)

@ventas.route('/ventas/listar', methods=['GET', 'POST'])
@login_required
def listar():
  query = Venta.query
  
  filtro_mes = request.args.get('filtro_mes', type=str)
  filtro_estado = request.args.get('filtro_estado', type=int)
  
  ordenar_por = request.args.get('ordenar_por', type=str)
  ordenar_de = request.args.get('ordenar_de', type=str)
  
  if ordenar_por:
    if ordenar_por == 'fecha':
        query = query.order_by(asc(Venta.fecha) if ordenar_de == 'asc' else desc(Venta.fecha))
    elif ordenar_por == 'monto_neto':
        query = query.order_by(asc(Venta.monto_neto) if ordenar_de == 'asc' else desc(Venta.monto_neto))
    elif ordenar_por == 'monto_iva':
        query = query.order_by(asc(Venta.monto_iva) if ordenar_de == 'asc' else desc(Venta.monto_iva))
    elif ordenar_por == 'monto_total':
        query = query.order_by(asc(Venta.monto_total) if ordenar_de == 'asc' else desc(Venta.monto_total))
    elif ordenar_por == 'estado':
        query = query.order_by(asc(Venta.estado) if ordenar_de == 'asc' else desc(Venta.estado))
    elif ordenar_por == 'empresa_mandante':
        query = query.join(Empresa).order_by(asc(Empresa.nombre) if ordenar_de == 'asc' else desc(Empresa.nombre))
    elif ordenar_por == 'empresa_venta':
        query = query.order_by(asc(Venta.empresa_venta) if ordenar_de == 'asc' else desc(Venta.empresa_venta))
    else:
        flash('El ordenamiento por no es válido', 'error')
  else:
    if ordenar_de:
      flash('No hay nada que ordenar', 'error')
      
  if filtro_mes:
    primer_dia, ultimo_dia = obtener_rango_mes(filtro_mes)
    query = query.filter(Venta.fecha >= primer_dia, Venta.fecha <= ultimo_dia)
    if query.count() == 0:
      flash('No se encontraron ventas en el mes seleccionado', 'warning')
      filtro_mes = None
    
  if filtro_estado:
    # Comprobar que filtro estado sea solo 0 o 1
    if filtro_estado not in [0, 1]:
      flash('El estado debe ser 0 o 1', 'error')
      # Vaciar filtro estado
      filtro_estado = None
    else:
      query = query.filter(Venta.estado == int(filtro_estado))
  
  pagina = request.args.get('pagina', 1, type=int)
  por_pagina = request.args.get('por_pagina', 10, type=int)
      
  ventas = query.paginate(page=pagina, per_page=por_pagina, error_out=False)
  
  def obtener_nombre_empresa(empresa_id):
    empresa = Empresa.query.get(empresa_id)
    if empresa:
      return empresa.nombre
    return None
  
  def obtener_glosa(factura_id):
    factura = Factura.query.get(factura_id)
    if factura:
      return factura.glosa
    return None
  
  def obtener_num_factura(factura_id):
    factura = Factura.query.get(factura_id)
    if factura:
      return factura.numero_factura
    return None
  
  return render_template('ventas/listar.html', ventas=ventas, obtener_nombre_empresa=obtener_nombre_empresa, obtener_glosa=obtener_glosa, obtener_num_factura=obtener_num_factura, dinero_formato=dinero_formato, convertir_mes=convertir_mes, convertir_fecha=convertir_fecha)

@ventas.route('/ventas/descargar/todas', methods=['GET'])
@login_required
def descargar_todas():
  def obtener_nombre_empresa(empresa_id):
    empresa = Empresa.query.get(empresa_id)
    if empresa:
      return empresa.nombre
    return None
  
  def obtener_glosa(factura_id):
    factura = Factura.query.get(factura_id)
    if factura:
      return factura.glosa
    return None
  
  def obtener_num_factura(factura_id):
    factura = Factura.query.get(factura_id)
    if factura:
      return factura.numero_factura
    return None
  
  ventas = Venta.query.all()
  
  libro_trabajo = openpyxl.Workbook()
  hoja_calculo = libro_trabajo.active
  
  hoja_calculo['A1'] = 'ID'
  hoja_calculo['B1'] = 'FECHA'
  hoja_calculo['C1'] = 'MES'
  hoja_calculo['D1'] = 'MANDANTE'
  hoja_calculo['E1'] = 'EMPRESA'
  hoja_calculo['F1'] = 'GLOSA'
  hoja_calculo['G1'] = 'MONTO NETO'
  hoja_calculo['H1'] = 'MONTO IVA'
  hoja_calculo['I1'] = 'MONTO TOTAL'
  hoja_calculo['J1'] = 'FACTURA'
  hoja_calculo['K1'] = 'ESTADO'
  
  hoja_calculo.title = 'Ventas'
  
  for fila, venta in enumerate(ventas, start=2):
    hoja_calculo['A' + str(fila)] = venta.id
    hoja_calculo['B' + str(fila)] = convertir_fecha(venta.fecha)
    hoja_calculo['C' + str(fila)] = convertir_mes(venta.fecha)
    hoja_calculo['D' + str(fila)] = obtener_nombre_empresa(venta.empresa_mandante)
    hoja_calculo['E' + str(fila)] = obtener_nombre_empresa(venta.empresa_venta)
    hoja_calculo['F' + str(fila)] = obtener_glosa(venta.factura)
    hoja_calculo['G' + str(fila)] = venta.monto_neto
    hoja_calculo['H' + str(fila)] = venta.monto_iva
    hoja_calculo['I' + str(fila)] = venta.monto_total
    hoja_calculo['J' + str(fila)] = obtener_num_factura(venta.factura)
    if venta.estado:
      hoja_calculo['K' + str(fila)] = 'PAGADA'
    else:
      hoja_calculo['K' + str(fila)] = 'POR PAGAR'
    
  archivo_temporal = tempfile.NamedTemporaryFile(delete=False)
  libro_trabajo.save(archivo_temporal.name)
  
  fecha_hora = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
  nombre_archivo = 'ventas_' + fecha_hora + '.xlsx'
  
  return send_file(archivo_temporal.name, as_attachment=True, download_name=nombre_archivo)