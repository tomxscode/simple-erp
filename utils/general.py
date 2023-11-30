from datetime import datetime, timedelta
import locale
from models.Factura import Factura
from models import db

from models.Venta import Venta


def dinero_formato(monto):
  return f"${monto:,.0f}"

def convertir_mes(fecha):
  locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
  return fecha.strftime("%B %Y")

def convertir_fecha(fecha):
  locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
  return fecha.strftime("%d/%m/%Y")

def obtener_rango_mes(input_fecha):
    # Convertir la cadena a un objeto datetime
    fecha_obj = datetime.strptime(input_fecha, "%m/%Y")

    # Obtener el primer día del mes
    primer_dia = fecha_obj.replace(day=1)

    # Calcular el último día del mes sumando un mes y restando un día
    ultimo_dia = (fecha_obj.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)

    return primer_dia, ultimo_dia
  
def actualizar_venta_montos(id_venta):
  venta = Venta.query.get(id_venta)
  factura = Factura.query.filter_by(id=venta.factura).first()
  venta.monto_neto = factura.monto_neto
  venta.monto_iva = factura.monto_iva
  venta.monto_total = factura.monto_neto + factura.monto_iva
  db.session.commit()