from . import db

class Factura(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  numero_factura = db.Column(db.String(50), unique=True, nullable=False)
  glosa = db.Column(db.String(100), nullable=False)
  fecha_factura = db.Column(db.Date, nullable=False)
  empresa_id = db.Column(db.Integer, db.ForeignKey('empresa.id'), nullable=False)
  responsable = db.Column(db.String(10), db.ForeignKey('usuario.run'), nullable=False)
  monto_neto = db.Column(db.Float, nullable=False)
  monto_iva = db.Column(db.Float, nullable=False)
  
class DetalleFactura(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  factura_id = db.Column(db.Integer, db.ForeignKey('factura.id'), nullable=False)
  descripcion = db.Column(db.String(100), nullable=False)
  cantidad = db.Column(db.Integer, nullable=False)
  precio_unitario = db.Column(db.Float, nullable=False)
  monto_neto = db.Column(db.Float, nullable=False)
  monto_iva = db.Column(db.Float, nullable=False)