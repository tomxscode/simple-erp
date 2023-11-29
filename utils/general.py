import locale


def dinero_formato(monto):
  return f"${monto:,.0f}"

def convertir_mes(fecha):
  locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
  return fecha.strftime("%B %Y")

def convertir_fecha(fecha):
  locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
  return fecha.strftime("%d/%m/%Y")