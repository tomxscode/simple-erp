from . import db

class Venta(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  fecha = db.Column(db.Date, nullable=False)
  empresa_mandante = db.Column(db.Integer, db.ForeignKey('empresa.id'), nullable=False)
  empresa_venta = db.Column(db.Integer, db.ForeignKey('empresa.id'), nullable=False)
  factura = db.Column(db.Integer, db.ForeignKey('factura.id'), nullable=False)
  monto_neto = db.Column(db.Float, nullable=False)
  monto_iva = db.Column(db.Float, nullable=False)
  monto_total = db.Column(db.Float, nullable=False)