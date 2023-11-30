from datetime import datetime, timedelta
import locale


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